[![macos-catalina](https://img.shields.io/badge/macos-catalina-brightgreen.svg)](https://www.apple.com/macos/catalina-preview)
[![black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

    
# WRI_WellBeing_Data_Layer
- The scope of the project ✅
- The data received and requested deliverables from the project partner ✅
- Methodology when analyzing the data and creating the deliverables ✅
- The final format of the deliverables ✅
- Next steps for incorporating the final deliverable with the project partner ✅

## Project Scope
Conducting economic surveys requires huge resources; thus, modern means of acquiring this information using publicly available data and open source technologies create the possibilities of replacing current processes.
Satellite images can act as a proxy for existing data collection techniques such as surveys and census to predict the economic well-being of a region.

The aim of the project is to propose an alternative to Demographic Health Surveys using opoen source data such us Open Street Map, Sentinel and Night Light data.

The initial prototype created a model that had an accuracy of almost 70 percent. 
The aim is to create a model for India that can be adapted and scaled to other countries.

## The Data

### Demographic Health Surveys
#### Introduction
Demographic Health Surveys collect information on population, health, and nutrition for each state and union territory. They are jointly funded by the United States Agency for International Development (USAID), the United Kingdom Department for International Development (DFID), the Bill and Melinda Gates Foundation (BMGF) and United Nations. All datasets are easily available at their website.

#### Omdena's Dataset
The team analyzed a dataset already cleaned by the Omdena Team. Although the dataset was skewed towards the poorest wealth class, the unbalance lied within 1 standard deviation, warranting the dataset workable.  

#### 
### Open Street Maps Data
#### Introduction
OpenStreetMap (OSM) is an opensource project that crowdsources the world map and has made it available totally free of cost. The data quality is generally seen as reliable although it varies across the world. 

#### Data set
Datasets were downloaded via the OSM api. For Minimum Viable Product purpose, data was downloaded only for the Maharashtra state of India. The dataset contained important information like coordinates and counts of geographical landmarks like highways, hospitals and educational institutes. The team posited these landmarks might indicate wealth of the region. 

### Night Time Light Data
#### Introduction
Night time light data can highlight areas of greater economic activity as these regions tend to be reletively more lit. Image data to proceed with this approach was obtained via Google Earth Engine (GEE). GEE provides a quickly accessible collection of data images captured across timelines, light wavelenghts and satellite systems. The data open and free to use for non-commerical uses. 

#### Data set
The team used NASA’s VIIRS/NPP LunarBRDF-Adjusted Nighttime Lights data. Lat-Lon grid setting was adjusted to 500m. 

## Project Deliverables (I think, not sure)
The project had following deliverables:
1. A model prototype
2. A report with an extensive evaluation of the model 

The deliverables will be shared in the following manner:
1. A Github repository containing all the code data and documentation
2. A report explaining model performance and decision making process (.pptx)

## Project Methodology
### Exploratory Data Analysis
#### DHS Dataset
The dataset was explored via Pandas Profiling libary. The target was to correlate wealth class with other factors. A few correlations were noticed: the problem was identified to be non-linear and multivariable, the dataset, highly related. 

#### OSM Dataset
Due to computing resource constraint, the area of study was restricted to Araria district of Maharastra state. A disparity was noticed between the clusters in OSM dataset and DHS dataset. Clusters, not shared by both dataset, were removed. 

The remaining clusters demonstrated a normal distribution of wealth index. 

#### Night Time Light Data
The data was explored but due to a pressing need of computational resources and time, the data was not integrated with the other data sources and hence not utilized for solution building. 


### Modeling
##### Classification Models
A number classification models were tested including decision trees, Logistic regression and Catboost. Their performance was compared on basis of Mean Absolute Error. The impact of encoding technique was also taken into consideration: experiments were carried out with both One Hot Encoding, Label encoding and Catboost Encoder. 

##### Regression Models
The problem was also analyzed as a regression model. Numerous models were tested including Lasso, Linear Regression, Catboost, Decision Tree Regression. Their performance was compared on basis of Mean Absolute Error. The impact of encoding technique was also taken into consideration: experiments were carried out with both One Hot Encoding, Label encoding and Catboost Encoder. 

### Conclusions
'Hybrid' regression model (Decision Tree Regression) performed reletively better. Mean Absolute Error was only 0.64 for a range of scores 1 to 5 (1 representing Poorest wealth class and 5 representing the richest wealth class).

An added benefit is the easy explainable of the model while preserving a high accuracy i.e 70%. 

## Next Steps
1. The model achieved a high accuracy of 70% for the Araria district of Maharashtra. Its performance on state and national level remains to be evaluated. 
2. Nighttime Light Data can be worked to provide an additional layer of information for the model's decision making process. 
3. A neural network regression model can be experiment with to see if Deep Learning techniques can further improve the model performance.
4. Although the model performed very well, its performance over time needs to be evaluated.  

#### Participants
Carlos Mougan
Sunayana Ghosh
Gijs van den Dool
Rohan Nadeem 
#### Referencees

