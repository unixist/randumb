import os
import sys
import math

class Frequency(object):
  '''Byte-frequency of an input'''

  # If the calculation is more than RAND_THRESHOLD, it's possibly random.
  RAND_THRESHOLD = .6

  def __init__(self, data, chunk_size=256, byte_width=256, case_sensitive=True):
    '''
    data           - string of bytes to consider
    chunk_size     - number of bytes to evaluate at a time
    byte_width     - spectrum of valid byte values for the data (not working)
    case_sensitive - when data is ASCII, consider 'A' the same as 'a', etc.
    '''
    self.data = data
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

  # Split data into equal-sized chunks (except for final chunk)
  def _chunk_it(self):
    return [self.data[i:i+self.chunk_size]
              for i in range(0, len(self.data), self.chunk_size)]

  def _frequency(self, chunk):
    histo = self._histogram(chunk)
    histo_len = len(histo)
    # chunk_len should only be different than self.chunk_size for the final
    # chunk, or when data < self.chunk_size
    chunk_len = len(chunk)
    # This expression doesn't factor in byte_width.
    if histo_len == 0 or chunk_len == 0:
      return 0.0
    return float(histo_len) / chunk_len

  ### API
  def frequency_list(self):
    '''
    List of frequency values. Similar to avg_frequency except
    don't perform avg
    '''
    chunks = self._chunk_it()
    return map(lambda c: self._frequency(c), chunks)

  def gap(self):
    '''Gap between the highest and lowest frequency chunks'''
    freqs = self.frequency_list()
    return float(max(freqs)) - float(min(freqs))

  def avg(self):
    '''Average of the uniformity of bytes over all chunks'''
    freqs = self.frequency_list()
    return float(sum(freqs)) / float(len(freqs))

class Skewness(object):
  '''
  Pearson's second skewness coefficient:
    3 * (avg - median) / std_dev
 '''
  # If the calculation is less than RAND_THRESHOLD, it's possibly random.
  RAND_THRESHOLD = .2

  def __init__(self, data):
    self.data = data

  def _avg(self, l):
    return sum(l) * 1.0 / len(l)

  def _median(self, l):
    l.sort()
    c = len(l)
    sub = c % 2 == 0
    return l[c/2-sub]

  def _std_deviation(self, l):
    return math.sqrt(self._avg(map(lambda x: (x - self._avg(l))**2, l)))

  def skew(self, tuples):
    cur_bin_num = ''
    # Map the 2^tuple number of keys to the frequency that bit sequence occurs.
    bin_map = {}  
    i = 0
    for byte in self.data:
      for bit in bin(ord(byte))[2:]:
        if len(cur_bin_num) == tuples:
          if cur_bin_num in bin_map:
            bin_map[cur_bin_num] += 1
          else:
            bin_map[cur_bin_num] = 1
          # Now that we've tallied this bit-sequence, start over.
          cur_bin_num = ''
        else:
          cur_bin_num += bit

    vals = bin_map.values()
    
    # Corner case where all bit tuple patterns occur the same number of times.
    # This prevents a divide-by-zero when calculating standard deviation.
    # Hmm, smells janky.
    if len(set(vals)) <= 1: 
      return 1

    # Calculate skewness 
    return 3 * (self._avg(vals) - self._median(vals)) / self._std_deviation(vals)

class Random(object):
  '''
  Mash up some characteristics of randomness and make an arbitrary decision
  as to whether the input is statistically random.

  Returns:
    True if random
    False if not random
  '''

  @staticmethod
  def is_random(data, bit_tuples=8):
    freq = Frequency(data)
    skew = Skewness(data)

    skew.skew(bit_tuples)
    if freq.avg() >= freq.RAND_THRESHOLD and \
       skew.skew(bit_tuples) <= skew.RAND_THRESHOLD:
      return True
    else:
      return False
    
def main(args):
  if len(args) > 1:
    data = open(args[1], 'rb').read()
  else:
    data = sys.stdin.read()

  return 0 if Random.is_random(data) else 1

if __name__ == '__main__':
	sys.exit(main(sys.argv))
