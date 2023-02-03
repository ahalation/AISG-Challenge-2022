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
