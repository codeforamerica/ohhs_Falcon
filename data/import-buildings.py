#!/usr/bin/env python
from json import load, dump
from os import makedirs

from lib import load_violations, load_inspections, load_buildings
from lib import match_inspection_violations, match_building_inspections

def load_parcels(path):
    '''
    '''
    parcels = list()
    
    with open(path) as file:
        features = load(file).get('features')
        
        for feature in features:
            parcels.append(feature)
    
    return parcels

def match_building_parcel(parcels, buildings):
    ''' Add a parcel to each building in a dictionary.
    
        Modifies buildings dictionary in-place.
    '''
    matches, misses = 0, 0
    
    for parcel in parcels:
        if parcel['properties']['MAPBLKLOT'] in buildings:
            building_id = parcel['properties']['MAPBLKLOT']
        
        elif parcel['properties']['BLKLOT'] in buildings:
            building_id = parcel['properties']['BLKLOT']
        
        else:
            misses += 1
            continue
        
        del parcel['properties']['SHAPE__Are']
        del parcel['properties']['SHAPE__Len']
        del parcel['properties']['Shape_Leng']

        matches += 1
        buildings[building_id]['parcel'] = parcel
    
    print len(buildings), 'buildings'
    print len(parcels), 'parcels'
    print matches, 'matches and', misses, 'misses'

if __name__ == '__main__':

    print 'Getting parcels...'

    parcels_url = 'Parcel.geojson'
    parcels = load_parcels(parcels_url)
    
    print 'Getting violations...'

    violations_url = 'file:///Users/migurski/Sites/OHHS-Map/data/Violations.csv'
    violations = load_violations(violations_url)

    print 'Getting inspections...'

    inspections_url = 'file:///Users/migurski/Sites/OHHS-Map/data/Inspections.csv'
    inspections = load_inspections(inspections_url)

    print 'Getting buildings...'

    buildings_url = 'file:///Users/migurski/Sites/OHHS-Map/data/Buildings.csv'
    buildings = load_buildings(buildings_url)
    
    print 'Matching inspection violations...'
    
    match_inspection_violations(violations, inspections)
    
    print 'Matching building inspections...'
    
    match_building_inspections(inspections, buildings)
    
    print 'Matching building parcels...'
    
    match_building_parcel(parcels, buildings)
    
    print 'Writing', len(buildings), 'buildings...'
    
    try:
        makedirs('buildings')
    except OSError:
        pass # directory probably exists
    
    for (building_id, building) in buildings.items():
        with open('buildings/%(building_id)s.json' % locals(), 'w') as out:
            dump(building, out, indent=2)
