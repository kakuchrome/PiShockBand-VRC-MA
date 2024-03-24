from pythonosc.osc_server import AsyncIOOSCUDPServer
from pythonosc.dispatcher import Dispatcher
from configparser import ConfigParser
import requests
import asyncio
import json

config=ConfigParser()
config.read('pishock.cfg')

APIKEY=config['API']['APITOKEN']
USERNAME=config['API']['USERNAME']
NAME=config['API']['APPNAME']
pets=config['PETS']['PETS'].split()
touchpoints=config['TOUCHPOINTS']['TOUCHPOINTS'].split()
shockbones=config['SHOCKBONES']['SHOCKBONES'].split()



verbose=0
funtype="2"
fundelaymax="10"
fundelaymin="0"
funduration="5"
funintensity="0"
funtouchpointstate="False"
funshockbonestate="False"
boolsend='False'
typesend="beep"


def set_verbose(address, *args):
    piverbose=str({args})
    cleanverbose=''.join((x for x in piverbose if x.isdigit()))
    global verbose
    verbose=int(cleanverbose)

#Pet functions
def set_target(address, *args):
    global funtarget
    global pets
    pitarget=str({args})
    cleantarget=''.join((x for x in pitarget if x.isdigit()))
    arratarget=int(cleantarget)
    funtarget=pets[arratarget]
    #print(f"target set to {funtarget}")

def set_pet_type(adress, *args):
    pitype=str({args})
    global funtype
    global typesend
    global verbose
    funtype= ''.join((x for x in pitype if x.isdigit()))
    if funtype == '0':
        typesend="shock"
    if funtype == '1':
        typesend="vibrate"
    if funtype == '2':
        typesend="beep"

    #print(funtype)

def set_pet_intensity(address, *args):
    piintensity=str({args})
    global funintensity
    global verbose
    tempintensity=str(piintensity.strip("{()},")[:4])
    floatintensity=float(tempintensity)
    intensity=floatintensity*100
    funintensity=int(intensity)

    #print(funintensity)

def set_pet_duration(address, *args):
    piduration=str({args})
    global funduration
    global verbose
    cleanduration=str(piduration.strip("{()},")[:4])
    floatduration=float(cleanduration)
    time=floatduration*15
    funduration=int(time)
    #print(funduration)
    #print(cleanduration)

def set_pet_state(address:str, *args) -> None:
    global boolsend
    global verbose
    booltest=str({args})
    boolsend= ''.join((x for x in booltest if x.isalpha()))

    #print(boolsend)

#TouchPointFunctions
def set_touchpoint(address, *args):
    global funtouchpoint
    global funtouchpointstate
    pitouchpointstate=str({args})
    cleantouchpointstate=''.join((x for x in pitouchpointstate if x.isalpha()))
    if cleantouchpointstate == "True":
        pitouchpoint=str({address})
        cleantouchpoint=''.join((x for x in pitouchpoint if x.isdigit()))
        touchpointtarget=int(cleantouchpoint)
        funtouchpoint=touchpoints[touchpointtarget]
        funtouchpointstate=cleantouchpointstate
    if cleantouchpointstate == "False":
        funtouchpointstate=cleantouchpointstate

    print(funtouchpoint)
    print(funtouchpointstate)

def set_TP_type(adress, *args):
    piTPtype=str({args})
    global funTPtype
    global typeTPsend
    global verbose
    funTPtype= ''.join((x for x in piTPtype if x.isdigit()))
    if funTPtype == '0':
        typeTPsend="shock"
    if funTPtype == '1':
        typeTPsend="vibrate"
    if funTPtype == '2':
        typeTPsend="beep"

    print(funTPtype)

def set_TP_intensity(address, *args):
    piTPintensity=str({args})
    global funTPintensity
    global verbose
    tempTPintensity=str(piTPintensity.strip("{()},")[:4])
    floatTPintensity=float(tempTPintensity)
    TPintensity=floatTPintensity*100
    funTPintensity=int(TPintensity)

    print(funTPintensity)

def set_TP_duration(address, *args):
    piTPduration=str({args})
    global funTPduration
    global verbose
    cleanTPduration=str(piTPduration.strip("{()},")[:4])
    floatTPduration=float(cleanTPduration)
    TPtime=floatTPduration*15
    funTPduration=int(TPtime)

    print(cleanTPduration)
    print(funTPduration)


#ShockbonesFunctions
def set_Shockbone(address, *args):
    global funshockbone
    global funshockbonestate
    pishockbonestate=str({args})
    cleanshockbonestate=''.join((x for x in pishockbonestate if x.isalpha()))
    if cleanshockbonestate == "True":
        pishockbone=str({address})
        cleanshockbone=''.join((x for x in pishockbone if x.isdigit()))
        shockbonetarget=int(cleanshockbone)
        funshockbone=shockbones[shockbonetarget]
        funshockbonestate=cleanshockbonestate
    if cleanshockbonestate == "False":
        funshockbonestate=cleanshockbonestate

    print(funshockbone)
    print(funshockbonestate)

def set_SB_type(adress, *args):
    piSBtype=str({args})
    global funSBtype
    global typeSBsend
    global verbose
    funSBtype= ''.join((x for x in piSBtype if x.isdigit()))
    if funSBtype == '0':
        typeSBsend="shock"
    if funSBtype == '1':
        typeSBsend="vibrate"
    if funSBtype == '2':
        typeSBsend="beep"

    print(funSBtype)

def set_SB_intensity(address, *args):
    piSBintensity=str({args})
    global funSBintensity
    global verbose
    tempSBintensity=str(piSBintensity.strip("{()},")[:4])
    floatSBintensity=float(tempSBintensity)
    SBintensity=floatSBintensity*100
    funSBintensity=int(SBintensity)

    print(funSBintensity)

def set_SB_duration(address, *args):
    piSBduration=str({args})
    global funSBduration
    global verbose
    cleanSBduration=str(piSBduration.strip("{()},")[:4])
    floatSBduration=float(cleanSBduration)
    SBtime=floatSBduration*15
    funSBduration=int(SBtime)

    print(cleanSBduration)
    print(funSBduration)

dispatcher = Dispatcher()
#dispatchers for pet functions
dispatcher.map("/avatar/parameters/pishock/Type", set_pet_type)
dispatcher.map("/avatar/parameters/pishock/Intensity", set_pet_intensity)
dispatcher.map("/avatar/parameters/pishock/Duration", set_pet_duration)
dispatcher.map("/avatar/parameters/pishock/Shock", set_pet_state)
dispatcher.map("/avatar/parameters/pishock/Target", set_target)
#dispatchers for touchpoint functions
dispatcher.map("/avatar/parameters/pishock/TPType", set_TP_type)
dispatcher.map("/avatar/parameters/pishock/TPIntensity", set_TP_intensity)
dispatcher.map("/avatar/parameters/pishock/TPDuration", set_TP_duration)
dispatcher.map("/avatar/parameters/pishock/Touchpoint_*", set_touchpoint)
#dispatchers for shockbone functions
dispatcher.map("/avatar/parameters/pishock/SBType", set_SB_type)
dispatcher.map("/avatar/parameters/pishock/SBIntensity", set_SB_intensity)
dispatcher.map("/avatar/parameters/pishock/SBDuration", set_SB_duration)
dispatcher.map("/avatar/parameters/pishock/Shockbone_*", set_Shockbone)
##physbone Parameter option prefix 
##just prepare for logic , maybe prefer to use parameter driver to build shock logic
#dispatcher.map("/avatar/parameters/*_IsGrabbed", tempA)
#dispatcher.map("/avatar/parameters/*_IsPosed", tempB)
#dispatcher.map("/avatar/parameters/*_Angle", tempC)
#dispatcher.map("/avatar/parameters/*_Stretch", tempD)


#verbose functions
dispatcher.map("/avatar/parameters/pishock/Debug", set_verbose)


ip = "127.0.0.1"
port = 9010


async def loop():
    global boolsend
    global verbose
    global funtype
    global funduration
    global funintensity
    global USERNAME
    global NAME
    global SHARECODE
    global APIKEY
    global typesend
    global funtarget
    global funtouchpoint
    global typeTPsend
    global funTPtype
    global funTPduration
    global funTPintensity
    await asyncio.sleep(0.1)
    if boolsend == 'True':
        sleeptime=funduration+1.7
        print(f"sending {typesend} at {funintensity} for {funduration} seconds")
        datajson = str({"Username":USERNAME,"Name":NAME,"Code":funtarget,"Intensity":funintensity,"Duration":funduration,"Apikey":APIKEY,"Op":funtype})
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
        sendrequest=requests.post('https://do.pishock.com/api/apioperate', data=datajson, headers=headers)

        print(f"waiting {sleeptime} before next command")
        print(sendrequest)
        print (sendrequest.text)

        await asyncio.sleep(sleeptime)

    if funtouchpointstate == 'True':
        #original
        #sleeptime=funTPduration+1.7
        
        #prefer touchpoint as a vibration haptic device (reduce sleeptime)
        sleeptime=funTPduration+0.2
        print(f"touch point sending {typeTPsend} at {funTPintensity} for {funTPduration} seconds")
        datajson = str({"Username":USERNAME,"Name":NAME,"Code":funtouchpoint,"Intensity":funTPintensity,"Duration":funTPduration,"Apikey":APIKEY,"Op":funTPtype})
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
        sendrequest=requests.post('https://do.pishock.com/api/apioperate', data=datajson, headers=headers)

        print(f"waiting {sleeptime} before next command")
        print(sendrequest)
        print (sendrequest.text)

        await asyncio.sleep(sleeptime)

    #shockbone function
    if funshockbonestate == 'True':
        sleeptime=funSBduration+5.0
        print(f"touch point sending {typeSBsend} at {funSBintensity} for {funSBduration} seconds")
        datajson = str({"Username":USERNAME,"Name":NAME,"Code":funtouchpoint,"Intensity":funSBintensity,"Duration":funSBduration,"Apikey":APIKEY,"Op":funSBtype})
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
        sendrequest=requests.post('https://do.pishock.com/api/apioperate', data=datajson, headers=headers)

        print(f"waiting {sleeptime} before next command")
        print(sendrequest)
        print (sendrequest.text)

        await asyncio.sleep(sleeptime)


async def init_main():
    server = AsyncIOOSCUDPServer((ip, port), dispatcher, asyncio.get_event_loop())
    transport, protocol = await server.create_serve_endpoint()

    while True:
        await loop()

    transport.close()


asyncio.run(init_main())
