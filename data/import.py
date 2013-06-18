from itertools import product
from os import makedirs
from json import dump

from ModestMaps.Geo import Location
from ModestMaps.Core import Coordinate
from ModestMaps.OpenStreetMap import Provider

from lib import load_violations, load_inspections, load_buildings
from lib import match_inspection_violations, match_building_inspections

min_zoom = 14
max_zoom = 17

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
    
    match_inspection_violations(violations, inspections)
    
    print 'Matching building inspections...'
    
    match_building_inspections(inspections, buildings)
    
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
