# sussy.py

a sus Python library.

## examples

To generate an ejected message:
```py
from sussy import prompts

print(prompts.Voting.ejected("Bye", False, 2))
                #  (name, isImposter, remaining)

# Returns 
# '''Bye was not the Imposter.
#    2 Imposters remain.'''

print(prompts.Voting.ejected_noconf("Bye"))
                #  (name)

# Returns
# 'Bye was ejected.'
```
