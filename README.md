# Summary

seebinrand quickly guesses at a binary's randomness by analyzing its .text segment. 

The type of analysis currently supported is the first of Kendall and Smith's randomness tests: the frequency test. It tries to answer the question of how uniform is the distribution of characters in a given body of bytes.

# Example
```bash
vagrant@precise64:~$ python seebinrand/seebinrand.py vmlinux
Frequency(avg): 0.110906
vagrant@precise64:~$
```

The closer to "1", the more of a chance portions of the program are encrypted. I've found that aes-encrypted content will yield about .6-.7 in my testing.

# Future
* Support for more randomness tests, and how the tests should be evaluated in combination
* Example encrypted binaries.
