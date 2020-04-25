import cherrypy

from config import (WEBHOOK_LISTEN, WEBHOOK_PORT, WEBHOOK_SSL_CERT,
                    WEBHOOK_SSL_PRIV, WEBHOOK_URL_BASE, WEBHOOK_URL_PATH)


class WebhookServer(object):

    def __init__(self, bot):
        self.bot = bot

    @cherrypy.expose
    def index(self):
        if 'content-length' in cherrypy.request.headers and \
                        'content-type' in cherrypy.request.headers and \
                        cherrypy.request.headers['content-type'] == 'application/json':
            length = int(cherrypy.request.headers['content-length'])
            json_string = cherrypy.request.body.read(length).decode("utf-8")
            update = self.bot.types.Update.de_json(json_string)
            # Эта функция обеспечивает проверку входящего сообщения
            self.bot.process_new_updates([update])
            return ''
        raise cherrypy.HTTPError(403)

def serv_start(bot):
    cherrypy.config.update({'server.socket_host': WEBHOOK_LISTEN,
                            'server.socket_port': WEBHOOK_PORT,
                            'server.ssl_module': 'builtin',
                            'server.ssl_certificate': WEBHOOK_SSL_CERT,
                            'server.ssl_private_key': WEBHOOK_SSL_PRIV})

    bot.set_webhook(url=WEBHOOK_URL_BASE + WEBHOOK_URL_PATH,
                    certificate=open(WEBHOOK_SSL_CERT, 'r'))

    cherrypy.quickstart(WebhookServer(bot), WEBHOOK_URL_PATH, {'/': {}})
