#!/usr/bin/env python3
#requires python>3.6
#Requires - pip install pyyaml
#Proxy issue - pip install urllib3==1.25.11

#upload - https://www.youtube.com/watch?v=zhpI6Yhz9_4&ab_channel=MakerBytes
#python setup.py sdist
#twine upload --repository-url https://upload.pypi.org/legacy/ dist/*

#github actions - https://docs.github.com/en/actions/reference/workflow-commands-for-github-actions#setting-an-environment-variable
#https://stackoverflow.com/questions/66642705/why-requests-raise-this-exception-check-hostname-requires-server-hostname

from urllib.parse import quote
import os
import sys
import subprocess
import shutil
import json
import requests
import re
from requests.auth import HTTPProxyAuth
import csv
import datetime
from shutil import copyfile
from xml.etree.ElementTree import ElementTree
import xml.etree.ElementTree as ET
try:
   import yaml
except ImportError:
   print('Error, yaml is required, please run pip install pyyaml')

testtoadd = "ApplicationMgrInitializeProduct (866389,Philips North America LLC,222 Jacobs Street FL 3\nCambridge, MA 02141 USA,Veenpluis 6\n5684PC Best, The Netherlands) row 2"
print(testtoadd)
print("1#######################################")
testtoadd = testtoadd.encode('unicode_escape').decode()
print(testtoadd)
print("2#######################################")
testtoadd = testtoadd.replace("\\", "\\\\")
print(testtoadd)
print("3#######################################")
testtoadd = testtoadd.replace("\n", "\\n")
                                #testtoadd = testtoadd.replace("\\u00F6", "")
print(testtoadd)
print("4#######################################")
                                