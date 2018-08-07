'''
this is the `init` part of a user script. it imports several libraries which
need some time to initialize. then it creates a regex pattern for later use.
'''

import os
import re
import setuptools
import sys

pattern = re.compile('he.*ld')

