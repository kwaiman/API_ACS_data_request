# API_ACS_data_request
A Jupyter Notebook to pull the data for American Community Survey

## Description of the project
This project allows user to pull the data on the male population grouped by race and age in the Chicago Metropolitan Area from American Community Survey (ACS) by the US Census Bureau. Users can input the year of the ACS they desire and get the data accordingly.

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

``` shell
pip install pandas
pip install requests
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



## 3. Get an API Key

https://api.census.gov/data/key_signup.html; input the fields required and save the key as a .txt file


## 4. Run the Jupyter Notebook
Follow along the markdowns in the notebook to query the data for the male population in Chicagoland (Chicago Metropolitan Area) by age and race by inputting the year desired (the latest is 2019).
