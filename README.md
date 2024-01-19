<!-- omit from toc -->
# Description About TicTacToe With Deep-Q Learning

Dobot plays tictactoe on a 4-by-4 field with reinforcement learning.

<!-- omit from toc -->
## Table of Contents
- [Start up](#start-up)
    - [Install core software](#install-core-software)
    - [Install packages](#install-packages)
    - [run the project](#run-the-project)
- [Role of each file](#role-of-each-file)
- [working environment](#working-environment)
- [Packages](#packages)
- [How to change python version with pip](#how-to-change-python-version-with-pip)
- [About API](#about-api)
  - [Overflow of API error in October, 2023 (fixed)](#overflow-of-api-error-in-october-2023-fixed)
- [System Structure](#system-structure)
- [Possible Errors](#possible-errors)
- [Photos](#photos)


## What we improved in this fall semester in 2023
- extended field size to 4-by-4 field.
- combined AI with TicTacToe.

## Two big parts in implementation
- 4-by-4 TicTacToe on Dobot
- reinforcement learning

## References
3-by-3 TicTacToe on Dobot: https://github.com/v3gard/opencv_tictactoe_engine

Deep-Q-learnig on n-by-n field TicTacToe: https://github.com/kaifishr/TicTacToe

---

## Important things
- API is available only for 32bits python
- AI is available only for 64bits python
---

# Start up
needs two environments: 64bit python, 32bit python on windows


### Install core software
1. install Logitech Camera Settings

2. install DobotStudio (DOBOT Magician) v1.9.4 · Jan 10, 2022

3. install python 3.10 (64bit) and python 3.10 (32bit) series installer from https://www.python.org/downloads/windows/

### Install packages
Run the following code

```
py -3.10-32 -m pip install -r game_requirements.txt
py -3.10 -m pip install -r ai_requirements.txt
```

### run the project

Create a folder named "TTT_project" in Desktop 

Open it with Editer (Visual Studio Code)

Open terminal from "New Terminal" in "Terminal" on the menu bar

Run the following command.

```
git clone https://github.com/PotatoPotato12345678/TTT
cd TTT
```

Run the following code.

```
py -3.10 ai_setup.py
```

It doesn't output anything, but it's fine.

create a new Terminal from "New Terminal" in "Terminal"

Run the following command.
If it doesn't work, make sure your current directory on terminal using `cd`, `pwd` command. The path must be like this: `C:\Users\Robolab\Desktop\TTT_project\TTT`

```
cd TTT
py -3.10-32 .\Calibrate_Dobot.py
```



> WARNING! 
>
> Calibration data already exists!
>
>If you continue, the existing data will be deleted.
>
>Continue? [y\/N]

If above statement is printed, put 'y' and push Enter.

>1\. Calibrate Dobot for Tic Tac Toe board
>
>2\. Show Dobot arm position
>
>3\. Reinitialize home position
>
>4\. Test calibration (without tokens)
>
>5\. Pick and place token
>
>X. Exit

put '1' and push Enter.


>            +-------------+
>            |  1  2  3  4 | 
>            |  5  6  7  8 |  O1 05
>            |  9 10 11 12 |  O2 06
>            | 13 14 15 16 |  O3 07
>            |     D       |  04 08
>            +-------------+   
D is Dobot. Calibrate the field positions from 1 to 16, the buffer positions, Camera position, and pose position in order following the instruction.

- __field position__:  where the arm put a piece

- __buffer position__: where the arm picks up a piece

- __camera position__: where camera see the game field

- __pose position__: where the arm move after game ends

The Dobot arm moves while pushing the white button on the arm.
Make sure the light is green, release the white button when putting Enter.

When setting camera and pose position, open the software "Logitech Camera Settings" and adjust a point. You can use WideScreen or Standard. Close the app before putting Enter key.

After calibration is done, run the following command.

```
py -3.10-32 play.py
```

First move is randomly decided. a person put 'X', AI put 'O'.

Push Enter after putting your piece.

The win condition is to line up 4 pieces in a row.

You can start a game without Dobot with `play.py -m`: It uses /images/Jan5/empty.jpg as a empty field.

---

# Role of each file

__Game System Part__
- tictactoe/\__init__.py : main game system

- play.py : Game system execution file, call Dobot API, manages parser arguments
    - Dobot.py: interface of Dobot API
    - Dobot directory: API itself

- Calibrate_Dobot.py: set up arm positions for each area
    - calibration.data: stored each arm position

__AI part__
- tictactoe/environment.py: main AI system
    - by reference to model.py, utils.py, weights/agent_a_deep_q_learning.pth

- ai_setup.py: AI executiion file

__Communication part between AI Game System and AI__
- data_delivery.txt

--- 

# working environment

__AI__
- python 3.10(64bit) : less than 3.11(64bit) to use pyTorch 

__Game system__
- python 3.10-32(32bit) : 32bit python to use API

---

# Packages

__AI part (version: 3.10)__
- numpy==1.26.3

- opencv-python==4.9.0.80

- imutils==0.5.4

- tensorboard==2.15.1

- torch==2.1.2

__Game system and API part (version: 3.10-32)__
- numpy==1.26.3

- opencv-python==4.9.0.80

- imutils==0.5.4

please make sure available python version to each package in case that you can not install these.

please make sure to install packages into a desired pip version.

--- 
# How to change python version with pip

`py -0p` : check current and available python versions on the windows. current version is shown with '*' at the end.

`py -*.** -m pip list` : (-*.** : put version number) check installed packages in specified python version.

`py -*.** -m pip install ***` : install *** into specified python version.

`py -*.** filename` : run filename with specified version


__change a default pip version__
1. go settings
2. go Edit Environment variables for your account
3. Edit PYTHON_PATH to a desired version in System variables
    the name should be same as the one indicated by command `py -0p`.
4. Restart terminal or PC and comfirm current version by `py -0p`

---

# About API

DobotDll.dll is a API and it is written in C language and it needs 32bit python.
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


## Overflow of API error in October, 2023 (fixed)

solution: manage python verision properly

From this issue, we realized API uses 32bit python.

<details><summary>code details</summary><div>

<br>

__play.py : try to create an instance of DobotManger class in Dobot.py__

```Python
#play.py
api = dType.load()
```
```Python
#Play.py
state = dType.ConnectDobot(api, "", 115200)[0]
dm = DobotManager(dType, api)
```


__DobotManager class :try to initialize the instance__

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

__self.set_speed function is called__

```Python
    #Dobot.py
    def set_speed(self, velocity=100, acceleration=100):
        self.dType.SetPTPCommonParams(self.api, velocity, acceleration, isQueued=0)
```

__call self.dType.SetPTPCommonParams function in DobotDllType.py__

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

__call api.SetPTPCommonParams function in DobotDll.h.__

```Python
# DobotDll.h
extern "C" DOBOTDLLSHARED_EXPORT int SetPTPCommonParams(PTPCommonParams *ptpCommonParams, bool isQueued, uint64_t *queuedCmdIndex);
```
It doesn't return correct value.


</div></details>

--- 
---
---

# System Structure
Game system and AI system cannot communicate to each other directly. Therefore, there is a intermediary file called data_delivery.txt. \__init__.py and ai_setup.py read the file every 1 second, and rewrite it if necessary.

![system-structure](https://github.com/PotatoPotato12345678/TTT/assets/146937279/08b4f76e-a057-463d-a24f-cc1aff4ec7b7)


# Possible Errors

The following things are parts of possible Errors. When it doesn't go well after trying a solution, please try other solution.

In `py -3.10-32 .\Calibrate_Dobot.py`

- Dobot doesn't put a piece onto a correct position: Some Calibration steps don't go well. please calibrate it carefully.

- a piece sticks to Dobot arm: It's a physical problem. Please put tape on the piece.

In `py -3.10-32 play.py`

__Before first movement__

- __OSError:[WinError 193]%1 is not a valid Win32 application__: Make sure you run with `py -3.10-32 play.py`. This Error happens when you use 64bit python.

- __ValueError__: make sure logitech camera is used in detection. the small lights on PC is turned on when camera on PC is used. Please change the first argument in line 228 in \__init__.py to
```
cam = cv2.VideoCapture(1, cv2.CAP_DSHOW)
```
or
```
cam = cv2.VideoCapture(0, cv2.CAP_DSHOW)
```

If it doesn't work yet, please run `py -3.10-32 play.py -d -d -d -d -d`. You then realize images in images/test are updated.

- __Exception: Board is not empty__: Make sure any pieces are not on the field.

__In the middle of game process__

- __Error: Unable to parse gameboard__ or <br>__Unable to detect game board intersections. Try to adjust the weight.__: Make sure anything is not on intersection. If intersection is covered, game board detection doesn't go well. Shadow of pieces might cover it.

- __No new token on board__: Open Logitech Camera Settings and make sure symbol 'X' is shown in camera view. Sometimes, Light reflection hide the symbol.

In `py -3.10 ai_setup.py`

If you want to train AI again, please use this project https://github.com/kaifishr/TicTacToe. After training with deep_q_learning, please put agent_a_deep_q_learning.pth into weights directory.

# Photos

__arrangement__

![IMG_7542](https://github.com/PotatoPotato12345678/TTT/assets/146937279/b8165c89-e65b-4041-a4bb-50c8d79b9ec3)
![IMG_7541](https://github.com/PotatoPotato12345678/TTT/assets/146937279/a082cfb7-712e-46f9-a996-878c791e663d)

__area__

![rc1](https://github.com/PotatoPotato12345678/TTT/assets/146937279/d30e0f2d-c3f5-445f-9818-ff564c47b773)

__Intersection__

![cnt-24](https://github.com/PotatoPotato12345678/TTT/assets/146937279/88f33687-5307-4064-ac34-d5d7961fa3d7)
