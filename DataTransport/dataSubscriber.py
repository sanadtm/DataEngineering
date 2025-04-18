from google.cloud import pubsub_v1
import time
import time

project_id = "cool-furnace-456819-e5"
sub_id = "my-sub"
timeout = 500.0

msgs = []

def callback(msg):
    msgs.append(msg.data)
    msg.ack()

subscriber = pubsub_v1.SubscriberClient()
sub_path = subscriber.subscription_path(project_id, sub_id)

pull = subscriber.subscribe(sub_path, callback=callback)
start = time.time()

with subscriber:
    try:
        pull.result(timeout=timeout)
    except:
        pull.cancel()
        pull.result()

end = time.time()

print("Got", len(msgs), "messages")
print("Took", round(end - start, 2), "seconds")