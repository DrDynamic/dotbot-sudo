
#!/usr/bin/env sh

# This is a valid shell script and also a valid Python script. When this file
# is executed as a shell script, it finds a python binary and executes this
# file as a Python script, passing along all of the command line arguments.
# When this file is executed as a Python script, it loads and runs Dotbot. This
# is useful because we don't know the name of the python binary.

''':' # begin python string; this line is interpreted by the shell as `:`
command -v python  >/dev/null 2>&1 && exec python  "$0" "$@"
command -v python3 >/dev/null 2>&1 && exec python3 "$0" "$@"
command -v python2 >/dev/null 2>&1 && exec python2 "$0" "$@"
>&2 echo "error: cannot find python"
exit 1
'''
# python code
import sys, os, json

data = json.loads(sys.stdin.read())

#print(data)

if data['plugins'] is None:
    data['plugins'] = []

sys.path.insert(0, data['dotbot'])

import dotbot
from dotbot.util import module
from dotbot.dispatcher import Dispatcher, DispatchError
from dotbot.plugins import Clean, Create, Link, Shell

for plugin in data['plugins']:
    module.load(plugin)

os.chdir(data['base_directory'])
dispatcher = Dispatcher(data['base_directory'])
success = dispatcher.dispatch(data['tasks'])

for line in sys.stdin:
    print("line: " + line)


