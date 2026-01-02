import asyncio
import time
import Adafruit_ADS1x15
import json
import asyncio
import websockets

async def connect_to_wss():
    uri = "wss://ws.jukbox.remllez.com:443/pubsub/juk/"
    async with websockets.connect(uri) as websocket:
        while(True):
            adc = Adafruit_ADS1x15.ADS1115(address=0x48, busnum=1)
            GAIN = 16
            #f = open('Geophone_Data.txt','w')
            t0 = time.time()
            t_end = time.time() + 1
            #time.time() < t_end
            json_string = '''{
            "start": 0,
            "end": 0,
            "data": [],
            "network": "WW",
            "station": "JUK",
            "location": "02",
            "channel": "BHN",
            "sampleRate": 50,
            "id": "WW.JUK.02.BHN"
            }'''
            jukdata = json.loads(json_string)
            jukdata['start'] = int(round(t0,3)*1000)
            jukdata['end'] = int(round(t_end,3)*1000)
            while(time.time() < t_end):#True):
                value = adc.read_adc_difference(0, gain=GAIN)
                #f.write(f"{value}\n")
                jukdata['data'].append(value)
                
                await asyncio.sleep(0.01) 

            #f.close()
            
            message = json.dumps(jukdata, indent=2)
            await websocket.send(message)
            print(len(jukdata['data']))
            print(f"Data collection took {time.time() - t0:.2f} seconds")
        
        
if __name__ == "__main__":
    asyncio.run(connect_to_wss())
