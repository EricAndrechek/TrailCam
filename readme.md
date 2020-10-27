# Open Trail Cam
The repository for a open sourced and free trail cam service easy to install on raspberry pi's.

For the purpose of this readme, the following examples will be outlined on a raspberry pi.

## Installation
To begin, install [motion](https://motion-project.github.io/) on your camera hardware.
This can be accomplished by running `sudo apt-get install motion`

Next, you'll need to install this repo onto your pi. This is done by pasting `git clone https://github.com/EricAndrechek/TrailCam.git`

Now we need to tell our pi what we want it to do on boot. We need to make the boot file executable and then edit rc.local and tell it to run our boot script.

First navigate to the motion directory by typing `cd TrailCam/motion`
Now there should be a file called boot.sh. Make that file executable by running `sudo chmod +x boot.sh`

Run `sudo nano /etc/rc.local` or open it in your desired editor and then add a line above `exit 0` so that it says `sudo bash /home/pi/TrailCam/motion/boot.sh &`

Your rc.local file should look something like this:

```bash
#!/bin/sh -e
#
# rc.local
#
# This script is executed at the end of each multiuser runlevel.
# Make sure that the script will "exit 0" on success or any other
# value on error.
#
# In order to enable or disable this script just change the execution
# bits.
#
# By default this script does nothing.

# Print the IP address
_IP=$(hostname -I) || true
if [ "$_IP" ]; then
  printf "My IP address is %s\n" "$_IP"
fi

sudo bash /home/pi/TrailCam/motion/boot.sh &

exit 0
```

Now we need to install the python modules required. To install them, run `pip3 install -r requirements.txt`

Now create service accounts for firebase and google cloud storage and download the .json files and copy and paste the contents into the firebase.json and cloud-storage.json, with firebase's web data put into database.json.

