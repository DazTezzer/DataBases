from elasticsearch import Elasticsearch, helpers
import psycopg2
import random

database_name = "university"
user_name = "postgres"
password = "12345"
host_ip = "localhost"
host_port ="5432"
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


# --------------------------elasticsearch таблица Materials-------------------------
kolvo_materials = 300
get_array_lecture_id = "SELECT array_agg(id) FROM public.lecture"
cursor.execute(get_array_lecture_id)
array_lecture_ids=cursor.fetchall()

def get_lecture_id():
    l_id = random.randint(0,len(array_lecture_ids[0][0])-1)
    lecture_id = array_lecture_ids[0][0][l_id]
    return lecture_id

mappings = {
        "properties": {
            "description": {"type": "text"},
            "lecture_id": {"type": "integer"}
    }
}

index_name = "materials"

es = Elasticsearch("http://elastic:12345@localhost:9200")

try:
    es.indices.create(index="materials", mappings=mappings)
except:
    print("index materials exists")

docs = []
description = ['Версионирование и поддержка целостности микросервисной системы', 'Устранение ада зависимостей на примере решения Банка', 'Коммуникация сервисов между собой', 'Почему важны стандарты и какие они бывают. CDC (client driven contracts) и кононические модели данных', 'Under- и Overfetching данных. GraphQL как современный язык разработки контрактов микросервисов. Многоязычные среды', 'Альтернативы и проблемы. Событийная модель и брокеры сообщений. Децентрализованный подход к сервисам аутентификации и авторизации. ',
               'Ролевая модель и уровни доступа. Доступ клиент-сервер и сервер-сервер. Токены, API key, использование различных каналов аутентификации.', ]
try:
    for i in range(kolvo_materials):
        docs.append({
            'description': random.choice(description),
            'lecture_id' : get_lecture_id()
        })
    helpers.bulk(es, docs, index=index_name)
except Exception as err:
    print("Error in creating docs in ES (materials)", err)

print("ES Данные добавлены")