import os
from collections import namedtuple
from pkg_resources import resource_filename

from dotenv import load_dotenv

from blueshed.micro.orm.orm_utils import heroku_db_url


if os.path.isfile('.env'):
    load_dotenv('.env')


def get_debug_env():
    debug = os.getenv('DEBUG', '')
    return False if debug.lower() in ['', 'no', 'false', '0'] else True


def get_db_url_env():
    db_url = os.getenv('CLEARDB_DATABASE_URL')
    if not db_url:
        raise ValueError('Requires CLEARDB_DATABASE_URL environment variable')
    return heroku_db_url(db_url)


def get_origins_env():
    origins = os.getenv('ORIGINS', '').split(',')
    return [o.strip() for o in origins]


def get_cookie_name_env():
    return os.getenv('COOKIE_NAME', 'photo-stream')


def get_cookie_secret_env(default="don't-you-dare-tell-anyone"):
    debug  = get_debug_env()
    secret = os.getenv('COOKIE_SECRET', default)
    if not debug and secret == default:
        raise ValueError('Default cookie secret used on production. Please set COOKIE_SECRET environment variable')  # noqa
    return secret


def get_port_env():
    return int(os.getenv('PORT', 8888))


def get_ws_url():
    return os.getenv('WS_URL', 'ws://localhost:{}/websocket'.format(get_port_env()))  # noqa


def get_pool_size():
    return int(os.getenv('POOL_SIZE', 0))


Constants = namedtuple(
    'Constants',
    'DEBUG, DB_URL, ORIGINS, COOKIE_NAME, COOKIE_SECRET, PORT, WS_URL, POOL_SIZE',  # noqa
)


CONSTS = Constants(
    DEBUG=get_debug_env(),
    DB_URL=get_db_url_env(),
    ORIGINS=get_origins_env(),
    COOKIE_NAME=get_cookie_name_env(),
    COOKIE_SECRET=get_cookie_secret_env(),
    PORT=get_port_env(),
    WS_URL=get_ws_url(),
    POOL_SIZE=get_pool_size(),
)
