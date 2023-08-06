"""DB-API implementation backed by HiveServer2 (Thrift API)
See http://www.python.org/dev/peps/pep-0249/
Many docstrings in this file are based on the PEP, which is in the public domain.
"""

from __future__ import absolute_import
from __future__ import unicode_literals

import datetime
# Make all exceptions visible in this e6xdb per DB-API
import logging
import re
import socket
import sys
from decimal import Decimal
from io import BytesIO
from ssl import CERT_NONE, CERT_OPTIONAL, CERT_REQUIRED
from urllib.parse import urlparse

from thrift.protocol import TBinaryProtocol, TMultiplexedProtocol
from thrift.transport import TSocket
from thrift.transport import TTransport

from e6xdb import common
from e6xdb.common import DBAPITypeObject
from e6xdb.constants import *
from e6xdb.datainputstream import DataInputStream, read_values_from_array, get_query_columns_info
from e6xdb.server import QueryEngine
from e6xdb.typeId import *

apilevel = '2.0'
threadsafety = 2  # Threads may share the e6xdb and connections.
paramstyle = 'pyformat'  # Python extended format codes, e.g. ...WHERE name=%(name)s
key = b"teamuniphi@cunninghamroadfrmbang"

_logger = logging.getLogger(__name__)

_TIMESTAMP_PATTERN = re.compile(r'(\d+-\d+-\d+ \d+:\d+:\d+(\.\d{,6})?)')

ssl_cert_parameter_map = {
    "none": CERT_NONE,
    "optional": CERT_OPTIONAL,
    "required": CERT_REQUIRED,
}


def _parse_timestamp(value):
    if value:
        match = _TIMESTAMP_PATTERN.match(value)
        if match:
            if match.group(2):
                format = '%Y-%m-%d %H:%M:%S.%f'
                # use the pattern to truncate the value
                value = match.group()
            else:
                format = '%Y-%m-%d %H:%M:%S'
            value = datetime.datetime.strptime(value, format)
        else:
            raise Exception(
                'Cannot convert "{}" into a datetime'.format(value))
    else:
        value = None
    return value


TYPES_CONVERTER = {"DECIMAL_TYPE": Decimal,
                   "TIMESTAMP_TYPE": _parse_timestamp}


class HiveParamEscaper(common.ParamEscaper):
    def escape_string(self, item):
        # backslashes and single quotes need to be escaped
        # TODO verify against parser
        # Need to decode UTF-8 because of old sqlalchemy.
        # Newer SQLAlchemy checks dialect.supports_unicode_binds before encoding Unicode strings
        # as byte strings. The old version always encodes Unicode as byte strings, which breaks
        # string formatting here.
        if isinstance(item, bytes):
            item = item.decode('utf-8')
        return "'{}'".format(
            item
                .replace('\\', '\\\\')
                .replace("'", "\\'")
                .replace('\r', '\\r')
                .replace('\n', '\\n')
                .replace('\t', '\\t')
        )


_escaper = HiveParamEscaper()


def connect(*args, **kwargs):
    """Constructor for creating a connection to the database. See class :py:class:`Connection` for
    arguments.
    :returns: a :py:class:`Connection` object.
    """
    return Connection(*args, **kwargs)


class Connection(object):
    """Wraps a http e6xdb session"""

    def __init__(
            self,
            host=None,
            port=None,
            scheme=None,
            username=None,
            database='default',
            auth=None,
            configuration=None,
            kerberos_service_name=None,
            password=None,
            check_hostname=None,
            ssl_cert=None,
            thrift_transport=None
    ):
        username = username
        password = password
        database = database
        port = port
        scheme = "e6xdb"

        if scheme != "e6xdb":
            raise ValueError("scheme is not e6xdb")

        if password is None:
            raise ValueError("Password should be set")

        if port is None:
            port = 9000
        self._transport = TSocket.TSocket(host, port, socket_keepalive=True)
        self._transport = TTransport.TBufferedTransport(self._transport)

        protocol = TBinaryProtocol.TBinaryProtocol(self._transport)
        protocol = TMultiplexedProtocol.TMultiplexedProtocol(protocol, "E6x")
        self._client = QueryEngine.Client(protocol)
        self._transport.open()

        try:
            authSession = self._client.authenticate(username, password)
            if not authSession:
                raise ValueError("invalid username or password")

            buffer = self._client.isSchemaSet()
            buffer = BytesIO(buffer)
            dis = DataInputStream(buffer)
            is_schema_set = dis.read_boolean()
            if not is_schema_set:
                self._client.setSchema(database)
        except Exception as e:
            self._transport.close()
            raise e

    def __enter__(self):
        """Transport should already be opened by __init__"""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Call close"""
        self.close()

    def close(self, query_id):
        self._client.clear(query_id)
        self._transport.close()

    def reopen(self):
        self._transport.close()
        self._transport.open()

    def commit(self):
        """Hive does not support transactions, so this does nothing."""
        pass

    def cursor(self, *args, **kwargs):
        """Return a new :py:class:`Cursor` object using the connection."""
        return Cursor(self, *args, **kwargs)

    def rollback(self):
        raise Exception("e6xdb does not support transactions")  # pragma: no cover

    @property
    def client(self):
        return self._client


"""
Reading from Java DataInputStream format.
"""


class Cursor(common.DBAPICursor):
    """These objects represent a database cursor, which is used to manage the context of a fetch
    operation.
    Cursors are not isolated, i.e., any changes done to the database by a cursor are immediately
    visible by other cursors or connections.
    """

    def __init__(self, connection, arraysize=1000):
        super(Cursor, self).__init__()
        self._arraysize = arraysize
        self.connection = connection
        self._data = None
        self._query_columns_description = None
        self._description = None
        self._query_id = None
        self._count = 10000000  # 10 millions, used for select in batch

    def _reset_state(self):
        """Reset state about the previous query in preparation for running another query"""
        pass

    @property
    def arraysize(self):
        return self._arraysize

    @arraysize.setter
    def arraysize(self, value):
        """Array size cannot be None, and should be an integer"""
        default_arraysize = 1000
        try:
            self._arraysize = int(value) or default_arraysize
        except TypeError:
            self._arraysize = default_arraysize

    @property
    def description(self):
        """This read-only attribute is a sequence of 7-item sequences.
        Each of these sequences contains information describing one result column:
        - name
        - type_code
        - display_size (None in current implementation)
        - internal_size (None in current implementation)
        - precision (None in current implementation)
        - scale (None in current implementation)
        - null_ok (always True in current implementation)
        This attribute will be ``None`` for operations that do not return rows or if the cursor has
        not had an operation invoked via the :py:meth:`execute` method yet.
        The ``type_code`` can be interpreted by comparing it to the Type Objects specified in the
        section below.
        """
        if self._description is None:
            self._description = []
            for col in self._query_columns_description:
                type_code = col.split(":")[1]
                column_name = col.split(":")[0]
                self._description.append((
                    column_name,
                    type_code,
                    None, None, None, None, True
                ))
        return self._description

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def close(self):
        """Close the operation handle"""
        self.connection.close(self._query_id)
        pass

    def execute(self, operation, parameters=None, **kwargs):
        """Prepare and execute a database operation (query or command).
        Return values are not defined.
        """
        # Prepare statement
        if parameters is None:
            sql = operation
        else:
            sql = operation % _escaper.escape_args(parameters)

        client = self.connection.client
        self._query_id = client.prepareStatement(sql)
        client.executeStatement(self._query_id)

        _logger.info("getting result metadata")
        buffer = client.getResultMetadata(self._query_id)
        buffer = BytesIO(buffer)
        self._query_columns_description = get_query_columns_info(buffer)
        _logger.info("finished populating metadata")
        return

    def cancel(self):
        """Uniphi does not support cancelling of queries as yet"""
        pass

    def _fetch_more(self):
        _logger.info("fetching batch")
        batch_size = self._arraysize
        self._data = list()
        for i in range(batch_size):
            row = self.fetchone()
            if row is None:
                return
            self._data.append(row)

        _logger.info("fetched batch of {num}".format(num=len(self._data)))
        return self._data

    def _fetch_all(self):
        _logger.info("fetching all from overriden method")
        self._data = list()
        row = self.fetchone()
        while row:
            self._data.append(row)
            row = self.fetchone()

        return self._data

    def fetchall(self):
        _logger.info("fetching all")
        return self._fetch_all()

    def fetchone(self):
        _logger.info("fetching one")
        client = self.connection.client
        buffer = client.getNextResultRow(self._query_id)

        if not buffer:
            return None

        buffer = BytesIO(buffer)
        dis = DataInputStream(buffer)
        value_array = read_values_from_array(self._query_columns_description, dis)
        return value_array

    def __iter__(self):
        return self

    def __next__(self):
        return next(self.select_in_batch())

    def select_in_batch(self):
        for i in range(self._count):
            yield self.fetchone()

    def poll(self, get_progress_update=True):
        """Poll for and return the raw status data provided by the Hive Thrift REST API.
        :returns: ``ttypes.TGetOperationStatusResp``
        :raises: ``ProgrammingError`` when no query has been started
        .. note::
            This is not a part of DB-API.
        """
        pass

    def fetch_logs(self):
        """Retrieve the logs produced by the execution of the query.
        Can be called multiple times to fetch the logs produced after the previous call.
        :returns: list<str>
        :raises: ``ProgrammingError`` when no query has been started
        .. note::
            This is not a part of DB-API.
        """
        pass


class Error(Exception):
    pass


if __name__ == '__main__':
    now = datetime.datetime.now()
    print('Query started at', now)
    connection = connect(host='107.21.159.218',
                         port=9000,
                         scheme='e6xdb',
                         username='admin',
                         database='s3a://e6x2-tpcds-spark/parquet330mb',
                         auth=None,
                         configuration=None,
                         kerberos_service_name=None,
                         password='admin',
                         check_hostname=None,
                         ssl_cert=None,
                         thrift_transport=None)
    cursor = Cursor(connection)
    print('Cursor created at', datetime.datetime.now() - now)
    # cursor.execute("select count(*) from date_dim")
    # count_data = cursor.fetchone()
    # print(count_data[0])
    # cursor._count = count_data[0]
    cursor.execute("select * from date_dim")
    bdata = cursor.select_in_batch()
    count = 0
    print('Query time', datetime.datetime.now() - now)
    for item in bdata:
        print(count, item)
        count += 1
        if count > 3:
            break
    cursor.close()
    print('Execution time', datetime.datetime.now() - now)
    # try:
    #     while bdata:
    #         print(len(bdata))
    #         bdata = cursor._fetch_more()
    # except Exception as e:
    #     cursor.close()

#
# Type Objects and Constructors
#

for type_id in PRIMITIVE_TYPES:
    name = TypeId._VALUES_TO_NAMES[type_id]
    setattr(sys.modules[__name__], name, DBAPITypeObject([name]))
