import sys
from EventPublisher import Environment
from EventPublisher import Configuration, Send

Send.send_events_a('[{"name":"a"}, {"name":"aa"}]')
#Environment.set_environment()
