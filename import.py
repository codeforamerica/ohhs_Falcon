from requests import get
from csv import DictReader
from StringIO import StringIO
from itertools import product
from ModestMaps.Geo import Location
from ModestMaps.Core import Coordinate
from ModestMaps.OpenStreetMap import Provider

def load_violations(url):
    '''
    '''
    req = get(url)
    csv = DictReader(StringIO(req.text))
    return dict([(row['violation_id'], row) for row in csv])

def load_inspections(url):
    '''
    '''
    req = get(url)
    csv = DictReader(StringIO(req.text))
    return dict([(row['inspection_id'], row) for row in csv])

def load_buildings(url):
    '''
    '''
    req = get(url)
    csv = DictReader(StringIO(req.text))
    buildings = dict()
    
    for row in csv:
        row.update(dict(building_latitude=float(row['building_latitude'])))
        row.update(dict(building_longitude=float(row['building_longitude'])))
        buildings[row['building_id']] = row
    
    return buildings

def starting_tiles(buildings):
    ''' Gets tile coordinates for a dictionary of buildings.
    '''
    minlat = min([b['building_latitude'] for b in buildings.values()])
    minlon = min([b['building_longitude'] for b in buildings.values()])
    maxlat = max([b['building_latitude'] for b in buildings.values()])
    maxlon = max([b['building_longitude'] for b in buildings.values()])
    
    osm = Provider()
    
    ul = osm.locationCoordinate(Location(maxlat, minlon)).zoomTo(14).container()
    lr = osm.locationCoordinate(Location(minlat, maxlon)).zoomTo(14).container()
    
    rows, cols = range(int(ul.row), int(lr.row+1)), range(int(ul.column), int(lr.column+1))
    coords = [Coordinate(row, col, 14) for (row, col) in product(rows, cols)]
    
    return coords

if __name__ == '__main__':

    print 'Getting violations...'
    violations_url = 'http://localhost/~migurski/OHHS-Map/Violations.csv'
    violations = load_violations(violations_url)

    print 'Getting inspections...'
    inspections_url = 'http://localhost/~migurski/OHHS-Map/Inspections.csv'
    inspections = load_inspections(inspections_url)

    print 'Getting buildings...'
    buildings_url = 'http://localhost/~migurski/OHHS-Map/Buildings.csv'
    buildings = load_buildings(buildings_url)
    
    starting_tiles(buildings)
