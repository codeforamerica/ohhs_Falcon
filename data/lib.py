from dateutil import parser

from csv import DictReader
from urllib import urlopen
from StringIO import StringIO
from operator import itemgetter
from time import strftime

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
    req = urlopen(url)
    csv = DictReader(StringIO(req.read()))
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
    req = urlopen(url)
    csv = DictReader(StringIO(req.read()))
    inspections = dict()
    
    for row in csv:
        row.update(dict(inspection_date=yyyymmdd(row['inspection_date'])))
        inspections[row['inspection_id']] = strip_keys(row, 'inspection_')
    
    return inspections

def load_buildings(url):
    ''' Load buildings data dictionary from a given URL.
    
        Return dictionary is keyed on "building_id".
    '''
    req = urlopen(url)
    csv = DictReader(StringIO(req.read()))
    buildings = dict()
    
    for row in csv:
        del row['ID'] # useless spreadsheet row
        row.update(dict(building_latitude=float(row['building_latitude'])))
        row.update(dict(building_longitude=float(row['building_longitude'])))
        buildings[row['building_id']] = strip_keys(row, 'building_')
    
    return buildings

def match_inspection_violations(violations, inspections):
    ''' Add list of violations to each inspection in a dictionary.
    
        Modifies inspections dictionary in-place.
    '''
    for (violation_id, violation) in violations.items():
        if violation['inspection_id'] not in inspections:
            continue
    
        inspection = inspections[violation['inspection_id']]
    
        if 'violations' not in inspection:
            inspection['violations'] = []
        
        inspection['violations'].append(violation)
        inspection['violations'].sort(key=itemgetter('date'))

def match_building_inspections(inspections, buildings):
    ''' Add list of inspectionss to each building in a dictionary.
    
        Modifies buildings dictionary in-place.
    '''
    for (inspection_id, inspection) in inspections.items():
        if inspection['building_id'] not in buildings:
            continue
    
        building = buildings[inspection['building_id']]
    
        if 'inspections' not in building:
            building['inspections'] = []
        
        building['inspections'].append(inspection)
        building['inspections'].sort(key=itemgetter('date'))
