from datetime import datetime
import json
import requests
# from airflow import DAG
# from airflow.operators.python import PythonOperator

default_args = {
    'owner': 'agus',
    'start_date': datetime(2024, 2, 1, 10, 00)
}

def get_data():
    res = requests.get("https://randomuser.me/api/")
    res = res.json()
    res = res['results'][0]
    return res

def format_data(res):
    data =  {}
    location = res['location']
    # data['id'] = uuid.uuid4()
    data['first_name'] = res['name']['first']
    data['last_name'] = res['name']['last']
    data['gender'] = res['gender']
    data['address'] = f"{str(location['street']['number'])} {location['street']['name']}, " \
                      f"{location['city']}, {location['state']}, {location['country']}"
    data['post_code'] = location['postcode']
    data['email'] = res['email']
    data['username'] = res['login']['username']
    data['dob'] = res['dob']['date']
    data['registered_date'] = res['registered']['date']
    data['phone'] = res['phone']
    data['picture'] = res['picture']['medium']
    return data


def stream_data():
    import json
    from kafka import KafkaProducer
    import time
    res = get_data()
    res = format_data(res)
    # print(json.dumps(res, indent=3))
    # kafka_config = {
    #     'bootstrap_servers': ['localhost:9091'],
    #     'max_block_ms': 5000,
    #     'bootstrap_topics_filter': None
    # }
    producer = KafkaProducer(bootstrap_servers=['broker:9021'],
                             max_block_ms=5000
                             )
    
    # KafkaProducerafkaProducer(bootstrap_servers=['localhost:9092'],
    #           api_version=(0,11,5),
    #           value_serializer=lambda x: dumps(x).encode('utf-8'))

    producer.send('users_created', json.dumps(res).encode('utf-8'))


# with DAG('user_automation',
#          default_args=default_args,
#          schedule_interval='@daily',
#          catchup=False) as dag:
#
#     streaming_task = PythonOperator(
#         task_id='stream_data_from_api',
#         python_callable=stream_data
#     )

stream_data()
# format_data()
