from .Base import *

EventHub.connection_string = "Endpoint=sb://storis-eventhub-devel.servicebus.windows.net/;SharedAccessKeyName=SendAndListenAccessPolicy;SharedAccessKey=bGdkSFKIdnWx3eIJ0OXzIYG18WZgKQM46z6gWP/OHc8=;EntityPath=ingestion"
EventHub.name = "ingestion"
