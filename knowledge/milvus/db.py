import random

from pymilvus import (
    connections,
    FieldSchema, CollectionSchema, DataType,
    Collection,
    db,
)
from pymilvus.orm import utility

class MilvusDB:
    def __init__(self):
        return
    def connect_to_milvus(host, port, user, password, db_name):
        print(f"connect to milvus\n")
        connections.connect(host, port, user, password, db_name)


    def connect_to_milvus_with_uri(host, port, db_name="default"):
        print(f"connect to milvus\n")
        connections.connect(
            alias="uri-connection",
            uri="http://{}:{}/{}".format(host, port, db_name),
        )


    def create_collection(collection_name, db_name):
        default_fields = [
            FieldSchema(name="id", dtype=DataType.INT64, is_primary=True),
            FieldSchema(name="double", dtype=DataType.DOUBLE),
            FieldSchema(name="fv", dtype=DataType.FLOAT_VECTOR, dim=128)
        ]
        default_schema = CollectionSchema(fields=default_fields)
        print(f"Create collection:{collection_name} within db:{db_name}")
        return Collection(name=collection_name, schema=default_schema)


    def insert(collection, num, dim):
        data = [
            [i for i in range(num)],
            [float(i) for i in range(num)],
            [[random.random() for _ in range(dim)] for _ in range(num)],
        ]
        collection.insert(data)
        return data[2]


    def drop_index(collection):
        collection.drop_index()
        print("\nDrop index sucessfully")


    def search(collection, vector_field, id_field, search_vectors, metric_type, nprobe):
        search_param = {
            "data": search_vectors,
            "anns_field": vector_field,
            "param": {"metric_type": metric_type, "params": {"nprobe": nprobe}},
            "limit": _TOPK,
            "expr": "id >= 0"}
        results = collection.search(**search_param)
        for i, result in enumerate(results):
            print("\nSearch result for {}th vector: ".format(i))
            for j, res in enumerate(result):
                print("Top {}: {}".format(j, res))


    def collection_read_write(collection, db_name, dim, index_type, nlist, metric_type):
        col_name = "{}:{}".format(db_name, collection.name)
        vectors = insert(collection, 10000, _DIM)
        collection.flush()
        print("\nInsert {} rows data into collection:{}".format(collection.num_entities, col_name))

        # create index
        index_param = {
            "index_type": index_type,
            "params": {"nlist": nlist},
            "metric_type": metric_type}
        collection.create_index("fv", index_param)
        print("\nCreated index:{} for collection:{}".format(collection.index().params, col_name))

        # load data to memory
        print("\nLoad collection:{}".format(col_name))
        collection.load()
        # search
        print("\nSearch collection:{}".format(col_name))
        search(collection, "fv", "id", vectors[:3])

        # release memory
        collection.release()
        # drop collection index
        collection.drop_index()
        print("\nDrop collection:{}".format(col_name))


