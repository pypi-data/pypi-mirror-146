import sys
import os
from pathlib import Path

currentDirectory = os.getcwd()
#eventHubDirectory = currentDirectory + "\EventPublisher\EventHub"
#settingsDirectory = currentDirectory + "\EventPublisher\Settings"
eventPublisherDirectory = currentDirectory + "\EventPublisher"
#path = Path(currentDirectory) 
#absolutePath = str(path.parent.absolute())
sys.path.append(eventPublisherDirectory)
#sys.path.append(currentDirectory)
#sys.path.append(eventHubDirectory)
#sys.path.append(settingsDirectory)
#sys.path.append(absolutePath)

import EventHub.SendEvents as SendEvents

SendEvents.send_events_a('[{"name":"a"}, {"name":"aa"}]')
#Environment.set_environment()
