__author__ = 'scorpio'

import os
os.environ['CLASSPATH'] = "/Users/scorpio/Dev/Apache/Tika/tika-app-1.7.jar"

from jnius import autoclass

## Import the Java classes we are going to need
Tika = autoclass('org.apache.tika.Tika')
Metadata = autoclass('org.apache.tika.metadata.Metadata')
FileInputStream = autoclass('java.io.FileInputStream')
URL = autoclass('java.net.URL')

tika = Tika()
meta = Metadata()
url = URL('http://murdockbuildersmerchants.com')
text = tika.parseToString(url.openStream(), meta)

print(text)