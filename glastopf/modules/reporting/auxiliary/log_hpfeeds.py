# Copyright (C) 2013 Johnny Vestergaard <jkv@unixcluster.dk>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import json
import logging
import os
from ConfigParser import ConfigParser
import base64

import hpfeeds
from glastopf.modules.reporting.auxiliary.base_logger import BaseLogger


logger = logging.getLogger(__name__)


class HPFeedsLogger(BaseLogger):

    def __init__(self, data_dir, config="glastopf.cfg", reconnect=True):
        self.files_dir = os.path.join(data_dir, 'files/')

        self.enabled = False
        #legacy
        self.options = {'enabled': self.enabled}

        conf_parser = ConfigParser()
        conf_parser.read(config)

        if conf_parser.getboolean("hpfeed", "enabled"):
            host = conf_parser.get("hpfeed", "host")
            port = int(conf_parser.getint("hpfeed", "port"))
            ident = conf_parser.get("hpfeed", "ident")
            secret = conf_parser.get("hpfeed", "secret")
            self.enabled = True
            #legacy
            self.options = {'enabled': self.enabled}
            self.chan_files = conf_parser.get("hpfeed", "chan_files")
            self.chan_events = conf_parser.get("hpfeed", "chan_events")
            self.hpc = hpfeeds.new(host, port, ident, secret, reconnect=reconnect)

    def insert(self, attack_event):
        if attack_event.file_name is not None:
            with file(os.path.join(self.files_dir, attack_event.file_name), 'r') as file_handler:
                file_content = file_handler.read()
                file_data = attack_event.file_name + " " + base64.b64encode(file_content)
                self.hpc.publish(self.chan_files, file_data)

        event_data = json.dumps(attack_event.event_dict())
        self.hpc.publish(self.chan_events, event_data)
