# -*- coding: utf-8 -*-
"""
Created on Sun Aug 30 07:21:48 2020

@author: Valhala
"""
pip install Selenium
#%% Library import
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException
from selenium import webdriver
import selenium
import time
import pandas as pd

#%% Webdriver setup
options = webdriver.FirefoxOptions()
options.set_headless(True)
driver = webdriver.Firefox(options = options)
#%% Scrapping
rentals = []
for p in range(11):
    url = "https://www.spacelist.ca/listings/on/toronto/retail/for-lease/page/" + str(p)
    driver.get(url)
    listings = driver.find_elements_by_class_name('meta-card')
    for i in range(len(listings)):
        area = listings[i].find_elements_by_class_name('dark-font')[0].text
        rent = listings[i].find_elements_by_class_name('dark-font')[1].text
        address = listings[i].find_elements_by_class_name('dark-font')[2].text
        rentals.append({'Address': address, 'Area': area, 'Rent': rent})

rent_df = pd.DataFrame(rentals)
driver.close()
#%% See what was scrapped
rent_df.head()
rent_df.to_csv('rent_df_1.csv', index = False)

#%% Geocoding the Dataframe
rent_df = pd.read_csv('rent_df_1.csv')
rent_df = rent_df[rent_df.Rent != 'Contact']
rent_df.drop_duplicates(subset = ['Address'], inplace = True)
rent_df.Address.value_counts()
rent_df.Address = rent_df.Address.str.replace('For Rent - ', '')
rent_df.Address = rent_df.Address.str.replace('ground - ', '')
rent_df.reset_index(inplace = True, drop = True)
rent_df.Address = rent_df.Address.astype(str) + ', Toronto ON'
rent_df.to_csv('rent_df_2.csv', index = False)
#%%
rent_df = pd.read_csv('rent_df_2.csv')
#%% Install geocoder
pip install geopy
#%% Geocoding
from geopy.geocoders import Nominatim
geolocator = Nominatim(user_agent='Rental_venues_locations')
from geopy.extra.rate_limiter import RateLimiter
geocode = RateLimiter(geolocator.geocode, min_delay_seconds=1)
rent_df['location'] = rent_df['Address'].apply(geocode)
rent_df.to_csv('rent_df_3.csv', index = False)
#%% Cleaning up address, if there were any empty values on the geocoding.
rent_df = pd.read_csv('rent_df_3.csv')

for place in range(len(rent_df.Address)):
    if pd.isna(rent_df.location[place]):
        rent_df.Address[place] = rent_df.Address[place].split(' - ')[1]

rent_df['location'] = rent_df['Address'].apply(geocode)

rent_df['Latitude'] = rent_df['location'].apply(lambda loc: loc.latitude if loc else None)
rent_df['Longitude'] = rent_df['location'].apply(lambda loc: loc.longitude if loc else None)

rent_merged = rent_df.drop('location', axis = 1)
rent_merged.to_csv('toronto_rental.csv', index = False)
#%% Typecasting and further clening
rent_merged = pd.read_csv('toronto_rental.csv')
rent_merged.Rent = rent_merged.Rent.apply(lambda x: x.split('$')[1])
rent_merged.Rent = rent_merged.Rent.apply(lambda x: x.replace(',', ''))
rent_merged.Rent = rent_merged.Rent.apply(lambda x: x.replace('/mo', ''))
rent_merged[['Rent_min', 'Rent_max']] = rent_merged['Rent'].str.split('-', expand = True)

#Typecasting the various rent columns
rent_merged[['Rent_min', 'Rent_max']] = rent_merged[['Rent_min', 'Rent_max']].astype(float)

for place in range(len(rent_merged.Address)):
    if pd.isna(rent_merged.Rent_max[place]):
        rent_merged.Rent[place] = rent_merged.Rent_min[place]
    else:
        rent_merged.Rent[place] = (rent_merged.Rent_min[place] + rent_merged.Rent_max[place])/2
        
rent_merged['Rent'] = rent_merged['Rent'].astype(float)
rent_merged.to_csv('toronto_rental.csv', index = False)
#%% More cleaning
rent_merged.drop(['Rent_min', 'Rent_max'], axis = 1, inplace = True)
#%% Even more cleaning
rent_merged['Area']= rent_merged['Area'].str.replace(' ft²', '')
rent_merged['Area']= rent_merged['Area'].str.replace(',', '')
#%%
rent_merged[['Area_min', 'Area_max']] = rent_merged['Area'].str.split('-', expand = True)
rent_merged[['Area_min', 'Area_max']] = rent_merged[['Area_min', 'Area_max']].astype(float)

for place in range(len(rent_merged.Address)):
    if pd.isna(rent_merged.Area_max[place]):
        rent_merged.Area[place] = rent_merged.Area_min[place]
    else:
        rent_merged.Area[place] = (rent_merged.Area_min[place] + rent_merged.Area_max[place])/2
        
rent_merged['Area'] = rent_merged['Area'].astype(float)
rent_merged.drop(['Area_min', 'Area_max'], axis = 1, inplace = True)

#%%Shapely
conda install -c conda-forge shapely

#%% Time to add the neighbourhood according the coordiantes using toronto's Geojson
import json
from shapely.geometry import shape, Point
# depending on your version, use: from shapely.geometry import shape, Point

# load GeoJSON file containing sectors
with open('Toronto_Neighbourhoods.geojson') as f:
    js = json.load(f)
rent_merged['Neighbourhood Number'] = 0
temp = []
# construct point based on lon/lat returned by geocoder
for i in range(len(rent_merged.Address)):
    point = Point(rent_merged.Longitude[i], rent_merged.Latitude[i])
    
    # check each polygon to see if it contains the point
    for feature in js['features']:
        polygon = shape(feature['geometry'])
        if polygon.contains(point):
            rent_merged['Neighbourhood Number'][i] = feature['properties']['AREA_SHORT_CODE']

rent_merged.to_csv('toronto_rental.csv', index = False)

        


