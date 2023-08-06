import sys
import os
from pathlib import Path

currentDirectory = os.getcwd()
path = Path(currentDirectory) 

eventPublisherDirectory = currentDirectory + "\EventPublisher"
u2Path = str(path.parent.absolute()) + '\\PYEVENTS\\EventPublisher'

sys.path.append(eventPublisherDirectory)
sys.path.append(u2Path)

print(sys.path)
print(u2Path)

import EventHub.SendEvents as SendEvents

SendEvents.run('order.scheduled')
print('order.scheduled events were sent.')


