# Function Scripts for the ACS API Task

## Import the modules needed
import pandas as pd
import requests

## Create the functions

# This function pulls down this table: https://api.census.gov/data/2019/acs/acs1/variables.html
# This table is basically a lookup for the variable names we need 
def get_variable_table_df(year):
    variable_table_url = f'https://api.census.gov/data/{year}/acs/acs1/variables.html'
    v_table = pd.read_html(variable_table_url)
    variable_df = pd.DataFrame(v_table[0])
    variable_df['Label'].replace({"!!": " ", ":": ""}, regex=True, inplace=True) # replace !! with spaces

    return variable_df


# Find the indices for the variables we want in the the table. 

## Function to return indices of Variables of interest in the variable table

def get_male_by_age_race_index(variable_table):
    indices = []

    ## Tuple of Racial Groups needed for querying; unwanted ones are commented out
    racial_groups = (
        #"WHITE ALONE", 
        "BLACK OR AFRICAN AMERICAN ALONE",
        #"AMERICAN INDIAN AND ALASKA NATIVE ALONE", 
        #"ASIAN ALONE",
        #"NATIVE HAWAIIAN AND OTHER PACIFIC ISLANDER ALONE",
        #"SOME OTHER RACE ALONE", 
        #"TWO OR MORE RACES", 
        "WHITE ALONE, NOT HISPANIC OR LATINO",
        "HISPANIC OR LATINO")
    
    for race in racial_groups: 

        ## Used for querying against the "CONCEPT" variable 
        
        # total pop size of each race by age 
        query = "SEX BY AGE (" + race + ")"
        condition_start = "Label == 'Estimate Total Male' and Concept == '" + query + "'"
        condition_end = "Label == 'Estimate Total Male 85 years and over' and Concept == '" + query + "'"

        index_start = variable_table.query(condition_start).index[0]
        index_end = variable_table.query(condition_end).index[0]

        indices.extend((index_start, index_end))
        
    return indices


## Function to get the names of the variables of interest;
## Using argument of the variable table, and the indices of the variables of interest

def get_variable_names(variable_table, indices):
    
    ### Placeholder list to store the variables
    total_male_by_age_variables = []
    
    ### Note that it is limited to 50 variables for each API Call
    
    ### Here, we make a step of 2 in the for loop, because we want all the indices BETWEEN each of the 
    ### 2-pairs of element in the indices list
    for i in range(0,len(indices),2):
        
        temp = list((variable_table.iloc[indices[i]: indices[i+1]+1, 0].values))
        total_male_by_age_variables += temp
        
    ## Returning a string of the names of variables joined by a comma    
    return ','.join(total_male_by_age_variables)


## Function to return the state code and the city code of the desired city
def get_city_code(year, state_name, city_name):
    
    ## Request the table of city code via the API of ACS
    city_table = requests.get("https://api.census.gov/data/2019/acs/acs1?get=NAME,B01001_001E&for=place:*")
    
    city_table_list = list(map(lambda x:x.split(','),city_table.text.split('\n')))

    ## Create four pandas Series for the city, state name & code
    city_series = pd.Series(list(map(lambda x:x[2:], list(zip(*city_table_list))[0])))
    city_series[0] = 'city_name'

    state_series = pd.Series(list(map(lambda x:x[1:-1], list(zip(*city_table_list))[1])))
    state_series[0] = 'state_name'

    state_code_series = pd.Series(list(map(lambda x:x[1:-1], list(zip(*city_table_list))[3])))
    state_code_series[0] = 'state_code'

    city_code_series = pd.Series(list(map(lambda x:x[1:-2], list(zip(*city_table_list))[4])))
    city_code_series[0] = 'city_code'

    ## Concatenate into a Dataframe
    df_city_table = pd.concat([city_series, state_series, state_code_series, city_code_series], axis=1)
    header = df_city_table.iloc[0,]
    df_city_table = df_city_table[1:]
    df_city_table.columns = header

    ## Return the query results based on the city and state name input
    query_result = df_city_table.query(f'city_name == "{city_name.title()} city" & state_name == "{state_name.title()}"')
    
    ## Store the resulting city and state code
    query_state_code = query_result.iloc[0,2]
    query_city_code = query_result.iloc[0,3]

    return (query_state_code, query_city_code)

## To query you have to look up a specific url -- this function combines all of the information for us. 

def get_query_url(year, variables, api_key, state_name, city_name):
    # API Reference: https://www.census.gov/data/developers/guidance/api-user-guide.Example_API_Queries.html
    # Data Dictionary: https://api.census.gov/data.html
    host = 'https://api.census.gov/data'
    year = f'/{year}'
    dataset_acronym = '/acs/acs1'
    g = '?get='
    
    ## Use the helper function to get the code for the city and the state
    area_code = get_city_code(year, state_name, city_name)
    state_code = area_code[0]
    city_code = area_code[1]

    #location = f'&for=metropolitan%20statistical%20area/micropolitan%20statistical%20area:16980'
    location = f'&for=place:{city_code}&in=state:{state_code}'

    ## api_key object from the first cell in this notebook 
    usr_key = f"&key={api_key}"

    query_url = f"{host}{year}{dataset_acronym}{g}{variables}{location}{usr_key}"

    return query_url


## Get the response data from the URL generated earlier

def get_query_text(query_url):
    response = requests.get(query_url)
    return response.text



## Get the values in the specified columns in the requested data

def get_col_name(variable_df, indices, col_name):
    
    col_values = []
    
    for i in range(0, len(indices),2):
        temp = [i.replace("!!", " ").replace(":", "") for i in variable_df.iloc[indices[i]:indices[i+1]+1][col_name].values]
        col_values += temp
    
    return col_values


## Function to execute the query

def start_query(year, api_key, state_name, city_name):

    ## Get the variable table for the year
    table = get_variable_table_df(year)

    ## Get the index
    index = get_male_by_age_race_index(table)

    ## Get the Variable Names Based on the Index and the Variable Table
    var_names = get_variable_names(table, index)

    ## Call the get_query_url function to get the URL for passing along to the API call function
    url = get_query_url(year="2018", variables="NAME," + var_names, api_key=api_key, state_name=state_name, city_name=city_name)

    ## Call the get_query_text function to obtain the names of the variables
    response_text = get_query_text(url)

    ## Split the response by new lines ('\n')
    response_split = response_text.split('\n')

    ## Then slice the 2nd element of the response object to obtain the values we need
    response_value = response_split[1].split(',')[:-2]

    ## Change the formatting of the response values to interger
    response_value_Series = pd.Series(response_value[2:]).apply(lambda x:int(x.replace("[","").replace('"','')))

    ## Get the names of the LABEL and CONCEPT in the dataset we requested
    label = get_col_name(table, index, "Label")
    concept = get_col_name(table, index, "Concept")

    ## Convert LABEL and CONCEPT into pandas series
    label_Series = pd.Series(label)
    concept_Series = pd.Series(concept)

    ## Extract the text string of the city value (i.e. Chicago city)
    city_value = response_value[0][2:]

    ## Create a dataframe as the final output
    df_output = pd.DataFrame(data=dict(Value=response_value_Series, Concept=concept_Series, City=city_value))
    df_output.rename(columns={'Value':f'Value_{year}'}, inplace=True)
    df_output.index = label_Series

    ## Display the final data frame output
    display(df_output)

    return df_output


## Function to save the file and create a timestamp
def save_output_df(city_name, df_output):
    
    from datetime import datetime
    time_stamp = datetime.now().strftime(format='%B_%d_%Y_%H%M')

    ## Save the output table to a .csv file with timestamp in the file name
    df_output.to_csv(f"df_{city_name}_{time_stamp}.csv")


