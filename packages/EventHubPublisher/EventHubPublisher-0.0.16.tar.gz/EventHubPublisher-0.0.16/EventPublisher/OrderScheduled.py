import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__)))

import EventHub.SendEvents as SendEvents

SendEvents.run('order.scheduled')
print('order.scheduled events were sent.')


