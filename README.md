# Dramatis Personae

## Database setup
Set up a blank database (with reference data):
```bash
(dp_dir) $ scripts/db_load_initial.sh
```
...or reload the one previously dumped:
```bash
(dp_dir) $ scripts/db_load_custom.sh
```

Create a superuser to access the admin section:
```
(dp_dir) $ python3 manage.py createsuperuser
```

## Backup custom database
```bash
(dp_dir) $ scripts/db_dump.sh
```


## Run tests
```bash
(dp_dir) $ scripts/test.sh
```
