from google.cloud import pubsub_v1
from dotenv import load_dotenv
import os

load_dotenv()

# TODO(developer)
project_id = os.getenv("project_id")
topic_id = os.getenv("topic_id")

publisher = pubsub_v1.PublisherClient()
# The `topic_path` method creates a fully qualified identifier
# in the form `projects/{project_id}/topics/{topic_id}`
topic_path = publisher.topic_path(project_id, topic_id)
print(topic_path)

for n in range(10):
    data_str = f"Ola mundo numero {n}"
    # Data must be a bytestring
    data = data_str.encode("utf-8")

    # When you publish a message, the client returns a future.
    future = publisher.publish(topic_path, data)
    print(future.result())

    print(f"Published messages to {topic_path}.")