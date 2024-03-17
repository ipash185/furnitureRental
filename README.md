# furnitureRental
Furniture Rental System

> # create .env file with
>  > Database config </br>
>  > SECRET_KEY

 
# Make migration
```console
python manage,py makemigrations
```

# Migrate
```console
python manage,py migrate
```

# Create admin account
```console
python manage.py createsuperuser 
```
provide information
```consloe
Usename:
Email address:
Password:
Password( again ):
Bypass password validation and create user anyway? [y/N]: 
Superuser created successfully.

```

# Run app
```console
 python manage.py runserver 
```
> Visit -> http://127.0.0.1:8000/
