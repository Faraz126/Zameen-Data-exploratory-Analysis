import pandas as pd

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
    
    dataset = dataset.drop(columns = ['page_url'])

    print("pre-poccessed successfully.")
    
    return dataset
    
