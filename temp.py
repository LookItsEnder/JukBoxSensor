import asyncio
import time
#import Adafruit_ADS1x15
import json
import asyncio
import websockets

with open("station.json",'r') as file:
    stat_data = json.load(file)

async def connect_to_wss():
    global stat_data
    uri = f"wss://ws.jukbox.remllez.com:{stat_data['port']}/pubsub/juk/"
    async with websockets.connect(uri) as websocket:
        while(True):
            #adc = Adafruit_ADS1x15.ADS1115(address=0x48, busnum=1)
            GAIN = 16
            #f = open('Geophone_Data.txt','w')
            t0 = time.time()
            t_end = time.time() + 1
            #time.time() < t_end
            json_string = '''{
            "start": 0,
            "end": 0,
            "data": [],
            "network": "",
            "station": "",
            "location": "",
            "channel": "",
            "sampleRate": 50,
            "id": ""
            }'''
            jukdata = json.loads(json_string)
            jukdata['start'] = int(round(t0,3)*1000)
            jukdata['end'] = int(round(t_end,3)*1000)
            jukdata['network'] = stat_data['network']
            jukdata['station'] = stat_data['station']
            jukdata['location'] = stat_data['location']
            jukdata['channel'] = stat_data['channel']
            jukdata['id'] = f"{stat_data['network']}.{stat_data['station']}.{stat_data['location']}.{stat_data['channel']}"
            while(time.time() < t_end):#True):
                #value = adc.read_adc_difference(0, gain=GAIN)
                #f.write(f"{value}\n")
                value = 15
                jukdata['data'].append(value)
                
                await asyncio.sleep(0.01) 

            #f.close()
            
            message = json.dumps(jukdata, indent=2)
            await websocket.send(message)
            print(len(jukdata['data']))
            print(f"Data collection took {time.time() - t0:.2f} seconds")
        
        
if __name__ == "__main__":
    asyncio.run(connect_to_wss())



# async def noop(websocket):
#     await websocket.wait_closed()

# async def show_data(server):
#     message = "Hello World!"
#     broadcast(server.connections, message)
#     await asyncio.sleep(5)

# async def main():
#     async with serve(noop, "localhost", port=portconfig.port_s) as server:
#         while(True):
#             await show_data(server)

# if __name__ == "__main__":
#     asyncio.run(main())
