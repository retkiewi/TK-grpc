from configparser import ConfigParser

import grpc
import concurrent.futures
from Connection import GRPCConnection
from Message.MessageAbstracts import GRPCMessage


class GRPCQueryDispatcher:
    def dispatch_query(self, query: GRPCMessage):
        print(f'Dispatching to {query.topic()}')
        with GRPCConnection.from_config(query.topic()) as gc:
            results = []
            grpcm = query.grpc()
            for path in query.paths:
                res = gc.get_result(grpcm(path)).return_value
                if query.approved(res):
                    results.append(path)
            return {"paths":results}


class GRPCQueryListener:
    def listen(self, add_func, server_config_name):
        config = ConfigParser()
        config.read('config.ini')
        address = config['GRPC'].get(server_config_name)
        print(f'listening to {server_config_name}@{address}')

        server = grpc.server(concurrent.futures.ThreadPoolExecutor(max_workers=10))
        add_func(server)
        server.add_insecure_port(address)
        server.start()
        server.wait_for_termination()


