from google.cloud import pubsub_v1
import json, time

project_id = "cool-furnace-456819-e5"
topic_id = "my-topic"

publisher = pubsub_v1.PublisherClient()
topic = publisher.topic_path(project_id, topic_id)

with open("glitch_all_data.json") as f:
    data = json.load(f)

start = time.time()

for d in data:
    msg = json.dumps(d).encode("utf-8")
    publisher.publish(topic, msg)

end = time.time()

print("Sent", len(data), "records to", topic)
print("Took", round(end - start, 2), "seconds")