
## To run application on production


```bash
docker-compose -f docker-compose-deploy.yml build
docker-compose -f docker-compose-deploy.yml up
```
## Create super user by running below command 

```bash
docker-compose -f docker-compose-deploy.yml run --rm app sh -c "python manage.py createsuperuser"
```
It will ask you to enter login, email and password. 

Docker images: Nginx, Django(app), PostgreSQL