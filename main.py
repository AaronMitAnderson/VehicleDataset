import requests
from bs4 import BeautifulSoup

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

  page_url = f'https://shoppersapp-gateway.carmax.com/api/search/results?Take={numResultsShown}&UserStoreId={storeID}&StoreId={storeID}&ZipCode={zipCode}&SearchText={searchText}&Distance={distance}&MileageMax={maxMilage}'
  # page_url = f'https://www.carmax.com/cars/api/search/run?uri=%2Fcars%3Fmileage%3D80000%26search%3DTruck&skip=0&take=50&zipCode=28226&radius=40&shipping=0&sort=20&scoringProfile=BestMatchScoreVariant3'
  print(page_url)
  response = requests.get(page_url)
  print("Response Received")

  # get JSON from requests and return the results subsection
  # print(response.json()['results'][0:]['stockNumber'])
  listOfStockNumbers = []
  results = response.json()['results']
  for x in results:
    if x['type'] == 'vehicle':
      if x['transferInfo']['isTransferable'] == True:
        listOfStockNumbers.append(x['stockNumber'])
    
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
  listOfCars = get_carmax_page_api()
  print()
  getDictofCars(listOfCars)

if __name__ == "__main__":
  main()
  


# Need the stockNumber of a car within certain optional params (milage, type of car, etc) -> then use the stock number to get the price of the vehicle

# store south blvd - 7197
# within 250 miles
# ford
# truck
# under 10 miles