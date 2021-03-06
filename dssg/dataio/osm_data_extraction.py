import pandas as pd
import geopandas as gpd
import contextily as ctx
import matplotlib.pyplot as plt
import osmnx as ox
import networkx
from shapely.geometry import mapping, Polygon
import os
from dotenv import load_dotenv
load_dotenv()


def extract_district_dataframe(countryGDF: gpd.geodataframe.GeoDataFrame, district_name: str) -> gpd.geodataframe.GeoDataFrame:

    district_gdf = countryGDF[countryGDF['NAME_2'] == district_name]
    district_gdf = district_gdf[['NAME_2', 'geometry']]
    return district_gdf


def plot_district_boundary_on_osm_tile(district_gdf: gpd.geodataframe.GeoDataFrame, figsize: int, linewidth: float, zoom: int):
    district_ax = district_gdf.plot(figsize=(
        figsize, figsize), alpha=0.5, edgecolor='k', facecolor="none", linewidth=linewidth)
    return ctx.add_basemap(district_ax, crs=district_gdf.crs, zoom=zoom)


def write_district_osm_tile(district_gdf: gpd.geodataframe.GeoDataFrame, filename: str) -> bool:
    district_bbox = district_gdf.bounds
    w, s, e, n = (district_bbox.minx.values[0], district_bbox.miny.values[0],
                  district_bbox.maxx.values[0], district_bbox.maxy.values[0])
    img, ex = ctx.bounds2raster(w, s, e, n, ll=True, path=os.environ.get(
        "OSM_DIR") + filename, source=ctx.providers.CartoDB.Positron)
    if img.size != 0:
        return True
    else:
        return False


def plot_district_tif(filename: str, figsize: int):
    import rasterio
    from rasterio.plot import show
    district_tif = rasterio.open(filename)
    plt.imshow(district_tif.read(1))
    plt.rcParams["figure.figsize"] = (figsize, figsize)
    plt.rcParams["grid.color"] = 'k'
    plt.rcParams["grid.linestyle"] = ":"
    plt.rcParams["grid.linewidth"] = 0.5
    plt.rcParams["grid.alpha"] = 0.5
    plt.show()


def create_district_knots_and_edges_model(district_gdf: gpd.geodataframe.GeoDataFrame) -> (Polygon, networkx.classes.multidigraph.MultiDiGraph):

    g = [i for i in district_gdf.geometry]
    district_all_coords = list(mapping(g[0])["coordinates"][0])
    district_poly = Polygon(district_all_coords)
    district_graph = ox.graph_from_polygon(district_poly)
    return district_poly, district_graph


def extract_osm_csv(district_poly: Polygon, tags: dict) -> pd.DataFrame:
    """
    Returns the data frame after extraction and writes the dataframe to csv file
    """
    district_osmdf = ox.geometries_from_polygon(district_poly, tags=tags)
    return district_osmdf


def plot_dhs_data(shapefile: str, dhs_cleanded_csv_file: str, figsize: int):
    ctry0_gpd = gpd.read_file(shapefile)
    dhs_df = pd.read_csv(dhs_cleanded_csv_file)
    dhs_points_gdf = gpd.GeoDataFrame(dhs_df, geometry=gpd.points_from_xy(
        dhs_df['LONGNUM'], dhs_df['LATNUM']), crs='EPSG:4326')
    dhs_ax = dhs_points_gdf.plot(figsize=(figsize, figsize))
    ctx.add_basemap(dhs_ax, crs=ctry0_gpd.crs, zoom=8)
