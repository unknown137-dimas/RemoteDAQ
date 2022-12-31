
from uuid import uuid3, NAMESPACE_DNS
from socket import gethostname
from influxdb_client.client.influxdb_client import InfluxDBClient
from datetime import datetime
import remoteDAQ_Logger
from remoteDAQ_USB import ai_daq, di_daq, doi_daq


# InfluxDB Client Config
bucket = 'remote-data-acquisition' # CHANGE THIS
org = 'UGM' # CHANGE THIS
token = 'PXCJT5naU4g1R04-b9U_MtMBFLYkimD4-QZ0GyswJiBwov7MzOMj_ABppwuxvNXIK2HknQnp_qrVYXLfwY2cww=='  # CHANGE THIS
url='http://192.168.117.132:8086' # CHANGE THIS
send_to_db = False

# DAQ Config
devDesc = 'USB-4704,BID#0' # CHANGE THIS
portList = [_ for _ in range(0,8)]

#Logger Config
my_logger = remoteDAQ_Logger.get_logger('RemoteDAQ')

# Node Config
dev_id = str(uuid3(NAMESPACE_DNS, gethostname()))
      
'''Create an InfluxDB Dictionary'''
def line_protocol(measurement_name, port, value, id):
   return '{measurement},nodeID={id},port={port} value={val}'.format(
         measurement=measurement_name,
         id=id,
         port=port,
         val=value
      )

'''Send Data to InfluxDB'''
def send_to_influxdb(url, token, org, bucket, data, logger=my_logger):
   with InfluxDBClient(url, token, org) as client:
      with client.write_api() as write_client:
         logger.info('### Starting Sending input data to DB ###')
         write_client.write(bucket, data)

'''Main Function'''
async def main(devDesc, portList):
   ai_res = await ai_daq(devDesc, portList)
   di_res = await di_daq(devDesc, portList)
   doi_res = await doi_daq(devDesc, portList)

if __name__ == '__main__':
   now = datetime.now()
   while True:
        check = datetime.now()
        diff = check - now
        if diff.total_seconds() > 5:
            print(datetime.now())
            print('Starting...')
            
            # t1 = Thread(target=square, args=(iter, iter2))
            # t2 = Thread(target=cube, args=(iter2, iter))
            # t3 = Thread()
            # t1.start()
            # t2.start()
            # t1.join()
            # t2.join()
            print('Finished...')
            print(datetime.now())
            now = check