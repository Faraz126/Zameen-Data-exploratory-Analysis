import pandas as pd
import numpy as np

def pre_poccess(dataset):
    
    ##adding indivdual where agency is not given
    dataset['agency'][dataset['agency'].isnull()] = 'Individual'
    
    
    #using the conversion of urban https://www.zameen.com/forum/discussions/other_and_misc/kanal__marla__square_feet__square_yards_conversion-12358.html
    converted_area = []
    for area in dataset['area']:
        if area.endswith('Marla'):
            #print("MARLA", str(area))
            converted_area.append(float(area.split()[0].replace(',', '')) * 500)
        if area.endswith('Kanal'):
            #print("Kanal", str(area))
            converted_area.append(float(area.split()[0].replace(',', '')) * 25)
            
    #print(converted_area)
    dataset['area'] = converted_area

    #creating unique location column
    dataset['unique_location'] = dataset['location'] + ' ' + dataset['city']

    # dividing price by area to get price per unit area
    dataset['price_per_area'] = dataset['price'] / dataset['area']

    # filtering out empty plots / commercial properties
    dataset = dataset[dataset['bedrooms'] != 0]

    # removing values outside of 95% interval
    dataset['price_z_score'] = 0

    # for sales
    arr = np.array(dataset['price_per_area'][dataset['purpose'] == 'For Sale'])
    z_score = (dataset['price_per_area'][dataset['purpose'] == 'For Sale'] - np.mean(arr[np.isfinite(arr)])) / np.std(
        arr[np.isfinite(arr)])
    dataset['price_z_score'][dataset['purpose'] == 'For Sale'] = z_score

    # for rent
    arr = np.array(dataset['price_per_area'][dataset['purpose'] == 'For Rent'])
    z_score = (dataset['price_per_area'][dataset['purpose'] == 'For Rent'] - np.mean(arr[np.isfinite(arr)])) / np.std(
        arr[np.isfinite(arr)])
    dataset['price_z_score'][dataset['purpose'] == 'For Rent'] = z_score
    dataset = dataset.drop(dataset[(dataset['price_z_score'] > 3) | (dataset['price_z_score'] < -3)].index)

    dataset = dataset.drop(columns = ['page_url', 'property_id', 'location_id'])

    print("pre-poccessed successfully.")
    
    return dataset
    