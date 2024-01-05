# Description about this project.

### Goal
Dobot plays tictactoe on a 4-by-4 field with reinforcement learning.

### Two big parts in implementation
- play with Dobot
- reinforcement learning

### Progress so far
- play on a 4-by-4 with random choice


### Future works
- Understanding and implementing reinforcement learning
    -- details
- Fixing the detection system.

---

## important things
- Release the white button when putting Enter in Calibration
- API uses 32bits python

## current issue
- when detecting over 25 intersections, get an error in dicision of each area

## working on
- system will reuse intersection data from first detection.

- combine AI with this project.
--- 

## About API

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



## Overflow of API error

solution: changing to new laptop.

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



