import os
import sys
import urllib2
from cStringIO import StringIO
from numpy import int32, float32
import csv

class AEMO(object):

    BASE_URL = "http://windml.org/data/aemo/"

    AEMO_META_DTYPE = [('id', int32),
                       ('latitude', float32),
                       ('longitude', float32),
                       ('power_capacity', float32)]

    AEMO_DATA_DTYPE = [('date', int32),
                       ('power_output', float32)]

    IDS = {
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

    data_home = os.getenv("HOME") + "/aemo_data/raw/"

    years = [2009, 2010, 2011, 2012]
    months_in_year = {2009 : range(8, 13),\
                      2010 : range(1, 13),\
                      2011 : range(1, 13),\
                      2012 : range(1, 4)}

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
        fileh = file(location, "w")

        num_units = 40

        fhandle = urllib2.urlopen(urlstr)

        total_size = int(fhandle.info().getheader('Content-Length').strip())
        chunk_size = total_size / num_units

        print "Downloading %s" % urlstr
        nchunks = 0
        buf = StringIO()
        total_size_str = self.bytes_to_string(total_size)

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
        fileh.write(buf.getvalue())
        fileh.close()

    def fetch_aemo_data(self):

        if not os.path.exists(self.data_home):
            os.makedirs(self.data_home)

        # meta
        meta_location = self.data_home + "meta.csv"
        if not os.path.exists(meta_location):
            self.download(meta_location, self.BASE_URL + "meta.csv")

        # data
        for year in self.years:
            for month in self.months_in_year[year]:
                location = self.data_home + self.filename(year, month)
                if not os.path.exists(location):
                    self.download(location, self.url(year, month))


    def convert(self):
        csvf = open(self.data_home + "meta.csv", "r")

        reader = csv.reader(csvf.read(), delimiter=',')
        reader.next()

        data = []
        for row in reader:
            point = []
            point.append(self.IDS[row[0]])
            point.append(self.IDS[row[1]])
            point.append(self.IDS[row[2]])
            point.append(self.IDS[row[3]])
            data.append(point)

        data_arr = np.array([(a,b,c,d) for (a,b,c,d) in data], dtype = self.AEMO_META_DTYPE)

ds = AEMO()
ds.fetch_aemo_data()
ds.convert()
