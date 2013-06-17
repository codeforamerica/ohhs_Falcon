venv-ohhs-map: venv-ohhs-map/bin/activate

venv-ohhs-map/bin/activate: requirements.txt
	test -d venv-ohhs-map || virtualenv --system-site-packages venv-ohhs-map
	. venv-ohhs-map/bin/activate; pip install -Ur requirements.txt
	touch venv-ohhs-map/bin/activate
