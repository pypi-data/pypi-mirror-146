import sys
sys.path.append('../EventPublisher')
from EventHub import SendEvents

SendEvents.run('order.create')


