venv-ohhs-map: venv-ohhs-map/bin/activate

venv-ohhs-map/bin/activate: requirements.txt
	test -d venv-ohhs-map || virtualenv --system-site-packages venv-ohhs-map
	. venv-ohhs-map/bin/activate; pip install -Ur requirements.txt
	touch venv-ohhs-map/bin/activate

Parcel.geojson: Parcel.shp
	ogr2ogr -t_srs EPSG:4326 -f GeoJSON -lco COORDINATE_PRECISION=7 -lco WRITE_BBOX=YES Parcel.geojson Parcel.shp

Parcel.shp:
	curl --compress -OL "http://data.codeforamerica.org/OHHS/SF/1.2/Parcel.{dbf,prj,shp,shx}"
