# Project Description
SFUExchange is a safe and collaborative community wherein SFU alumni and current students can ask meaningful questions and contribute answers to each other. The site is built with privacy and security first mindset. While other community solutions such as discord lack the proper organization and design for category based questions, SFUExchange offers a clean and intuitive experience to its users. The application is powered by Django, PostgreSQL, and nginx. Made with love in Vancouver ❤️.

# Run production
1. Run `docker-compose -f docker-compose.prod.yml up -d --build`
2. Navigate to `http://localhost:1337`
3. Login to a existing user to use the application (Or you can register a new account):
  Username: ggbaker
  Password: password
4. Once finished, run `docker-compose -f docker-compose.prod.yml down -v`

# Working Features
- Posting question with markdown, CSRF protection, 
  - Tagging question(s)
- Answer a question with markdown, CSRF protection, 
- Allow users to anonymize their question and answers
- Upvoting/downvotes questions and answers
  - Answers are ordered by votes
- Search bar using tags, users and questions as queries
- Profiles
  - User profile customization including changing images
- View other user profiles
- Login/Registration
- Authentication/Authorization
- Filtering by tags
- Sorting questions
- Mobile responsiveness
- Intelligent full text search using PostgreSQL
- Ranking search results by relevance

# Easily Missed Feature
- Notification (top-right) created for the author when an answer to the question is posted
- Notification created for new question by current user

# Missing Features
- Commenting on a answer
- Editing answers
- Deleting questions
- Moderation

# Run development (Not Necessary If Not Making Changes)

1. Run `docker-compose up -d --build`
2. Navigate to `http://localhost:8080`
3. Any credentials will work for the login page.
4. Once finished, run `docker-compose down -v`
5. Proceed to the database setup section.

# Database setup (Not Necessary If Not Making Changes)

1. Start up the docker containers from the [Run Development](#Run development) instructions
2. Create superuser account for admin page: `docker-compose exec web python manage.py createsuperuser`
3. OPTIONAL: To generate the dummy data run: `docker exec sfu-exchange-project_web_1 python manage.py seed_database`. Note: In order to play around with different users, every user has the password: `password`.
