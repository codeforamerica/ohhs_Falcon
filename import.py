from requests import get
from dateutil import parser

from csv import DictReader
from StringIO import StringIO
from itertools import product
from operator import itemgetter
from time import strftime
from os import makedirs
from json import dump

from ModestMaps.Geo import Location
from ModestMaps.Core import Coordinate
from ModestMaps.OpenStreetMap import Provider

min_zoom = 14
max_zoom = 17

def yyyymmdd(date_string):
    ''' Normalize a date string format to YYYY-MM-DD.
    '''
    return strftime('%Y-%m-%d', parser.parse(date_string).timetuple())

def strip_keys(data, prefix):
    ''' Return a new dictionary with all keys stripped of the given prefix.
    '''
    return dict([(key[len(prefix):] if key.startswith(prefix) else key, value)
                 for (key, value) in data.items()])

def load_violations(url):
    ''' Load violations data dictionary from a given URL.
    
        Return dictionary is keyed on "violation_id".
    '''
    req = get(url)
    csv = DictReader(StringIO(req.text))
    violations = dict()
    
    for row in csv:
        row.update(dict(violation_date=yyyymmdd(row['violation_date'])))
        row.update(dict(violation_date_closed=yyyymmdd(row['violation_date_closed'])))
        violations[row['violation_id']] = strip_keys(row, 'violation_')
    
    return violations

def load_inspections(url):
    ''' Load inspections data dictionary from a given URL.
    
        Return dictionary is keyed on "inspection_id".
    '''
    req = get(url)
    csv = DictReader(StringIO(req.text))
    inspections = dict()
    
    for row in csv:
        row.update(dict(inspection_date=yyyymmdd(row['inspection_date'])))
        inspections[row['inspection_id']] = strip_keys(row, 'inspection_')
    
    return inspections

def load_buildings(url):
    ''' Load buildings data dictionary from a given URL.
    
        Return dictionary is keyed on "building_id".
    '''
    req = get(url)
    csv = DictReader(StringIO(req.text))
    buildings = dict()
    
    for row in csv:
        row.update(dict(building_latitude=float(row['building_latitude'])))
        row.update(dict(building_longitude=float(row['building_longitude'])))
        buildings[row['building_id']] = strip_keys(row, 'building_')
    
    return buildings

def starting_tiles(buildings):
    ''' Get tile coordinates at min_zoom for a list of buildings.
    '''
    minlat = min([b['latitude'] for b in buildings])
    minlon = min([b['longitude'] for b in buildings])
    maxlat = max([b['latitude'] for b in buildings])
    maxlon = max([b['longitude'] for b in buildings])
    
    osm = Provider()
    
    ul = osm.locationCoordinate(Location(maxlat, minlon)).zoomTo(min_zoom).container()
    lr = osm.locationCoordinate(Location(minlat, maxlon)).zoomTo(min_zoom).container()
    
    rows, cols = range(int(ul.row), int(lr.row+1)), range(int(ul.column), int(lr.column+1))
    coords = [Coordinate(row, col, min_zoom) for (row, col) in product(rows, cols)]
    
    return coords

def search_tile(coord, buildings):
    ''' Search list of buildings for those within a tile coordinate.
    '''
    osm = Provider()
    
    sw = osm.coordinateLocation(coord.down())
    ne = osm.coordinateLocation(coord.right())
    
    found_buildings = [b for b in buildings
                       if sw.lon <= b['longitude'] < ne.lon
                       and sw.lat <= b['latitude'] < ne.lat]
    
    return found_buildings

if __name__ == '__main__':

    print 'Getting violations...'

    violations_url = 'http://s3.amazonaws.com/data.codeforamerica.org/OHHS/SF/1.2/Violations.csv'
    violations = load_violations(violations_url)

    print 'Getting inspections...'

    inspections_url = 'http://s3.amazonaws.com/data.codeforamerica.org/OHHS/SF/1.2/Inspections.csv'
    inspections = load_inspections(inspections_url)

    print 'Getting buildings...'

    buildings_url = 'http://s3.amazonaws.com/data.codeforamerica.org/OHHS/SF/1.2/Buildings.csv'
    buildings = load_buildings(buildings_url)
    
    print 'Matching inspection violations...'
    
    for (violation_id, violation) in violations.items():
        if violation['inspection_id'] not in inspections:
            continue
    
        inspection = inspections[violation['inspection_id']]
    
        if 'violations' not in inspection:
            inspection['violations'] = []
        
        inspection['violations'].append(violation)
        inspection['violations'].sort(key=itemgetter('date'))
    
    print 'Matching building inspections...'
    
    for (inspection_id, inspection) in inspections.items():
        if inspection['building_id'] not in buildings:
            continue
    
        building = buildings[inspection['building_id']]
    
        if 'inspections' not in building:
            building['inspections'] = []
        
        building['inspections'].append(inspection)
        building['inspections'].sort(key=itemgetter('date'))
    
    building_list = buildings.values()
    search_coords = [(coord, building_list) for coord in starting_tiles(building_list)]
    
    while search_coords:
        coord, building_list = search_coords.pop(0)
        found_buildings = search_tile(coord, building_list)
        
        print ('%(zoom)d/%(column)d/%(row)d' % coord.__dict__),
        print len(found_buildings), 'of', len(building_list)
        
        try:
            makedirs('tiles/%(zoom)d/%(column)d' % coord.__dict__)
        except OSError:
            pass # directory probably exists
        
        with open('tiles/%(zoom)d/%(column)d/%(row)d.json' % coord.__dict__, 'w') as out:
            features = [dict(
                            type='Feature',
                            properties=p,
                            geometry=dict(
                                type='Point',
                                coordinates=(p['longitude'], p['latitude'])
                                )
                            )
                        for p in found_buildings]
        
            geojson = dict(
                type='FeatureCollection',
                features=features
                )
        
            dump(geojson, out, indent=2)
        
        if coord.zoom < max_zoom:
            search_coords.append((coord.zoomBy(1), found_buildings))
            search_coords.append((coord.zoomBy(1).down(), found_buildings))
            search_coords.append((coord.zoomBy(1).right(), found_buildings))
            search_coords.append((coord.zoomBy(1).right().down(), found_buildings))
