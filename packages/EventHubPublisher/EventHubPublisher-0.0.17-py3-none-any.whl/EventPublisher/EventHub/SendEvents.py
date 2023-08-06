import argparse, asyncio, json
import EventHub.Event as Event
import Settings.Environment as Environment

def run(event_type):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        loop.run_until_complete(send_events(event_type))
    except Error:
        print(Error)
    except:
        print("Something went wrong")
    finally:
        loop.close()


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

args, unknown = parser.parse_known_args()

#Set environment
Environment.set_environment(args.env)


    
