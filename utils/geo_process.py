#!/usr/bin/env python
# coding: utf-8

# In[ ]:


#importing necessary modules
import shutil
from osgeo import gdal,ogr
import osr
import sys
import os
import matplotlib.pyplot as plt



def geo_ref(ref_image_dir,target_image_dir,output_image_dir):
    """
    Georeferencing an image 
    - 
    
    arguments:
        ref_image_dir (str): original geotiff image directory// Example "C:\Desktop\OriginalImage.tif"
        target_image_dir (str): predicted image directory // Example "C:\Desktop\PredictedImage.png"
        output_image_dir(str) : georeferenced predicted image // Example "C:\Desktop\PredictedImage_Georef.tif"
    returns:
        georeferenced predicted image (numpy)
    """
    
    tiff = gdal.Open(ref_image_dir) #ref image directory
    gt = tiff.GetGeoTransform()

    inputImage = target_image_dir #target image directory
    outputImage = output_image_dir #output image directory

    dataset = gdal.Open(inputImage) 
    I = dataset.ReadAsArray(0,0,dataset.RasterXSize,dataset.RasterYSize)


    outdataset = gdal.GetDriverByName('GTiff') 
    output_SRS = osr.SpatialReference() 
    output_SRS.ImportFromEPSG(32647)
    outdataset = outdataset.Create(outputImage,dataset.RasterXSize,dataset.RasterYSize,1)                  
    outdataset.GetRasterBand(1).WriteArray(I)

                    

    outdataset.SetProjection(output_SRS.ExportToWkt()) 
    outdataset.SetGeoTransform(gt)
    wkt = outdataset.GetProjection() 
    srs =gdal.WarpOptions(dstSRS='ESPG:32647')
    gdal.Warp(outputImage, outdataset)
    outdata = outdataset.ReadAsArray()
    outdataset = None
    
    return(outdata)




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
