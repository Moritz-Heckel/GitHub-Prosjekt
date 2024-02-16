import json
import csv
import matplotlib.pyplot as plt
import numpy as np

import os
import pathlib
PATH = pathlib.Path(__file__).parent.resolve()
os.chdir(PATH)

countryToContinent = {}
continentYearData = {} 
totalAvgChangeOverTime = {}
countries = {}
globalFemaleLife = {}
globalMaleLife = {}

continentFiles = {
    "Africa": "../continent/Africa.txt",
    "Americas": "../continent/Americas.txt",
    "Asia": "../continent/Asia.txt",
    "Australia": "../continent/Australia.txt",
    "Europe": "../continent/Europe.txt"
}

def readFile(filename):
    with open(filename, "r") as file:
        countries = file.read().splitlines()
    return set(countries)

for continent, filepath in continentFiles.items():
    for country in readFile(filepath):
        countryToContinent[country] = continent

import csv

def prepareData(filename):
    global totalAvgChangeOverTime
    with open(filename, encoding="utf-8-sig") as theFile:
        filecontent = csv.reader(theFile, delimiter=",")
        next(filecontent)  
        for row in filecontent:
            country, year = row[1], int(row[3])
            if 1950 <= year <= 2018:
                femaleLifeExpectancy, maleLifeExpectancy = float(row[4]), float(row[5])
                avgLifeExpectancy = (femaleLifeExpectancy + maleLifeExpectancy) / 2

                if year in globalFemaleLife:
                    globalFemaleLife[year].append(femaleLifeExpectancy)
                else:
                    globalFemaleLife[year] = [femaleLifeExpectancy]

                if year in globalMaleLife:
                    globalMaleLife[year].append(maleLifeExpectancy)
                else:
                    globalMaleLife[year] = [maleLifeExpectancy]

                continent = countryToContinent.get(country, "Other")
                continentYearData.setdefault((continent, year), []).append(avgLifeExpectancy)

                countries.setdefault(country, [[], [], None])[0].append(femaleLifeExpectancy)
                countries[country][1].append(maleLifeExpectancy)

                totalAvgChangeOverTime.setdefault(country, [0, 0, None])

                if year == 1950:
                    totalAvgChangeOverTime[country][0] = avgLifeExpectancy
                if year == 2018:
                    totalAvgChangeOverTime[country][1] = avgLifeExpectancy
                    if len(countries[country][1]) > 65:
                        totalAvgChangeOverTime[country][2] = avgLifeExpectancy - totalAvgChangeOverTime[country][0]

            



def avgPerContinent():
    avgLifeExpectancyByContinent = {}
    for (continent, year), lifeExpentancies in continentYearData.items():
        avgLifeExpectancyByContinent[(continent, year)] = sum(lifeExpentancies) / len(lifeExpentancies)
    
    convertedData = {json.dumps(key): value for key, value in avgLifeExpectancyByContinent.items()}

    file_path = '../JSON/continentPerYear.json'

    with open(file_path, 'w') as json_file:
        json.dump(convertedData, json_file, indent=4)

    print(f"{file_path} saved")


    years = sorted(set(year for _, year in continentYearData.keys()))
    continents = sorted(set(continent for continent, _ in continentYearData.keys()))

    plt.figure(figsize=(10, 6))

    for continent in continents:
        avgLifeExpentancies = [avgLifeExpectancyByContinent.get((continent, year)) for year in years]
        plt.plot(years, avgLifeExpentancies, label=continent)

    #print(avgLifeExpectancyByContinent)

    plt.xlabel('Year')
    plt.ylabel('Average life expectancy')
    plt.title('Average life expectancy per continent over time')
    plt.legend()
    plt.show()


def graphCountryOverTime(country, avg=True):
    years = list(range(1950, 2019))  

    plt.figure(figsize=(10, 6))

    country = country.capitalize()

    if avg:
        avgLifeExpentancies = [(f + m) / 2 for f, m in zip(countries[country][0], countries[country][1])]
        plt.plot(years, avgLifeExpentancies, label=f'{country} Average life expectancy')
    else:
        plt.plot(years, countries[country][0], label=f"{country}'s Female life expectancy", color='pink')
        plt.plot(years, countries[country][1], label=f"{country}'s Male life expectancy", color='lightblue')

    plt.xlabel('Year')
    plt.ylabel('Life expectancy')
    plt.title(f'Life expectancy in {country} over time')
    plt.legend()
    plt.show()

def countryWithFastestChange():
    validCountries = {country: change for country, change in totalAvgChangeOverTime.items() if change[2] is not None}

    fastestChangeCountry = max(validCountries.items(), key=lambda x: x[1][2])
    smallestChangeCountry = min(validCountries.items(), key=lambda x: x[1][2])

    # Prepare data for plotting and saving
    avgLifeExpentancies = {}

    #print(fastestChangeCountry, smallestChangeCountry)

    plt.figure(figsize=(10, 6))

    countryFastest = fastestChangeCountry[0]
    yearsFastest = list(range(1950, 1950 + len(countries[countryFastest][0])))
    avgLifeExpentanciesFastest = [(countries[countryFastest][0][i] + countries[countryFastest][1][i]) / 2 for i in range(len(yearsFastest))]
    plt.plot(yearsFastest, avgLifeExpentanciesFastest, label=f'{countryFastest} (Fastest change)')

    countrySmallest = smallestChangeCountry[0]
    yearsSmallest = list(range(1950, 1950 + len(countries[countrySmallest][0])))
    avgLifeExpentanciesSmallest = [(countries[countrySmallest][0][i] + countries[countrySmallest][1][i]) / 2 for i in range(len(yearsSmallest))]
    plt.plot(yearsSmallest, avgLifeExpentanciesSmallest, label=f'{countrySmallest} (Smallest change)')

    #print(avgLifeExpentanciesFastest)
    #print(avgLifeExpentanciesSmallest)

    for country in [fastestChangeCountry[0], smallestChangeCountry[0]]:
        years = list(range(1950, 1950 + len(countries[country][0])))
        avgLifeExpentanciesCountry = [(countries[country][0][i] + countries[country][1][i]) / 2 for i in range(len(years))]
        avgLifeExpentancies[country] = avgLifeExpentanciesCountry
    
    file_path = '../JSON/change.json'
    with open(file_path, 'w') as json_file:
        json.dump(avgLifeExpentancies, json_file, indent=4)

    print(f"{file_path} saved")


    plt.xlabel('Year')
    plt.ylabel('Average life expectancy')
    plt.title('Countries with fastest and smallest change in life expectancy (1950-2018)')
    plt.legend()
    plt.show()

def maleFemale():
    years = sorted(globalFemaleLife.keys())
    avgFemaleLifeExpentancies = [
        sum(globalFemaleLife[year]) / len(globalFemaleLife[year]) 
        for year in years
    ]
    avgMaleLifeExpentancies = [
        sum(globalMaleLife[year]) / len(globalMaleLife[year]) 
        for year in years
    ]

    data = {
        year: [avgFemaleLifeExpentancies[i], avgMaleLifeExpentancies[i]] 
        for i, year in enumerate(years)
    }

    file_path = '../JSON/maleFemale.json'

    with open(file_path, 'w') as json_file:
        json.dump(data, json_file, indent=4)

    print(f"{file_path} saved")

    plt.figure(figsize=(10, 6))
    plt.plot(years, avgFemaleLifeExpentancies, label='Female average life expectancy', color='pink')
    plt.plot(years, avgMaleLifeExpentancies, label='Male average life expectancy', color='lightblue')
    
    plt.xlabel('Year')
    plt.ylabel('Life expectancy')
    plt.title('Global average life expectancy over time by gender')
    plt.legend()
    plt.show()




filename = "life_expectancy.csv"
prepareData(filename)
#avgPerContinent()
graphCountryOverTime('norway', avg=True)
#countryWithFastestChange()
#maleFemale()


file_path = '../JSON/country.json'


with open(file_path, 'w') as json_file:
    json.dump(countries, json_file, indent=4)

print(f"{file_path} saved")

#print(countries)

"""
countryToContinent = {}
continentYearData = {}
totalAvgChangeOverTime = {}
countries = {}
change = {}
"""

#print(continentYearData)