venv-ohhs-map: venv-ohhs-map/bin/activate

venv-ohhs-map/bin/activate: requirements.txt
	test -d venv-ohhs-map || virtualenv --system-site-packages venv-ohhs-map
	. venv-ohhs-map/bin/activate; pip install -Ur requirements.txt
	touch venv-ohhs-map/bin/activate

Parcel.geojson:
	curl -OL "http://data.codeforamerica.org/OHHS/SF/1.2/Parcel.{dbf,prj,shp,shx}"
	ogr2ogr -t_srs EPSG:4326 -f GeoJSON Parcel.geojson Parcel.shp
	rm Parcel.dbf Parcel.prj Parcel.shp Parcel.shx
