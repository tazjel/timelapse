#!/bin/bash

# download web2py and place it in the timelapse folder
git clone https://github.com/web2py/web2py

# move the timelapse application to the web2py/applications/
ln -s timelapse web2py/applications/timelapse

