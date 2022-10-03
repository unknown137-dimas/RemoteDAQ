"""
/*******************************************************************************
Copyright (c) 1983-2021 Advantech Co., Ltd.
********************************************************************************
THIS IS AN UNPUBLISHED WORK CONTAINING CONFIDENTIAL AND PROPRIETARY INFORMATION
WHICH IS THE PROPERTY OF ADVANTECH CORP., ANY DISCLOSURE, USE, OR REPRODUCTION,
WITHOUT WRITTEN AUTHORIZATION FROM ADVANTECH CORP., IS STRICTLY PROHIBITED. 

================================================================================
REVISION HISTORY
--------------------------------------------------------------------------------
$Log:  $

--------------------------------------------------------------------------------
$NoKeywords:  $
*/
/******************************************************************************
*
* Windows Example:
*    StaticDI.py
*
* Example Category:
*    DIO
*
* Description:
*    This example demonstrates how to use Static DI function.
*
* Instructions for Running:
*    1. Set the 'deviceDescription' for opening the device. 
*    2. Set the 'profilePath' to save the profile path of being initialized device. 
*    3. Set the 'startPort' as the first port for Di scanning.
*    4. Set the 'portCount' to decide how many sequential ports to operate Di scanning.
*
* I/O Connections Overview:
*    Please refer to your hardware reference manual.
*
******************************************************************************/
"""
import sys
sys.path.append('..')
from CommonUtils import kbhit
import time

from Automation.BDaq import *
from Automation.BDaq.InstantDiCtrl import InstantDiCtrl
from Automation.BDaq.BDaqApi import AdxEnumToString, BioFailed

deviceDescription = "USB-4704,BID#0"
profilePath = u"..\\..\\profile\\DemoDevice.xml"
startPort = 0
portCount = 1

def AdvInstantDI():
    ret = ErrorCode.Success

    # Step 1: Create a 'InstantDiCtrl' for DI function.
    # Select a device by device number or device description and specify the access mode.
    # In this example we use ModeWrite mode so that we can fully control the device,
    # including configuring, sampling, etc.
    instantDiCtrl = InstantDiCtrl(deviceDescription)
    for _ in range(1):
        instantDiCtrl.loadProfile = profilePath

        # Step 2: Read DI ports' status and show.
        print("Reading ports status is in progress, any key to quit!")
        while not kbhit():
            ret, data = instantDiCtrl.readAny(startPort, portCount)
            if BioFailed(ret):
                break

            for i in range(startPort, startPort + portCount):
                print("DI port %d status is %#x" % (i, data[i-startPort]))
            time.sleep(1)
        print("\n DI output completed !")

    # Step 3: Close device and release any allocated resource
    instantDiCtrl.dispose()

    # If something wrong in this execution, print the error code on screen for tracking.
    if BioFailed(ret):
        enumStr = AdxEnumToString("ErrorCode", ret.value, 256)
        print("Some error occurred. And the last error code is %#x. [%s]" % (ret.value, enumStr))
    return 0


if __name__ == '__main__':
    AdvInstantDI()
