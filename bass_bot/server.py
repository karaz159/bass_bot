"""
Server module which contains launcher for webhook method
"""
import ssl
from telebot import types
from aiohttp import web
from functools import partial

from config import WH_LISTEN, WH_PORT, WH_SSL_CERT, WH_SSL_PRIV, WH_URL_BASE, WH_URL_PATH, sys_log


async def handle(request, bot):
    if request.match_info.get('token') == bot.token:
        request_body_dict = await request.json()
        update = types.Update.de_json(request_body_dict)
        bot.process_new_updates([update])
        return web.Response()


def serv_start(bot):
    context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
    sys_log.debug(f'Trying to load cert, path is {WH_SSL_PRIV} and {WH_SSL_CERT}')
    context.load_cert_chain(WH_SSL_CERT, WH_SSL_PRIV)
    sys_log.debug(f'A`ha, starting!')

    bot.remove_webhook()
    bot.set_webhook(url=WH_URL_BASE + WH_URL_PATH, certificate=open(WH_SSL_CERT, 'r'))

    app = web.Application()
    app.router.add_post('/{token}/', partial(handle, bot=bot))
    web.run_app(app, host=WH_LISTEN, port=WH_PORT, ssl_context=context)
