from azure.eventhub.aio import EventHubProducerClient
from azure.eventhub import EventData
import Configuration

async def run(event_type, client_code, events):
    producer = get_producer()
    await send_event_data_batch_with_partition_key(producer, event_type, client_code, events)


async def send_event_data_batch_with_partition_key(producer, event_type, client_code, events):
    #Specifying partition_key
    event_data_batch_with_partition_key = await producer.create_batch(partition_key=get_partition_key(event_type))

    #Add events to the batch.
    length = len(events)
    for index in range(0, length):
        event_data = create_event_data(events[index], client_code, event_type)
        event_data_batch_with_partition_key.add(event_data)
        #print(event_data)
        
    await producer.send_batch(event_data_batch_with_partition_key)

def get_producer():
    producer = EventHubProducerClient.from_connection_string(
        conn_str=get_connection_string(), 
        eventhub_name=get_eventhub_name())
    return producer

def get_connection_string():
    print(Configuration.get())
    return Configuration.get().EventHub.connection_string

def get_eventhub_name():
    return Configuration.get().EventHub.name

def get_partition_key(event_type):
    return event_type

def create_event_data(event_body, client_code, event_type):
    event_data = EventData(str(event_body))
    event_data.properties = {'event_type': event_type, 'client_code': client_code}
    return event_data

    


