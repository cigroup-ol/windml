"""
Copyright (c) 2013,
Fabian Gieseke, Justin P. Heinermann, Oliver Kramer, Jendrik Poloczek,
Nils A. Treiber
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

    Redistributions of source code must retain the above copyright notice, this
    list of conditions and the following disclaimer.

    Redistributions in binary form must reproduce the above copyright notice,
    this list of conditions and the following disclaimer in the documentation
    and/or other materials provided with the distribution.

    Neither the name of the Computational Intelligence Group of the University
    of Oldenburg nor the names of its contributors may be used to endorse or
    promote products derived from this software without specific prior written
    permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

----

This data and software ("Data") is provided by the National Renewable Energy
Laboratory ("NREL"), which is operated by the Alliance for Sustainable Energy,
LLC ("ALLIANCE") for the U.S. Department Of Energy ("DOE").

Access to and use of these Data shall impose the following obligations on the
user, as set forth in this Agreement.  The user is granted the right, without
any fee or cost, to use, copy, modify, alter, enhance and distribute these Data
for any purpose whatsoever, provided that this entire notice appears in all
copies of the Data.  Further, the user agrees to credit DOE/NREL/ALLIANCE in
any publication that results from the use of these Data.  The names
DOE/NREL/ALLIANCE, however, may not be used in any advertising or publicity to
endorse or promote any products or commercial entities unless specific written
permission is obtained from DOE/NREL/ ALLIANCE.  The user also understands that
DOE/NREL/Alliance is not obligated to provide the user with any support,
consulting, training or assistance of any kind with regard to the use of these
Data or to provide the user with any updates, revisions or new versions of
these Data.

YOU AGREE TO INDEMNIFY DOE/NREL/Alliance, AND ITS SUBSIDIARIES, AFFILIATES,
OFFICERS, AGENTS, AND EMPLOYEES AGAINST ANY CLAIM OR DEMAND, INCLUDING
REASONABLE ATTORNEYS' FEES, RELATED TO YOUR USE OF THESE DATA.  THESE DATA ARE
PROVIDED BY DOE/NREL/Alliance "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES,
INCLUDING BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND
FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED.  IN NO EVENT SHALL
DOE/NREL/ALLIANCE BE LIABLE FOR ANY SPECIAL, INDIRECT OR CONSEQUENTIAL DAMAGES
OR ANY DAMAGES WHATSOEVER, INCLUDING BUT NOT LIMITED TO CLAIMS ASSOCIATED WITH
THE LOSS OF DATA OR PROFITS, WHICH MAY RESULT FROM AN ACTION IN CONTRACT,
NEGLIGENCE OR OTHER TORTIOUS CLAIM THAT ARISES OUT OF OR IN CONNECTION WITH THE
ACCESS, USE OR PERFORMANCE OF THESE DATA.
"""

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
from windml.model.turbine import Turbine
from windml.util.distance import haversine

class NREL(DataSource):
    """ The National Renewable Energy Laboratory ("NREL") data source
    contains measurements of more than 32,000 turbines.
    The data set allows the access of wind speeds and wind power measurements
    of a turbine at a specified time based on the id. For an easier startup,
    we provide a dictionary with pre-defined turbines, containing ids of:

        * tehachapi
        * cheyenne
        * palmsprings
        * reno
        * lasvegas
        * hesperia
        * lancaster
        * yuccavalley
        * vantage
        * casper

    One can access those ids via the dictionary, e.g. *NREL.park_id['tehachapi']*.

    Detailed information about the data set can be found at:
    http://www.nrel.gov/electricity/transmission/about_datasets.html
    GUI: http://wind.nrel.gov/Web_nrel/
    """

    BASE_URL = "http://vegas.informatik.uni-oldenburg.de:80/data/nrel/"

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

    def get_turbine(self, target_idx, year_from, year_to=0):
        """This method fetches and returns a single turbine object.

        Parameters
        ----------

        target_idx : int
                     see windml.datasets.nrel.park_id for example ids.
        year_from  : int
                     2004 - 2006
        year_to    : int
                     2004 - 2006

        Returns
        -------

        Turbine
            An according turbine for target id and time span.
        """

        #if only one year is desired
        if year_to==0:
            year_to=year_from

        # determine the coordinates of the target
        target=self.fetch_nrel_meta_data(target_idx)

        #add target turbine as last element
        newturbine = Turbine(target[0], target[1] , target[2] , target[3] , target[4] , target[5], target[6])
        for y in range(year_from, year_to+1):
           measurement = self.fetch_nrel_data(target[0], y, ['date','corrected_score', 'speed'])
           if y==year_from:
               measurements = measurement
           else:
               measurements = np.concatenate((measurements, measurement))
        newturbine.add_measurements(measurements)
        return newturbine

    def get_windpark_nearest(self, target_idx, n_nearest,\
                    year_from=0, year_to=0):
        """This method fetches and returns a windpark from NREL, which consists
        of the target turbine with the given target_idx and the surrounding
        n-nearest turbines around the target turbine. When called, the wind
        measurements for a given range of years are downloaded for every
        turbine in the park.

        Parameters
        ----------

        target_idx : int
                     see windml.datasets.nrel.park_id for example ids.
        year_from  : int
                     2004 - 2006
        year_to    : int
                     2004 - 2006

        Returns
        -------

        Windpark
            An according windpark for target id, n-nearest, and time span.
        """

        #if only one year is desired
        if year_to==0:
            year_to=year_from

        meta = self.fetch_nrel_meta_data_all()
        target = self.fetch_nrel_meta_data(target_idx)
        tlat, tlon = target[1], target[2]

        marked = []
        nearest = []
        distances = []
        for i in xrange(n_nearest):
            smallest = None
            for t in xrange(meta.shape[0]):
                d = haversine((tlat, tlon), (meta[t][1], meta[t][2]))
                if(smallest == None and t != target_idx - 1 and t not in marked):
                    smallest = t
                    smallest_d = d
                else:
                    if(d <= smallest_d and t != target_idx - 1 and t not in marked):
                        smallest = t
                        smallest_d = d

            marked.append(smallest)
            nearest.append(meta[smallest])
            distances.append(smallest_d)

        result = Windpark(target_idx, distances[-1])

        for row in nearest:
            newturbine = Turbine(row[0], row[1] , row[2] , row[3] , row[4],\
                                 row[5], row[6])
            if year_from != 0:
                for y in range(year_from, year_to+1):
                   measurement = self.fetch_nrel_data(row[0], y,\
                                   ['date','corrected_score','speed'])
                   if y==year_from:
                       measurements = measurement
                   else:
                       measurements = np.concatenate((measurements, measurement))
                newturbine.add_measurements(measurements)
            result.add_turbine(newturbine)

        #add target turbine as last element
        newturbine = Turbine(target[0], target[1] , target[2] , target[3],\
                             target[4] , target[5], target[6])
        if year_from != 0:
            for y in range(year_from, year_to+1):
               measurement = self.fetch_nrel_data(target[0], y,\
                               ['date','corrected_score','speed'])
               if y==year_from:
                   measurements = measurement
               else:
                   measurements = np.concatenate((measurements, measurement))
            newturbine.add_measurements(measurements)
        result.add_turbine(newturbine)

        return result

    def get_windpark(self, target_idx, radius, year_from=0, year_to=0):
        """This method fetches and returns a windpark from NREL, which consists of
        the target turbine with the given target_idx and the surrounding turbine
        within a given radius around the target turbine. When called, the wind
        measurements for a given range of years are downloaded for every turbine
        in the park.

        Parameters
        ----------

        target_idx : int
                     see windml.datasets.nrel.park_id for example ids.
        year_from  : int
                     2004 - 2006
        year_to    : int
                     2004 - 2006

        Returns
        -------

        Windpark
            An according windpark for target id, radius, and time span.
        """

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

        #fetch all turbines
        turbines = self.fetch_nrel_meta_data_all()
        for row in turbines:
            turbine_index = np.int(row[0])
            if (turbine_index != target_idx):
                lat_act = math.radians(np.float64(row[1]))
                lon_act = math.radians(np.float64(row[2]))
                dLat = (lat_act-lat_target)
                dLon = (lon_act-lon_target)

                # Haversine formula:
                a = math.sin(dLat/2) * math.sin(dLat/2) + math.cos(lat_target) * math.cos(lat_act) * math.sin(dLon/2) * math.sin(dLon/2)
                c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
                distance_act = Earth_Radius * c;
                if (distance_act < radius):
                    newturbine = Turbine(row[0], row[1] , row[2] , row[3] , row[4] , row[5], row[6])
                    if year_from != 0:
                        for y in range(year_from, year_to+1):
                           measurement = self.fetch_nrel_data(row[0], y, ['date','corrected_score','speed'])
                           if y==year_from:
                               measurements = measurement
                           else:
                               measurements = np.concatenate((measurements, measurement))
                        newturbine.add_measurements(measurements)
                    result.add_turbine(newturbine)

        #add target turbine as last element
        newturbine = Turbine(target[0], target[1] , target[2] , target[3] , target[4] , target[5], target[6])
        if year_from != 0:
            for y in range(year_from, year_to+1):
               measurement = self.fetch_nrel_data(target[0], y, ['date','corrected_score','speed'])
               if y==year_from:
                   measurements = measurement
               else:
                   measurements = np.concatenate((measurements, measurement))
            newturbine.add_measurements(measurements)
        result.add_turbine(newturbine)
        return result

    def fetch_nrel_meta_data_all(self, columns=['id','latitude','longitude','power_density','power_capacity','speed','elevation'], \
                             data_home = None):
        """ Loader for NREL meta data (all entries).

        Parameters
        ----------
        columns : optional, default=['id','latitude','longitude','power_density','power_capacity','speed','elevation']
                  Specify the columns to be selected, see code above.
        data_home : optional, default=None
                    Specify another download and cache folder for the datasets.
                    By default, data is stored in ~/nrel_data on Unix systems.
        Returns
        -------
        numpy.array
            Array of meta data for a turbines.
        """
        data_home = str(os.getenv("HOME")) + "/nrel_data/"
        archive_file_name = "meta.csv"
        DATA_URL = self.BASE_URL + "site_meta.csv"
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

    def fetch_nrel_meta_data(self, turbine_id, columns=['id','latitude','longitude','power_density','power_capacity','speed','elevation'], \
                                data_home = None):
        """ Loader for NREL meta data, gets one entry by id.

        Parameters
        ----------
        turbine_id : specifies the id of the WEA to be used.
        columns : optional, default=['id','latitude','longitude','power_density','power_capacity','speed','elevation']
                  Specify the columns to be selected, see code above.
        data_home : optional, default=None
                    Specify another download and cache folder for the datasets.
                    By default, data is stored in ~/nrel_data on Unix systems.
        Returns
        -------
        numpy.array
            array of meta data for a turbine.
        """

        attributes = ['id','latitude','longitude','power_density','power_capacity','speed','elevation']
        data=self.fetch_nrel_meta_data_all(attributes, data_home)
        for turbine in data:
            if turbine_id==turbine[0]:
                ret=[]
                for c in columns:
                    ret.append(turbine[c])
                return ret

    def bytes_to_string(self, nbytes):
        """Byte representation for progress bar.

        Parameters
        ----------
        nbytes : int
                 Amount of bytes.

        Returns
        -------
        str
            Representation of bytes.
        """

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
        """Download a file, showing progress.

        Parameters
        ----------
        data_url : string
                   web address.
        return_buffer : boolean (optional)
                        if true, return a StringIO buffer rather than a string.

        Returns
        -------
        str
            Content of the file.
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

    def fetch_nrel_data(self, turbine_id, year,\
        columns=['date','speed','power_output','score','corrected_score'], data_home = None):
        """ Loader for NREL wind measurements.

        Parameters
        ----------
        turbine_id : id of the turbine that shall be fetched.
                 Number between 1 and 32043
        year : year for that the data shall be fetched. can be 2004, 2005, 2006
        columns : optional, default=['date','speed','power_output','score','corrected_score']
                  Specify the columns to be selected, see code above.
        data_home : optional, default=None
                    Specify another download and cache folder for the datasets.
                    By default, data is stored in ~/nrel_data on Unix systems.
        Returns
        -------
        numpy.array
            Includes all values of given attributes (columns) for a given year.
        """

        #todo assert that year is in [2004,2005,2006] and turbine_id is valid, too
        data_home = os.getenv("HOME") + "/nrel_data/"+str(year)+"/"
        archive_file_name = str(turbine_id) +".npy"
        DATA_URL = self.BASE_URL + str(year)+"/"+str(turbine_id)+".csv"
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
                fmt = "%Y-%m-%d %H:%M:%S"
                timestamp=int(time.mktime(datetime.datetime.strptime(row[0], fmt).timetuple()))
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


