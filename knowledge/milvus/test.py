
from server import Server
from db import MilvusDB

_HOST = '127.0.0.1'
_PORT = '19530'
_ROOT = "root"
_ROOT_PASSWORD = "Milvus"
_METRIC_TYPE = 'IP'
_INDEX_TYPE = 'IVF_FLAT'
_NLIST = 1024
_NPROBE = 16
_TOPK = 3

# Vector parameters
_DIM = 128
_INDEX_FILE_SIZE = 32  # max file size of stored index

if __name__ == '__main__':
    server = Server()
    # connect to milvus and using database db1
    # there will not check db1 already exists during connect
    connect_to_milvus(db_name="default")

    # create collection within default
    col1_db1 = create_collection("col1_db1", "default")

    # create db1
    if "db1" not in db.list_database():
        print("\ncreate database: db1")
        db.create_database(db_name="db1")

    # use database db1
    db.using_database(db_name="db1")
    # create collection within default
    col2_db1 = create_collection("col1_db1", "db1")

    # verify read and write
    collection_read_write(col2_db1, "db1")

    # list collections within db1
    print("\nlist collections of database db1:")
    print(utility.list_collections())

    print("\ndrop collection: col1_db2 from db1")
    col2_db1.drop()
    print("\ndrop database: db1")
    db.drop_database(db_name="db1")

    # list database
    print("\nlist databases:")
    print(db.list_database())
