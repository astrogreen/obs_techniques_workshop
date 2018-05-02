
# Introduction

Notes available at http://tinyurl.com/otws-db

## What is a data archive?

## How might you use a data archive in astronomy?

# Vizier

Interested in the paper Green et al., [MNRAS 437, 1070 (2014)](http://adsabs.harvard.edu/abs/2014MNRAS.437.1070G).

Would be interested in plotting Halpha vs Mgas to test the analysis in the paper.

Type numbers into python from the paper? *Ridiculous!!!*

## Use Vizier to retrieve tabular data for published papers

Go to Vizier!

Search "Green 2014"

Catalog appears (name is J/MNRAS/437/1070) in [search results][2]. Looking at the catalogs available, it looks like we want the "sample" catalog.

We could download this file in some format, and then parse it into python...or we could just see if python can get the data directly.

## Connecting to Vizier using a script/program

Search "Vizier API" on Google. Looks like there is a python [package called "Astroquery"][4] that can directly query Vizier.

ipython

from astroquery.vizier import Vizier

(error)

Install astroquery using pip

```bash
# Check that python is correctly set-up

pip install astroquery
```

```python
cat_list = Vizier.get_catalogs('J/MNRAS/437/1070/sample')

cat = cat_list[0]

cat.colnames
cat['logLIHa']
cat['Mgas']

import matplotlib.pyplot as plt

plt.scatter(cat['Mgas'], cat['logLIHa'])
plt.show()
```

# Gemini Archive

## Simple data retrieval

Interested in downloading some raw data from the archive. I want NIFS data on the galaxy "GDDS 22-2172" at RA 22:17:39.85, DEC +00:15:26.42.

Go to the [Gemini Archive][1]

Type in details to find data. Hit Search. [Results view][3] appears below search fields

* Files available to download.
* link to download all (selected) at the bottom of the page
* Permanent link to this data.

# Using the API

Now what if I want to get data automatically, e.g. as part of an automated data reduction pipeline?

Look at the [Help](https://archive.gemini.edu/help/index.html). Under "Accessing the Archive from scripts and the command line", there is a link to the [API Help](https://archive.gemini.edu/help/api.html).

Scroll down to find Python script

Copy and paste it to ipython.

Paste into editor and edit to match our program:

```python

import urllib
import json

# Construct the URL. We'll use the jsonfilelist service
url = "https://archive.gemini.edu/jsonsummary/"

# List the files for GN-2010B-Q-22 taken with GMOS-N on 2010-12-31
url += "GN-2008A-Q-18/GMOS-N/NIFS/20090828/science/GDDS-22-2172"

# Open the URL and fetch the JSON document text into a string
u = urllib.urlopen(url)
jsondoc = u.read()
u.close()

# Decode the JSON
files = json.loads(jsondoc)

# This is a list of dictionaries each containing info about a file
total_data_size = 0
print "%20s %22s %10s %8s %s" % ("Filename", "Data Label", "ObsClass",
                                 "QA state", "Object Name")
for f in files:
    total_data_size += f['data_size']
    print "%20s %22s %10s %8s %s" % (f['name'], f['data_label'],
                                     f['observation_class'], f['qa_state'],
                                     f['object'])

print "Total data size: %d" % total_data_size
```

Paste updates into python.

## Open a FITS file from the archive directly in python

Look at download URL from the web page.

Looks something like https://archive.gemini.edu/file/N20090828S0182.fits

So we just need the filename to download the file.

The previous script has created a `files` variable, which we can use to get the filenames of our files. Lets see if we can open one of the files directly in python.

```python

a_filename = files[0]['name']

response = urllib.urlopen("http://archive.gemini.edu/file/" + a_filename)

fits_bytes = response.read()
response.close()

from io import BytesIO
from astropy.io import fits

f = fits.open(BytesIO(fits_bytes))

f.info()

f[0].header

f[1].data.shape

plt(f[1].data, clim=(0,500), interpolation='nearest')

```

[1]: https://archive.gemini.edu
[2]: http://vizier.u-strasbg.fr/viz-bin/VizieR-2?-ref=VIZ5727fab821b6&-to=2&-from=-2&-this=-2&%2F%2Fsource=&-out.max=50&%2F%2FCDSportal=&-out.form=HTML+Table&-out.add=_r&-out.add=_RAJ%2C_DEJ&%2F%2Foutaddvalue=&-sort=_r&-order=I&-oc.form=sexa&-meta.foot=1&-meta=1&-meta.ucd=2&-source=Green+2014&%21-2%3B=+Find...+&-ucd=&%2F%2Fucdform=on&-c=&-c.eq=J2000&-c.r=++2&-c.u=arcmin&-c.geom=r&-sort=_r&-order=I&-sort=_r&-order=I&-meta.ucd=2&-usenav=1&-bmark=GET
[3]: https://archive.gemini.edu/searchform/cols=CTOWEQ/notengineering/NIFS/ra=22:17:39.85/dec=+00:15:26.42/NotFail
[4]: http://astroquery.readthedocs.io/en/latest/vizier/vizier.html
