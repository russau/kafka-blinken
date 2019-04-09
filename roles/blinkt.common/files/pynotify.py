# many thanks to https://github.com/manos/python-inotify-tail_example/blob/master/tail-F_inotify.py

import sys, os, pyinotify
from optparse import OptionParser
from blinkt import set_pixel, show, clear


global myfile 
myfile = "/var/lib/kafka/data/replication-offset-checkpoint"


wm = pyinotify.WatchManager()
    
# watched events on the directory, and parse $path for file_of_interest:
dirmask = pyinotify.IN_MODIFY | pyinotify.IN_DELETE | pyinotify.IN_MOVE_SELF | pyinotify.IN_CREATE
    
# the event handlers:
class PTmp(pyinotify.ProcessEvent):
    def process_IN_MODIFY(self, event):
        if myfile in os.path.join(event.path, event.name):
            print("modify")
            fh = open(myfile, 'r')
            self.getOffset(fh.readlines())
            fh.close()
    

    def process_IN_CREATE(self, event):
        if myfile in os.path.join(event.path, event.name):
            print("create")
            fh = open(myfile, 'r')
            self.getOffset(fh.readlines())
            fh.close()

    
    def getOffset(self, lines):
        # replicated-topic-one 0
        match = [f for f in lines if f.startswith("replicated-topic-one 0")]
        offset = int(match[0].replace("replicated-topic-one 0", ""))
        for i in range(8):
            print(offset % 9)
            red = 255 if offset % 9 > i else 0
            set_pixel(7 - i, red, 0, 0, 0.05)
        show()


notifier = pyinotify.Notifier(wm, PTmp())

# watch the directory, so we can get IN_CREATE events and re-open the file when logrotate comes along.
# if you just watch the file, pyinotify errors when it moves, saying "can't track, can't trust it.. watch 
#  the directory".
index = myfile.rfind('/')
wm.add_watch(myfile[:index], dirmask)

while True:
    try:
        notifier.process_events()
        if notifier.check_events():
            notifier.read_events()
    except KeyboardInterrupt:
        break

# cleanup: stop the inotify, and close the file handle:
notifier.stop()

sys.exit(0)