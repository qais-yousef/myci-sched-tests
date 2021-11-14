# Requirements

## On Jenkins Node

`pip3 install pandas`
`pip3 install matplotlib`
`pip3 install wlauto`
`pip3 install tabulate`
`pip3 install perfetto`

## On Android DUT

You need to install pcmark from Play store.

You need to push `hackbench` binary into `/system/bin`.

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
