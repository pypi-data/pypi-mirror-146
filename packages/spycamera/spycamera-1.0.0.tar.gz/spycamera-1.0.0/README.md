# Spycamera

Spycamera is a small package to record and save a webcamclip. You can download it from
[Github](https://github.com/Official-BReep/spycam)
too.

##Installation
Install Opencv:
```
pip install opencv-python
```

Install spycamera
```
pip install spycamera==1.0.0
```
Create a python file

Import Package:
```
from spycam import record
```

Write Line:
```
record.webcam(duration_in_seconds, filepath, <False>)
```

Example 1:
```
from spycam import record

record.webcam(10, "video.avi", False)


> 10 seconds video as video.avi in Project folder without Output
```

Example 2:
```
from spycam import record
import os

os.mkdir("video") #Create a folder called video in your Projects folder
record.webcam(30, "./video/video.avi") # 30 seconds Video called video.avi in created video folder
```

