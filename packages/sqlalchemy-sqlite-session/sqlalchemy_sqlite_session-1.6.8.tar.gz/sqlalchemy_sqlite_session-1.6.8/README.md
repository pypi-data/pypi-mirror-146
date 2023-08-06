# Sqlalchemy Sqlite Session

This is tools to get session and engine for Sqlalchemy Sqlite. 


### install package
``` 
pip install sqlalchemy-sqlite-session -i https://pypi.org/simple


### update package
``` 
pip install -U sqlalchemy-sqlite-session -i https://pypi.org/simple
```

### example
```
from sqlalchemy_sqlite_session.adapters import get_sqlite_session

session = get_sqlite_session('C:\sqlite_path.db')

engine = get_sqlite_engine('C:\sqlite_path.db')

```

### Packaging project
```
py -m pip install twine
py -m pip install build

py -m build --sdist
```

### Uploading Project to PyPI
```
twine check dist/*
twine upload dist/*
```