# Run development

1. Run `docker-compose up -d --build`
2. Run migrations `docker-compose exec web python manage.py migrate --noinput`
2. Navigate to `http://localhost:8080`
3. Once finished, run `docker-compose down -v`

# Run production

1. Run `docker-compose -f docker-compose.prod.yml up -d --build`
2. Run `docker-compose -f docker-compose.prod.yml exec web python manage.py migrate --noinput`
3. Run `docker-compose -f docker-compose.prod.yml exec web python manage.py collectstatic --no-input --clear`
4. Navigate to `http://localhost:1337`
4. Once finished, run `docker-compose -f docker-compose.prod.yml down -v`


# Create Superuser

1. Run `docker exec -it container_id python manage.py createsuperuser`
- Replace `container_id` with the id of the web container
