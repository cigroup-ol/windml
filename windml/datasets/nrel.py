import os
import numpy as np
from numpy import *
import urllib2
from cStringIO import StringIO
import sys
import csv
import datetime
import time

from windml.datasets.data_source import DataSource
from windml.model.windpark import Windpark
from windml.model.windmill import Windmill

class NREL(DataSource):

    park_id = {
        'tehachapi': 4155,
        'cheyenne': 17423,
        'palmsprings' : 1175,
        'reno' : 11637,
        'lasvegas' : 6272,
        'hesperia' : 2028,
        'lancaster' : 2473,
        'yuccavalley': 1539,
        'vantage': 28981,
        'casper': 23167
    }

    NREL_META_DTYPE = [('id', int32),
                ('latitude', float32),
                ('longitude', float32),
                ('power_density', float32),
                ('power_capacity', float32),
                ('speed', float32),
                ('elevation', float32)]

    NREL_DATA_DTYPE = [('date', int32),
                    ('speed', float32),
                    ('power_output', float32),
                    ('score', float32),
                    ('corrected_score', float32)]

    def get_windmill(self, target_idx, year_from, year_to=0):
        """
        This method fetches and returns a single windfarm.
        """
        #if only one year is desired
        if year_to==0:
            year_to=year_from

        # determine the coordinates of the target
        target=self.fetch_nrel_meta_data(target_idx)

        #add target farm as last element
        newmill = Windmill(target[0], target[1] , target[2] , target[3] , target[4] , target[5], target[6])
        for y in range(year_from, year_to+1):
           measurement = self.fetch_nrel_data(target[0], y, ['date','corrected_score', 'speed'])
           if y==year_from:
               measurements = measurement
           else:
               measurements = np.concatenate((measurements, measurement))
        newmill.add_measurements(measurements)
        return newmill

    def get_windpark(self, target_idx, radius, year_from=0, year_to=0):
        """This method fetches and returns a windpark from NREL, which consists of
        the target farm with the given target_idx and the surrounding wind farm
        within a given radius around the target farm. When called, the wind
        measurements for a given range of years are downloaded for every farm
        in the park."""

        #if only one year is desired
        if year_to==0:
            year_to=year_from

        result = Windpark(target_idx, radius)

        # determine the coordinates of the target
        target=self.fetch_nrel_meta_data(target_idx)

        Earth_Radius = 6371
        lat_target = math.radians(np.float64(target[1]))
        lon_target = math.radians(np.float64(target[2]))

        rel_input_lat = []
        rel_input_lon = []

        #fetch all farms
        mills = self.fetch_nrel_meta_data_all()
        for row in mills:
            mill_index = np.int(row[0])
            if (mill_index != target_idx):
                lat_act = math.radians(np.float64(row[1])) # todo "latitude" instead of 1
                lon_act = math.radians(np.float64(row[2]))
                dLat = (lat_act-lat_target)
                dLon = (lon_act-lon_target)

                # Haversine formula:
                a = math.sin(dLat/2) * math.sin(dLat/2) + math.cos(lat_target) * math.cos(lat_act) * math.sin(dLon/2) * math.sin(dLon/2)
                c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
                distance_act = Earth_Radius * c;
                if (distance_act < radius):
                    newmill = Windmill(row[0], row[1] , row[2] , row[3] , row[4] , row[5], row[6])
                    if year_from != 0:
                        for y in range(year_from, year_to+1):
                           measurement = self.fetch_nrel_data(row[0], y, ['date','corrected_score','speed'])
                           if y==year_from:
                               measurements = measurement
                           else:
                               measurements = np.concatenate((measurements, measurement))
                        newmill.add_measurements(measurements)
                    result.add_windmill(newmill)

        #add target farm as last element
        newmill = Windmill(target[0], target[1] , target[2] , target[3] , target[4] , target[5], target[6])
        if year_from != 0:
            for y in range(year_from, year_to+1):
               measurement = self.fetch_nrel_data(target[0], y, ['date','corrected_score','speed'])
               if y==year_from:
                   measurements = measurement
               else:
                   measurements = np.concatenate((measurements, measurement))
            newmill.add_measurements(measurements)
        result.add_windmill(newmill)
        return result

    def fetch_nrel_meta_data_all(self, columns=['id','latitude','longitude','power_density','power_capacity','speed','elevation'], \
                             data_home = None):
        """ Loader for NREL meta data (all entries)
        Parameters
        ----------
        columns : optional, default=['id','latitude','longitude','power_density','power_capacity','speed','elevation']
            Specify the columns to be selected, see code above.
        data_home : optional, default=None
            Specify another download and cache folder for the datasets.
            By default, data is stored in ~/nrel_data on Unix systems.
        Returns
        -------
        Notes
        -----
        Based on astroML
        """
        data_home = os.getenv("HOME") + "/nrel_data/"
        archive_file_name = "meta.csv"
        DATA_URL = "http://stromberg.informatik.uni-oldenburg.de/data/nrel/site_meta.csv"
        if not os.path.exists(data_home):
            os.makedirs(data_home)
        archive_file = os.path.join(data_home, archive_file_name)
        if not os.path.exists(archive_file):
            u = urllib2.urlopen(DATA_URL)
            localFile = open(archive_file, 'w')
            localFile.write(u.read())
            localFile.close()
            print ("downloaded NREL meta data from from %s to %s"
                   % (DATA_URL, data_home))
        reader=csv.reader(open(archive_file, "U"), delimiter=',')
        data = []
        for row in reader:
            point=[]
            point.append(int(row[0]))
            point.append(float(row[1]))
            point.append(float(row[2]))
            point.append(float(row[3]))
            point.append(float(row[4]))
            point.append(float(row[5]))
            point.append(float(row[7]))
            data.append(point)
        # abcde stuff for "TypeError: expected a readable buffer object"
        # todo maybe better solution possible...
        data_arr=np.array([(a,b,c,d,e,f,g) for (a,b,c,d,e,f,g) in data], dtype=self.NREL_META_DTYPE)
        return data_arr[columns]

    def fetch_nrel_meta_data(self, farm_id, columns=['id','latitude','longitude','power_density','power_capacity','speed','elevation'], \
                                data_home = None):
        """ Loader for NREL meta data, gets one entry by id
        Parameters
        ----------
        farm_id : specifies the id of the WEA to be used
        columns : optional, default=['id','latitude','longitude','power_density','power_capacity','speed','elevation']
            Specify the columns to be selected, see code above.
        data_home : optional, default=None
            Specify another download and cache folder for the datasets.
            By default, data is stored in ~/nrel_data on Unix systems.
        Returns
        -------
        Notes
        -----
        Based on astroML
        """
        data=self.fetch_nrel_meta_data_all(['id','latitude','longitude','power_density','power_capacity','speed','elevation'],data_home)
        for farm in data:
            if farm_id==farm[0]:
                ret=[]
                for c in columns:
                    ret.append(farm[c])
                return ret

    def bytes_to_string(self, nbytes):
        if nbytes < 1024:
            return '%ib' % nbytes

        nbytes /= 1024.
        if nbytes < 1024:
            return '%.1fkb' % nbytes

        nbytes /= 1024.
        if nbytes < 1024:
            return '%.2fMb' % nbytes

        nbytes /= 1024.
        return '%.1fGb' % nbytes

    def download_with_progress_bar(self, data_url, return_buffer=False):
        """Download a file, showing progress

        Parameters
        ----------
        data_url : string
            web address
        return_buffer : boolean (optional)
            if true, return a StringIO buffer rather than a string

        Returns
        -------
        s : string
            content of the file
        """
        num_units = 40

        fhandle = urllib2.urlopen(data_url)
        total_size = int(fhandle.info().getheader('Content-Length').strip())
        chunk_size = total_size / num_units

        print "Downloading %s" % data_url
        nchunks = 0
        buf = StringIO()
        total_size_str = self.bytes_to_string(total_size)
        #total_size_str=total_size.decode('utf-8')

        while True:
            next_chunk = fhandle.read(chunk_size)
            nchunks += 1

            if next_chunk:
                buf.write(next_chunk)
                s = ('[' + nchunks * '='
                     + (num_units - 1 - nchunks) * ' '
                     + ']  %s / %s   \r' % (self.bytes_to_string(buf.tell()),
                                            total_size_str))
            else:
                sys.stdout.write('\n')
                break

            sys.stdout.write(s)
            sys.stdout.flush()

        buf.reset()
        if return_buffer:
            return buf
        else:
            return buf.getvalue()

    def fetch_nrel_data(self, farm_id, year, columns=['date','speed','power_output','score','corrected_score'], \
                                data_home = None):
        """ Loader for NREL wind measurements
        Parameters
        ----------
        wae_id : id of the WEA that shall be fetched.
            Number between 1 and 32043
        year : year for that the data shall be fetched. can be 2004, 2005, 2006
        columns : optional, default=['date','speed','power_output','score','corrected_score']
            Specify the columns to be selected, see code above.
        data_home : optional, default=None
            Specify another download and cache folder for the datasets.
            By default, data is stored in ~/nrel_data on Unix systems.
        Returns
        -------
        Notes
        -----
        Based on astroML
        """
        #todo assert that year is in [2004,2005,2006] and farm_id is valid, too
        data_home = os.getenv("HOME") + "/nrel_data/"+str(year)+"/"
        archive_file_name = str(farm_id) +".npy"
        DATA_URL = "http://stromberg.informatik.uni-oldenburg.de/data/nrel/"+str(year)+"/"+str(farm_id)+".csv"
        if not os.path.exists(data_home):
            os.makedirs(data_home)
        archive_file = os.path.join(data_home, archive_file_name)
        if not os.path.exists(archive_file):
            print ("downloading NREL wind measurements from from %s to %s"
                   % (DATA_URL, data_home))
            buf = self.download_with_progress_bar(DATA_URL, return_buffer=True)
            reader=csv.reader(buf, delimiter=',')
            data = []
            reader.next() # skip first, header of csv
            i=0
            for row in reader:
                point=[]
                #convert datetime to unix timestamp
                timestamp=int(time.mktime(datetime.datetime.strptime(row[0], "%Y-%m-%d %H:%M:%S").timetuple()))
                point.append(timestamp)
                point.append(float(row[1]))
                point.append(float(row[2]))
                point.append(float(row[3]))
                point.append(float(row[4]))
                data.append(point)
                i=i+1
            # abcde stuff for "TypeError: expected a readable buffer object"
            # todo maybe better solution possible...
            data_arr=np.array([(a,b,c,d,e) for (a,b,c,d,e) in data], dtype=self.NREL_DATA_DTYPE)
            data_arr.setflags(align=True)
            np.save(archive_file, data_arr)
        else:
            data = np.load(archive_file)
            data_arr = np.array(data, dtype=self.NREL_DATA_DTYPE)
        return data_arr[columns]

