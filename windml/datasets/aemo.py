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

---

The data is available at http://windfarmperformance.info/.
"""
from __future__ import print_function
import os
import sys
from six.moves.urllib.request import urlopen
from socket import timeout
import datetime
import time
try:
    from cStringIO import StringIO
except ImportError:
    from io import StringIO
from numpy import int32, float32, array, save, nan, load
from math import radians, sin, cos, atan2, sqrt
import csv

from windml.datasets.data_source import DataSource
from windml.model.windpark import Windpark
from windml.model.turbine import Turbine

class AEMO(object):
    """ Australian Energy Market Operator ("AEMO") data source contains measurements of 28
    turbines. The data set allows the access of wind power measurements of a turbine at
    a specified time based on the id. A dictionary is provided , which associates
    turbine names to ids.

    * captl_wf
    * cullrgwf
    * gunning1
    * woodlwn1
    * cnundawf
    * cathrock
    * clemgpwf
    * hallwf1
    * hallwf2
    * lkbonny1
    * lkbonny2
    * lkbonny3
    * mtmillar
    * nbhwf1
    * snowtwn1
    * starhlwf
    * bluff1
    * waterlwf
    * wpwf
    * musselr1
    * woolnth1
    * challhwf
    * macarth1
    * mlwf1
    * oakland1
    * portwf
    * waubrawf
    * yambukwf

    One can access those ids via the dictionary, e.g. *AEMO.park_id['hallwf1']*.

    Detailed information about the data set can be found at:
    http://windfarmperformance.info/
    """

    BASE_URL = "http://windml.org/data/aemo/"

    AEMO_META_DTYPE = [('id', int32),
                       ('latitude', float32),
                       ('longitude', float32),
                       ('power_capacity', float32)]

    AEMO_DATA_DTYPE = [('date', int32),
                       ('corrected_score', float32),
                       ('speed', float32)]

    park_id = {
        'captl_wf' : 0,
        'cullrgwf' : 1,
        'gunning1' : 2,
        'woodlwn1' : 3,
        'cnundawf' : 4,
        'cathrock' : 5,
        'clemgpwf' : 6,
        'hallwf1' : 7,
        'hallwf2' : 8,
        'lkbonny1' : 9,
        'lkbonny2' : 10,
        'lkbonny3' : 11,
        'mtmillar' : 12,
        'nbhwf1' : 13,
        'snowtwn1' : 14,
        'starhlwf' : 15,
        'bluff1' : 16,
        'waterlwf' : 17,
        'wpwf' : 18,
        'musselr1' : 19,
        'woolnth1' : 20,
        'challhwf' : 21,
        'macarth1' : 22,
        'mlwf1' : 23,
        'oakland1' : 24,
        'portwf' : 25,
        'waubrawf' : 26,
        'yambukwf' : 27 }

    data_home = str(os.getenv("HOME")) + "/aemo_data/"
    data_home_raw = data_home + "raw/"
    data_home_npy = data_home + "npy/"

    years = [2009, 2010, 2011, 2012]
    months_in_year = {2009 : range(8, 13),\
                      2010 : range(1, 13),\
                      2011 : range(1, 13),\
                      2012 : range(1, 4)}

    def check_availability(self):
        if not os.path.exists(self.data_home_raw):
            self.fetch_aemo_data()
        if not os.path.exists(self.data_home_npy):
            self.convert()
        return

    def get_windpark(self, target_idx, radius):
        """This method fetches and returns a windpark from AEMO, which consists of
        the target turbine with the given target_idx and the surrounding turbine
        within a given radius around the target turbine. When called, the wind
        measurements for a given range of years are downloaded for every turbine
        in the park.

        Parameters
        ----------

        target_idx : int
                     see windml.datasets.nrel.park_id for example ids.

        Returns
        -------

        Windpark
            An according windpark for target id, radius.
        """

        self.check_availability()

        result = Windpark(target_idx, radius)
        target_turbine = self.get_turbine(target_idx)
        lat_target = radians(target_turbine.latitude)
        lon_target = radians(target_turbine.longitude)

        turbines = self.get_all_turbines()

        Earth_Radius = 6371

        for turbine in turbines:
            # because we append the target as last element
            if(turbine.idx == target_idx):
                continue

            lat_act = radians(turbine.latitude)
            lon_act = radians(turbine.longitude)
            dLat = (lat_act - lat_target)
            dLon = (lon_act - lon_target)

            # Haversine formula:
            a = sin(dLat/2) * sin(dLat/2) + cos(lat_target) *\
                cos(lat_act) * sin(dLon/2) * sin(dLon/2)

            c = 2 * atan2(sqrt(a), sqrt(1-a))
            distance_act = Earth_Radius * c;

            if(distance_act < radius):
                result.add_turbine(turbine)

        result.add_turbine(target_turbine)
        return result

    def get_all_turbines(self):
        self.check_availability()

        turbines = []
        for key, idx in self.park_id.items():
            turbines.append(self.get_turbine(idx))
        return turbines

    def get_turbine(self, target_idx):
        """This method fetches and returns a single turbine object.

        Parameters
        ----------

        target_idx : int
                     see windml.datasets.nrel.park_id for example ids.

        Returns
        -------

        Turbine
            An according turbine for target id.
        """

        self.check_availability()

        meta = load(self.data_home_npy + "meta.npy")
        mdata = meta[target_idx]
        measurements = load(self.data_home_npy + "%i.npy" % target_idx)
        latitude, longitude = mdata['latitude'], mdata['longitude']
        power_density = nan
        power_capacity = mdata['power_capacity']
        speed = nan
        elevation = nan
        turbine = Turbine(target_idx, latitude, longitude, power_density,\
                        power_capacity, speed, elevation)
        turbine.add_measurements(measurements)
        return turbine

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

    def filename(self, year, month):
        m = "0" + str(month) + ".csv" if month < 10 else str(month) + ".csv"
        return str(year) + m

    def url(self, year, month):
        return self.BASE_URL + self.filename(year, month)

    def download(self, location, urlstr):
        with open(location, "w") as fileh:
            num_units = 40

            fhandle = urlopen(urlstr)

            total_size = int(fhandle.getheader('Content-Length').strip())
            chunk_size = total_size // num_units

            print("Downloading %s" % urlstr)
            nchunks = 0
            buf = StringIO()
            total_size_str = self.bytes_to_string(total_size)

            while True:
                try:                        
                    next_chunk = fhandle.read(chunk_size)
                    nchunks += 1
                except timeout:
                    print('request timeout for %s' % DATA_URL)
                    next_chunk = None

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

            #buf.reset()
            buf.seek(0)
            fileh.write(buf.getvalue())
            

    def fetch_aemo_data(self):
        if not os.path.exists(self.data_home_raw):
            os.makedirs(self.data_home_raw)

        # meta
        meta_location = self.data_home_raw + "meta.csv"
        if not os.path.exists(meta_location):
            self.download(meta_location, self.BASE_URL + "meta.csv")

        # data
        for year in self.years:
            for month in self.months_in_year[year]:
                location = self.data_home_raw + self.filename(year, month)
                if not os.path.exists(location):
                    self.download(location, self.url(year, month))

    def convert(self):
        def time_to_unix(datestr):
            t = datetime.datetime.strptime(datestr, "%Y-%m-%d %H:%M:%S")
            return time.mktime(t.timetuple())

        if not os.path.exists(self.data_home_npy):
            os.makedirs(self.data_home_npy)

        # convert meta csv to meta numpy array
        csvf = open(self.data_home_raw + "meta.csv", "r")

        buf = csvf.readlines()
        reader = csv.reader(buf, delimiter=',')
        next(reader)

        data = []
        for row in reader:
            point = []
            point.append(self.park_id[row[0]])
            point.append(row[3])
            point.append(row[4])
            point.append(row[5])
            data.append(point)

        data_arr = array([(a,b,c,d) for (a,b,c,d) in data], dtype = self.AEMO_META_DTYPE)
        save(self.data_home_npy + "meta.npy", data_arr)

        # convert data to windml format
        turbine_arrays, turbine_npy_arrays = {}, {}
        for k in self.park_id.keys():
            turbine_arrays[k] = []

        print("The following procedures are only necessary for the first time.")
        print("Converting AEMO data to lists and filtering missing data.")

        for year in self.years:
            for month in self.months_in_year[year]:
                location = self.data_home_raw + self.filename(year, month)
                current = open(location, "r")
                buf = current.readlines()
                reader = csv.reader(buf, delimiter=',')
                keys = next(reader)

                for row in reader:
                    for i in range(1, len(row)):

                        # filter corrupt data
                        if(row[0] == ""):
                            break
                        if(row[i] == ""):
                            continue

                        timestamp = time_to_unix(row[0])
                        power = row[i]
                        turbine_arrays[keys[i]].append([timestamp, power])

                current.close()

        print("Converting to numpy arrays")
        for k in turbine_arrays.keys():
            data = turbine_arrays[k]
            a = array([(a,b,nan) for (a,b) in data], dtype = self.AEMO_DATA_DTYPE)
            turbine_npy_arrays[k] = a
            save(self.data_home_npy + "%i.npy" % self.park_id[k], a)

ds = AEMO()
ds.get_windpark(0, 5)
