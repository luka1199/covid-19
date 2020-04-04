import requests
import csv


CONFIRMED = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv"
DEATHS = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv"
RECOVERED = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_recovered_global.csv"

def get_data(url):
    r = requests.get(url)
    csvfile = r.text
    
    reader = csv.reader(csvfile.splitlines(), delimiter=',', quotechar='"')
    result = {}
    next(reader)
    for row in reader:
        country = row[1]
        if country not in result:
            result[country] = 0
        if row[-1] == "":
            result[country] += 0
        else:
            result[country] += int(row[-1])
    return result
    
    
if __name__ == "__main__":
    confirmed_data = get_data(CONFIRMED)
    deaths_data = get_data(DEATHS)
    recovered_data = get_data(RECOVERED)
    
    mortality_rate = {}
    for country, deaths in deaths_data.items():
        if confirmed_data[country] == 0:
            mortality_rate[country] = 0
            continue
        mortality_rate[country] = deaths/confirmed_data[country]

    for country, confirmed in sorted(list(confirmed_data.items()), 
                                 key=lambda x: x[1], 
                                 reverse=True)[:10]:
        print("{}: {} confirmed, {} deaths, {} recovered, {}% mortality rate".format(
            country, 
            confirmed, 
            deaths_data[country], 
            recovered_data[country], 
            round(mortality_rate[country]*100,2)))
