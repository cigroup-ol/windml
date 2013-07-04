import os
import numpy as np
from numpy import *
import urllib2
from cStringIO import StringIO
import sys
import csv
import datetime
import time

NREL_DATA_DTYPE = [('date', int32),
                ('speed', float32),
                ('power_output', float32),
                ('score', float32),
                ('corrected_score', float32)]


def bytes_to_string(nbytes):
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

    
def download_with_progress_bar(data_url, return_buffer=False):
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
    total_size_str = bytes_to_string(total_size)
    #total_size_str=total_size.decode('utf-8')
    

    while True:
        next_chunk = fhandle.read(chunk_size)
        nchunks += 1

        if next_chunk:
            buf.write(next_chunk)
            s = ('[' + nchunks * '='
                 + (num_units - 1 - nchunks) * ' '
                 + ']  %s / %s   \r' % (bytes_to_string(buf.tell()),
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

def fetch_nrel_data(farm_id, year, columns=['date','speed','power_output','score','corrected_score'], \
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
        buf = download_with_progress_bar(DATA_URL, return_buffer=True)
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
        data_arr=np.array([(a,b,c,d,e) for (a,b,c,d,e) in data], dtype=NREL_DATA_DTYPE)
        data_arr.setflags(align=True)
        np.save(archive_file, data_arr)
    else:
        data = np.load(archive_file)
        data_arr = np.array(data, dtype=NREL_DATA_DTYPE)
    return data_arr[columns]



