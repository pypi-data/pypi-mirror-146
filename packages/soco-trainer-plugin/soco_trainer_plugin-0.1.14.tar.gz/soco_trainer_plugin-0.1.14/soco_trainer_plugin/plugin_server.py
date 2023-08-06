from .core.server import Connector


class PluginServer(object):
    def __init__(self, trainer, host, port, debug, param, redis_url, mongo_url, server_name):
        self.host = host
        self.port = port
        self.debug = debug
        self.trainer = trainer
        self.param = param
        self.redis_url = redis_url
        self.mongo_url = mongo_url
        self.server_name = server_name

    def run_server(self):
        connector = Connector(debug=self.debug,
                              trainer=self.trainer,
                              param=self.param,
                              mongo_url=self.mongo_url,
                              redis_url=self.redis_url,
                              server_name=self.server_name)
        application = connector.app
        application.run(host=self.host, port=self.port)

