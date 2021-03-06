# Requirements

## On Jenkins Node

`pip3 install pandas`
`pip3 install scipy`
`pip3 install matplotlib`
`pip3 install wlauto`
`pip3 install perfetto`

## Common tools on all type of DUTs

- uclampset
- sysbench

### uclampset

We need uclampset which is part of util-linux 2.37.2

`sudo apt install util-linux`

If your distro's version is old you can build it from source:

[https://github.com/util-linux/util-linux](https://github.com/util-linux/util-linux)

```
git clone https://github.com/util-linux/util-linux.git
cd util-linux
./autogen.sh
./configure
make uclampset
sudo cp uclampset /usr/local/bin/
```

### sysbench

On Linux systems you can just install it

`sudo apt install sysbench`

On Android, you need to follow best way to get binaries for your arch

[https://github.com/akopytov/sysbench](https://github.com/akopytov/sysbench)

## On Android DUT

You need to install pcmark from Play store.

Workload-Automation framework should push hackbench binary to the device into
temporary folder when you run the test.

## On Linux DUT

`sudo apt install firefox`
`sudo apt install chromium-browser`
`sudo apt install rt-app`

### Setup firefox for auto media playback

You must login as `jenkins` user and launch firefox GUI and open a youtube
video. On the left-most side of the url bar click on the video icon and select
`allwo video and audio`. By default firefox will block autoplay back.

During some tests we launch fierfox in headless mode to play a youtube video to
create lightweight background activities.

It was observed that the backgound activities is still reasonable even if the
video is blocked from playing back automatically.

### Chromium headless mode note

chromium-browser headless mode allows auto playback via command line, but it
was observed that without adding the additional `--remote-debugging-port=9223`
it'll exit almost immediately.

I suspect the video is not playing back correctly in the background for some
reason and setting the debug port forces the browser not to exit immediately.

So while we will still have some form of background activities generated, but
not the intended one.
