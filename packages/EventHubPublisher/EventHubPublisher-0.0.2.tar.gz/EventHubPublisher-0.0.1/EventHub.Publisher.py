import sys
from EventPublisher import Environment
from EventPublisher import Configuration

#Environment.set_environment()
print(Configuration.get())
print(Configuration.get().EventHub.connection_string )
