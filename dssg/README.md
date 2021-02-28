# India Well-Being

<!-- TOC -->
- [India Well-Being](#india-well-being)
  - [How to setup the environment](#how-to-setup-the-environment)


## How to setup the environment
- Create an `.env` file and do not commit it. Here is an example : 
```
AZURE_URL = <path_to_omdena_azure_blob_storage>
BLOB_CONTAINER = "tif-images"
LOCAL_BLOB_PATH = <local_path_to_download_blob_storage>
DATA_DIR = <local_path_to_data_dir>
OSM_DIR = <path_to_dir_to_download_osm_data>
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
