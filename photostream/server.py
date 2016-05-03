import logging

from tornado import autoreload
from tornado import ioloop
from tornado.web import Application

from concurrent.futures.process import ProcessPoolExecutor
from blueshed.micro.orm import db_connection, orm_utils
from blueshed.micro.utils import executor
from blueshed.micro.utils.service import Service
from blueshed.micro.web.rpc_handler import RpcHandler
from blueshed.micro.web.rpc_websocket import RpcWebsocket

from photostream.utils.consts import CONSTS
from photostream import actions
from photostream.actions.utils.context import Context


HANDLERS = [
    (r"/websocket/?", RpcWebsocket, {'origins': CONSTS.ORIGINS}),
    (r"/control(.*)", RpcHandler),
]


def make_app():
    db_connection.db_init(CONSTS.DB_URL)

    if CONSTS.POOL_SIZE:
        micro_pool = ProcessPoolExecutor(CONSTS.POOL_SIZE)
        executor.pool_init(micro_pool)
        if CONSTS.DEBUG:
            autoreload.add_reload_hook(micro_pool.shutdown)

    logging.info('Pool size: {}'.format(CONSTS.POOL_SIZE))

    if CONSTS.DEBUG:
        orm_utils.create_all(orm_utils.Base, db_connection._engine_)

    return Application(
        HANDLERS,
        services=Service.describe(actions),
        micro_context=Context,
        debug=CONSTS.DEBUG,
        allow_exception_messages=CONSTS.DEBUG,
        cookie_name=CONSTS.COOKIE_NAME,
        cookie_secret=CONSTS.COOKIE_SECRET,
        ws_url=CONSTS.WS_URL,
        login_url='control/sign_in',
        gzip=True,
    )


def main():
    logging.basicConfig(level=logging.INFO,
        format="[%(levelname)1.1s %(asctime)s %(process)d %(thread)x  %(module)s:%(lineno)d] %(message)s")  # noqa
    logging.getLogger("micro.utils.service").setLevel(logging.WARN)
    logging.getLogger("micro.utils.pika_tool").setLevel(logging.WARN)

    app = make_app()
    app.listen(CONSTS.PORT)
    logging.info("listening on port {}".format(CONSTS.PORT))

    ioloop.PeriodicCallback(RpcWebsocket.keep_alive, 30000).start()
    ioloop.IOLoop.current().start()


if __name__ == "__main__":
    main()
