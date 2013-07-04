import os
import numpy as np
from numpy import *
import urllib2
from cStringIO import StringIO
import sys
import csv

NREL_META_DTYPE = [('id', int32),
                ('latitude', float32),
                ('longitude', float32),
                ('power_density', float32),
                ('power_capacity', float32),
                ('speed', float32),
                ('elevation', float32)]

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

def download_with_progress_bar(data_url, top_level_url, username, password, return_buffer=False):
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

    password_mgr = urllib2.HTTPPasswordMgrWithDefaultRealm()
    password_mgr.add_password(None, top_level_url, username, password)
    handler = urllib2.HTTPBasicAuthHandler(password_mgr)
    opener = urllib2.build_opener(handler)
    urllib2.install_opener(opener)

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

def fetch_nrel_meta_data_all(columns=['id','latitude','longitude','power_density','power_capacity','speed','elevation'], \
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
    data_arr=np.array([(a,b,c,d,e,f,g) for (a,b,c,d,e,f,g) in data], dtype=NREL_META_DTYPE)
    return data_arr[columns]


def fetch_nrel_meta_data(farm_id, columns=['id','latitude','longitude','power_density','power_capacity','speed','elevation'], \
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
    data=fetch_nrel_meta_data_all(['id','latitude','longitude','power_density','power_capacity','speed','elevation'],data_home)
    for farm in data:
	if farm_id==farm[0]:
            ret=[]
            for c in columns:
                ret.append(farm[c])
            return ret
