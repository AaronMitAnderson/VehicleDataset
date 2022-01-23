import requests
from bs4 import BeautifulSoup
import csv

def get_carmax_page_api():
  """Get data for a page of 20 vehicles from the CarMax API."""
  # make a GET request to the vehicles endpoint
  # page_url = 'https://api.carmax.com/v1/api/vehicles?apikey=adfb3ba2-b212-411e-89e1-35adab91b600'
  numResultsShown = '100'
  zipCode = '28226'
  # searchText = 'Truck'
  distance = '1'
  # maxMilage = '80000'

  page_url = f'https://www.carmax.com/cars/api/search/run?uri=%2Fcars%3Fsearch%3DTruck&skip=0&take={numResultsShown}&zipCode={zipCode}&radius={distance}&shipping=0&sort=20'

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
  print(page_url)
  try:
    response = requests.request("GET", page_url, headers=headers, data=payload, timeout=10)
  except TimeoutError:
    print('Request Timeout')
  else:
    print("Response Received")
    num_results = response.json()['totalCount']
    # print(response.text)

  print()
  # get JSON from requests and return the results subsection
  # print(response.json()['results'][0:]['stockNumber'])
  listOfStockNumbers = []
  vehicles = response.json()['items']
  for vehicle in vehicles:
    if vehicle['isTransferable'] == True or vehicle['transferText'] == "Available at your store":
      listOfStockNumbers.append(vehicle['stockNumber'])
    
  print(listOfStockNumbers)
  return listOfStockNumbers, vehicles


def getDictofCars(listOfStock, vehicles):
  listOfCars = []

  for vehicle in vehicles:
    Type = f"{vehicle['year']} {vehicle['make']} {vehicle['model']} {vehicle['trim']}"
    carDict = {"StockNumber": vehicle['stockNumber'],
               "Price" : vehicle['basePrice'],
               "MSRP" : vehicle['msrp'],
               "Markdown" : vehicle['currentMarkdown'],
               "Type" : Type,
               "Drive Train" : vehicle['driveTrain'],
               "Location" : vehicle['storeName']+ " " + vehicle['storeCity'],
               "URL" : f"https://www.carmax.com/car/{vehicle['stockNumber']}"}
    listOfCars.append(carDict)
  
  field_names= ['StockNumber', 'Price', 'MSRP', 'Markdown', 'Type', 'Drive Train', 'Location', 'URL']

  with open('Cars.csv', 'w') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=field_names, lineterminator='\n')
    writer.writeheader()
    writer.writerows(listOfCars)

  erroneousCars = []
  for car in listOfCars:
    if car['Price'] <= 30000:
      erroneousCars.append(car)
    print(car)

  print()
  if erroneousCars == []:
    print("No mispriced Cars")
  else:
    print("Mispriced Cars:")
    for misprice in erroneousCars:
      print(misprice)

def main():
  listOfStock, vehicles = get_carmax_page_api()
  getDictofCars(listOfStock, vehicles)

if __name__ == "__main__":
  main()
  


# Need the stockNumber of a car within certain optional params (milage, type of car, etc) -> then use the stock number to get the price of the vehicle

# store south blvd - 7197
# within 250 miles
# ford
# truck
# under 10 miles