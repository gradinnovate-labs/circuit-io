##
# @file   ispd2005_2015.py
# @author Yibo Lin, Zixuan Jiang, Jiaqi Gu
# @date   Mar 2019
#

import os
import sys
import tarfile
import lzma
if sys.version_info[0] < 3:
    import urllib2 as urllib
    from StringIO import StringIO
else:
    import urllib.request as urllib
    from io import BytesIO as StringIO

baseURL = "http://www.cerc.utexas.edu/~zixuan/"
target_dir = os.path.dirname(os.path.abspath(__file__))
filenames = ["ispd2005dp.tar.xz", "ispd2015dp.tar.xz"]

for filename in filenames:
    file_url = baseURL + filename
    path_to_file = os.path.join(target_dir, filename)

    print("Download from %s to %s" % (file_url, path_to_file))
    response = urllib.urlopen(file_url)
    content = response.read()
    with open(path_to_file, 'wb') as f:
        f.write(content)

    print("Uncompress %s to %s" % (path_to_file, target_dir))
    with lzma.open(path_to_file, 'rb') as xz:
        with tarfile.open(fileobj=xz) as tar:
            tar.extractall(target_dir)

    print("remove downloaded file %s" % (path_to_file))
    os.remove(path_to_file)
