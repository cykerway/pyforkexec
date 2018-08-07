'''
this is the `init` part of a user script. it imports several libraries which
need some time to initialize. then it creates a regex pattern for later use.
'''

import os
import re
import setuptools
import sys

pattern = re.compile('he.*ld')

'''
this is the `run` part of a user script. it matches a str with the regex pattern
created in the `init` part of the user script.
'''

print(pattern.match("helloworld"))

