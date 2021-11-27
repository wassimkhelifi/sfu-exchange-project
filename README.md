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
3. OPTIONAL: To generate the dummy data run: `docker exec sfu-exchange-project_web_1 python manage.py seed_database`. Note: In order to play around with different users, every user has the password: `password`.

# Project Checkpoint Notes

- In its simplest form, the project is a Stackoverflow-like application specifically for SFU students from different faculties

- It is currently compatible with production-style deployment with a Postgres database

- The application can be prepulated with [dummy data](#Database setup) while endpoints are being developed

- For further reference on the schema, please view the 'database-schema.png' file.

- A number of basic routes are set up in html/css with Boostrap enhancements to come later:

  - http://localhost:8080/ (Login)
  - http://localhost:8080/exchange/profile/
  - http://localhost:8080/exchange/questions/
  - http://localhost:8080/exchange/register
  - http://localhost:8080/admin (need to create a super user to update users, questions, answers etc)

- The profile, questions list and individual question pages based on our Figma designs:

  ![Profile](https://bit.ly/3remUI4)

  ![Question list](https://bit.ly/3rcHQ2g)

  ![Individual question](https://bit.ly/3nVRLHt)
