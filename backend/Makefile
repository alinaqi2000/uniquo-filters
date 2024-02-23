watch:
	watchman watch .
	watchman -- trigger . reload_on_py_changes '**/*.py' -- echo 1 > uwsgi-reloads
stop:
	watchman watch-del-all