
# Subway Suggest

Subway Suggest is an intelligent recommendation and automation system designed to optimize customer service and improve efficiency in restaurant environments.  
It automatically suggests sandwiches and deals to customers based on real-time demographic recognition and previously collected data.

By reducing order times and improving customer engagement, Subway Suggest is intended to increase throughput, enhance the customer experience, and ultimately drive higher revenue.

---

## 🚀 Overview

Subway Suggest uses a front-facing camera and pre-trained models to estimate the age and gender of customers, using them as input to a model producing a personalized menu and deal recommendations.  

It comprises:
- A Python backend using OpenCV-based facial analysis and a Keras-based sandwich recommendation model.
- A browser-based frontend displaying recommendations to customers in real time.
- Logging and dataset management scripts for continual learning and local customization.

The system can be adapted for other quick-service restaurants by modifying the training data and configuration files.

---


## 🗂️ Directory Structure

data/  
├── SandwichPrefsData.xlsx 			# Age/gender preference data  
├── Subdata.xlsx 								# Sub names, descriptions, prices  
├── ...compiled face, age, gender models

src/  
├── utils/  
│ ├── css/  
│ ├── images/  
│ ├── index.html  
│ └── indexjs.js  
├── camera.py  
├── cashier.py  
├── datamanager.py  
├── deals.py  
├── guiLaunch.py  
├── htmledit.py  
├── main.py  
└── sandwichDNN.py

README.md  
requirements.txt  
source_code.txt

---

## ⚙️ Installation and Setup

### 1. Clone the Repository
~~~
git clone https://github.com/YourRepo/SubwaySuggest.git
cd SubwaySuggest/src
~~~

### 2. Create a Virtual Environment
We recommended creating a virtual environment to isolate installed modules:
~~~
python -m venv .venv
source .venv/bin/activate        # On macOS/Linux
.venv\Scripts\activate           # On Windows
~~~

### 3. Install Dependencies
~~~
pip install -r requirements.txt
~~~

### 4. Prepare Displays
The program opens **two interfaces**:
- A **CV2 camera window** for employee-side monitoring.
- An **HTML webpage** for the customer display.

Place these on separate monitors for proper operation.

---

## 🧩 Data Configuration

- `SandwichPrefsData.xlsx`  
  Contains collected preference data organized by age group and gender.  
  You can expand this file to reflect different regional or store-specific datasets.

- `Subdata.xlsx`  
  Contains menu data.

---

## 🧰 Running the Application

To start the system:
~~~
python main.py
~~~

This will:
1. Launch the CV2 camera feed.
2. Start the customer-facing webpage.
3. Begin real-time demographic analysis and sandwich recommendation for recognized users.
4. Log employee-entered sandwich purchases in command line for ongoing learning.

---

## 🧮 System Components

### `camera.py`
- Uses OpenCV’s DNN models for detecting faces and estimating age and gender.
- Returns demographic data in real-time to the main thread.

### `sandwichDNN.py`
- Defines a Keras neural network that learns correlations between demographics and sandwich preferences.
- Provides the `Predict()` method for generating top-N sandwich suggestions.


### `datamanager.py`
- Handles reading and transforming `.xlsx` data into numerical encodings for model training.

### `htmledit.py`
- Dynamically updates the HTML recommendation display with new sandwiches and deals.

### `cashier.py`
- Provides a command-line tool for logging actual customer purchases to improve dataset accuracy.

### `deals.py` and `guiLaunch.py`
- Handle deal selection logic and launching or refreshing the local webpage interface.


