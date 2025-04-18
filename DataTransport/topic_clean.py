from google.cloud import pubsub_v1
import time

project_id = "cool-furnace-456819-e5"
subscription_id = "my-sub"

subscriber = pubsub_v1.SubscriberClient()
sub_path = subscriber.subscription_path(project_id, subscription_id)

def callback(msg):
    msg.ack()

start = time.time()

pull_future = subscriber.subscribe(sub_path, callback=callback)

with subscriber:
    try:
        pull_future.result(timeout=5)
    except:
        pull_future.cancel()
        pull_future.result()

end = time.time()
print(f"\nCleaned all messages in {end - start:.2f} seconds.")