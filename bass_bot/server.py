"""
Server module which contains launcher for webhook method
"""
import logging
import ssl
from telebot import types
from aiohttp import web

from config import WH_LISTEN, WH_PORT, WH_SSL_CERT, WH_SSL_PRIV, WH_URL_BASE, WH_URL_PATH, bot, log

logging.basicConfig(level='INFO')


async def handle(request):
    if request.match_info.get('token') == bot.token:
        request_body_dict = await request.json()
        update = types.Update.de_json(request_body_dict)
        bot.process_new_updates([update])
        return web.Response()

    return web.Response(status=403)


def serv_start():
    context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
    log.debug(f'Trying to load cert, path is {WH_SSL_PRIV} and {WH_SSL_CERT}')
    context.load_cert_chain(WH_SSL_CERT, WH_SSL_PRIV)

    bot.remove_webhook()
    bot.set_webhook(url=WH_URL_BASE + WH_URL_PATH, certificate=open(WH_SSL_CERT, 'r'))

    app = web.Application()
    app.router.add_post('/{token}/', handle)

    web.run_app(app, host=WH_LISTEN, port=WH_PORT, ssl_context=context)
    log.debug(f'App is running')
