'''
this is the `init` part of a user script. it imports several libraries which
need some time to initialize. then it creates a regex pattern for later use.
'''

#import argparse
#import array
#import bisect
#import bz2
#import calendar
#import cmath
#import codecs
#import collections
#import collections.abc
#import configparser
#import copy
#import copyreg
#import csv
#import ctypes
#import curses
#import curses.ascii
#import curses.panel
#import curses.textpad
#import datetime
#import dbm
#import decimal
#import difflib
#import enum
#import errno
#import filecmp
#import fileinput
#import fnmatch
#import fractions
#import functools
#import getopt
#import getpass
#import glob
#import gzip
#import hashlib
#import heapq
#import hmac
#import io
#import itertools
#import linecache
#import logging
#import logging.config
#import logging.handlers
#import lzma
#import macpath
#import marshal
#import math
#import netrc
#import numbers
#import operator
#import os
#import os.path
#import pathlib
#import pickle
#import platform
#import plistlib
#import pprint
#import random
#import re
#import readline
#import reprlib
#import rlcompleter
#import secrets
#import setuptools
#import shelve
#import shutil
#import sqlite3
#import stat
#import statistics
#import string
#import stringprep
#import struct
#import tarfile
#import tempfile
#import textwrap
#import time
#import time
#import types
#import unicodedata
#import weakref
#import xdrlib
#import zipfile
#import zlib

#import os
import re
#import setuptools
#import sys

pattern = re.compile('he.*ld')

'''
this is the `run` part of a user script. it matches a str with the regex pattern
created in the `init` part of the user script.
'''

print(pattern.match("helloworld"))

