# <AI Singapore> National AI Student Challenge 2022

## Objective
**To design and build a tool with AI Singapore's AI Brick PeekingDuck (Computer Vision) and/or SGnlp (Natural Language Processing), that can help, assist, inform or entertain Singaporeans or businesses.**

## Problem Statement

**How might we utilise Computer Vision (PeekingDuck) to aid the correction of poor posture among local students?**

# Proposal: Posture Alert

A tool that monitors the sitting posture of a subject positioned perpendicularly to a monitoring camera to estimate the user's sitting posture and alert when undesirable behaviour is detected (e.g. slouching)

## Installation (Windows)

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

#### 5. Verify installation:
```
pipenv shell
cd test_pose
peekingduck run
```

## Installation (Apple Silicon Mac)

#### 1. Follow the first two steps on the website
https://peekingduck.readthedocs.io/en/latest/getting_started/03_custom_install.html#apple-silicon-mac


If you experience an error when trying to run `conda activate`...
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
##### Moving on from the error

-  Make sure to activate the conda environment before moving on to download [Tensorflow](#2-downloading-the-correct-version-of-tensorflow-for-mac) in the next step of this readme.
```shell
conda activate pkd
```
- This is assuming that you created your conda package with the name `pkd`
#### 2. Downloading the correct version of Tensorflow for Mac

##### macOS Monterey and Big Sur
- Follow the [documentation](https://peekingduck.readthedocs.io/en/latest/getting_started/03_custom_install.html#apple-silicon-mac) again for step 3.

##### macOS Ventura
- Run the following
```shell
python -m pip install tensorflow-macos
```
and
```shell
python -m pip install tensorflow-metal
```

#### 3. Install PyTorch
```shell
pip3 install torch torchvision torchaudio
```

#### 4. Main Installation and verification of Peeking Duck
```shell
pip3 install peekingduck --no-dependencies

peekingduck verify-install
```
#### 5. Note to user
  Always make sure to...
```shell
conda activate pkd
```
so that you will have all the packages needed.
- `pipenv` has been tested and does ***not*** work in this implementation without workarounds.
- `conda` is enough to handle our virtual environment in this case.

## Execute Pipeline (Windows)

#### 1. Return to the model directory:
```
cd model
```

#### 2. If not already, enter the pipenv shell:
```
pipenv shell
```

#### 3. Ensure your webcam is connected, then begin running the pipeline:
```
cd posture_calc
peekingduck run
```

#### 4. Terminated session logs can be found in the output directory of the model:
```
/log
```

#### 5. Convert the obtained logs to records for keeping track of your posture during the session:
```
python convert_logs.py
```

#### 6. The converted records will be generated as text files of identical name as the origin log in the same directory.