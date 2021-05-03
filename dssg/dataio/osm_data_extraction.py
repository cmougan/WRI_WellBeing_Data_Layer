from typing import Tuple
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

Extents = Tuple[float, float, float, float]


def extract_district_dataframe(countryGDF: gpd.geodataframe.GeoDataFrame, district_name: str) -> gpd.geodataframe.GeoDataFrame:
    """Extracts the geo data frame for a given district from the gadm level 2 shapefile of a country

    Args:
        countryGDF (gpd.geodataframe.GeoDataFrame): GeoDataFrame of the gadm36 level 2 shapefile of a country
        district_name (str): Name of a district present in the country represented by countryGDF

    Returns:
        gpd.geodataframe.GeoDataFrame: GeoDataFrame of the district as extracted from countryGDF
    """

    district_gdf = countryGDF[countryGDF['NAME_2'] == district_name]
    district_gdf = district_gdf[['NAME_2', 'geometry']]
    return district_gdf


def district_extents(district_gdf: gpd.geodataframe.GeoDataFrame) -> Extents:
    """Computes the extents the bounding box of a given geo dataframe.

    Args:
        district_gdf (gpd.geodataframe.GeoDataFrame): Geo Dataframe of a district.

    Returns:
        Extents: Denotes the coordinates of the bounding box of the geo dataframe.
    """
    district_bbox = district_gdf.bounds
    w, s, e, n = (district_bbox.minx.values[0], district_bbox.miny.values[0],
                  district_bbox.maxx.values[0], district_bbox.maxy.values[0])
    return (w, s, e, n)


def plot_district_boundary_on_osm_tile(district_gdf: gpd.geodataframe.GeoDataFrame, figsize: int, linewidth: float, zoom: int):
    """Gets the image tile corresponding to the bounding box of a district geo dataframe and plots the tile along with the district boundary.

    Args:
        district_gdf (gpd.geodataframe.GeoDataFrame): Geo dataframe of a district.
        figsize (int): The figure size of the plot, we assume that the length and breadth are the same.
        linewidth (float): Denotes the width of the line used in plotting the boundary of the district 
        zoom (int): level of zoom to be used with contextily library to get the zoom detail on a map tile.
    """
    district_ax = district_gdf.plot(figsize=(
        figsize, figsize), alpha=0.5, edgecolor='k', facecolor="none", linewidth=linewidth)
    return ctx.add_basemap(district_ax, crs=district_gdf.crs, zoom=zoom)


def write_district_osm_tile(district_gdf: gpd.geodataframe.GeoDataFrame, filename: str) -> bool:
    """Writes the map tile corresponding to a district geo dataframe to a geotiff.

    Args:
        district_gdf (gpd.geodataframe.GeoDataFrame): District for which map tile needs to be extracted
        filename (str): geotiff file name to which the map tile is written to.

    Returns:
        bool: Returns True if the map tile is not empty. 
    """
    (w, s, e, n) = district_extents(district_gdf)
    img, ex = ctx.bounds2raster(w, s, e, n, ll=True, path=os.environ.get(
        "OSM_DIR") + filename, source=ctx.providers.CartoDB.Positron)
    if img.size != 0:
        return True
    else:
        return False


def plot_district_tif(filename: str, figsize: int):
    """Plots a geotiff file

    Args:
        filename (str): A geotiff file
        figsize (int): The figure size to plot the tiff.
    """
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


KnotsEdges = Tuple[Polygon, networkx.classes.multidigraph.MultiDiGraph]
default_tags = {'amenity': True, 'building': True, 'emergency': True,
                'highway': True, 'footway': True, 'landuse': True, 'water': True}


def create_district_knots_and_edges_model(district_gdf: gpd.geodataframe.GeoDataFrame) -> KnotsEdges:
    """Given a district geo dataframe this extracts the district polygon from a list of all coordinates 
    and the corresponding graph is created from the district polygon.

    Args:
        district_gdf (gpd.geodataframe.GeoDataFrame): District geo dataframe.

    Returns:
        KnotsEdges: Tuple of the district polygon and district graph.
    """

    g = [i for i in district_gdf.geometry]
    district_all_coords = list(mapping(g[0])["coordinates"][0])
    district_poly = Polygon(district_all_coords)
    district_graph = ox.graph_from_polygon(district_poly)
    return district_poly, district_graph


def create_knots_and_edges_from_boundary(district_voronoi_gdf: gpd.geodataframe.GeoDataFrame, cs: str) -> KnotsEdges:
    district_poly = district_voronoi_gdf.unary_union
    ox.config(overpass_settings=cs)
    district_graph = ox.graph_from_polygon(
        district_poly, truncate_by_edge=False, network_type='all', retain_all=True, )
    return (district_poly, district_graph)


def extract_osm_csv(district_poly: Polygon, tags: dict = default_tags) -> pd.DataFrame:
    """Given the geometry of a district polygon and a set of tags (for different ammenities), the method extracts 
    a pandas dataframe using OpenStreetMaps API. 

    Args:
        district_poly (Polygon): Polygon geometry of a district
        tags (dict, optional): Tags to be passed on the OSM API to extract relevant data for a district. Defaults to default_tags.

    Returns:
        pd.DataFrame: A pandas dataframe containing a list of ammenities and other features for a given district.
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
