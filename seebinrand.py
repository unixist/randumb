import os
import sys
import math

from elftools.elf.elffile import ELFFile
from elftools.elf.sections import SymbolTableSection

class Entropy(object):
  '''
  Naively estimate content's entropic probability
  '''
  def __init__(self, content, chunk_size=256, byte_width=256, case_sensitive=True):
    '''
    content        - string of bytes to consider
    chunk_size     - number of bytes to evaluate at a time
    byte_width     - spectrum of valid byte values for the content (not working)
    case_sensitive - when content is ASCII, consider 'A' the same as 'a', etc.
    '''
    self.content = content
    self.chunk_size = chunk_size
    self.byte_width = byte_width
    self.case_sensitive = case_sensitive

  def _min_max_gap(self, histogram):
    items = histogram.values()
    return max(items) - min(items)

  def _histogram(self, chunk):
    b = {}
    for c in map(ord, chunk):
      if not self.case_sensitive:
        c = c.lower()
      if c in b:
        b[c] += 1
      else:
        b[c] = 1
    return b

  # Split content into equal-sized chunks (except for final chunk)
  def _chunk_it(self):
    return [self.content[i:i+self.chunk_size]
              for i in range(0, len(self.content), self.chunk_size)]

  def _frequency(self, chunk):
    histo = self._histogram(chunk)
    histo_len = len(histo)
    # chunk_len should only be different than self.chunk_size for the final
    # chunk, or when content < self.chunk_size
    chunk_len = len(chunk)
    # This expression doesn't factor in byte_width.
    return float(histo_len) / chunk_len

  ### API
  def frequency_list(self):
    '''
    List of frequency values. Similar to avg_frequency except
    don't perform avg
    '''
    chunks = self._chunk_it()
    return map(lambda c: self._frequency(c), chunks)

  def frequency_gap(self):
    '''Gap between the highest and lowest frequency chunks'''
    freqs = self.frequency_list()
    return float(max(freqs)) - float(min(freqs))

  def frequency_avg(self):
    '''Average of the uniformity of bytes over all chunks'''
    freqs = self.frequency_list()
    return float(sum(freqs)) / float(len(freqs))

def main(filename):
  elf = ELFFile(open(filename, 'rb'))
  section = elf.get_section_by_name('.text')
  content = section.stream.read()

  e = Entropy(content)

  print("Frequency(avg): %f" % e.frequency_avg())
  print("Frequency(gap): %f" % e.frequency_gap())

#def parse_args():
#  import argparse
#  parser = argparse.ArgumentParser()
#  parser.add_argument('filename', metavar='N', type=int, nargs='+',
#                     help='an integer for the accumulator')
#  parser.add_argument('--sum', dest='filename', action='store_true',
#                     const=sum, default=max,
#                     help='sum the integers (default: find the max)')
#
#  args = parser.parse_args()
#  print(args.accumulate(args.integers))

if __name__ == '__main__':
	sys.exit(main(sys.argv[1]))
