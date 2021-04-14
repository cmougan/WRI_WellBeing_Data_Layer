# India Well-Being

<!-- TOC -->

- [India Well-Being](#india-well-being)
  - [How to setup the environment](#how-to-setup-the-environment)
  - [Download Nighttime Lights from NASA Site](#download-nighttime-lights-from-nasa-site)
    - [How to create LADS Token for downloading Night Time Lights Files](#how-to-create-lads-token-for-downloading-night-time-lights-files)
    - [Add dssg directory to PYTHONPATH](#add-dssg-directory-to-pythonpath)
    - [How to use the python script](#how-to-use-the-python-script)

## How to setup the environment

- Create an `.env` file and do not commit it. Here is an example :

```
AZURE_URL = <path_to_omdena_azure_blob_storage>
BLOB_CONTAINER = "tif-images"
LOCAL_BLOB_PATH = <local_path_to_download_blob_storage>
DATA_DIR = <local_path_to_data_dir>
OSM_DIR = <path_to_dir_to_download_osm_data>
NTL_HDF5_DIR = <path_to_dir_to_download_hdf5_files>
NTL_TIF_DIR = <path_to_store_hdf5_converted_to_tiff>
LADS_TOKEN = <lads token as obtained from LADS site>
```

please make sure **never** to commit this file into Git.

In your `DATA_DIR` store the shape files related to india in `gadm36_shp` folder.

- Download the India related shapefiles from [here](https://biogeo.ucdavis.edu/data/gadm3.6/shp/gadm36_IND_shp.zip)
- Make sure `pip` is installed in your OS and then install pipenv `pip install pipenv`
- After cloning any of the following branches `dssg/<specific-name>` do the following

```
pipenv shell
pipenv install
```

## Download Nighttime Lights from NASA Site

### How to create LADS Token for downloading Night Time Lights Files

- Create a login on [Earth Data](https://urs.earthdata.nasa.gov/users/new)
- Login by going to [Profile -> Earthdata Login](https://urs.earthdata.nasa.gov/)
- Select [Profile -> Generate Token](https://ladsweb.modaps.eosdis.nasa.gov/tools-and-services/data-download-scripts/#generate-token)from the top menu

### Add dssg directory to PYTHONPATH

- To be able to work with all modules add the dssg directory to python path:
  - In Linux to your `.bashrc` add  `export PYTHONPATH=<path_to_WRI_India_ext/dssg/>:$PYTHONPATH`
  - For Windows follow the instructions [here](https://stackoverflow.com/questions/3701646/how-to-add-to-the-pythonpath-in-windows-so-it-finds-my-modules-packages)

### How to use the python script

- Run the script `download-nightlights.py` from command line using the following steps

```
pipenv shell
python dssg/apps/download-nightlights.py <district_name> <start_date> <end_date>
```

an example : `python dssg/apps/download-nightlights.py 'Araria' '2015-01-01' '2015-01-05'`.

- Before running the script make sure to set the following variables in the `.env` file:

  - `NTL_HDF5_DIR` where all the h5 files will be downloaded,
  - `NTL_TIF_DIR` where all the geo tiff files converted from h5 files are stored.
  - `LADS_TOKEN` that you created.
- After the script finishes you will find the following file e.g., `araria-2015-01-01-2015-01-05.json` created in the `NTL_HDF5_DIR`. This will contain the list of all files associated with a district in the date range. e.g.,

```
"district_id": 61, 
"start_time": "2015-01-01", 
"end_time": "2015-01-05", 
"file_list": ["VNP46A2.A2015001.h26v06.001.2020220053423.h5", "VNP46A2.A2015002.h26v06.001.2020220091927.h5", "VNP46A2.A2015003.h26v06.001.2020220134728.h5", "VNP46A2.A2015004.h26v06.001.2020220174848.h5", "VNP46A2.A2015005.h26v06.001.2020220232713.h5"]
```

## Computing weighted voronoi tessellation

The weighted voronoi tessellation is computed in a separate algorithm and the resulting shapefile can be used directly in the notebook `araria_voronoi.ipynb` . The full process of computing the weighted voronoi of the DHS data for a country has been implemented separately [here](https://github.com/dai-mo/gis-laguerre)
