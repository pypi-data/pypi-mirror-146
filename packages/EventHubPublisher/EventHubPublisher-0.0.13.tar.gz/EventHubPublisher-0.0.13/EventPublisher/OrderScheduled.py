import sys
import os

currentDirectory = os.getcwd()
eventPublisherDirectory = currentDirectory + "\EventPublisher"
sys.path.append(eventPublisherDirectory)
print(sys.path)

import EventHub.SendEvents as SendEvents

SendEvents.run('order.scheduled')
print('order.scheduled events were sent.')


