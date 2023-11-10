  
# :sparkles: Used Car Listing Price Range Prediction :sparkles:
---

<center><img src="https://raw.githubusercontent.com/anthonynamnam/anthonynamnam/main/icons/image/car-banner.png" alt="memes" width="600" /></center>

---

## :memo: Table of Contents :memo:
- [Project Overview](#overview)
    - [Introduction](#intro)
    - [Story Behind](#story)
    - [Problem Statement](#problem)
    - [Our Solution](#solution)
    - [Objectives](#objective)
    - [Potential Impact](#impact)
- [Dataset](#dataset) 
    - [Data Description](#desc)
    - [Data Dictionary](#data-dict)
    - [Data Source](#data-source)
    - [Data Coverage](#data-coverage)
- [Project Roadmap](#roadmap)
    - [Data Cleaning](#cleaning)
    - [Exploratory Data Analysis](#eda)
    - [Feature Engineering](#engine)
    - [Feature Selection](#select)
    - [Model Development](#develop)
    - [Model Deployment](#deploy)
    - [Simple User Interface](#ui)
- [Insights & Findings](#insights)

---

## :eyes: Project Overview :eyes: <a class="anchor" id="overview"></a>

### Introduction :clipboard: <a class="anchor" id="intro"></a>
The North American used car market is a boundless and dynamic landscape, characterized by a huge industry of vehicle makes, models, and relentnessly evolving market dynamics. In 2022, the used car market recorded **38.6 millions** sales volume in United States [[Source: statista]](https://www.statista.com/statistics/183713/value-of-us-passenger-cas-sales-and-leases-since-1990/).  

Buyers and sellers often grapple with the challenge of accurately determining the fair market value of a used car, leading to potential disparities in pricing, suboptimal transactions, and general market inefficiencies. The dilemma of accurately pricing a used vehicles remains a persistent enigma for years. According to [canadadrives](https://www.canadadrives.ca/blog/car-guide/selling-a-used-car-privately), it takes up to 4 weeks to sell a used car. For both sellers and buyers, this dilemma often transforms into uncertainty, frustration, and even missed opportunities. 

### Story Behind :notebook_with_decorative_cover: <a class="anchor" id="story"></a>
My friend, Jason, who lived in Vancouver for 2 years, wanted to get a car recently. He did not have enough budget to get a new car. Therefore, he decided to buy a second-hand vehicle. He went to several dealers for inquiries. However, all dealer agents tried to persuade him to pay at a higher price to get a better car. At last, he got his car from craigslist directly from the previous owner within his budget and his requirement.

<center><img src="https://raw.githubusercontent.com/anthonynamnam/anthonynamnam/main/icons/image/meme-1.png" alt="memes" width="200"/></center>

### Problem Statement :weary: <a class="anchor" id="problem"></a>
The problem we try to address in this project remains focus on **the need for accurate and transparent pricing** in the North American used car market. The wide variety of vehicles, including numerous makes, models, years, mileage, drivetrains, transmission and geographic locations, contributes to the complexity of this problem. 

- **Buyers** often find it difficult to assess whether a listed car's price is reasonable, leading to price uncertainty and the potential for overpayment.  
- **Sellers** may often struggle to set competitive (higher) and attractive (lower) listing prices, potentially resulting in unsuccessful sales or missed opportunity. 

### Our Solution :bulb: <a class="anchor" id="solution"></a>
<center><img src="https://raw.githubusercontent.com/anthonynamnam/anthonynamnam/main/icons/image/meme-2.webp" alt="Project Banner" width="220"/></center>

**To address these issues**, our purposed solution is to develop advanced machine learning and deep learning models that can accurately predict the price range of used cars in North America, considering multiple factors such as make, model, year, mileage, engine condition, location, and other optional features.

### Objectives :dart: <a class="anchor" id="objective"></a>
#### :one: Develop advanced predictive models that estimates the price range for used cars. 
The primary objective is the development of machine learning / deep learning models capable of accurately predicting price ranges for a used car, which will assist both sellers and buyers make informed pricing decisions.

#### :two: Improve market efficiency by enhancing the transparency and fairness in the used car market. 
One of the objectives is to the improve the market efficiency. By providing AI price range predictions, it reduces **information asymmetry** between buyers and sellers ,which also helps users **understand the fair market value** of the used vehicle.

#### :three: Faciliate decision-making process for both sellers and buyers with informed pricing prediction. 
Sellers can benefit by setting **competitive and fair** prices, which can lead to **faster** sales. Buyers can make more informed and data-driven decisions to ensure they are **not overpaying** for a used vehicle.

#### :four: Provide a user-friendly interface (simple website) for easy access to price range predictions.
The project includes the development of a simple and interactive user interface, making it accessible to a wide range of users. This interface allows sellers and buyers to input their vehicle details easily and obtain price range predictions quickly and conveniently.

### Potential Impact :boom: <a class="anchor" id="impact"></a>
According to the research by [Straits Research](https://www.globenewswire.com/en/news-release/2023/03/14/2626611/0/en/Online-Car-Buying-Market-Size-is-projected-to-reach-USD-722-billion-by-2030-growing-at-a-CAGR-of-12-21-Straits-Research.html), ***"Online Car Buying Market Size is projected to reach USD 722 billion by 2030, growing at a CAGR of 12.21%"***. Online used car listing platform empowered by AI would facilitate the makret efficiency, which generate more profit and reduce costs. The time cost and manpower saved for negoiation between parties would save up to 10% of the operation cost.

Assume being part of the data team in an online car listing platform, the price range prediction service could be a premium feature that requires extra transaction percentage or, along with some free services, which is known as **Freemium Model**. The estimated growth of gross profit would be 20%.

---
## :capital_abcd: Dataset :1234: <a class="anchor" id="dataset"></a>

### Dataset Description :abc: <a class="anchor" id="desc"></a>
- There are two separate datasets for Canada data (CA) and United States data (US). However, some data are wrongly located. For example, there are records with `city` of `Burnaby` and `state` of `BC` in the US dataset.
- We will concatenate both datasets together and generate a column `country` during feature engineering stage.
- Both datasets have the same set of columns.
- Dimension of the Datasets:
    |Filename|Country|#. of Rows|#. of Columns|Size|
    |---|:---:|:---:|:---:|:---:|
    |`data/ca-dealers-used.csv`|`CA`|393,603|21|69.60 MB|
    |`data/us-dealers-used.csv`|`US`|7,104,304|21|1.28 GB|
    ||**TOTAL**|7,497,907|21|
- Unique Vehicle Count:
    |Filename|Country|#. of Unique Car|
    |---|:---:|:---:|
    |`data/ca-dealers-used.csv`|`CA`|226,691|
    |`data/us-dealers-used.csv`|`US`|2,387,394|
    ||**TOTAL**|2,614,085|

### Data Dictionary :bookmark: <a class="anchor" id="data-dict"></a>
|Column|Data Type|Description|Remarks/Examples|
|:---|:---:|:---|:---|
|`id`|`str`|Unique ID for each listing on different platforms.||
|`vin`|`str`|`V`ehicle `I`dentifier `N`umber: A 17-char long unique string assigned to the vehicle.||
|`price`|`float`|The listing price of the vehicle on the website.||
|`miles`|`float`|The miles travelled / odometer value listed on the website.||
|`stock_no`|`str`|Stock number of the car listed on the website.||
|`year`|`int`|Model Year of the vehicle.||
|`make`|`str`|Manufacturer of the vehicle.||
|`model`|`str`|Model of the vehicle.||
|`trim`|`str`|Trim Year of the vehicle.||
|`body_type`|`str`|Body type of the vehicle.||
|`vehicle_type`|`str`|Vehicle type of the vehicle.||
|`drivetrain`|`str`|Drivetrain type of the vehicle.||
|`transmission`|`str`|Transmission type of the vehicle.||
|`fuel_type`|`str`|Supported fuel type of the vehicle.|Multiple fuel types in one cell|
|`engine_size`|`float`|Size of the vehicle engine||
|`engine_block`|`str`|Type of the vehicle engine||
|`seller_name`|`str`|Name of the Dealer||
|`street`|`str`|Dealer Location (Street)||
|`city`|`str`|Dealer Location (City)||
|`state`|`str`|Dealer Location (State)||
|`zip`|`str`|Dealer Location (Zip Code / Postal Code)|Different formats in US and CA|

### Data Source :information_desk_person: <a class="anchor" id="data-source"></a>
Dataset can be found on Kaggle :arrow_right: [:door:Teleport:door:](https://www.kaggle.com/datasets/3ea0a6a45dbd4713a8759988845f1a58038036d84515ded58f65a2ff2bd32e00/data)

### Data Coverage :calendar: <a class="anchor" id="data-coverage"></a>
- Temporal Coverage :date:
    - Starting Date: 01 April 2015
    - Ending Date: 05 Jun 2021
    
- Geospatial Coverage :airplane:
    - North America (Canada and United States)

---

## :runner: Project Roadmap / Framework :runner: <a class="anchor" id="roadmap"></a>
### :white_check_mark: Data Cleaning / Preprocessing :bathtub: <a class="anchor" id="cleaning"></a>  
- Remove records without target variable data
- Target variable labelling
- Handling Missing Value
- Features Flattening

### :white_check_mark: Exploratory Data Analysis :mag: <a class="anchor" id="eda"></a>
- Univariate Analysis
- Bivariate Analysis
- Statistical Analysis
- Correlation Analysis

### :white_check_mark: Feature Engineering <a class="anchor" id="engine"></a>
- Feature Transformation 
    - Log Transformation
    - Categorical Encoding
- Multiple Listing Reduction
    - Exact same vehicle with multiple listing ranges in different dealers
- Class Imbalance
    - Over-Sampling
    - Hybrid-Sampling (To be tested)

### :white_check_mark: Model Development <a class="anchor" id="develop"></a>
- Model Tested:
    - :white_check_mark: Logistic Regression **(Baseline Model)**
    - :white_check_mark: Decision Tree
    - :white_check_mark: Stochastic Gradient Boosting
    - :white_check_mark: Adative Boosting
    - :white_check_mark: XGBoost
- Model To Be Tested:
    - :white_square_button: Random Forest
    - :white_square_button: CatBoost
    - :white_square_button: Naive Bayes
    - :white_square_button: K-Nearest Neightbor
    - :white_square_button: Neural Networks

- Model Evaluation
    - Metric: `weighted_f1_score`

#### TODO: Fill Score
|`model`|`train_score`|`test_score`|
|:---|:---:|:---:|
|`Logistic Regression`|`__%`|`__%`|
|`Decision Tree`|`__%`|`__%`|
|`Support Vector Classifier`|`__%`|`__%`|
|`AdaBoost`|`__%`|`__%`|
|`Stochastic Gradient Boosting`|`__%`|`__%`|
|`XGBoost`|`__%`|`__%`|


### :white_check_mark: Feature Selection <a class="anchor" id="select"></a>
- Prinicipal Component Analysis
    - Not useful to improve model performance in our dataset

### :white_square_button: Model Deployment <a class="anchor" id="deploy"></a>
### :white_square_button: User Interface Development <a class="anchor" id="ui"></a>

## :bulb: Insights & Findings :bulb: <a class="anchor" id="insights"></a>
To be concluded.