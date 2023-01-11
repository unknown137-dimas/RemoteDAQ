from fastapi import FastAPI, Body
from pydantic import BaseModel
import uvicorn
from remoteDAQ_USB import ai_daq, ao_daq, di_daq, do_daq, doi_daq
from remoteDAQ_DB_Upload import main, url, bucket, org, token
import asyncio
from apscheduler.schedulers.background import BlockingScheduler
from apscheduler.schedulers.asyncio import AsyncIOScheduler

# DAQ Config
devDesc = 'USB-4704,BID#0' # CHANGE THIS
portList = [_ for _ in range(0,8)]

'''API'''
'''Request Model'''
class request_data(BaseModel):
   data: list

'''Response Model'''
class response_data(BaseModel):
    port: str
    data: str

class response(BaseModel):
    success: bool
    data: list[response_data]

app = FastAPI()
   
@app.get('/ping')
async def ping():
    return 'pong!!!'

@app.get('/analog/input', response_model=response)
async def get_analog_input():
   result = await ai_daq(devDesc, portList)
   return result

@app.get('/digital/input', response_model=response)
async def get_digital_input():
   result = await di_daq(devDesc, portList)
   return result

@app.get('/digital_output/input', response_model=response)
async def get_digital_output_input():
   result = await doi_daq(devDesc, portList)
   return result

@app.put('/analog/output', response_model=response, response_model_exclude={'measurement_name'})
async def set_analog_output(data: request_data = Body(example={'data':[1.2, 3.4]})):
   result = await ao_daq(devDesc, data.data)
   return result

@app.put('/digital/output', response_model=response, response_model_exclude={'measurement_name'})
async def set_digital_output(data: request_data = Body(example={'data':[0, 1, 0, 0, 0, 1, 0, 0]})):
   result = await do_daq(devDesc, data.data)
   return result

if __name__ == '__main__':
   sched = AsyncIOScheduler()
   sched.add_job(lambda: asyncio.run(main(devDesc, portList)), 'interval', seconds=5)
   sched.start()
   uvicorn.run('remoteDAQ_API:app', reload=True)