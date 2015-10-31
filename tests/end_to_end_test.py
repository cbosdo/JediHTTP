#     Copyright 2015 Cedraro Andrea <a.cedraro@gmail.com>
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
#    limitations under the License.


import sys
from . import utils
import requests
import subprocess
from jedihttp import hmaclib
from os import path
from hamcrest import assert_that, equal_to

try:
  from http import client as httplib
except ImportError:
  import httplib


PATH_TO_JEDIHTTP = path.abspath( path.join( path.dirname( __file__ ),
                                            '..', 'jedihttp' ) )

def test_it_works():
  port = 50000
  secret = "secret"

  with hmaclib.TemporaryHmacSecretFile( secret ) as hmac_file:
    command = [ sys.executable,
                '-u', # this flag makes stdout non buffered
                PATH_TO_JEDIHTTP,
                '--port', str( port ),
                '--hmac-file-secret', hmac_file.name ]
    jedihttp = utils.SafePopen( command,
                                stderr = subprocess.STDOUT,
                                stdout = subprocess.PIPE )

  # wait for the process to print something, so we know it is ready
  jedihttp.stdout.readline()

  headers = {}
  hmachelper = hmaclib.JediHTTPHmacHelper( secret )
  hmachelper.SignRequestHeaders( headers,
                                 method = 'POST',
                                 path = '/ready',
                                 body = '' )

  response = requests.post( 'http://127.0.0.1:{0}/ready'.format( port ),
                            headers = headers )
  utils.TerminateProcess( jedihttp.pid )

  assert_that( response.status_code, equal_to( httplib.OK ) )
  assert_that( hmachelper.IsResponseAuthenticated( response.headers,
                                                   response.content ) )