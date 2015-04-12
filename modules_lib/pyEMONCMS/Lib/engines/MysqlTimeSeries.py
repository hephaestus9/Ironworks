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
from math import ceil
from ironworks import serverTools


class MysqlTimeSeries():

    def __init__(self):
        self.settings = serverTools.getCMSSettings()
        self.logger = serverTools.getLogger()

    #*
    #* Creates a histogram type mysql table.
    #*
    #* @param integer $feedid The feedid of the histogram table to be created
    #*
    def createHistogram(self, feedid, options):
        feedname = "feed_" + str(feedid)
        self.settings.setMysqlTimeSeriesHistogram(feedname)
        return True

    def postToFeedHistogram(self, feedid, time, value):
        feedname = "feed_" + str(feedid)
        self.settings.postToFeedHistogram(feedname, time, value)

    def updateFeedHistogram(self, feedid, time, value):
        feedname = "feed_" + str(feedid)
        # a. update or insert data value in feed table
        self.settings.updateFeedHistogram(feedname, time, value)
        return value

    def get_data(self, feedid, start, end, outinterval):
        if outinterval < 1:
            outinterval = 1
        dp = ceil((end - start) / outinterval);
        end = start + (dp * outinterval)
        if dp < 1:
            return False

        # Check if datatype is daily so that select over range is used rather than
        # skip select approach
        data = []
        datatype = self.settings.getFeedDataType(feedid)

        if datatype == 2:
            dp = 0

        feedname = "feed_" + str(feedid)

        dataRange = end - start
        if dataRange > 180000 and dp > 0:  # 50 hours
            td = dataRange / dp
            results = self.settings.getFeedDataRange(feedname, start, end)

            for result in results:
                if result[1] != "null":  # Remove this to show white space gaps in graph
                        time = $dataTime * 1000;
                        $data[] = array($time, (float)$dataValue);
                    }
                }
                $t = $tb;
            }
        else:
            if dataRange > 5000 and dp > 0:
                td = int(dataRange / dp)
                queryStr = "SELECT FLOOR(time/" + td + ") AS time, AVG(data) AS data" +
                    " FROM " + feedname + " WHERE time BETWEEN " + start + " AND " + end +
                    " GROUP BY 1 ORDER BY time ASC"
            else:
                td = 1
                queryStr = "SELECT time, data FROM " + feedname +
                    " WHERE time BETWEEN " + start + " AND " + end + " ORDER BY time ASC"

            results = self.settings.query(queryStr)
            if len(results) > 0:
                while($row = $result->fetch_array()) {
                    $dataValue = $row['data'];
                    if ($dataValue!=NULL) { // Remove this to show white space gaps in graph
                        $time = $row['time'] * 1000 * $td;
                        $data[] = array($time , (float)$dataValue);

        return data

    def lastvalue(self, feedid):
        feedname = "feed_" + str(feedid)
        result = self.settings.getLastFeedValue(feedname)
        if result:
            return {'time': result[0], 'value': result[1]}
        else:
            return result

    def export(self, feedid, start):
    {
        // Feed id and start time of feed to export
        $feedid = intval($feedid);
        $start = intval($start)-1;

        // Open database etc here
        // Extend timeout limit from 30s to 2mins
        set_time_limit (120);

        // Regulate mysql and apache load.
        $block_size = 400;
        $sleep = 80000;

        $feedname = "feed_".trim($feedid)."";
        $fileName = $feedname.'.csv';

        // There is no need for the browser to cache the output
        header("Cache-Control: no-cache, no-store, must-revalidate");

        // Tell the browser to handle output as a csv file to be downloaded
        header('Content-Description: File Transfer');
        header("Content-type: text/csv");
        header("Content-Disposition: attachment; filename={$fileName}");

        header("Expires: 0");
        header("Pragma: no-cache");

        // Write to output stream
        $fh = @fopen( 'php://output', 'w' );

        // Load new feed blocks until there is no more data
        $moredata_available = 1;
        while ($moredata_available)
        {
            // 1) Load a block
            $result = $this->mysqli->query("SELECT * FROM $feedname WHERE time>$start
            ORDER BY time Asc Limit $block_size");

            $moredata_available = 0;
            while($row = $result->fetch_array())
            {
                // Write block as csv to output stream
                if (!isset($row['data2'])) {
                    fputcsv($fh, array($row['time'],$row['data']));
                } else {
                    fputcsv($fh, array($row['time'],$row['data'],$row['data2']));
                }

                // Set new start time so that we read the next block along
                $start = $row['time'];
                $moredata_available = 1;
            }
            // 2) Sleep for a bit
            usleep($sleep);
        }

        fclose($fh);
        exit;
    }

    def delete_data_point(self, feedid, time):
    {
        $feedid = intval($feedid);
        $time = intval($time);

        $feedname = "feed_".trim($feedid)."";
        $this->mysqli->query("DELETE FROM $feedname where `time` = '$time' LIMIT 1");
    }

    def deletedatarange(self, feedid, start, end):
    {
        $feedid = intval($feedid);
        $start = intval($start/1000.0);
        $end = intval($end/1000.0);

        $feedname = "feed_".trim($feedid)."";
        $this->mysqli->query("DELETE FROM $feedname where `time` >= '$start' AND `time`<= '$end'");

        return true;
    }

    def deleteTable(self, feedid):
        feedname = "feed_" + feedid
        self.settings.deleteTable(feedname)

    def get_feed_size(self, feedid):
        feedname = "feed_" + feedid
        return self.settings.getFeedSize(feedname)

    def get_meta(self, feedid):
        pass

    def csv_export(self, feedid, start, end, outinterval):
    {
        //echo $feedid;
        $outinterval = intval($outinterval);
        $feedid = intval($feedid);
        $start = floatval($start/1000);
        $end = floatval($end/1000);

        if ($outinterval<1) $outinterval = 1;
        $dp = ceil(($end - $start) / $outinterval);
        $end = $start + ($dp * $outinterval);
        if ($dp<1) return false;

        if ($end == 0) $end = time();

        $feedname = "feed_".trim($feedid)."";

        // There is no need for the browser to cache the output
        header("Cache-Control: no-cache, no-store, must-revalidate");

        // Tell the browser to handle output as a csv file to be downloaded
        header('Content-Description: File Transfer');
        header("Content-type: application/octet-stream");
        $filename = $feedid.".csv";
        header("Content-Disposition: attachment; filename={$filename}");

        header("Expires: 0");
        header("Pragma: no-cache");

        // Write to output stream
        $exportfh = @fopen( 'php://output', 'w' );

        $data = array();
        $range = $end - $start;
        if ($range > 180000 && $dp > 0) // 50 hours
        {
            $td = $range / $dp;
            $stmt = $this->mysqli->prepare("SELECT time, data FROM $feedname WHERE time BETWEEN ? AND ? LIMIT 1");
            $t = $start; $tb = 0;
            $stmt->bind_param("ii", $t, $tb);
            $stmt->bind_result($dataTime, $dataValue);
            for ($i=0; $i<$dp; $i++)
            {
                $tb = $start + intval(($i+1)*$td);
                $stmt->execute();
                if ($stmt->fetch()) {
                    if ($dataValue!=NULL) { // Remove this to show white space gaps in graph
                        $time = $dataTime * 1000;
                        fwrite($exportfh, $dataTime.",".number_format($dataValue,2)."\n");
                    }
                }
                $t = $tb;
            }
        } else {
            if ($range > 5000 && $dp > 0)
            {
                $td = intval($range / $dp);
                $sql = "SELECT FLOOR(time/$td) AS time, AVG(data) AS data".
                    " FROM $feedname WHERE time BETWEEN $start AND $end".
                    " GROUP BY 1 ORDER BY time ASC";
            } else {
                $td = 1;
                $sql = "SELECT time, data FROM $feedname".
                    " WHERE time BETWEEN $start AND $end ORDER BY time ASC";
            }

            $result = $this->mysqli->query($sql);
            if($result) {
                while($row = $result->fetch_array()) {
                    $dataValue = $row['data'];
                    if ($dataValue!=NULL) { // Remove this to show white space gaps in graph
                        $time = $row['time'] * 1000 * $td;
                        fwrite($exportfh, $dataTime.",".number_format($dataValue,2)."\n");
                    }
                }
            }
        }

        fclose($exportfh);
        exit;
    }

}
