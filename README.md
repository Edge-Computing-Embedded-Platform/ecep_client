# Edge-computing-embedded-platform
Project aims at providing a common platform for edge computing applications such as video analytics, smart city and so on. 
This is helps in orchestration of end devices

###Hardware Requirements: 
**End Node:** A linux embedded board (Ex:Beaglebone Black Rev C)


**End Node:**
* For dockers, library to be installed is docker.io

      `apt-get install docker.io`
  
* To fetch CPU info: psutil, json, requests, has to be installed.
  
      `sudo pip install psutil simplejson requests`
      
* Wamp messaging services are used. Library to be installed is autobahn

      `pip install autobahn`
