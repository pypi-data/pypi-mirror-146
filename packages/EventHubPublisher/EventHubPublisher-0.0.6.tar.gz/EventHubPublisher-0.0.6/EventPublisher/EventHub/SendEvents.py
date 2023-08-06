import argparse, asyncio, json
from EventHub import Event
import Environment

def run(event_type):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(send_events(event_type))

async def send_events(event_type):
    events = (json.loads(args.events))
    #print(events)    
    client_code = args.code
    await Event.run(event_type, client_code, events)


#Declare script parameters
parser = argparse.ArgumentParser()
parser.add_argument("--env", help="Sets environment. Development, Production, QA or Learn", type=str)
parser.add_argument("--code", help="Sets Storis client code", type=str)
parser.add_argument("--events", help="Sets Storis client code")

args = parser.parse_args()

#Set environment
Environment.set_environment(args.env)


    
