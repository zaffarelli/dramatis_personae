# Dramatis Personae

## Fresh database setup

Rename / replace `db.sqlite3.orig` to `db.sqlite3`.

If you don't want the default data, you can do:

```bash
(dp_dir) $ python3 manage.py flush
(dp_dir) $ .initdb.sh

```

## Access Admin interface

Create an admin superuser
```
(dp_dir) $ python3 manage.py createsuperuser

```
