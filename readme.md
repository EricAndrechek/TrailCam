# Open Trail Cam

The repository for an open-source and free trail cam service easy to install on Raspberry Pi's.

For the purpose of this readme, the following examples will be outlined on a Raspberry Pi.

## Installation

To begin, install [motion](https://motion-project.github.io/) on your camera hardware.
This can be accomplished by running `sudo apt-get install motion` (Note: you will need at least motion 4.2 or higher installed, if apt fails to install an adequate version, you will need to install it manually from their github releases.)

Next, you'll need to install this repo onto your pi. This is done by pasting `git clone https://github.com/EricAndrechek/TrailCam.git`

Now we need to tell our pi what we want it to do on boot. We need to make the boot file executable and then edit rc.local and tell it to run our boot script.

First navigate to the motion directory by typing `cd TrailCam/motion`

There should be a file called `trailcam.service`. We will want to move that file by running `sudo cp trailcam.service /etc/systemd/system/trailcam.service`
Next we run `sudo systemctl daemon-reload` and then `sudo systemctl enable trailcam.service`. It should now run next time you boot up your computer.

Next, we need to move the custom `motion.conf` files to a few places in order to have motion automatically run with our desired settings. Run `sudo cp motion.conf /home/pi/.motion/motion.conf` and `sudo cp motion.conf /etc/motion/motion.conf`.

Now we need to install the python modules required. To install them, run `pip3 install -r requirements.txt`

Now create service accounts for firebase and google cloud storage and download the .json files and copy and paste the contents into the firebase.json and cloud-storage.json, with firebase's web data put into database.json.

Once everything is finished installing and being setup, run `sudo reboot`. To see that everything is working, navigate back to the motion directory with `cd TrailCam/motion` and then view motion logs by running `tail -f motion.log` and view the python logs with `tail -f main.log`.

To run your website to view things in a pretty format, clone this repo to your computer and copy over your credentials and firebase information. Next change the URL's in your `index.html` to reflect your URL's in firebase.

In order to be able to keep track of whether your Pi is online or not, create a free account at [dataplicity](https://dataplicity.com) and follow their installation instructions for your Pi. Finally, change the settings in dataplicity to turn on the web forwarding, and copy the URL they give to `index.html` for the second half of the `reverse_proxy_url`

Once you think you have everything set up, go ahead and run `firebase deploy` and visit your new site!
