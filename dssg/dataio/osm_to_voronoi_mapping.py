import dssg.dataio.osm_data_extraction as ode
import geopandas as gpd
import os
from dotenv import load_dotenv
from osgeo import gdal, ogr, osr
import matplotlib.pyplot as plt


def clean_initial_voronoi_shape_file(input_voronoi_shp: str, output_voronoi_shp: str):
    srs = osr.SpatialReference()
    srs.ImportFromEPSG(4326)
    driver = ogr.GetDriverByName('ESRI Shapefile')
    voronoi_ds = driver.Open(input_voronoi_shp)
    outfile = driver.CreateDataSource(output_voronoi_shp)
    outlayer = outfile.CreateLayer(
        'voronoi', geom_type=ogr.wkbPolygon, srs=srs)
    nameField = ogr.FieldDefn('DHSCLUST', ogr.OFTString)
    outlayer.CreateField(nameField)
    nameField = ogr.FieldDefn('LATNUM', ogr.OFTReal)
    outlayer.CreateField(nameField)
    nameField = ogr.FieldDefn('LONGNUM', ogr.OFTReal)
    outlayer.CreateField(nameField)
    featureDefn = outlayer.GetLayerDefn()

    voronoi_layer = voronoi_ds.GetLayer(0)
    for feature in voronoi_layer:
        ingeom = feature.GetGeometryRef()
        outgeom = ingeom.Centroid().Buffer(1.0)

        outFeature = ogr.Feature(featureDefn)
        outFeature.SetGeometry(outgeom)
        outFeature.SetField('DHSCLUST', feature.GetField('DHSCLUST'))
        outFeature.SetField('LATNUM', feature.GetField('LATNUM'))
        outFeature.SetField('LONGNUM', feature.GetField('LONGNUM'))
        outlayer.CreateFeature(outFeature)
        outFeature = None

    voronoi_layer.ResetReading()
    outfile = None


def extract_district_voronoi(india_voronoi_gpd: gpd.geodataframe.GeoDataFrame, district_gdf: gpd.geodataframe.GeoDataFrame) -> gpd.geodataframe.GeoDataFrame:
    (district_poly, district_graph) = ode.create_district_knots_and_edges_model(
        district_gdf)
    district_voronoi_gpd = gpd.clip(india_voronoi_gpd, district_poly)

    # Ignore missing geometries
    district_voronoi_gpd = district_voronoi_gpd[~district_voronoi_gpd.is_empty]

    return district_voronoi_gpd


def plot_district_voronoi(voronoi_gpd: gpd.geodataframe.GeoDataFrame, district_name: str):
    fig, ax = plt.subplots(1, 1, figsize=(10, 10))
    voronoi_gpd.plot(ax=ax)
    ax.set_title("Clipped Voronoi of " + district_name)
    ax.set_axis_off()
    plt.axis('equal')
    plt.show()
