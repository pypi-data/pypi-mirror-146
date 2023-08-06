# overwrite connections, catch exception and raise
from rqdatac import thread_local, connection_pool
from rqdatac.share.errors import RQDataError


class ThreadLocalConnection(thread_local.ThreadLocalConnection):
    def execute(self, method, *args, **kwargs):
        try:
            return super(ThreadLocalConnection, self).execute(method, *args, **kwargs)
        except RQDataError as e:
            raise e.__class__() from None


class ConnectionPool(connection_pool.ConnectionPool):
    def execute(self, method, *args, **kwargs):
        try:
            return super(ConnectionPool, self).execute(method, *args, **kwargs)
        except RQDataError as e:
            raise e.__class__() from None
