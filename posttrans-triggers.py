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

triggers_configs_path = "/etc/yum/pluginconf.d/posttrans-triggers.conf.d"


def posttrans_hook(conduit):
    global always_run_triggers

    opts, args = conduit.getCmdLine()
    conf = conduit.getConf()

    if not always_run_triggers and not (opts and opts.posttrans_triggers):
        return

    # Parse the trigger configs
    triggers_files = glob.glob(os.path.join(triggers_configs_path, "*.conf"))
    triggers_config = RawConfigParser()
    triggers_config.read(triggers_files)

    for s in triggers_config.sections():
        if not triggers_config.has_option(s, "exec"):
            conduit._base.logger.error("posttrans-triggers: Ignoring path %s:"\
                                          " no 'exec' option found" % s)
            triggers_config.remove_section(s)

    # Look at the files impacted by the transaction
    files_seen = []
    triggers = set()
    ts = conduit.getTsInfo()
    for tsmem in ts.getMembers():
        pkg_files = tsmem.po.filelist

        for f in pkg_files:
            if f in files_seen:
                continue

            for path in triggers_config.sections():
                if f.startswith(path):
                    cmd = triggers_config.get(path, "exec")
                    triggers.add(shlex.split(cmd))

            files_seen.append(f)

    for cmd in triggers:
        proc = subprocess.Popen(cmd.split(), stdout=subprocess.NULL, stderr=subprocess.NULL)
        proc.communicate()

def config_hook(conduit):
    global always_run_triggers
    always_run_triggers = conduit.confBool('main', 'always_run_triggers', default=False)

    parser = conduit.getOptParser()
    if parser:
        if hasattr(parser, 'plugin_option_group'):
            parser = parser.plugin_option_group

        parser.add_option('', '--posttrans-triggers', dest='posttrans_triggers',
                action='store_true', default=False,
                help="run the file triggers at the end of a a yum transaction")
