import requests
from bs4 import BeautifulSoup
from urllib3 import Timeout

def get_carmax_page_api():
  """Get data for a page of 20 vehicles from the CarMax API."""
  # make a GET request to the vehicles endpoint
  # page_url = 'https://api.carmax.com/v1/api/vehicles?apikey=adfb3ba2-b212-411e-89e1-35adab91b600'
  numResultsShown = '20'
  storeID = '7197'
  zipCode = '28226'
  searchText = 'Truck'
  distance = '1'
  maxMilage = '80000'

  # DEPRECIATED
  # ________________________
  # # page_url = f'https://shoppersapp-gateway.carmax.com/api/search/results?Take={numResultsShown}&UserStoreId={storeID}&StoreId={storeID}&ZipCode={zipCode}&SearchText={searchText}&Distance={distance}&MileageMax={maxMilage}'
  # page_url = "https://www.carmax.com/cars/api/search/run?uri=%2Fcars%3Fsearch%3DTruck&skip=0&take=48&zipCode=28226&radius=40&shipping=0&sort=20&scoringProfile=BestMatchScoreVariant3&visitorID=6ec4db73-f249-497a-9735-48ca92858ffd"
  # print(page_url)
  # response = requests.get(page_url)
  # print("Response Received")
  # ________________________

  page_url = f'https://www.carmax.com/cars/api/search/run?uri=%2Fcars%3Fsearch%3DTruck&skip=0&take=100&zipCode=28226&radius=40&shipping=0&sort=20'

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
    # print(response.text)

  # get JSON from requests and return the results subsection
  # print(response.json()['results'][0:]['stockNumber'])
  listOfStockNumbers = []
  vehicles = response.json()['items']
  for vehicle in vehicles:
    if vehicle['isTransferable'] == True:
      listOfStockNumbers.append(vehicle['stockNumber'])
    
  print(listOfStockNumbers)
  # for stockNumber in listOfStockNumbers:
  #   print(stockNumber)
  return listOfStockNumbers


def getDictofCars(listOfStock):
  listOfCars = []
  # page_url = f'https://shoppersapp-gateway.carmax.com/api/vehicles/21403097'
  # response = requests.get(page_url)
  # result = response.json()['vehicle']
  # price = response.json()['price']
  # sN = result['stockNumber']
  # carDict = {"stockNumber": result['stockNumber'],
  #            "type" : result['description'],
  #            "price" : price['displayPrice'],
  #            "url" : f"https://www.carmax.com/car/{sN}"}
  # print(carDict)

  for stockNumber in listOfStock:
    carDict = {}
    page_url = f'https://shoppersapp-gateway.carmax.com/api/vehicles/{stockNumber}'
    response = requests.get(page_url)
    result = response.json()['vehicle']
    price = response.json()['price']
    sN = result['stockNumber']
    carDict = {"stockNumber": result['stockNumber'],
              "price" : price['displayPrice'],
              "type" : result['description'],
              "location" : result['storeName'],
              "url" : f"https://www.carmax.com/car/{sN}"}
    listOfCars.append(carDict)
  
  erroneousCars = []
  for car in listOfCars:
    if car['price'] <= 30000:
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
  listOfStock = get_carmax_page_api()
  print()
  getDictofCars(listOfStock)

if __name__ == "__main__":
  main()
  


# Need the stockNumber of a car within certain optional params (milage, type of car, etc) -> then use the stock number to get the price of the vehicle

# store south blvd - 7197
# within 250 miles
# ford
# truck
# under 10 miles