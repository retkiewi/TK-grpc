from configparser import ConfigParser

import grpc
from Connection import GRPCConnection
from Message.MessageAbstracts import GRPCMessage


class GRPCQueryDispatcher:
    def dispatch_query(self, query: GRPCMessage):
        with GRPCConnection.from_config(query.filter_name) as gc:
            results = []
            grpcm = query.grpc()
            for path in query.paths:
                res = gc.get_result(grpcm(path)).return_value
                if query.approved(res):
                    results.append(path)
            return results


class GRPCQueryListener:
    def listen(self, add_func, server_config_name):
        server = grpc.server(concurrent.futures.ThreadPoolExecutor(max_workers=10))
        add_func(server)
        config = ConfigParser()
        config.read('config.ini')
        server.add_insecure_port(config['GRPC'].get(server_config_name))
        server.start()
        server.wait_for_termination()

