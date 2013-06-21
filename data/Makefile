venv-ohhs-map: venv-ohhs-map/bin/activate

venv-ohhs-map/bin/activate: requirements.txt
	test -d venv-ohhs-map || virtualenv --system-site-packages venv-ohhs-map
	. venv-ohhs-map/bin/activate; pip install -Ur requirements.txt
	touch venv-ohhs-map/bin/activate

Parcel.geojson: parcel.shp
	ogr2ogr -overwrite -skipfailures -t_srs EPSG:4326 -f GeoJSON -lco COORDINATE_PRECISION=7 -lco WRITE_BBOX=YES Parcel.geojson parcel.shp

parcel.shp:
	curl -OL "http://s3.amazonaws.com/data.codeforamerica.org/OHHS/Olathe-KS/parcel.{dbf,prj,shp,shx}"
