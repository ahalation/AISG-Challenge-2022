# <AI Singapore> National AI Student Challenge 2022

## Objective
**To design and build a tool with AI Singapore's AI Brick PeekingDuck (Computer Vision) and/or SGnlp (Natural Language Processing), that can help, assist, inform or entertain Singaporeans or businesses.**

## Problem Statement

**How might we utilise Computer Vision (PeekingDuck) to aid the correction of poor posture among local students?**

# Proposal: Posture Alert

A tool that monitors the sitting posture of a subject positioned perpendicularly to a monitoring camera to estimate the user's sitting posture and alert when undesirable behaviour is detected (e.g. slouching)

## Installation (Windows only)

#### 1. Install Python 3.8:
https://www.python.org/downloads/release/python-3810/

#### 2. Enter the model directory:
``` 
cd model
```

#### 3. Initiate virtual environment with Python 3.8:
```
pipenv --python 3.8
```

#### 4. Install PeekingDuck:
```
pipenv install
```

#### 4. Test installation:
```
pipenv shell
cd test_pose
peekingduck run
```

## Installation for Mac (Apple Silicon Mac)
- This solution will work around the use of a pip environment and will use conda to have a separate environment to install mac specific packages.

### 1. Follow the first two steps on the website
- https://peekingduck.readthedocs.io/en/latest/getting_started/03_custom_install.html#apple-silicon-mac
- If you experience an error when trying to run `conda activate`...
```shell
CommandNotFoundError: Your shell has not been properly configured to use 'conda activate'.
If using 'conda activate' from a batch script, change your
invocation to 'CALL conda.bat activate'.

To initialize your shell, run

    $ conda init <SHELL_NAME>

Currently supported shells are:
  - bash
  - cmd.exe
  - fish
  - tcsh
  - xonsh
  - zsh
  - powershell
```

Run the following code
```shell
conda init zsh
```
#### Moving on from the error

-  Make sure to activate the conda environment before moving on to download [Tensorflow](#2-downloading-the-correct-version-of-tensorflow-for-mac) in the next step of this readme.
```shell
conda activate pkd
```
- This is assuming that you created your conda package with the name `pkd`
### 2. Downloading the correct version of Tensorflow for Mac

#### Monterey and Big Sur
- Follow the [documentation](https://peekingduck.readthedocs.io/en/latest/getting_started/03_custom_install.html#apple-silicon-mac) again for step 3.

#### For macOS Ventura
- Run the following
```shell
python -m pip install tensorflow-macos
```
and
```shell
python -m pip install tensorflow-metal
```

### 3. Install PyTorch as per the documentation
```shell
pip3 install torch torchvision torchaudio
```

### 4. Main Installation and verification of Peeking Duck
```shell
pip3 install peekingduck --no-dependencies

peekingduck verify-install
```
- You will see a popout window with a man waving and with the bounding boxes to verify that your version of PeekingDuck is working fine. 


### 5. Note to user
- Always make sure to...
```shell
conda activate pkd
```
so that you will have all the packages needed.
- Never use the `pipenv install` and `pipenv shell` commands as those are meant for other OS.
- `conda` is enough to handle our virtual environments in this case.