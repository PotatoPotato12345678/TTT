# Description

### Goal
Dobot plays tictactoe on a 4-by-4 field with reinforcement learning.

### Two big parts in implementation
- play with Dobot
- reinforcement learning

### Progress so far
- implementation for game system and deep-Q-learning

### Future works
- communicate the game system with AI via a server.

### Remaining works

- accuracy of detection
    - when detecting over or less than 25 intersections

- understanding deep-Q-learning

---

## important things
- Release the white button when putting Enter in Calibration
- API is available only for 32bits python
- AI is available only for 64bits python
- AI is only available on last attack

---

## system structure

#### Game System Part
- tictactoe/\__init__.py : main game system

- play.py : main execution file, call Dobot API, manages parser arguments
    - Dobot.py: interface of Dobot API
    - Dobot directory: API itself

- Calibrate_Dobot.py: set up arm positions for each area
    - calibration.data: stored each arm position

#### AI part
- tictactoe/environment.py: main AI system
    - by reference to model.py, utils.py, weights/agent_a_deep_q_learning.pth

- ai_setup.py: AI executiion file

#### server part
- server_setup.py: build a localhost server


## working on
- combine AI with this project.

64bit python
```
py server_setup.py
py ai_setup.py
```

32bit python
```
py Calibrate_Dobot.py
py play.py
```

---

## working environment

#### AI
- python 3.10(64bit) : less than 3.11(64bit) to use pyTorch 

#### Game system and server
- python 3.10-32(32bit) : must use 32bit python to use API

---

## Packages

### AI part 
- numpy

- opencv-python

- imutils

- tensorboard 

- torch

### Game system and server parts
- numpy

- opencv-python

- imutils

please make sure available python version to each package in case that you can not install these.

please make sure to install packages into a desired pip version.

#### How to change a pip version (windows)
- install a specified Python version from python.org

```
py -0p : check current and available python versions
py -*.** -m pip list : (-*.** : put version number) check installed packages in specified python version.
py -*.** -m pip install *** : install *** into specified python version.
py -*.** filename : run filename with specified version
```
#### change a default pip version (windows)
change PYTHON_PATH to a desired version from environment setting

--- 

### About API

DobotDll.dll is a API and it is written in C language
<details><summary>details</summary><div>

```Python
#play.py
import Dobot.DobotDllType as dType
api = dType.load()
```
```Python
# DobotDllType.py
def load():
    if platform.system() == "Windows":
        return CDLL("Dobot\DobotDll.dll",  RTLD_GLOBAL) 
```
DobotDll.dll is a API and it is written in C language

the Functions in C are converted to python in DobotDll.h. We can check its name and arguments
```commandline
# DobotDll.h
#these are part of functions in DobotDll.h
.
.
.
extern "C" DOBOTDLLSHARED_EXPORT int SetPTPJointParams(PTPJointParams *ptpJointParams, bool isQueued, uint64_t *queuedCmdIndex);
extern "C" DOBOTDLLSHARED_EXPORT int GetPTPJointParams(PTPJointParams *ptpJointParams);
extern "C" DOBOTDLLSHARED_EXPORT int SetPTPCoordinateParams(PTPCoordinateParams *ptpCoordinateParams, bool isQueued, uint64_t *queuedCmdIndex);
extern "C" DOBOTDLLSHARED_EXPORT int GetPTPCoordinateParams(PTPCoordinateParams *ptpCoordinateParams);
extern "C" DOBOTDLLSHARED_EXPORT int SetPTPLParams(PTPLParams *ptpLParams, bool isQueued, uint64_t *queuedCmdIndex);
extern "C" DOBOTDLLSHARED_EXPORT int GetPTPLParams(PTPLParams *ptpLParams);

extern "C" DOBOTDLLSHARED_EXPORT int SetPTPJumpParams(PTPJumpParams *ptpJumpParams, bool isQueued, uint64_t *queuedCmdIndex);
extern "C" DOBOTDLLSHARED_EXPORT int GetPTPJumpParams(PTPJumpParams *ptpJumpParams);
extern "C" DOBOTDLLSHARED_EXPORT int SetPTPCommonParams(PTPCommonParams *ptpCommonParams, bool isQueued, uint64_t *queuedCmdIndex);
extern "C" DOBOTDLLSHARED_EXPORT int GetPTPCommonParams(PTPCommonParams *ptpCommonParams);
.
.
.
```

</div></details>

---



### Overflow of API error(fixed)

solution: ~~changing to new laptop.~~

solution: manage python verision properly

notice: OS update is not the cause.

<details><summary>code details</summary><div>


### play.py : try to create an instance of DobotManger class in Dobot.py

```Python
#play.py
api = dType.load()
```
```Python
#Play.py
state = dType.ConnectDobot(api, "", 115200)[0]
dm = DobotManager(dType, api)
```



### DobotManager class :try to initialize the instance
```Python
# Dobot.py
class DobotManager(object):
    def __init__(self, dType, api):
        self.dType = dType
        self.api = api
        data = None
        with open("calibration.data", "r") as f:
            data = f.read()
        jsondata = json.loads(data)
        self.camera, self.buffer, self.slot, self.pose = DobotPosition.deserialize(jsondata)
        self.set_speed(velocity=50)
```

### self.set_speed function is called
```Python
    #Dobot.py
    def set_speed(self, velocity=100, acceleration=100):
        self.dType.SetPTPCommonParams(self.api, velocity, acceleration, isQueued=0)
```

### call self.dType.SetPTPCommonParams function in DobotDllType.py
```Python
def SetPTPCommonParams(api, velocityRatio, accelerationRatio, isQueued=0):
    pbParam = PTPCommonParams()
    pbParam.velocityRatio = velocityRatio
    pbParam.accelerationRatio = accelerationRatio
    queuedCmdIndex = c_uint64(0)
    while(True):
        result = api.SetPTPCommonParams(byref(pbParam), isQueued, byref(queuedCmdIndex))
        if result != DobotCommunicate.DobotCommunicate_NoError:
            dSleep(5)
            continue
        break
    return [queuedCmdIndex.value]
```

### call api.SetPTPCommonParams function in DobotDll.h.
```Python
# DobotDll.h
extern "C" DOBOTDLLSHARED_EXPORT int SetPTPCommonParams(PTPCommonParams *ptpCommonParams, bool isQueued, uint64_t *queuedCmdIndex);
```
It doesn't return correct value.


</div></details>

--- 



