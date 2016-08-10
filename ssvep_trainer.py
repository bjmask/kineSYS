#!usb/bin/env/python

import ctypes
import datetime
import os
import speech
import time
import subprocess

import sys

import pandas as pd

from ctypes import *
from numpy import *

from ctypes.util import find_library
# print (ctypes.util.find_library('edk.dll'))
# print (os.path.exists('edk.dll'))
libEDK = cdll.LoadLibrary("edk.dll")

header = ['COUNTER','AF3','F7','F3','FC5','T7','P7','O1','O2','P8','T8','FC6','F4','F8','AF4','GYROX','GYROY','TIMESTAMP','FUNC_ID','FUNC_VALUE','MARKER','SYNC_SIGNAL','USER','CLASS']

# subprocess.Popen(["python", "ssvep_flash.py"])

if len(sys.argv) == 1:
    print "Please enter the name of the user being tested on"
    user_name = str(raw_input()).lower()

    print "Please enter the session time"
    session_time = float(raw_input())

    print "Please enter the number of sessions"
    number_of_sessions = int(raw_input())

    print "Please enter type of class"
    class_type = str(raw_input())
else:
    user_name = sys.argv[1]
    session_time = float(sys.argv[2])
    number_of_sessions = int(sys.argv[3])
    class_type = str(sys.argv[4])

timestamp = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d--%H-%M')

def record_data(session_time=8.0, target=None):
    session_log = pd.DataFrame()
    hData = libEDK.EE_DataCreate()
    libEDK.EE_DataSetBufferSizeInSec(secs)

    start_time = time.time()
    # print ("Buffer size in secs:")
    while time.time() < start_time + session_time + 1:

        if state == 0:
            eventType = libEDK.EE_EmoEngineEventGetType(eEvent)
            libEDK.EE_EmoEngineEventGetUserId(eEvent, user)
            #libEDK.EE_Event_enum.EE_UserAdded:
            if eventType == 16:
                libEDK.EE_DataAcquisitionEnable(userID, True)
                readytocollect = True

        if readytocollect is True:
            libEDK.EE_DataUpdateHandle(0, hData)
            libEDK.EE_DataGetNumberOfSample(hData, nSamplesTaken)
            print ("Wrote ", nSamplesTaken[0])
            if nSamplesTaken[0] != 0:
                nSam = nSamplesTaken[0]
                arr = (ctypes.c_double * nSamplesTaken[0])()
                ctypes.cast(arr, ctypes.POINTER(ctypes.c_double))
                #libEDK.EE_DataGet(hData, 3,byref(arr), nSam)
                # data = array('d')#zeros(nSamplesTaken[0],double)
                for sampleIdx in range(nSamplesTaken[0]):
                    row = []
                    for i in range(22):
                        libEDK.EE_DataGet(hData,targetChannelList[i], byref(arr), nSam)
                        # print >>f,arr[sampleIdx],",",
                        row.append(str(arr[sampleIdx]))
                    row = ','.join(row) + ',' + user_name + ',' + str(target)
                    row = row.split(',')

                    session_log = session_log.append([row])


            time.sleep(0.2)   
    libEDK.EE_DataFree(hData)
    session_log.columns = header
    return session_log[:((int(session_time) - 1)*128)]

ED_COUNTER = 0
ED_INTERPOLATED = 1
ED_RAW_CQ = 2
ED_AF3 = 3
ED_F7 = 4
ED_F3 = 5
ED_FC5 = 6
ED_T7 = 7
ED_P7 = 8
ED_O1 = 9
ED_O2 = 10
ED_P8 = 11
ED_T8 = 12
ED_FC6 = 13
ED_F4 = 14
ED_F8 = 15
ED_AF4 = 16
ED_GYROX = 17
ED_GYROY = 18
ED_TIMESTAMP = 19
ED_ES_TIMESTAMP = 20
ED_FUNC_ID = 21
ED_FUNC_VALUE = 22
ED_MARKER = 23
ED_SYNC_SIGNAL = 24
# IN DLL(edk.dll)
# typedef enum EE_DataChannels_enum {
# ED_COUNTER = 0, ED_INTERPOLATED, ED_RAW_CQ,
# ED_AF3, ED_F7, ED_F3, ED_FC5, ED_T7,
# ED_P7, ED_O1, ED_O2, ED_P8, ED_T8,
# ED_FC6, ED_F4, ED_F8, ED_AF4, ED_GYROX,
# ED_GYROY, ED_TIMESTAMP, ED_ES_TIMESTAMP, ED_FUNC_ID, ED_FUNC_VALUE, ED_MARKER,
# ED_SYNC_SIGNAL
# } EE_DataChannel_t;

targetChannelList = [ED_COUNTER, ED_AF3, ED_F7, ED_F3, ED_FC5, ED_T7,ED_P7, ED_O1, ED_O2, ED_P8, ED_T8,ED_FC6, ED_F4, ED_F8, ED_AF4, ED_GYROX, ED_GYROY, ED_TIMESTAMP, ED_FUNC_ID, ED_FUNC_VALUE, ED_MARKER, ED_SYNC_SIGNAL]
write = sys.stdout.write
eEvent = libEDK.EE_EmoEngineEventCreate()
eState = libEDK.EE_EmoStateCreate()
userID = c_uint(0)
nSamples = c_uint(0)
nSam = c_uint(0)
nSamplesTaken = pointer(nSamples)
da = zeros(128, double)
data = pointer(c_double(0))
user = pointer(userID)
composerPort = c_uint(1726)
secs = c_float(1)
datarate = c_uint(0)
readytocollect = False
option = c_int(0)
state = c_int(0)


classes_list = {
              0:'Left',
              1:'Up',
              2:'Right',
              3:'Down'
        }

print (libEDK.EE_EngineConnect("Emotiv Systems-5"))

if libEDK.EE_EngineConnect("Emotiv Systems-5") != 0:
    print "Emotiv Engine start up failed."
else:
    print "Emotiv Engine startup has completed successfully.\n\n"

master_session = pd.DataFrame(columns=header)

print "Press any key to being testing"
_ = raw_input()
state = libEDK.EE_EngineGetNextEvent(eEvent)

for _ in range(number_of_sessions):
    
    for target in classes_list:
        print "next class is {0}".format(classes_list[target])
        speech.say("next class is {0}".format(classes_list[target]))
        print "Press any key to continue"
        str(raw_input()).lower()
        for i in range(3):
            if i == 4:
                speech.say('Get ready!')
                print '\n\nGet ready!\n\n'
            time.sleep(0.5)
            print i + 1
            speech.say(str(i + 1))

        session_log = record_data(
            session_time=session_time,
            target=target,
        )

        print "\nDo you want to save the current session?"
        save_session_response = str(raw_input()).lower()

        while save_session_response != 'y':
            for i in range(3):
                if i == 4:
                    speech.say('Get ready!')
                    print '\n\nGet ready!\n\n'
                time.sleep(0.5)
                print i + 1
                speech.say(str(i + 1))
            session_log = record_data(
                session_time=session_time,
                target=target,
            )

            print "Do you want to save the current session? Hit \'y\' to save session.\n"
            save_session_response = str(raw_input()).lower()
        
        master_session = pd.concat([master_session, session_log])

libEDK.EE_EngineDisconnect()
libEDK.EE_EmoStateFree(eState)
libEDK.EE_EmoEngineEventFree(eEvent)

print master_session

master_session.to_csv('./logs/' + timestamp + '_' + user_name + '_' + 'ssvep' + '_' + class_type + '.csv', mode='a', index=None)

print '\nFile has been saved to:' + '/logs/' + timestamp + '_' + user_name + '_' + 'ssvep' + '_' + class_type + '.csv'
