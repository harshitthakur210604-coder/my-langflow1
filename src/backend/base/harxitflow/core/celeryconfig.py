# celeryconfig.py
import os

harxitflow_redis_host = os.environ.get("HARXITFLOW_REDIS_HOST")
harxitflow_redis_port = os.environ.get("HARXITFLOW_REDIS_PORT")
# broker default user

if harxitflow_redis_host and harxitflow_redis_port:
    broker_url = f"redis://{harxitflow_redis_host}:{harxitflow_redis_port}/0"
    result_backend = f"redis://{harxitflow_redis_host}:{harxitflow_redis_port}/0"
else:
    # RabbitMQ
    mq_user = os.environ.get("RABBITMQ_DEFAULT_USER", "harxitflow")
    mq_password = os.environ.get("RABBITMQ_DEFAULT_PASS", "harxitflow")
    broker_url = os.environ.get("BROKER_URL", f"amqp://{mq_user}:{mq_password}@localhost:5672//")
    result_backend = os.environ.get("RESULT_BACKEND", "redis://localhost:6379/0")
# tasks should be json or pickle
accept_content = ["json", "pickle"]
