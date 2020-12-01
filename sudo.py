import subprocess, dotbot, json
from os import path, getcwd
from dotbot.util import module

class Sudo(dotbot.Plugin):
    _directive = 'sudo'


    def can_handle(self, directive):
        return self._directive == directive

    def handle(self, directive, data):
        if directive != self._directive:
            raise ValueError('sudo cannot handle directive %s' %
                directive)
        
        data = [{'defaults': self._context.defaults()}] + data
        call_data = {
                'dotbot': path.dirname(path.dirname(dotbot.__file__)),
                'plugins': [

                    ],
                'base_directory': getcwd(),
                'tasks': data
                }

        for plugin in module.loaded_modules:
            call_data['plugins'].append(plugin.__file__)

        json_data = json.dumps(call_data)

        process = subprocess.Popen(
                'sudo ./execute_plugin.py', 
                shell=True, 
                cwd=path.dirname(__file__), 
                stdin=subprocess.PIPE)

        process.communicate(json_data.encode('utf-8'))


        return True
    def _find_dotbot(self):
        pass
    def _loadPlugin(self, path):
        pass
