## Building Footprint Extraction from Satellite Images with Deep learning Project

<img src="/dataset/Annotation%20Data/Labelme%20Output%20data/img.png" width="250" height="200" hspace="50">
<img src="/dataset/Annotation%20Data/Labelme%20Output%20data/label.png" width="250" height="200" > 


</br>

# Problem statment
Building footprints are being digitized,annotated from time to time depending on various use case in our Geoinformatic society. However, digitizing over large areas become a labour intensive work and therefore most of GIS related process are almost bottlenecked in this phase. However, with a help of emerging discipline as we all know as Deep learning, it become an easy work. Being able to use the model efficiently is the only thing we require comparing to labour intensive and time-consuming digitizing tasks.

Humbly published this repo in pursuits of trying our utmost to be a great lift for Myanmar Geoinformatic and Machine learning society. Since both contributors were still at their grittiest learning phase, sincere apologies are delivered if any mistakes or inconveiences are encountered.

This project aims to help beginners in both Geospatial technology and deep learning to understand and work out a particular segmentation project on their own.
There are two tracks with 
- one for using our model to extract building footprint his/her own needs
- one for those who would like to gain details insight on our project 

# For those who would like to use our model, please go through 
- Inference.ipynb 

# For those longing for details, please go through
-  Generate Images.ipynb
-  Train.ipynb
-  Inference
-  Geo-process.ipynb


# Utils
- image_utils.py (used for image preprocessing and postprocessing )
- geoprocess.py ( used for georeferencing and shapefile conversion )
- loss.py ( used to import custom loss function into model )

# Weights

Pretrained weights can be seen under weights folder

# Datasets

Datasets used in our training process can be found under this folder. Labelme annotation is used to produce binary mask file.

<p>Bianry mask images can be exported from labelme json format using the following syntax: </p> <br> 

> <code> labelme_json_to_dataset Clip_final_hlaing_thar_yar11.json -o Labelme_Output_data </code>


