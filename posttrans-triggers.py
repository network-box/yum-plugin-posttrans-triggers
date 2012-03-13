# Copyright 2011 Network Box
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


from ConfigParser import RawConfigParser
import glob
import os
import shlex
import subprocess

from yum.plugins import TYPE_CORE

requires_api_version = '2.6'
plugin_type = (TYPE_CORE,)

always_run_triggers = False
print_output = False

triggers_configs_path = "/etc/yum/pluginconf.d/posttrans-triggers.conf.d"


class TriggerSectionDict(dict):
    def __setitem__(self, key, value):
        """Allow multiple values to be specified for the same key.

        This is useful for example so that different files can specify an
        'exec' option for the same path. In such a case, we would want to
        execute all commands on the trigger, not just the one in the file
        we read last.
        """
        if self.has_key(key):
            new_value = "\n".join([self[key], value])
        else:
            new_value = value

        return super(TriggerSectionDict, self).__setitem__(key, new_value)


def posttrans_hook(conduit):
    global always_run_triggers, print_output

    opts, args = conduit.getCmdLine()
    conf = conduit.getConf()

    if not always_run_triggers and not (opts and opts.posttrans_triggers):
        return

    base = conduit._base

    # Parse the trigger configs
    triggers_files = glob.glob(os.path.join(triggers_configs_path, "*.conf"))
    triggers_config = RawConfigParser(dict_type=TriggerSectionDict)
    triggers_config.read(triggers_files)

    # Look at the files impacted by the transaction
    files_seen = []
    triggers = set()
    for tsmem in conduit.getTsInfo().getMembers():
        pkg_files = tsmem.po.filelist

        for f in pkg_files:
            if f in files_seen:
                continue

            for path in triggers_config.sections():
                if f.startswith(path):
                    try:
                        t = triggers_config.get(path, "exec")
                    except NoOptionError, e:
                        base.logger.error("posttrans-triggers: Ignoring path" \
                                          " %s: no 'exec' option found" % path)
                        triggers_config.remove_section(path)
                        continue

                    # Try to be helpful
                    env = {"file": f, "path": path}
                    t = t % env

                    triggers.add(t)

            files_seen.append(f)

    # Avoid evaluating that compound condition for each command of each trigger
    if print_output or (opts and opts.print_output):
        output_desired = True
    else:
        output_desired = False

    for t in triggers:
        for cmd in t.split("\n"):
            proc = subprocess.Popen(shlex.split(cmd), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            out, err = proc.communicate()

            if output_desired:
                base.logger.info("posttrans-triggers: %s" % out)
                base.logger.error("posttrans-triggers: %s" % err)

def config_hook(conduit):
    global always_run_triggers, print_output

    always_run_triggers = conduit.confBool('main', 'always_run_triggers', default=False)
    print_output = conduit.confBool('main', 'print_output', default=False)

    parser = conduit.getOptParser()
    if parser:
        if hasattr(parser, 'plugin_option_group'):
            parser = parser.plugin_option_group

        parser.add_option('', '--posttrans-triggers', dest='posttrans_triggers',
                action='store_true', default=False,
                help="run the file triggers at the end of a a yum transaction")
        parser.add_option('', '--posttrans-triggers-print-output', dest='print_output',
                action='store_true', default=False,
                help="print the output of the post-transaction file triggers to the console")
