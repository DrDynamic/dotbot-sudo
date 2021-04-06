import subprocess, dotbot, json
from os import path, remove
from dotbot.util import module
from io import open

class Sudo(dotbot.Plugin):
    _directive = 'sudo'

    def can_handle(self, directive):
        return self._directive == directive

    def handle(self, directive, data):
        if directive != self._directive:
            raise ValueError('sudo cannot handle directive %s' %
                directive)

        app = self._find_dotbot()
        base_directory = self._context.base_directory()
        data = [{'defaults': self._context.defaults()}] + data
        plugins = self._collect_plugins()
        sudo_conf = path.join(path.dirname(__file__), 'sudo.conf.json')

        self._write_conf_file(sudo_conf, data)

        proc_args = [
            'sudo', app,
            '--base-directory', base_directory,
            '--config-file', sudo_conf
            ] + plugins
        self._log.debug('sudo: args to pass: {}'.format(proc_args))

        try:
            self._log.lowinfo('sudo: begin subprocess')
            subprocess.check_call(
                proc_args,
                stdin=subprocess.PIPE)
            self._log.lowinfo('sudo: end subprocess')
            self._delete_conf_file(sudo_conf)
            return True
        except subprocess.CalledProcessError as e:
            self._log.lowinfo('sudo: end subprocess')
            self._log.error(e)
            return False

    def _collect_plugins(self):
        ret = []
        for plugin in module.loaded_modules:
            # HACK should we compare to something other than _directive?
            if plugin.__name__ != self._directive:
                ret.extend(iter([
                    '--plugin',
                    path.splitext(plugin.__file__)[0] + '.py']))
        return ret

    def _delete_conf_file(self, conf_file):
        if path.exists(conf_file):
            remove(conf_file)

    def _find_dotbot(self):
        base = path.dirname(path.dirname(dotbot.__file__))
        ret = path.join(base, 'bin', 'dotbot')
        self._log.debug('sudo: dotbot app path: {}'.format(ret))
        return ret

    def _write_conf_file(self, conf_file, data):
        self._delete_conf_file(conf_file)
        with open(conf_file, 'w', encoding='utf-8') as jfile:
            my_json_str = json.dumps(data, ensure_ascii=False)
            if isinstance(my_json_str, str):
                my_json_str = my_json_str.encode().decode("utf-8")

            jfile.write(my_json_str)
