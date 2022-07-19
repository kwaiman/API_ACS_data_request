# API_ACS_data_request
A Jupyter Notebook to pull the data for American Community Survey

## Description of the project
This project allows user to pull the data on the male population grouped by race and age in American cities from American Community Survey (ACS) by the US Census Bureau. Users can input the year and the city of the ACS they desire and get the data accordingly.

## 1. Create a virtual environment

* (a) Install the virtualenv package
``` shell
pip install virtualenv
```

* (b) Create a directory and set up the virtual environment 
``` shell
mkdir Environments
cd ./Environments
virtualenv project_acs 
```

* (c) Activate the virtual environment
``` shell
source project_acs/Scripts/activate # For Mac/Linux users, use: source project_acs/bin/activate
```

You should be able to see the prompt with (project_acs), and you can check that the Python interpreter is in this virtual environment by typing:
``` shell
which python
```

Reference for Winodws vs. Unix-based OS:
https://stackoverflow.com/questions/8921188/issue-with-virtualenv-cannot-activate

## 2. Install all the dependencies packages

Packages we need for this project:
* pandas
* requests
* jupyter (if you are using jupyter notebook)

``` shell
pip install pandas
pip install requests
pip install jupyter
```

We can check that now we have the packages we need in this virtual environment:
``` shell
pip list
```

Now, we can export the packages and versions needed for this project to requirements.txt
``` shell
pip freeze --local > requirements.txt
cat requirements.txt
```

To install all the packages (and the corresponding verisons) required for this project in a new virtual environment, move the requirements.txt to the working directory and type the following in shell:
``` shell
pip install -r requirements.txt
```

To exit the virtual environment:
``` shell
deactivate
```

## 3. Select the virtual environment as the Kernel on Jupyter Notebook

Install the virtual environment as a kernel onto Jupyter Notebook
``` shell
python -m ipykernel install --name=project_acs
```

Then, select "Kernel" > "Change Kernel" > name of your virtual environment 

![image](https://user-images.githubusercontent.com/64258575/174858711-ed6d2451-8019-46a3-9024-abea0b3169a4.png)


## 4. Get an API Key

Go to: https://api.census.gov/data/key_signup.html; 

Input the name of the university (University of Chicago) and your email address in the required fields; the key will be sent to the email you entered; save the key as a .txt file.


## 5. Run the Jupyter Notebook
### Notebook for using API to Pull the Data from ACS in US Census Bureau
Follow along the markdowns in the notebook *acs_data_pull.ipynb* to query the data for the male population in Chicago city by age and race by inputting the year desired (the latest is 2019). The notebook also demonstrates how to query the data for other American cities.

### Notebook for cross-validating the results
The notebook *data_cross_validation_CDC_wonder.ipynb* contains the dataset downloaded from the CDS Wonder Database for cross-validating the results from the API data pull, follow along the markdowns to query the dataset for reference point check to ensure that the data results from the API data pull is sensible.
