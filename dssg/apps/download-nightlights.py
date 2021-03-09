# Import argparse library
import argparse
import os
import dataio.ntl_data_extraction as nde
import dataio.osm_data_extraction as ode
import geopandas as gpd
from dotenv import load_dotenv

load_dotenv()

# Create the parser
download_ntl_data = argparse.ArgumentParser(
    description='Download Night Time Light Data')

# Add the arguments
download_ntl_data.add_argument(
    'DistrictName', metavar='string', type=str, help='name of a district')
download_ntl_data.add_argument(
    'StartDate', metavar='string', type=str, help='starting date: YYYY-MM-DD'
)
download_ntl_data.add_argument(
    'EndDate', metavar='string', type=str, help='ending date: YYYY-MM-DD'
)
download_ntl_data.add_argument(
    '-v', '--verbose', action='store_true', help='an optional argument'
)

# Execute the parse_args() method
args = download_ntl_data.parse_args()
print('If you read this line it means you have provided all the parameters.')

district_name = args.DistrictName
start_date = args.StartDate
end_date = args.EndDate

india_shape = os.environ.get("DATA_DIR") + "/gadm36_shp/gadm36_IND_2.shp"
india_gpd = gpd.read_file(india_shape)
district_gdf = ode.extract_district_dataframe(india_gpd, district_name)
file_url_list = nde.get_ntl_file_urls(
    district_gdf, 'VNP46A2', start_date, end_date, 5000, os.environ.get("NTL_HDF5_DIR") + district_name.lower())
print("Obtained File Url List.")
nde.run_downloader(4, file_url_list)
print("Download of hdf5 files completed")
nde.parallel_conversion_to_tiff()
print("Conversion to geotiff completed")

# Example usage : python nightlights-downloader.py 'Araria' '2015-01-01' '2015-01-05'
