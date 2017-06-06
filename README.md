# Summary

randumb naively estimates an input's level of entropy by running some tests on it. Possible values range from 0 to 1 where 1 is as random as randumb can guess.

The types of analysis currently supported are frequency and skewness. The first of [Kendall and Smith's randomness tests](https://en.wikipedia.org/wiki/Statistical_randomness) is the frequency test. It tries to answer the question of how uniform is the distribution of characters in a given body of bytes.

The skewness analysis is based upon [Pearson's second coefficient](http://mathworld.wolfram.com/PearsonsSkewnessCoefficients.html). It tries to make a binary guess of randomness based upon a distribution's variance.

# Description
Tests:
* Frequency - iterate over the input in chunks and find the ratio of "unique-number-of-bytes / length-of-chunk". A chunk of length `n`-bytes would be uniformly distributed (and equal 1 in the frequency test) if each value were a different byte value.
  * Example: if a 26-byte chunk contained the value "abcdefghijklmnopqrstuvwxyz", then it'd be random as far as the frequency test is concerned since each value is present only once. Of course there is a pattern there, but that's for another test to decide.
* Skewness - iterate over the input and make a histogram out of the input. Each bucket contains a bit tuple (8-bit tuple by default). The amount of variance across the distribution determines the input's randomness. I currently use an anecdotal constant as a threshold for determining randomness. The basis for this equation is [Pearson's second coefficient](http://mathworld.wolfram.com/PearsonsSkewnessCoefficients.html).

# Simple example
I use a naïve combination of the randomness tests described above to arrive at a guess of randomness. Given an input, randumb.py returns a binary value: 0 for random, 1 for non-random.

Let's look at an ELF binary in encrypted and unencrypted form.
```bash
# input - regular OpenSSH binary
vagrant@precise64:~/randumb$ python randumb.py < /usr/bin/ssh; echo $?
1
vagrant@precise64:~/randumb$

# input - encrypted OpenSSH binary 
vagrant@precise64:~/randumb$ python randumb.py < /tmp/ssh.enc; echo $?
0
vagrant@precise64:~/randumb$
```

# Cryptostalker example
This tool uses the randumb library to monitor a filesystem path and detect newly-written files. If these new files are deemed random and occur at a fast enough rate (configurable), then it notifes you.

## MOVED: cryptostalker.py has [moved to its own repository](https://github.com/unixist/cryptostalker) and been ported to the Go language. So it works on Linux, OSX and Windows.

#### Python version
I implemented this initially using linux's inotify facility. This allows a file write event to be filtered on IN_CLOSE_WRITE, which occurs when the file is finished writing. I'd prefer to use auditd to alert on new file writes since it can also give the process ID of the writer. That'd allow the process to be killed if we have enough confidence that it's probably bad. (Although auditd can place a recursive watch similar to inotify, I don't know if auditd can alert on a file only *after* all writes are complete and only if it was opened for writing.)

#### Go version
The file notification mechanism is Google's [fsnotify](https://github.com/fsnotify/fsnotify). Since it doesn't use the linux-specific [inotify](https://en.wikipedia.org/wiki/Inotify), cryptostalker currently relies on notifications of new files. So random/encrypted files will only be detected if they belong to new inodes; which means it wont catch the following case: a file is opened, truncated, and only then filled in with encrypted content. Fortunately, this is not how most malware works.

See the [new repo for the go version](https://github.com/unixist/cryptostalker).

#### Misc
* I'd be stoked if someone can show me how to get auditd to behave optimally for this use case!
* cryptostalker may incorrectly identify compressed files as encrypted files. I haven't found this to be true in my testing, but I can only imagine that given a quality compressor and the right type of data input this will yield some false positives. You can always tweak the `RAND_THRESHOLD`s in randumb.py to your liking.

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
