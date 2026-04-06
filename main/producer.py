import pika, json

params = pika.URLParameters('amqps://ssezfdmp:cw8GfYo0mhYVvxWaDIHLvt0cb1pAgTQ1@jaragua.lmq.cloudamqp.com/ssezfdmp')

connection = pika.BlockingConnection(params)

channel = connection.channel()

def publish(method, body):
    properties = pika.BasicProperties(method=method)
    channel.basic_publish(exchange='', routing_key='admin', body=json.dumps(body), properties=properties)
