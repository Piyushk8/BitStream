import dramatiq

from dramatiq.brokers.redis import RedisBroker

broker = RedisBroker(host="localhost", port=6379, db=0)

dramatiq.set_broker(broker=broker)


