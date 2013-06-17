from requests import get
from csv import DictReader
from StringIO import StringIO

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
    
    minlat = min([b['building_latitude'] for b in buildings.values()])
    minlon = min([b['building_longitude'] for b in buildings.values()])
    maxlat = max([b['building_latitude'] for b in buildings.values()])
    maxlon = max([b['building_longitude'] for b in buildings.values()])
    
    print minlat, minlon, maxlat, maxlon

