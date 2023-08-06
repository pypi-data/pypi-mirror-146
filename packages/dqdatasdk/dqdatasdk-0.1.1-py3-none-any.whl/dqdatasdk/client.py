# Overwrite rqdatac.client
from rqdatac.client import *
from .dqcertificate import get_dqdata_license


class DummyClient:
    PID = -1

    def execute(self, *args, **kwargs):
        raise RuntimeError("dqdata is not initialized")

    def reset(self):
        pass

    def info(self):
        print('dqdata is not initialized')

    def close(self):
        pass

    execute_with_timeout = execute


_DUMMY = DummyClient()

rqdatac.client._DUMMY = _DUMMY
rqdatac.client._CLIENT = _DUMMY


def init(username, password, *_, **kwargs):
    """initialize dqdatasdk.

    dqdatasdk connection is thread safe but not fork safe. Every thread have their own connection by
    default. you can set param 'use_pool' to True to use a connection pool instead.

    NOTE: if you are using dqdatasdk with python < 3.7 in a multi-process program, remember to call
    reset in child process.

    :param username: string
    :param password: string

    :keyword addr: ('127.0.0.1', 80) or '127.0.0.1:80'
    :keyword connect_timeout: socket connect connect timeout, default is 5 sec.
    :keyword timeout: socket time out, default is 60 sec.
    :keyword lazy: True by default, means "do not connect to server immediately".
    :keyword use_pool: use connection pool. default is False
    :keyword max_pool_size: max pool size, default is 8
    :keyword proxy_info: a tuple like (proxy_type, host, port, user, password) if use proxy, default is None
    :keyword auto_load_plugins: boolean, enable or disable auto load plugin, default to True.
    """

    # 使用 username 和 password 从点宽系统获取保存的license信息，
    # 然后使用license连接rqdata系统
    ###############################################################################################
    _license = get_dqdata_license(username=username, password=password)
    ###############################################################################################
    auth_info = {'username': 'license', 'password': _license, 'ver': rqdatac.__version__}

    addr = kwargs.pop("addr", ("rqdatad-pro.ricequant.com", 16011))

    extra_args = {k: kwargs.pop(k) for k in ('timeout', 'connect_timeout') if k in kwargs}
    proxy_info = kwargs.pop('proxy_info', None)
    rqdatac.client._set_sock_factory(proxy_info)

    logging.getLogger("dqdata").disabled = not kwargs.pop('debug', False)

    if rqdatac.client._CLIENT is not _DUMMY:
        warnings.warn("dqdata is already inited. Settings will be changed.", stacklevel=0)
        reset()

    if not rqdatac.client._PLUGINS_IMPORTED:
        if kwargs.get("auto_load_plugins", True):
            rqdatac.client._auto_import_plugin()
            rqdatac.client._PLUGINS_IMPORTED = True

    if kwargs.pop("use_pool", False):
        from .connections import ConnectionPool
        max_pool_size = kwargs.pop("max_pool_size", 8)
        _CLIENT = ConnectionPool(addr, auth=auth_info, max_pool_size=max_pool_size, **extra_args)
    else:
        from .connections import ThreadLocalConnection
        _CLIENT = ThreadLocalConnection(addr, auth=auth_info, **extra_args)

    _CLIENT.PID = os.getpid()

    def show_info():
        print("DigQuant user: {}".format(username))

    _CLIENT.info = show_info
    rqdatac.client._CLIENT = _CLIENT

    if username == "license":
        quota = get_client().execute("user.get_quota")
        remaining_days = quota["remaining_days"]
        is_trial = quota["license_type"] == "TRIAL"
        if is_trial or 0 <= remaining_days <= 14:
            warnings.warn("Your account will be expired after {} days.".format(remaining_days))
    elif not kwargs.get("lazy", True):
        get_client().execute("get_all_trading_dates")
