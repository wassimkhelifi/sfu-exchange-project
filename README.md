# Run development

1. Run `docker-compose up -d --build`
2. Navigate to `http://localhost:8080`
3. Once finished, run `docker-compose down -v`

# Run production

1. Run `docker-compose -f docker-compose.prod.yml up -d --build`
2. Navigate to `http://localhost:1337`
3. Once finished, run `docker-compose -f docker-compose.prod.yml down -v`


# Database setup 
1. Start up the docker containers from the [Run Development](#Run development) instructions 
2. Create superuser account for admin page: `docker-compose exec web python manage.py createsuperuser`
3. OPTIONAL: To generate the dummy data run: `docker exec sfu-exchange-project_web_1  python manage.py seed_database`. Note: In order to play around with different users, every user has the password: `password`. 