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

import utils
utils.AddVendorFolderToSysPath()

from argparse import ArgumentParser
from waitress import serve
import handlers
from hmac_plugin import HmacPlugin


def ParseArgs():
  parser = ArgumentParser()
  parser.add_argument( '--host', type = str, default = '127.0.0.1',
                       help = 'server host' )
  parser.add_argument( '--port', type = int, default = 0,
                       help = 'server port' )
  parser.add_argument( '--hmac-secret', type = str, required = True,
                       help = 'hmac secret' )
  return parser.parse_args()


def Main():
  args = ParseArgs()

  handlers.app.install( HmacPlugin( args.hmac_secret ) )
  serve( handlers.app,
         host = args.host,
         port = args.port )

if __name__ == "__main__":
  Main()
