# Building-Footprint-Extraction-Practical-Project
Practical Project for Semantic Segmentation of Building Footprint from Satellite Images

## Dataset Exploration
- Toby's dataset
- other's dataset

## Annotate (1 day)
- labelme

## preprocess (2 day)
Annotation
- labelme --> coco json
- coco --> binary mask np array --> png format save
- format ready to feed into model

Image
- read geotiff with tifffile --> np array
- visualize, resize(scale)
- pad, crop = 10000,10000 --> 256/512/324 tiles
- save png format

## Data Pipeline
- train (3 day)
	- model = UNet, Deep UNet
	- loss = Dice Focal
	- optimizer = Adam
	- metrics = ?

## Inference pipeline / post process (3 day)
- ?
