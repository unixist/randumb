# Summary

randumb naively estimates an input's level of entropy by running some tests on it. Possible values range from 0 to 1 where 1 is as random as randumb can guess.

The type of analysis currently supported is the first of [Kendall and Smith's randomness tests](https://en.wikipedia.org/wiki/Statistical_randomness): the frequency test. It tries to answer the question of how uniform is the distribution of characters in a given body of bytes.

# Description
Tests:
* Frequency - iterate over the input in chunks and find the ratio of "unique-number-of-bytes / length-of-chunk". A chunk of length `n`-bytes would be uniformly distributed (and equal 1 in the frequency test) if each value were a different byte value.
  * Example: if a 26-byte chunk contained the value "abcdefghijklmnopqrstuvwxyz", then it'd be random as far as the frequency test is concerned since each value is present only once. Of course there is a pattern there, but that's for another test to decide.
* Skewness - iterate over the input and make a histogram out of the input. Each bucket contains a bit tuple (8-bit tuple by default). The amount of variance across the distribution determines the inputs randomness. I currently use an anecdotal constant that is used as a threshold for determining randomness. The basis for this equation is [Pearson's second coefficient](http://mathworld.wolfram.com/PearsonsSkewnessCoefficients.html).

# Simple example
I use a naïve combination of the randomness tests described above to arrive at a guess of randomness. Given an input, randumb.py returns a binary value: 0 for random, 1 for non-random.

```bash
# input - regular OpenSSH binary
vagrant@precise64:~/randumb$ python randumb.py < /usr/bin/ssh; echo $?
1
vagrant@precise64:~/randumb$# input - encrypted OpenSSH binary 

vagrant@precise64:~/randumb$ python randumb.py < /tmp/ssh.enc; echo $?
0
vagrant@precise64:~/randumb$
```

# Cryptostalker example
This tool uses the randumb library to monitor a filesystem path and detect newly-written files. If these new files are deemed random and occur at a fast enough rate (configurable), then it notifes you.
```bash
# Run with only --path parameter defaults to a detection rate of 10/60seconds
vagrant@precise64:~/randumb$ python cryptostalker.py --path /home
Seen 10 random files in 30.1896209717 seconds:
/home/vagrant/.foo.8299
/home/vagrant/.foo.5266
/home/vagrant/.foo.10551
/home/vagrant/.foo.8444
/home/vagrant/.foo.20163
/home/vagrant/.foo.820
/home/vagrant/.foo.28854
/home/vagrant/.foo.27284
/home/vagrant/.foo.21306
/home/vagrant/.foo.24437

# See example usage
vagrant@precise64:~/randumb$ python cryptostalker.py  --help
usage: cryptostalker.py [-h] --path PATH [--count COUNT] [--window WINDOW]
                        [--sleep SLEEP]

Detect high throughput of newly-created encrypted files.

optional arguments:
  -h, --help       show this help message and exit
  --path PATH      The directory to watch.
  --count COUNT    The number of random files required to be seen within
                   <window>.
  --window WINDOW  The number of seconds within which <count> random files
                   must be observed.
  --sleep SLEEP    The time in seconds to sleep between processing each new
                   file to determine whether it is random.
vagrant@precise64:~/randumb$
```
# Frequency example (old)
```bash

# input - ASCII file
vagrant@precise64:~/randumb$ python randumb.py < /etc/passwd
Frequency(avg): 0.165232
vagrant@precise64:~/randumb$

# input - linux kernel .text
vagrant@precise64:~/randumb$ objcopy -O binary --only-section=.text ~/vmlinux /dev/stdout | python randumb.py
Frequency(avg): 0.326217
vagrant@precise64:~/randumb$

# input - /dev/random
vagrant@precise64:~/randumb$ python randumb.py < ~/input.random
Frequency(avg): 0.632422
vagrant@precise64:~/randumb$

# input - openssl enc -aes-256-cbc
vagrant@precise64:~/randumb$ python randumb.py < ~/input.enc
Frequency(avg): 0.613281
vagrant@precise64:~/randumb$
```

The closer to "1", the more of a chance portions of the program are encrypted. I've found that random/well-encrypted content will yield about .6-.7 in my testing.

# Future
* Support for more randomness tests, and how the tests should be evaluated in combination
* Example encrypted binaries.
