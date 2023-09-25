from milvus import default_server
from pymilvus import connections, utility

class Server:
    def __init__(self):
        self.server = None
        self.connection = None
    def start(self):
        # (OPTIONAL) Set if you want store all related data to specific location
        # Default location:
        #   %APPDATA%/milvus-io/milvus-server on windows
        #   ~/.milvus-io/milvus-server on linux
        # default_server.set_base_dir('milvus_data')

        # (OPTIONAL) if you want cleanup previous data
        # default_server.cleanup()

        # Start you milvus server
        default_server.start()
        self.server = default_server

        # Now you could connect with localhost and the given port
        # Port is defined by default_server.listen_port
        connection = connections.connect(host='127.0.0.1', port=default_server.listen_port)
        self.connection = connection
        print("listen port is: ", default_server.listen_port)

        # Check if the server is ready.
        print(utility.get_server_version())