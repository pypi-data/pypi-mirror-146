from flask import Flask, request, make_response
from kafka import KafkaConsumer
from redis import Redis

from os import environ

from .helper import Helper


class Translator:

  def __init__(self, translation_function: callable) -> None:
      self._translation_function = translation_function

  def translate (self, line: str) -> list:
    return self._translation_function(line)

  def serve (self, host='localhost', port=5000, debug=False):
    app = Flask(__name__)

    @app.route('/metrics')
    def metrics ():
      data = request.get_json(True, True)

      if not data or 'metrics' not in data.keys():
        response = make_response('', 400)
      
      else:
        response = Helper.concatenate_metrics(list(map(self._translation_function, [ line for line in data['metrics'].split('\n') if line ])))
        response = make_response(response, 200)

      response.mimetype="text/plain"
      return response

    app.run(host=host, port=port, debug=debug)

  def prod (self, redis_password='root', kafka_host='localhost', kafka_port=9093, kafka_topic='telegraf'):
    def consume (metrics: list):
      conn = Redis(password=redis_password)
      conn.rpush("METRICS", metrics)
      conn.close()

    consumer = KafkaConsumer(kafka_topic, bootstrap_servers=[ '%s:%i' % (kafka_host, kafka_port) ], value_deserializer=lambda m: Helper.concatenate_metrics(list(map(self._translation_function, m.decode('ascii').split('\n'))) if m else []))
    
    for msg in consumer: 
      if msg.value: 
        consume(msg.value)
