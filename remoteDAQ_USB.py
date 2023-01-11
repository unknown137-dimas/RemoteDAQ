import sys
sys.path.append('..')
from Automation.BDaq.InstantDiCtrl import InstantDiCtrl
from Automation.BDaq.InstantDoCtrl import InstantDoCtrl
from Automation.BDaq.InstantAiCtrl import InstantAiCtrl
from Automation.BDaq.InstantAoCtrl import InstantAoCtrl
import remoteDAQ_Logger

#Logger Config
my_logger = remoteDAQ_Logger.get_logger('RemoteDAQ_USB')

'''Function to Read Analog Input Signal'''
async def ai_daq(devDesc, portList, decimalPrecision=2, logger=my_logger):
   logger.info('### Starting reading analog input data ###')
   result = {}
   try:
      instanceAiObj = InstantAiCtrl(devDesc)
   except ValueError as e:
      logger.error(e)
      result['success'] = False
      result['data'] = [str(e)]
      return result
   else:
      tmp_list = []
      for i in portList:
         tmp = {}
         _, scaledData = instanceAiObj.readDataF64(i, 1)
         logger.info('Successfully read analog input port #' + str(i))
         tmp['port'] = i
         tmp['data'] = round(scaledData[0], decimalPrecision)
         tmp_list.append(tmp)
      logger.info('### Finished reading analog input data ###')
      instanceAiObj.dispose()
      result['success'] = True
      result['data'] = tmp_list
      return result

'''Function to Read Digital Input Signal'''
async def di_daq(devDesc, portList, logger=my_logger):
   logger.info('### Starting reading digital input data ###')
   result = {}
   try:
      instantDiCtrl = InstantDiCtrl(devDesc)
   except ValueError as e:
      logger.error(e)
      result['success'] = False
      result['data'] = [str(e)]
      return result
   else:
      tmp_list = []
      for i in portList:
         tmp = {}
         _, data = instantDiCtrl.readBit(0, i)
         logger.info('Successfully read digital input port #' + str(i))
         tmp['port'] = i
         tmp['data'] = data
         tmp_list.append(tmp)
      logger.info('### Finished reading digital input data ###')
      instantDiCtrl.dispose()
      result['success'] = True
      result['data'] = tmp_list
      return result

'''Function to Read Digital Output Signal'''
async def doi_daq(devDesc, portList, logger=my_logger):
   logger.info('### Starting reading digital output data ###')
   result = {}
   try:
      instantDoCtrl = InstantDoCtrl(devDesc)
   except ValueError as e:
      logger.error(e)
      result['success'] = False
      result['data'] = [str(e)]
      return result
   else:
      tmp_list = []
      for i in portList:
         tmp = {}
         _, data = instantDoCtrl.readBit(0, i)
         logger.info('Successfully read digital output port #' + str(i))
         tmp['port'] = i
         tmp['data'] = data
         tmp_list.append(tmp)
      logger.info('### Finished reading digital output data ###')
      instantDoCtrl.dispose()
      result['success'] = True
      result['data'] = tmp_list
      return result

'''Function to Write Analog Output Signal'''
async def ao_daq(devDesc, data, logger=my_logger):
   logger.info('### Starting writing analog output data ###')
   result = {}
   try:
      instantAoCtrl = InstantAoCtrl(devDesc)
   except ValueError as e:
      logger.error(e)
      result['success'] = False
      result['data'] = [str(e)]
      return result
   else:
      tmp_list = []
      for i in range(len(data)):
         tmp = {}
         _ = instantAoCtrl.writeAny(i, 1, None, [data[i]])
         logger.info('Successfully write analog output port #' + str(i))
         tmp['port'] = i
         tmp['data'] = data[i]
         tmp_list.append(tmp)
      logger.info('### Finished writing analog output data ###')
      instantAoCtrl.dispose()
      result['success'] = True
      result['data'] = tmp_list
      return result
   
'''Function to Write Digital Output Signal'''
async def do_daq(devDesc, data, logger=my_logger):
   logger.info('### Starting writing digital output data ###')
   result = {}
   try:
      instantDoCtrl = InstantDoCtrl(devDesc)
   except ValueError as e:
      logger.error(e)
      result['success'] = False
      result['data'] = [str(e)]
      return result
   else:
      tmp_list = []
      for i in range(len(data)):
         tmp = {}
         _ = instantDoCtrl.writeBit(0, i, data[i])
         logger.info('Successfully write digital output port #' + str(i))
         tmp['port'] = i
         tmp['data'] = data[i]
         tmp_list.append(tmp)
      logger.info('### Finished writing digital output data ###')
      instantDoCtrl.dispose()
      result['success'] = True
      result['data'] = tmp_list
      return result