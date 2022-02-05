from operator import index
import requests
from bs4 import BeautifulSoup
import csv
import sys
import pandas as pd

def get_page(starting_value = 0):
  """Get data for a page of 100 vehicles from the CarMax API."""
  


  # if len(sys.argv) > 1:
  #   if sys.argv[1] > 100:
  #     num_results_shown = 100
  #   else:
  #     num_results_shown = sys.argv[1]
  #   zip_code = sys.argv[2]
  #   search_text = 'Truck'
  #   distance = sys.argv[3]
  # else:
  num_results_shown = '75'
  zip_code = '28226'
  search_text = 'Truck'
  distance = '40'

  # make a GET request to the vehicles endpoint
  # page_url = f'https://www.carmax.com/cars/api/search/run?uri=%2Fcars%3Fsearch%3D{search_text}&skip={starting_value}&take={num_results_shown}&zipCode={zip_code}&radius={distance}&shipping=0&sort=20'
  page_url = f'https://www.carmax.com/cars/api/search/run?uri=/cars/pickup-trucks&skip={starting_value}&take={num_results_shown}&zipCode=28227&radius=90&shipping=0&sort=20&scoringProfile=BestMatchScoreVariant3'

  # Headers needed to allow the CM api to respond
  payload={}
  headers = {'Accept': '*/*',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'en-US,en;q=0.5',
    'Connection': 'keep-alive',
    'Content-Type': 'application/json',
    'DNT': '1',
    'Host': 'www.carmax.com',
    'Referer': 'https://www.carmax.com/cars/all',
    'apikey': 'adfb3ba2-b212-411e-89e1-35adab91b600',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'TE': 'trailers',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:96.0) Gecko/20100101 Firefox/96.0'
  }

  # Print page URL to confirm results shown
  print(page_url)
  # Attempt to get page, on timeout print error
  try:
    response = requests.request("GET", page_url, headers=headers, data=payload, timeout=20)
  except TimeoutError:
    print('Request Timeout')
  else:
    print("Response Received")
    num_results = response.json()['totalCount']

  count = num_results_shown
  # Blank line for readability
  print()

  # get JSON from requests and return the results subsection
  # response.json()['items'] returns a dictionary of all the items in the items subsection
  # listOfStockNumbers = []
  vehicles = response.json()['items']
  
  # Check if the vehicle is either transferable or at the home location. 
  # Add vehicle stock number to a list and print that list of Stock Numbers
  # Technically not needed anymore
  # _______________________________
  # for vehicle in vehicles:
  #   if vehicle['isTransferable'] == True or vehicle['transferText'] == "Available at your store":
  #     listOfStockNumbers.append(vehicle['stockNumber'])
  # print(listOfStockNumbers)
  return count, vehicles, num_results


def make_car_dict(count, vehicles, num_results):
  list_of_cars = []
  print(f'Number of total cars: {num_results}')
  
  # Make a dictionary entry of each vehicles data and append it to the list of cars while your total_count is less than the total number of results
  total_count = int(count)
  while True:
    for vehicle in vehicles:
      Type = f"{vehicle['year']} {vehicle['make']} {vehicle['model']} {vehicle['trim']}"
      car_dict = {"StockNumber": vehicle['stockNumber'],
                "Price" : vehicle['basePrice'],
                "MSRP" : vehicle['msrp'],
                #  "Markdown" : vehicle['currentMarkdown'],
                "Type" : Type,
                "Drive Train" : vehicle['driveTrain'],
                "Location" : vehicle['storeName']+ ":" + vehicle['storeCity'],
                "URL" : f"https://www.carmax.com/car/{vehicle['stockNumber']}"}
      list_of_cars.append(car_dict)
    if int(total_count) >= int(num_results):
      break
    count , vehicles, a = get_page(total_count)
    total_count = total_count + int(count)

  # Pull in the keys for the dictionary to act as the headers for the csv file
  field_names = car_dict.keys()

  # write the list of dictionarys to a csv file
  with open('Cars.csv', 'w') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=field_names, lineterminator='\n') #lineterminator needed; DictWriter uses '/r/n' by default
    writer.writeheader()
    writer.writerows(list_of_cars)

  
  car_df = pd.DataFrame(list_of_cars, columns=field_names)
  print(car_df)
  car_df.to_csv('dfCars.csv')

  # check for any cars under 30k and add them to a list.
  # This is my subsitute for a model. 
  erroneous_cars = []
  for car in list_of_cars:
    if car['Price'] <= 30000:
      erroneous_cars.append(car)

  print()
  # if erroneous_cars == []:
  #   print("No mispriced Cars")
  # else:
  #   print("Mispriced Cars:")
  #   for misprice in erroneous_cars:
  #     print(misprice)

def main():
  count, vehicles, num_results = get_page()
  make_car_dict(count, vehicles, num_results)

if __name__ == "__main__":
  main()
  