# Summary

seebinrand quickly guesses at a binary's randomness by analyzing its .text segment. 

The type of analysis currently supported is the first of Kendall and Smith's randomness tests: the frequency test. It tries to answer the question of how uniform is the distribution of characters in a given body of bytes.

# Description
* Frequency test - iterate over the input in chunks and find the ratio of "unique-number-of-bytes / length-of-chunk". A chunk of length `n`-bytes would be uniformly distributed (and equal 1 in the frequency test) if each value were a different byte value.
  * Example: if a 26-byte chunk contained the value "abcdefghijklmnopqrstuvwxyz", then it'd be random as far as the frequency test is concerned since each value is present only once. Of course there is a pattern there, but that's for another test to decide.

# Example
```bash

# input - linux kernel .text
vagrant@precise64:~/seebinrand$ objcopy -O binary --only-section=.text ~/vmlinux /dev/stdout | python seebinrand.py
Frequency(avg): 0.326217
vagrant@precise64:~/seebinrand$

# input - /dev/random
vagrant@precise64:~/seebinrand$ python seebinrand.py < ~/input.random
Frequency(avg): 0.632422
vagrant@precise64:~/seebinrand$

# input - openssl enc -aes-256-cbc
vagrant@precise64:~/seebinrand$ python seebinrand.py < ~/input.enc
Frequency(avg): 0.613281
vagrant@precise64:~/seebinrand$
```

The closer to "1", the more of a chance portions of the program are encrypted. I've found that random/well-encrypted content will yield about .6-.7 in my testing.

# Future
* Support for more randomness tests, and how the tests should be evaluated in combination
* Example encrypted binaries.
