# -*- coding: utf-8 -*-
#/*
#     All Emoncms code is released under the GNU Affero General Public License.
#     See COPYRIGHT.txt and LICENSE.txt.
#
#     ---------------------------------------------------------------------
#     Emoncms - open source energy visualisation
#     Part of the OpenEnergyMonitor project:
#     http://openenergymonitor.org
#*/

from ironworks import serverTools
from modules_lib.pyEMONCMS import cmsSettings


class Node():

    def __init__(self):
        self.logger = serverTools.getLogger()
        self.settings = serverTools.getCMSSettings()
        if self.settings == None:
            self.settings = cmsSettings.Settings()
            serverTools.setCMSSettings(self.settings)

    def createNode(self, data):
        success = {'success': False}
        userid = data['userid']
        description = data['description']
        apiKeyWrite = self.settings.getAPIKeyWrite(userid)[0]
        if apiKeyWrite == data['apikey_write']:
            success = self.settings.createNode(userid, description)
            return success
        else:
            return success


    """def set_decoder(self, userid, nodeid, decoder):
        if (!$decoder_in) return false;

        $decoder = new stdClass();
        $decoder->name = preg_replace('/[^\w\s-:()]/','',$decoder_in->name);
        $decoder->updateinterval = (int) $decoder_in->updateinterval;

        $decoder->variables = array();
        // Ensure each variable is defined with the allowed fields and correct types
        foreach ($decoder_in->variables as $variable)
        {
          $var = new stdClass();
          $var->name = preg_replace('/[^\w\s-:]/','',$variable->name);
          if (isset($variable->type)) $var->type = (int) $variable->type;
          if (isset($variable->scale)) $var->scale = (float) $variable->scale;
          if (isset($variable->units)) $var->units = preg_replace('/[^\w\s-°]/','',$variable->units);
          if (isset($variable->processlist)) {
              $var->processlist = preg_replace('/[^\d-:,.]/','',$variable->processlist);
          }
          $decoder->variables[] = $var;
        }

        // Load full nodes defenition from redis or mysql
        if ($this->redis) {
            $nodes = json_decode($this->redis->get("nodes:$userid"));
        } else {
            $nodes = $this->get_mysql($userid);
        }

        // Set the decoder part of the node defenition
        if ($nodes!=NULL && isset($nodes->$nodeid))
        {
            $nodes->$nodeid->decoder = $decoder;
            if ($this->redis) $this->redis->set("nodes:$userid",json_encode($nodes));
            $this->set_mysql($userid,$nodes);
        }

        return true;
    }

    def get_all(self, userid):
        if ($this->redis) {
            $nodes = $this->redis->get("nodes:$userid");
            if ($nodes) {
                return json_decode($nodes);
            } else {
                $nodes = $this->get_mysql($userid);
                $this->redis->set("nodes:$userid",json_encode($nodes));
                return $nodes;
            }

        } else {
            return $this->get_mysql($userid);
        }
    }

    #----------------------------------------------------------------------------------------------

    def process(self, userid, nodes, nodeid, time, data):
    {
        $bytes = explode(',',$data);
        $pos = 0;

        if (isset($nodes->$nodeid->decoder) && sizeof($nodes->$nodeid->decoder->variables)>0)
        {
            foreach($nodes->$nodeid->decoder->variables as $variable)
            {
                $value = null;

                // Byte value
                if ($variable->type==0)
                {
                    if (!isset($bytes[$pos])) break;
                    $value = (int) $bytes[$pos];
                    $pos += 1;
                }

                // signed integer
                if ($variable->type==1)
                {
                    if (!isset($bytes[$pos+1])) break;
                    $value = (int) $bytes[$pos] + (int) $bytes[$pos+1]*256;
                    if ($value>32768) $value += -65536;
                    $pos += 2;
                }

                // unsigned long
                if ($variable->type==2)
                {
                    if (!isset($bytes[$pos+3])) break;
                    $value = (int) $bytes[$pos] + (int) $bytes[$pos+1]*256 + (int) $bytes[$pos+2]*65536 + (int) $bytes[$pos+3]*16777216;
                    //if ($value>32768) $value += -65536;
                    $pos += 4;
                }

                if (isset($variable->scale)) $value *= $variable->scale;

                if (isset($variable->processlist) && $variable->processlist!='') $this->process->input($time,$value,$variable->processlist);
            }
        }
    }

    def setNodeData(self, userid, data):
    {
        $json = json_encode($data);
        $result = $this->mysqli->query("SELECT `userid` FROM node WHERE `userid`='$userid'");
        if ($result->num_rows) {
            $this->mysqli->query("UPDATE node SET `data`='$json' WHERE `userid`='$userid'");
        } else {
            $this->mysqli->query("INSERT INTO node (`userid`,`data`) VALUES ('$userid','$json')");
        }
    }

    def getNodeData(self, userid):
    {
        $result = $this->mysqli->query("SELECT `data` FROM node WHERE `userid`='$userid'");
        if ($row = $result->fetch_array()) {
          return json_decode($row['data']);
        } else {
          return false;
        }
        """
