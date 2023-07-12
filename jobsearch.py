#DB Career Search Criteria - https://careers.db.com/professionals/search-roles/#/professional/results/

import json
import pandas as pd

def load_lookup_table(tablename):
  # Specify the file path
  file_path = f"./data/{tablename}.json"
  print(f"file_path = {file_path}")

  # Open the file and load the JSON data
  with open(file_path, 'r') as file:
    data = json.load(file)

  # Parse JSON: string -> json data
  # data = json.loads(json_data)

  # Extract items
  items = data['lookup']['items']

  # Create a data frame
  df = pd.DataFrame(items)

  # # Rename columns
  # df.rename(columns={'id': 'ID', 'label': 'Label'}, inplace=True)
  return df

# Access the JSON data
# Example: printing the loaded JSON data
# df = load_lookup_table("career_level")
# print(df)


# Extract Label values to string
def extract_label_values_tostring(tablename):
  df = load_lookup_table(tablename)
  label_string = ', '.join(item for item in df['label'])
  return (label_string)

# Access all the label string
# Example: printing all the label string
# career_levels = extract_label_values_tostring("career_level")
# print(career_levels)

# Access a list of all citys
citynames = load_lookup_table("cityname")['label'].tolist()
# print(citynames)

# Access a list of all career_levels
career_levels = load_lookup_table("career_level")['label'].tolist()
# print(career_levels)


def get_city_code(city):
  df = load_lookup_table("cityname")
  city_code = df.loc[df['label'] == city, 'id'].values
  return city_code[0] if city_code else ""

# example
# result = get_city_code("Any")
# print(f"result = {result}")

# result = get_city_code("Cary")
# print(f"result = {result}")

# result = get_city_code("New York")
# print(f"result = {result}")

# result = get_city_code("NewYork")
# print(f"result = {result}")

def get_position_schedule_code(career_level):
  df = load_lookup_table("career_level")
  codes = df.loc[df['label'] == career_level, 'id'].values
  return codes[0] if codes else ""

# example
# print(get_position_schedule_code("Analyst"))



# --------------------------------------------------------------
#  DB Career API call Function, and wrap it as search_job_deutschebank
# --------------------------------------------------------------

import requests
import json
import pandas as pd

    

def search_job_deutschebank_call_api(career_level, cityname):
    print(f'career_level = {career_level} cityname = {cityname} ')

    citycode = get_city_code(cityname)
    positioncode = get_position_schedule_code(career_level)
    print(f'citycode = {citycode}  positioncode = {positioncode}')

    # API endpoint
    api_url = "https://api-deutschebank.beesite.de/search/"

    # Request payload
    payload = {
        "LanguageCode": "en",
        "SearchParameters": {
            "FirstItem": 1,
            "CountItem": 100,
            "MatchedObjectDescriptor": [
                "Facet:ProfessionCategory",
                "Facet:UserArea.ProDivision",
                "Facet:Profession",
                "Facet:PositionLocation.CountrySubDivision",
                "Facet:PositionOfferingType.Code",
                "Facet:PositionSchedule.Code",
                "Facet:PositionLocation.City",
                "Facet:PositionLocation.Country",
                "Facet:JobCategory.Code",
                "Facet:CareerLevel.Code",
                "Facet:PositionHiringYear",
                "Facet:PositionFormattedDescription.Content",
                "PositionID",
                "PositionTitle",
                "PositionURI",
                "ScoreThreshold",
                "OrganizationName",
                "PositionFormattedDescription.Content",
                "PositionLocation.CountryName",
                "PositionLocation.CountrySubDivisionName",
                "PositionLocation.CityName",
                "PositionLocation.Longitude",
                "PositionLocation.Latitude",
                "PositionIndustry.Name",
                "JobCategory.Name",
                "CareerLevel.Name",
                "PositionSchedule.Name",
                "PositionOfferingType.Name",
                "PublicationStartDate",
                "UserArea.GradEduInstCountry",
                "PositionImport",
                "PositionHiringYear",
                "PositionID"
            ],
            "Sort": [
                {
                    "Criterion": "PublicationStartDate",
                    "Direction": "DESC"
                }
            ]
        },
        "SearchCriteria": [
           {
			"CriterionName": "PositionOfferingType.Code",
			"CriterionValue": 2
		    },
            {
                "CriterionName": "PositionLocation.City",
                "CriterionValue": citycode
            },
            {
                "CriterionName": "PositionSchedule.Code",
                "CriterionValue": positioncode
            },
            {
                "CriterionName": "PositionFormattedDescription.Content"
            },
            None,
            None
        ]
    }

    # Convert payload to JSON string
    # payload_json = json.dumps(payload)
    

    # Make API call
    response = requests.get(api_url, params={"data": payload})

    # Check if the request was successful
    if response.status_code == 200:
        # Extract and return the response JSON
        response_json = response.json()
        return response_json
    else:
        # Request was not successful, handle the error
        print("Error:", response.status_code)
        return None

# example
response_json = search_job_deutschebank_call_api(career_level = "Analyst", cityname="New York")
df = pd.json_normalize(response_json['SearchResult']['SearchResultItems'])
print(df.info)
# df.loc[0]['MatchedObjectDescriptor.CareerLevel'][0]['Name']



def search_job_deutschebank(career_level: str, cityname: str) -> str:
  """Searches for job positions at Deutsche Bank based on the specified career level and city name.

    Args:
        career_level (str): The desired career level for the job search.
        cityname (str): The name of the city where the job search is to be performed.

    Returns:
        str: A JSON string containing the details of the job positions that match the specified career level
        and city name. The JSON structure includes the matched object ID, position title, organization name,
        and URL for each job position.
  """

  print(f"search_job_deutschebank is called. career_level = {career_level} cityname ={cityname}")
  response_json = search_job_deutschebank_call_api(career_level, cityname)

  # Convert JSON to DataFrame
  df = pd.json_normalize(response_json['SearchResult']['SearchResultItems'])

  # df['inscope'] = 'N'
  df['url'] = ""
  for index, row in df.iterrows():
    df['url'][index] =  "https://careers.db.com/professionals/search-roles/#/professional/job/" + df['MatchedObjectId'][index]
    # if (career_level in df['MatchedObjectDescriptor.CareerLevel'][index][0]['Name']):
      # print(df['MatchedObjectDescriptor.CareerLevel'][index][0]['Name'])
      # df['inscope'][index] ='Y'

  # result = df.loc[df['inscope'] == 'Y']
  df_result = df[['MatchedObjectId','MatchedObjectDescriptor.PositionTitle', 'MatchedObjectDescriptor.OrganizationName', 'url']]
  # df_result1 = df_result.rename(columns={"MatchedObjectId": "jobId", "MatchedObjectDescriptor.PositionTitle": "PositionTitle", \
  #                           'MatchedObjectDescriptor.OrganizationName':"OrganizationName"})

  json_data = df_result.to_json(orient='records')

  return json.dumps(json_data)


# example
# result = search_job_deutschebank('Analyst', 'New York')
# print(f'result = {result}')

# result


def search_job_deutschebank(career_level: str, cityname: str) -> str:
  """Searches for job positions at Deutsche Bank based on the specified career level and city name.

    Args:
        career_level (str): The desired career level for the job search.
        cityname (str): The name of the city where the job search is to be performed.

    Returns:
        str: A JSON string containing the details of the job positions that match the specified career level
        and city name. The JSON structure includes the matched object ID, position title, organization name,
        and URL for each job position.
  """
  response_json = search_job_deutschebank_call_api(career_level, cityname)

  # Convert JSON to DataFrame
  df = pd.json_normalize(response_json['SearchResult']['SearchResultItems'])

  df['url'] = ''
  for index, row in df.iterrows():
    df['url'][index] =  "https://careers.db.com/professionals/search-roles/#/professional/job/" + df['MatchedObjectId'][index]
    
  df_result = df[['MatchedObjectId','MatchedObjectDescriptor.PositionTitle', 'MatchedObjectDescriptor.OrganizationName', 'url']]
  df_result.rename(columns={"MatchedObjectId": "jobId", "MatchedObjectDescriptor.PositionTitle": "PositionTitle",
                                "MatchedObjectDescriptor.OrganizationName":"OrganizationName" }, inplace=True)
  json_data = df_result.to_json(orient='records')
  return json.dumps(json_data)


# --------------------------------------------------------------
# Use OpenAI’s Function Calling Feature
# --------------------------------------------------------------

function_descriptions = [
    {
        "name": "search_job_deutschebank",
        "description": "Find job position at Deutschebank",
        "parameters": {
            "type": "object",
            "properties": {
                "career_level": {
                    "type": "string",
                    "description": "The career level of the job, e.g. Analyst, Associate, Director ,Vice President",
                },
                "cityname": {
                    "type": "string",
                    "description": "The city where the job is located, e.g. New York, London, Sydney, Mumbai",
                },
            },
            "required": ["career_level", "cityname"],
        },
    }
]

# result = search_job_deutschebank('Analyst', 'New York')
# print(f'result = {result}')