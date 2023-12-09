from pymongo import MongoClient
import psycopg2
import redis
from elasticsearch import Elasticsearch
from neo4j import GraphDatabase


#  ----------------------------------------Mongo--------------------------------------------
CONNECTION_STRING = "mongodb://admin:12345@localhost:27017/?authMechanism=DEFAULT"
client = MongoClient(CONNECTION_STRING)

db = client.university
collection = db.institute

try:
   collection.delete_many({})
   print("Mongo clear")
except Exception as err:
    print("Mongo error",err)


#  ----------------------------------------Postgres--------------------------------------------
database_name = "university"
user_name = "postgres"
password = "12345"
host_ip = "localhost"
host_port ="5433"
try:
    connection = psycopg2.connect(
        database=database_name,
        user=user_name,
        password=password,
        host=host_ip,
        port=host_port
    )
    connection.autocommit = True
    cursor = connection.cursor()
except Exception as err:
    print("Error connect to Postgres",err)

try:
    delete_query = "DROP TABLE public.visits;"
    cursor.execute(delete_query)
    delete_query = "DROP TABLE public.students;"
    cursor.execute(delete_query)
    delete_query = "DROP TABLE  public.\"timeTable\"; "
    cursor.execute(delete_query)
    delete_query = "DROP TABLE  public.group; "
    cursor.execute(delete_query)
    delete_query = "DROP TABLE  public.lecture;"
    cursor.execute(delete_query)
    delete_query = "DROP TABLE  public.disciplines;"
    cursor.execute(delete_query)
    delete_query = "DROP TABLE  public.specialnost; "
    cursor.execute(delete_query)
    delete_query = "DROP TABLE  public.kafedra;"
    cursor.execute(delete_query)
    delete_query = "DROP TABLE  public.institute;"
    cursor.execute(delete_query)
    print('Postgres clear')
except Exception as err:
    print("Error in Postgres delete",err)

#  ----------------------------------------Redis--------------------------------------------
redis = redis.Redis(
     host= 'localhost',
     port= '6379',
     db=0)

try:
    keys = redis.keys('*')
    redis.delete(*keys)
    print("Redis clear")
except Exception as err:
    print("Error in redis delete ", err)

#  ----------------------------------------Elasticsearch--------------------------------------------
es = Elasticsearch("http://elastic:12345@localhost:9200")

try:
    es.indices.delete(index='materials')
    print("ElasticSearch clear")
except Exception as err:
    print("Error in ES delete",err)

#  ----------------------------------------Neo4j--------------------------------------------
uri = "bolt://localhost:7687"
userName = "neo4j"
password = "root12345"

graphDB_Driver  = GraphDatabase.driver(uri, auth=(userName, password))


with graphDB_Driver.session() as neo_session:
        neo_session.run("MATCH (n) DETACH DELETE n")
        print("Neo4J clear")