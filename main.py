from itertools import count
import requests
from bs4 import BeautifulSoup
import csv

def get_page(starting_value = 0):
  """Get data for a page of 100 vehicles from the CarMax API."""
  
  numResultsShown = '75'
  zipCode = '28226'
  searchText = 'Truck'
  distance = '40'

  # make a GET request to the vehicles endpoint
  page_url = f'https://www.carmax.com/cars/api/search/run?uri=%2Fcars%3Fsearch%3D{searchText}&skip={starting_value}&take={numResultsShown}&zipCode={zipCode}&radius={distance}&shipping=0&sort=20'

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
    response = requests.request("GET", page_url, headers=headers, data=payload, timeout=10)
  except TimeoutError:
    print('Request Timeout')
  else:
    print("Response Received")
    num_results = response.json()['totalCount']

  count = numResultsShown
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
  listOfCars = []
  print(f'Number of total cars: {num_results}')
  
  # Make a dictionary entry of each vehicles data and append it to the list of cars while your total_count is less than the total number of results
  total_count = int(count)
  while True:
    for vehicle in vehicles:
      Type = f"{vehicle['year']} {vehicle['make']} {vehicle['model']} {vehicle['trim']}"
      carDict = {"StockNumber": vehicle['stockNumber'],
                "Price" : vehicle['basePrice'],
                "MSRP" : vehicle['msrp'],
                #  "Markdown" : vehicle['currentMarkdown'],
                "Type" : Type,
                "Drive Train" : vehicle['driveTrain'],
                "Location" : vehicle['storeName']+ ":" + vehicle['storeCity'],
                "URL" : f"https://www.carmax.com/car/{vehicle['stockNumber']}"}
      listOfCars.append(carDict)
    if int(total_count) >= int(num_results):
      break
    count , vehicles, a = get_page(total_count)
    total_count = total_count + int(count)

  # Pull in the keys for the dictionary to act as the headers for the csv file
  field_names = carDict.keys()

  # write the list of dictionarys to a csv file
  with open('Cars.csv', 'w') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=field_names, lineterminator='\n') #lineterminator needed; DictWriter uses '/r/n' by default
    writer.writeheader()
    writer.writerows(listOfCars)

  # check for any cars under 30k and add them to a list.
  # This is my subsitute for a model. 
  erroneousCars = []
  for car in listOfCars:
    if car['Price'] <= 30000:
      erroneousCars.append(car)

  print()
  if erroneousCars == []:
    print("No mispriced Cars")
  else:
    print("Mispriced Cars:")
    for misprice in erroneousCars:
      print(misprice)

def main():
  count, vehicles, num_results = get_page()
  make_car_dict(count, vehicles, num_results)

if __name__ == "__main__":
  main()
  


# Need the stockNumber of a car within certain optional params (milage, type of car, etc) -> then use the stock number to get the price of the vehicle

# store south blvd - 7197
# within 250 miles
# ford
# truck
# under 10 miles