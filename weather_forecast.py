import requests
from pprint import pprint
import os

# set the API key
api_key = os.environ.get('WEATHER_KEY')

# set the url and query parameters
forecast_url = 'https://api.openweathermap.org/data/2.5/forecast'
    
def get_location():
    # get user input and format it for the query
    city = input('Enter desired city: ')
    country = input('Enter associated two-letter country code: ')
    location = city + ',' + country
    return location

def request_forecast(location, key):
    # set query parameters
    forecast_query = {'q': location, 'units': 'imperial', 'appid': key}

    # query the API and return the response
    try: 
        forecast_response = requests.get(forecast_url, params=forecast_query)
        forecast_response.raise_for_status()
        return forecast_response
    
    except Exception as e:
        print(e)
        print('Error contacting API. CHeck your spelling.')

def create_forecast(forecast_data):
    try:
        # convert to JSON and extract the list
        forecast_json = forecast_data.json()
        data = forecast_json['list']

        for time in range(len(data)):
            # pull temp, weather and timestamp from current dictionary
            current_temp = data[time]['main']['temp']
            daily_weather = data[time]['weather'][0]['description']
            wind_speed = data[time]['wind']['speed']
            timestamp = data[time]['dt_txt']

            # print a message to the user
            print(f'On {timestamp} the temperature will be {current_temp}F, the wind speed will be {wind_speed}MPH and the weather will be {daily_weather}.')

            # figure out the current day... kind of
            day_break = time + 1 
            day = int((day_break / 8) + 1)

            # print a message after every 8 forecasts to split it up by day
            # the days don't really line up but I had a use case for modulo so I had to do it
            if day_break % 8 == 0 and day_break < 40:
                print(f'Day {day}:')

    except Exception:
        print('Error Occurred:')
        print(e)

def main():
    forecast_location = get_location()
    forecast_data = request_forecast(forecast_location, api_key)
    # only call create_forecast if previous function calls were successful
    if forecast_data:
        create_forecast(forecast_data)

if __name__ == '__main__':
    main()
