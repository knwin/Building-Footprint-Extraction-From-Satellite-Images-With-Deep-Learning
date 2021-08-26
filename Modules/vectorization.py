#!/usr/bin/env python
# coding: utf-8

# In[9]:


from osgeo import gdal, ogr
import sys
import os
import matplotlib.pyplot as plt


# In[4]:


def to_shapefile(imageDir,outputShapefile):
    """
    Arguments :
        imageDir(str) : input geotif image
        outputShapefile(str) : output shapefile 

    Returns:
        null
        
    """
    
    #Vectorization 
    sourceRaster = gdal.Open(imageDir)
    band = sourceRaster.GetRasterBand(1)
    bandArray = band.ReadAsArray(1)
    outShapefile = outputShapefile
    driver = ogr.GetDriverByName("ESRI Shapefile")
    outDatasource = driver.CreateDataSource(outShapefile+ ".shp")
    outLayer = outDatasource.CreateLayer("polygonized", srs=None)
    gdal.Polygonize( band, None, outLayer, -1, [], callback=None )
    outDatasource.Destroy()
    sourceRaster = None

    


# In[ ]:




