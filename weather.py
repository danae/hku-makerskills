import requests

# Poll the current external temperature
def pollExternalTemperature(query = 'Utrecht,NL'):
  # Make the request
  url = 'https://api.openweathermap.org/data/2.5/find?q={}'.format(query)
  response = requests.get(url, params = {'appid': '6b1a98fea6d95bbb8239e5ab471d5dd7', 'units': 'metric'})
  responseJson = response.json()
  temperature = responseJson['list'][0]['main']

  # Return it
  return temperature


# Main function
def main():
  extTemp = pollExternalTemperature('Hilversum,NL')
  print(extTemp)

# Execute the main function
if __name__ == '__main__':
  main()
