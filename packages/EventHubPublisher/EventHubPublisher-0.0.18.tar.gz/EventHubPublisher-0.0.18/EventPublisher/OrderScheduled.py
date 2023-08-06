import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__)))

import EventHub.SendEvents as SendEvents

def run(env_name, client_code, events_json):
    return SendEvents.send_events('order.scheduled', env_name, client_code, events_json)

print(SendEvents.run('order.scheduled'))
print('order.scheduled events were sent.')


