# Greenhouse-Automation
Implements automatic responses to sensor inputs in a greenhouse setting.

###WIP
You need to be able to set up an Apache2 server on your RPi, and grant it permissions and make executable the 
/usr/lib/cgi-bin/ where you'll place the files greenhouse_monitor.py and greenhouse_webgui.py.

Currently I can't get a Cronjob to operate the monitor script, so you'll have to manually start it in terminal...
Once that's going you can check your server on a web browser and see the webgui displaying an HTML page. 

Uses a lot of open source code provided by Pyplate repurposed for our use.
