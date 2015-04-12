# -*- coding: utf-8 -*-
#
# All Emoncms code is released under the GNU Affero General Public License.
# See COPYRIGHT.txt and LICENSE.txt.
#
# ---------------------------------------------------------------------
# Emoncms - open source energy visualisation
# Part of the OpenEnergyMonitor project:
# http://openenergymonitor.org
#
from datetime import datetime
from math import ceil
from ironworks import serverTools
from modules_lib.pyEMONCMS import cmsSettings


class Process():

    def __init__(self):
        self.settings = serverTools.getCMSSettings()
        if self.settings == None:
            self.settings = cmsSettings.Settings()
            serverTools.setCMSSettings(self.settings)
        self.logger = serverTools.getLogger()
        self.timezoneoffset = None

    def set_timezone_offset(self, timezoneoffset):
        self.timezoneoffset = timezoneoffset

    def get_process_list(self):
        return self.settings.getProcessList()

    def input(self, time, value, processList):
        logString = "input received time=" + str(time) + ", value=" + str(value)
        self.logger.log(logString, "INFO")

        process_list = self.get_process_list()
        """for process in process_list:
            processid = process[0]                                    # Process id

            $arg = 0;
            if (isset($inputprocess[1]))
                $arg = $inputprocess[1];               // Can be value or feed id

            $process_public = $process_list[$processid][2];             // get process public function name

            $value = $this->$process_public($arg,$time,$value);           // execute process public function
        """

    def get_process(self, processid):
        processList = self.get_process_list()
        if processid > 0 and processid < len(processList):
            return processList[processid - 1]

    def scale(self, arg, time, value):
        return value * arg

    def divide(self, arg, time, value):
        return value / arg

    def offset(self, arg, time, value):
        return value + arg

    def allowpositive(self, arg, time, value):
        if value < 0:
            value = 0
        return value

    def allownegative(self, arg, time, value):
        if value > 0:
            value = 0
        return value

    def reset2zero(self, arg, time, value):
        value = 0
        return value

    def signed2unsigned(self, arg, time, value):
        if value < 0:
            value = value + 65536
        return value

    def log_to_feed(self, inputid, time, value):
        self.settings.logToFeed(inputid, time, value)
        return value

    #---------------------------------------------------------------------------------------
    # Times value by current value of another input
    #---------------------------------------------------------------------------------------
    def times_input(self, inputid, time, value):
        return value * self.settings.getLastValue(inputid)

    def divide_input(self, inputid, time, value):
        lastval = self.settings.getLastValue(inputid)
        if lastval > 0:
            return value / lastval
        else:
            return None  # should this be null for a divide by zero?

    def update_feed_data(self, inputid, time, value):
        self.settings.updateFeedData(inputid, time, value)
        return value

    def add_input(self, inputid, time, value):
        return value + self.settings.getLastValue(inputid)

    def subtract_input(self, inputid, time, value):
        return value - self.settings.getLastValue(inputid)

    #---------------------------------------------------------------------------------------
    # Power to kwh
    #---------------------------------------------------------------------------------------
    def power_to_kwh(self, feedid, time_now, value):
        new_kwh = 0

        # Get last value
        last = self.settings.getFeedTimeValue(feedid)

        last['time'] = datetime.strptime(last['time'])
        if last['value'] == "null":
            last['value'] = 0
        last_kwh = last['value'] * 1
        last_time = last['time'] * 1

        # only update if last datapoint was less than 2 hour old
        # this is to reduce the effect of monitor down time on creating
        # often large kwh readings.
        if last_time and (datetime.now() - last_time) < 7200:
            # kWh calculation
            time_elapsed = (time_now - last_time)
            kwh_inc = (time_elapsed * value) / 3600000.0
            new_kwh = last_kwh + kwh_inc
        else:
            # in the event that redis is flushed the last time will
            # likely be > 7200s ago and so kwh inc is not calculated
            # rather than enter 0 we enter the last value
            new_kwh = last_kwh

        self.settings.insertFeedData(feedid, time_now, time_now, new_kwh)

        return value

    def power_to_kwhd(self, feedid, time_now, value):
        new_kwh = 0

        # Get last value
        last = self.settings.getFeedTimeValue(feedid)

        last['time'] = datetime.strptime(last['time'])
        if last['value'] == "null":
            last['value'] = 0
        last_kwh = last['value'] * 1
        last_time = last['time'] * 1

        #$current_slot = floor($time_now / 86400) * 86400;
        #$last_slot = floor($last_time / 86400) * 86400;
        current_slot = self.getstartday(time_now)
        last_slot = self.getstartday(last_time)

        if last_time and (datetime.now() - last_time) < 7200:
            # kWh calculation
            time_elapsed = (time_now - last_time)
            kwh_inc = (time_elapsed * value) / 3600000.0
        else:
            # in the event that redis is flushed the last time will
            # likely be > 7200s ago and so kwh inc is not calculated
            # rather than enter 0 we dont increase it
            kwh_inc = 0

        if last_slot == current_slot:
            new_kwh = last_kwh + kwh_inc
        else:
            # We are working in a new slot (new day) so don't increment it with the data from yesterday
            new_kwh = kwh_inc

        self.settings.updateFeedData(feedid, time_now, current_slot, new_kwh)

        return value

    def kwh_to_kwhd(self, feedid, time_now, value):
        currentkwhd = self.settings.getFeedTimeValue(feedid)
        last_time = datetime.strptime(currentkwhd['time'])

        #$current_slot = floor($time_now / 86400) * 86400;
        #$last_slot = floor($last_time / 86400) * 86400;
        current_slot = self.getstartday(time_now)
        last_slot = self.getstartday(last_time)

        lastkwhvalue = self.settings.getLastKWHValue(feedid)
        kwhinc = value - lastkwhvalue['value']

        # kwh values should always be increasing so ignore ones that are less
        # assume they are errors
        if kwhinc < 0:
            kwhinc = 0
            value = lastkwhvalue['value']

        if last_slot == current_slot:
            new_kwh = currentkwhd['value'] + kwhinc
        else:
            new_kwh = kwhinc

        self.settings.updateFeedData(feedid, time_now, current_slot, new_kwh)

        return value

    #---------------------------------------------------------------------------------------
    # input on-time counter
    #---------------------------------------------------------------------------------------
    def input_ontime(self, feedid, time_now, value):
        # Get last value
        last = self.settings.getFeedTimeValue(feedid)
        last_time = datetime.strptime(last['time'])

        #$current_slot = floor($time_now / 86400) * 86400;
        #$last_slot = floor($last_time / 86400) * 86400;
        current_slot = self.getstartday(time_now)
        last_slot = self.getstartday(last_time)

        if last['value'] == "null":
            last['value'] = 0
        ontime = last['value']
        time_elapsed = 0

        if value > 0 and (time_now - last_time) < 7200:
            time_elapsed = time_now - last_time
            ontime += time_elapsed

        if last_slot != current_slot:
            ontime = time_elapsed

        self.settings.updateFeedData(feedid, time_now, current_slot, ontime)

        return value

    #--------------------------------------------------------------------------------
    # Display the rate of change for the current and last entry
    #--------------------------------------------------------------------------------
    def ratechange(self, feedid, time, value):
        lastvalue = self.settings.getProcessRateChange(feedid)
        ratechange = value - lastvalue['value']
        self.settings.insertFeedData(feedid, time, time, ratechange)

        return ratechange

    def save_to_input(self, inputid, time, value):
        self.settings.setTimeValue(inputid, time, value)
        return value

    def kwhinc_to_kwhd(self, feedid, time_now, value):
        last = self.settings.getFeedTimeValue(feedid)
        last_time = datetime.strptime(last['time'])

        #$current_slot = floor($time_now / 86400) * 86400;
        #$last_slot = floor($last_time / 86400) * 86400;
        current_slot = self.getstartday(time_now)
        last_slot = self.getstartday(last_time)

        new_kwh = last['value'] + (value / 1000.0)
        if last_slot != current_slot:
            new_kwh = (value / 1000.0)

        self.settings.updateFeedData(feedid, time_now, current_slot, new_kwh)

        return value

    def accumulator(self, feedid, time, value):
        last = self.settings.getFeedTimeValue(feedid)
        value = last['value'] + value
        self.settings.insertFeedData(feedid, time, time, value)
        return value

    """
    def accumulator_daily(self, feedid, time_now, value):
        last = self.settings.getFeedTimeValue(feedid)
        value = last['value'] + value
        feedtime = self.getstartday(time_now)
        self.settings.updateFeedData(feedid, time_now, feedtime, value)
        return value
    """

    #---------------------------------------------------------------------------------
    # This method converts power to energy vs power (Histogram)
    #---------------------------------------------------------------------------------
    def histogram(self, feedid, time_now, value):
        feedname = "feed_" + str(feedid)
        new_kwh = 0
        # Allocate power values into pots of varying sizes
        if value < 500:
            pot = 50

        if value < 2000:
            pot = 100

        else:
            pot = 500

        val = value / pot
        new_value = 0.5 * ceil(2.0 * val) * pot
        time = self.getstartday(time_now)

        # Get the last time
        lastvalue = self.settings.getFeedTimeValue(feedid)
        last_time = datetime.strptime(lastvalue['time'])

        # kWh calculation
        if (time() - last_time) < 7200:
            time_elapsed = (time_now - last_time)
            kwh_inc = (time_elapsed * value) / 3600000
        else:
            kwh_inc = 0

        # Get last value
        lastValue = self.settings.getLastFeedValue(feedname, time, new_value)
        #result = $this->mysqli->query("SELECT * FROM $feedname WHERE time = '$time' AND data2 = '$new_value'");

        """if !lastValue:
            return value

        last_row = result->fetch_array();

        if (!$last_row)
        {
            $result = $this->mysqli->query("INSERT INTO $feedname (time,data,data2) VALUES ('$time','0.0','$new_value')");

            $this->feed->set_timevalue($feedid, $new_value, $time_now);
            $new_kwh = $kwh_inc;
        }
        else
        {
            $last_kwh = $last_row['data'];
            $new_kwh = $last_kwh + $kwh_inc;
        }

        // update kwhd feed
        $this->mysqli->query("UPDATE $feedname SET data = '$new_kwh' WHERE time = '$time' AND data2 = '$new_value'");

        $this->feed->set_timevalue($feedid, $new_value, $time_now);
        return $value;
        """

    def pulse_diff(self, feedid, time_now, value):
        value = self.signed2unsigned(False, False, value)

        if value > 0:
            pulse_diff = 0
            last = self.settings.getFeedTimeValue(feedid)
            last['time'] = datetime.strptime(last['time'])
            if last['time']:
                # Need to handle resets of the pulse value (and negative 2**15?)
                if value >= last['value']:
                    pulse_diff = value - last['value']
                else:
                    pulse_diff = value

            # Save to allow next difference calc.
            self.settings.insertFeedData(feedid, time_now, time_now, value)

            return pulse_diff

    def kwh_to_power(self, feedid, time, value):
        process = self.settings.getProcess("kwhtopower", "feedid")
        if process:
            lastvalue = self.settings.getKWHToPower(feedid)
            kwhinc = value - lastvalue['value']
            joules = kwhinc * 3600000.0
            timeelapsed = (time - lastvalue['time'])
            power = joules / timeelapsed
            self.settings.insertFeedData(feedid, time, time, power)
        self.settings.setKWHToPower(feedid, time, value)

        return power

    def max_value(self, feedid, time_now, value):
        # Get last values
        last = self.settings.getFeedTimeValue(feedid)
        last_val = last['value']
        last_time = datetime.strptime(last['time'])
        feedtime = self.getstartday(time_now)
        time_check = self.getstartday(last_time)

        # Runs on setup and midnight to reset current value - (otherwise db sets 0 as new max)
        if time_check != feedtime:
            self.settings.insertFeedData(feedid, time_now, feedtime, value)
        else:
            if value > last_val:
                self.settings.updateFeedData(feedid, time_now, feedtime, value)
        return value

    def min_value(self, feedid, time_now, value):
        # Get last values
        last = self.settings.getFeedTimeValue(feedid)
        last_val = last['value']
        last_time = datetime.strptime(last['time'])
        feedtime = self.getstartday(time_now)
        time_check = self.getstartday(last_time)

        # Runs on setup and midnight to reset current value - (otherwise db sets 0 as new min)
        if time_check != feedtime:
            self.settings.insertFeedData(feedid, time_now, feedtime, value)
        else:
            if value < last_val:
                self.settings.updateFeedData(feedid, time_now, feedtime, value)
        return value

    def add_feed(self, feedid, time, value):
        last = self.settings.getFeedTimeValue(feedid)
        value = last['value'] + value
        return value

    def sub_feed(self, feedid, time, value):
        last = self.settings.getFeedTimeValue(feedid)
        myvar = last['value'] * 1
        return value - myvar

    def multiply_by_feed(self, feedid, time, value):
        last = self.settings.getFeedTimeValue(feedid)
        value = last['value'] * value
        return value

    def divide_by_feed(self, feedid, time, value):
        last = self.settings.getFeedTimeValue(feedid)
        myvar = last['value'] * 1

        if myvar != 0:
            return value / myvar
        else:
            return 0

    def wh_accumulator(self, feedid, time, value):
        max_power = 25000
        totalwh = value

        process = self.settings.getProcess("whaccumulator", feedid)
        if process:
            last_input = self.settings.getWHACCumulator(feedid)
            last_feed = self.settings.getFeedTimeValue(feedid)
            totalwh = last_feed['value']
            time_diff = time - last_feed['time']
            val_diff = value - last_input['value']
            power = (val_diff * 3600) / time_diff

            if val_diff > 0 and power < max_power:
                totalwh += val_diff

            self.settings.insertFeedData(feedid, time, time, totalwh)
        self.settings.setWHACCumulator(feedid, time, value)

        return totalwh

    #------------------------------------------------------------------------------------------------------
    # Calculate the energy used to heat up water based on the rate of change for the current and a previous temperature reading
    # See http://harizanov.com/2012/05/measuring-the-solar-yield/ for more info on how to use it
    #------------------------------------------------------------------------------------------------------
    def heat_flux(self, feedid, time_now, value):
        return value  # Removed to be reintroduced as a post-processing based visualisation calculated on the fly.

    # Get the start of the day
    def getstartday(self, time_now):
        # $midnight  = mktime(0, 0, 0, date("m",$time_now), date("d",$time_now), date("Y",$time_now)) - ($this->timezoneoffset * 3600);
        # $this->log->warn($midnight." ".date("Y-n-j H:i:s",$midnight)." [".$this->timezoneoffset."]");

        # fix this -> return mktime(0, 0, 0, date("m", time_now), date("d", time_now), date("Y", time_now)) - (self.timezoneoffset * 3600)
        return
