import requests
from multiprocessing.pool import ThreadPool
import geopandas as gpd
import os
from dotenv import load_dotenv
import dataio.osm_data_extraction as ode
import modapsclient
from osgeo import ogr, gdal
from gdalconst import *


def download_url(url: str) -> str:
    """Given a url for h5 file checks if the file exists in the pre-defined NTL_HDF5_DIR
    and downloads it if it does not exist.

    Args:
        url (str): web url of the hdf5 file

    Returns:
        str: url
    """
    print("downloading: ", url)
    # assumes that the last segment after the / represents the file name
    filepath = os.environ.get("NTL_HDF5_DIR")
    file_name_start_pos = url.rfind("/") + 1
    file_name = url[file_name_start_pos:]
    r = requests.get(url, stream=True, headers={
                     'Authorization': 'Bearer {}'.format(os.environ.get("LADS_TOKEN"))})
    if r.status_code == requests.codes.ok and not os.path.isfile(filepath+file_name):
        with open(filepath + file_name, 'wb') as f:
            for data in r:
                f.write(data)

    return url


def get_ntl_file_urls(district_gdf: gpd.geodataframe.GeoDataFrame, products: str, startTime: str, endTime: str,
                      collection: int, district_json_file: str) -> list:
    """Given a district geo dataframe and a specific product 

    Args:
        district_gdf (gpd.geodataframe.GeoDataFrame): [description]
        products (str): [description]
        startTime (str): [description]
        endTime (str): [description]
        collection (int): [description]
        district_json_file (str): [description]

    Returns:
        list: [description]
    """
    (w, s, e, n) = ode.district_extents(district_gdf)
    # Create a ModapsClient object
    a = modapsclient.ModapsClient()
    a.headers["Authorization"] = "Bearer " + os.environ.get("LADS_TOKEN")
    collections = a.getCollections('VNP46A2')
    fileIDs = a.searchForFiles(products=products, startTime=startTime, endTime=endTime,
                               north=n, south=s, east=e, west=w, coordsOrTiles='coords', dayNightBoth='N', collection=collection)
    file_url_list = []
    file_name_list = []
    for id in fileIDs:
        file_url = a.getFileUrls(id)[0]
        file_url_list.append(file_url)
        file_name_start_pos = file_url.rfind("/") + 1
        file_name = file_url[file_name_start_pos:]
        file_name_list.append(file_name)
    import json
    #file_name_list_json = json.dumps(file_name_list)
    district_json = {"district_id": int(district_gdf.index[0]),
                     "start_time": startTime,
                     "end_time": endTime,
                     "file_list": file_name_list}
    # write json to file
    with open(district_json_file + "-" + startTime + "-" + endTime + ".json", 'w', encoding='utf-8') as district_json_dumped:
        json.dump(json.dumps(district_json), district_json_dumped)

    return file_url_list


def run_downloader(process: int, file_urls: list):
    print(f'MESSAGE: Running {process} process')
    results = ThreadPool(process).imap_unordered(download_url, file_urls)
    for r in results:
        print(r)


def convert_hdf5_to_geotiff(filename: str) -> bool:
    from pathlib import Path

    ogr.UseExceptions()
    inp_dir = os.environ.get('NTL_HDF5_DIR')
    out_dir = os.environ.get('NTL_TIF_DIR')
    if filename.endswith('.h5'):
        targetfile = Path(filename).stem
        targetfile += '.tif'
        hdflayer = gdal.Open(inp_dir + filename, gdal.GA_ReadOnly)

        subhdflayer = hdflayer.GetSubDatasets()[0][0]
        rlayer = gdal.Open(subhdflayer, gdal.GA_ReadOnly)

        # collect bounding boxs
        horizontal_tile_number = int(rlayer.GetMetadata_Dict()[
                                     "HorizontalTileNumber"])
        vertical_tile_number = int(rlayer.GetMetadata_Dict()[
                                   "VerticalTileNumber"])
        west_bound_coord = (10 * horizontal_tile_number) - 180
        north_bound_coord = 90 - (10 * vertical_tile_number)
        east_bound_coord = west_bound_coord + 10
        south_bound_coord = north_bound_coord - 10

        epsg = "-a_srs EPSG:4326"  # WGS84 coordinate system

        translate_option_text = epsg+" -a_ullr " + str(west_bound_coord) + " " + str(
            north_bound_coord) + " " + str(east_bound_coord) + " " + str(south_bound_coord)
        translate_options = gdal.TranslateOptions(
            gdal.ParseCommandLine(translate_option_text))
        gdal.Translate(out_dir + targetfile, rlayer, options=translate_options)

        return True

    return False


def parallel_conversion_to_tiff():
    from multiprocessing import Pool
    from os import listdir

    p = Pool(12)
    p.map(convert_hdf5_to_geotiff, listdir(os.environ.get("NTL_HDF5_DIR")))
