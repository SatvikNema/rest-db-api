# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.

WEATHER_API_KEY = '349be02b64f54bbd9bb70758232302'

endpoint = f'http://api.weatherapi.com/v1/forecast.json?key={WEATHER_API_KEY}&q=London&days=1&aqi=no&alerts=no'

def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press ⌘F8 to toggle the breakpoint.


if __name__ == '__main__':
    print_hi('PyCharm')

