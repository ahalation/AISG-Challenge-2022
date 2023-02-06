# <AI Singapore> National AI Student Challenge 2022

## Objective
**To design and build a tool with AI Singapore's AI Brick PeekingDuck (Computer Vision) and/or SGnlp (Natural Language Processing), that can help, assist, inform or entertain Singaporeans or businesses.**

## Problem Statement

**How might we utilise Computer Vision (PeekingDuck) to aid the correction of poor posture among local students?**

## Proposal: Posture Alert

A tool that monitors the sitting posture of a subject positioned perpendicularly to a monitoring camera to estimate the user's sitting posture and alert when undesirable behaviour is detected (e.g. slouching)

## Procedure: Model Iteration

We created two pipelines to utilise CV to determine 'good' and 'bad' posture given a video input. The first,  `posture_detect`, used a custom trained inference model trained off images taken and classified by the contributors to the project. The resultant model was able to produce relatively accurate results when given images with the appropriate lighting and angle, but failed to give meaningful intepretation when fed a video feed.


The second pipeline, `posture_calc`, builds on the inbuilt PoseNet model within PeekingDuck to relativistically determine with body lengths the posture of a user in a video feed. The feed returns live feedback and tracks positional status in terms of number of frames, which is then output to a csv file throughout the duration of the video feed. A helper python script then estimates the total time elapsed, as well as time spent in various postures, using frame intervals. The resultant data is then used to give a recommendation to the user as to which area of their body to pay more attention to to correct their posture effectively.


The installation instructions will detail the installation of PeekingDuck and its prerequisites through a virtual environment after the download of this repository, as well as the execution of the inbuilt test pipeline.

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
/log/
```

#### 5. Convert the obtained logs to records for keeping track of your posture during the session:
```
python convert_logs.py
```

#### 6. The converted records will be generated as text files of identical name as the origin log in the same directory.

## Execute Pipeline (Mac)

#### 1. Return to the model directory:
```
cd model
```

#### 2. If not already, enter the conda environment:
```
conda activate pkd
```

#### 3. Ensure your webcam is connected, then begin running the pipeline:
```
cd posture_calc
peekingduck run
```
  > Note that this would work well with [Continuity Camera](https://support.apple.com/en-sg/HT213244) as long as your Mac is setup alongside an iPhone so that it can function as a webcam. 

#### 4. Terminated session logs can be found in the output directory of the model:
```
/log/
```

#### 5. Convert the obtained logs to records for keeping track of your posture during the session:
```
python3 convert_logs.py
```

#### 6. The converted records will be generated as text files of identical name as the origin log in the same directory.

## Credits

<!-- prettier-ignore-start -->
<!-- markdownlint-disable -->
<table>
  <tr>
    <td align="center"><a href="https://twitter.com/ahalation"><img src="https://media.licdn.com/dms/image/C5603AQEttkXiu0ekWg/profile-displayphoto-shrink_800_800/0/1657711282858?e=1681344000&v=beta&t=fUlkxONrygQae3NfqF5U0cno96otjN8swqyEUdcjHPY" width="100px;" alt=""/><br /><sub><b>Miguel Ong (@ahalation)</b></sub></a><br /><a href="https://github.com/ahalation" title="Code">💻</a></td>
    <td align="center"><a href="https://www.linkedin.com/in/cheng-nee-siew/"><img src="https://media.licdn.com/dms/image/D5603AQHaQWT_s_8lEw/profile-displayphoto-shrink_800_800/0/1663751899371?e=1681344000&v=beta&t=inlEcE7F7q24qxedoOu_kYsgQ54n8akHHEblcHYz9n8" width="100px;" alt=""/><br /><sub><b>Siew Cheng Nee</b></sub></a><br /><a href="https://github.com/cnjoanne" title="Code">💻</a></td>
    <td align="center"><a href="https://www.linkedin.com/in/kiithy/"><img src="https://media.licdn.com/dms/image/C5603AQHQ9p6XyAlrhw/profile-displayphoto-shrink_800_800/0/1667980946239?e=1681344000&v=beta&t=Tl9-WK_xUVC5iqrqdPJOo5_0cAiSrQDZqs60R5oyfZU" width="100px;" alt=""/><br /><sub><b>Keith Chua</b></sub></a><br /><a href="https://github.com/kiithy" title="Code">💻</a></td>
    <td align="center"><a href="https://www.linkedin.com/in/vidhimahajan/"><img src="https://cdn.pixabay.com/photo/2015/10/05/22/37/blank-profile-picture-973460__340.png" width="100px;" alt=""/><br /><sub><b>Vidhi Mahajan</b></sub></a><br /><a href="https://github.com/cryingcoralclouds" title="Code">💻</a></td>
    
  </tr>
</table>

<!-- markdownlint-restore -->
<!-- prettier-ignore-end -->