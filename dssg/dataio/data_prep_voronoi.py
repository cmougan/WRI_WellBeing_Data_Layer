# Code taken from :  https://github.com/sunayana/laguerre-voronoi
import geopandas as gpd
import os
import itertools
from shapely.geometry import Point
from shapely.ops import unary_union
import numpy as np
from dotenv import load_dotenv

load_dotenv()


def get_boundary_from_shapefile(filename: str):
    """This would extract the boundary from a gadm level 0, shapefile of a country

    Args:
        filename (str): GADM level-0 shape filepath of a country

    Returns:
        numpy.ndarray: Returns an array of boundary vertices
    """
    country_gpd = gpd.read_file(filename)

    # Get the outer hull of the country boundary
    outer_hull = unary_union(country_gpd.geometry)
    if outer_hull.type == "MultiPolygon":
        # Simplify the outer hull
        oh_s = outer_hull.simplify(0.1, preserve_topology=False)
        # Extract the largest component, which is a single polygon.
        country_bdry = oh_s[0]

        # Extract the coordinates of the country_bdry polygon.
        country_bdry_np = np.asarray(country_bdry.exterior.coords)
        return country_bdry_np
    elif outer_hull.type == "Polygon":
        return np.asarray(outer_hull.exterior.coords)
    else:
        raise NotImplementedError


def modify_dhs_shapefile(filename: str):
    dhs_gpd = gpd.read_file(filename)
    reduced_dhs_gpd = dhs_gpd[
        ["DHSID", "DHSREGNA", "URBAN_RURA", "LATNUM", "LONGNUM", "ALT_DEM", "DATUM"]
    ]
    # FIXME : figure out what 2km and 5km should be in EPSG4326 coordinates
    # Using the approximate formula where 1 degree Latitude = 111 km we have:
    # 2 km = 0.018018 degrees and 5 km = 0.045045 degrees.
    reduced_dhs_gpd["WEIGHT"] = [
        0.018018 if x == "U" else 0.045045 for x in reduced_dhs_gpd["URBAN_RURA"]
    ]
    # Create a geometry column
    reduced_dhs_gpd = gpd.GeoDataFrame(
        reduced_dhs_gpd,
        geometry=gpd.points_from_xy(reduced_dhs_gpd.LONGNUM, reduced_dhs_gpd.LATNUM),
    )

    # extract all the points as list from geoseries
    coordinates = reduced_dhs_gpd.geometry.apply(coord_lister_of_point_series)
    npcoord = coordinates.to_numpy()
    merged = list(itertools.chain(*npcoord))
    sites_list = [list(elem) for elem in merged]
    npsites = np.array([np.array(si) for si in sites_list])
    # extract all weights as list from panda.coreseries
    weights = reduced_dhs_gpd.WEIGHT
    weights_list = weights.to_list()
    npweights = np.array(weights_list)

    return (npsites, npweights)


def coord_lister_of_point_series(geom):
    coords = list(geom.coords)
    return coords
