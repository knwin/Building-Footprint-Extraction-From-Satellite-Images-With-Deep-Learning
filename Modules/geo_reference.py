#!/usr/bin/env python
# coding: utf-8

# In[1]:


import shutil
from osgeo import gdal
import os 
import glob
import osr


# In[3]:


os.chdir(r"C:\Users\Toby\Desktop\Building-Footprint-Extraction-Practical-Project-toby\Building-Footprint-Extraction-Practical-Project-toby\dataset\Annotation Data\Labelme Output data")


# In[13]:


import shutil
from osgeo import gdal 
import osr

tiff = gdal.Open(r"Clip_final_hlaing_thar_yar1.tif")
gt = tiff.GetGeoTransform()

inputImage = r"test_label.png"
outputImage = r"label_GCS_projected1.tif"

dataset = gdal.Open(inputImage) 
I = dataset.ReadAsArray(0,0,dataset.RasterXSize,dataset.RasterYSize)


outdataset = gdal.GetDriverByName('GTiff') 
output_SRS = osr.SpatialReference() 
output_SRS.ImportFromEPSG(32647)
outdataset = outdataset.Create(outputImage,dataset.RasterXSize,dataset.RasterYSize,1)                  
outdataset.GetRasterBand(1).WriteArray(I)

                     
#gcp_list = [] 
#gcp_list.append(gdal.GCP(west, north, 0, 0,650))
#gcp_list.append(gdal.GCP(east,south, 0, 650,0))

outdataset.SetProjection(output_SRS.ExportToWkt()) 
outdataset.SetGeoTransform(gt)
wkt = outdataset.GetProjection() 
#outdataset.SetGCPs(gcp_list,wkt)
srs =gdal.WarpOptions(dstSRS='ESPG:32647')
gdal.Warp(outputImage, outdataset)
print(type(outdataset))
#outdataset = None

#Final Georeferencing Code


# In[15]:


def geo_ref(ref_image_dir,target_image_dir,output_image_dir,crs):
    """
    Georeferencing an image 
    - 
    
    arguments:
        ref_image_dir (str): original geotiff image directory// Example "C:\Desktop\OriginalImage.tif"
        target_image_dir (str): predicted image directory // Example "C:\Desktop\PredictedImage.png"
        output_image_dir(str) : georeferenced predicted image // Example "C:\Desktop\PredictedImage_Georef.tif"
        crs (str) : Desired Coordinate sytem // Example "'ESPG:32647'"
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
    srs =gdal.WarpOptions(dstSRS=crs)
    gdal.Warp(outputImage, outdataset)
    outdata = outdataset.ReadAsArray()
    outdataset = None
    
    return(outdata)
    


# In[6]:


import glob as glob
data = glob.glob('*.tif')
print(data)

    


# In[16]:


geo_ref('Clip_final_hlaing_thar_yar1.tif','test_label.png','test_output2.tif','ESPG:32647')


# In[17]:


import numpy as np
outdata= outdataset.ReadAsArray()


# In[22]:


import matplotlib.pyplot as plt
plt.imshow(outdata)
plt.show()


# In[13]:


help(geo_ref)


# In[ ]:




