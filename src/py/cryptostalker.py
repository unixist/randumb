import argparse
import inotify.adapters
import os
import sys
import time

from randumb import Random

class Stalk(object):
  def __init__(self, path, count, window):
    self.path = path
    self.count = count
    self.window = window
    self.files = []
    self.last = time.time()

  def _reset(self):
    self.files = []
    self.last = time.time()

  def is_random(self, filename):
    try:
      data = open(filename, 'rb').read()
      if len(data) > 0 and Random.is_random(data):
        return True
    except Exception as e:
      pass
    return False

  def _log(self, diff):
    print('Seen {} random files in {} seconds:'.format(len(self.files), diff))
    for f in self.files:
      print(f)

  def meow(self):
    try:
      i = inotify.adapters.InotifyTree(self.path)
      for event in i.event_gen():
        if event:
          (header, type_names, d_name, f_name) = event
          if 'IN_CLOSE_WRITE' in type_names:
            filename = os.path.join(d_name, f_name)
            if self.is_random(filename):

              # Code needs to be a smidge ugly code to get immediate reporting.
              self.files.append(filename)
              now = time.time()
              if now - self.last <= self.window and len(self.files) >= self.count:
                self._log(now - self.last)
                self._reset()
              if now - self.last >= self.window:
                self._reset()
    except Exception as e:
      print('[Error]: ', e)
      return 1
    return 0


if __name__ == '__main__':

  p = argparse.ArgumentParser(description='Detect high throughput of newly-'
                                'created encrypted files.')
  p.add_argument('--path', required=True, help='The directory to watch.')
  p.add_argument('--count', type=int, default=10,
                 help='The number of random files required to be seen within'
                   ' <window>.')
  p.add_argument('--window', type=int, default=60,
                 help='The number of seconds within which <count> random files'
                   ' must be observed.')
  p.add_argument('--sleep', type=float, default=0.0,
                 help='The time in seconds to sleep between processing each new'
                   ' file to determine whether it is random.')

  args = p.parse_args()
  sys.exit(Stalk(args.path, args.count, args.window).meow())
