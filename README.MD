# Project Title

## Description

A brief description of your project goes here.

## Installation

Provide steps on how to install your project.

```
bash
git clone <your-repo-link>
cd <your-repo-directory>
npm install
Usage
Explain how to use your project.

Contributing
Details on how to contribute to your project.

License
Information about the license.

``` 

You can replace the placeholders with your project-specific information.

## NOTES

### REGISTERING

When submitting a form successfully SQLAlchemy logs the following interactions with the PostgreSQL database.

`BEGIN (implicit)`

1. SQLAlchemy is starting a new transaction. This is the start of a series of database operations that are treated as a single unit of work.

---

`INSERT INTO users (username, password, email, first_name, last_name) VALUES (%(username)s, %(password)s, %(email)s, %(first_name)s, %(last_name)s)`

2. SQLAlchemy is executing an SQL INSERT command to add a new record to the users table. The values for the new record are provided in the following dictionary.

---

`{'username': 'ahauser17', 'password': '$2b$12$p19qoNpipPDGZ6SjdVZUW.Z.2uXBV2kw5fkO22TTOGXB7K7rplSYe', 'email': 'arthur.hauser@gmail.com', 'first_name': 'Arthur', 'last_name': 'Hauser'}`

3. These are the values that are being inserted into the new record. The password appears to be hashed for security.

---

`COMMIT`

4. SQLAlchemy is committing the transaction. This makes all changes made during the transaction permanent.

---

`SELECT users.username AS users_username, users.password AS users_password, users.email AS users_email, users.first_name AS users_first_name, users.last_name AS users_last_name FROM users WHERE users.username = %(pk_1)s`

5. SQLAlchemy is executing an SQL SELECT command to retrieve the record for the user with the username 'ahauser17' from the users table.

---

6. This is the parameter being passed to the SELECT command.

`{'pk_1': 'ahauser17'}`

---

7. SQLAlchemy is rolling back the transaction. This undoes all changes made during the transaction. This is likely happening because the transaction is being managed by Flask's request handling code, which rolls back the transaction if no unhandled exceptions occurred during the request.

`ROLLBACK`

---

8. This is a log entry from Flask's development server. It shows that a POST request was made to the `/register` route and the server responded with a 302 status code, which indicates a redirect.

`127.0.0.1 - - [26/Apr/2024 16:38:28] "POST /register HTTP/1.1" 302 -`

---

9. The next few lines are similar to the previous ones, but this time SQLAlchemy is executing a SELECT command to retrieve feedback for the user 'ahauser17' from the `feedback` table.

```
2024-04-26 16:38:28,010 INFO sqlalchemy.engine.Engine BEGIN (implicit)
2024-04-26 16:38:28,010 INFO sqlalchemy.engine.Engine SELECT users.username AS users_username, users.password AS users_password, users.email AS users_email, users.first_name AS users_first_name, users.last_name AS users_last_name
FROM users
WHERE users.username = %(pk_1)s
2024-04-26 16:38:28,010 INFO sqlalchemy.engine.Engine [generated in 0.00013s] {'pk_1': 'ahauser17'}
2024-04-26 16:38:28,016 INFO sqlalchemy.engine.Engine SELECT feedback.id AS feedback_id, feedback.title AS feedback_title, feedback.content AS feedback_content, feedback.username AS feedback_username
FROM feedback
WHERE %(param_1)s = feedback.username
2024-04-26 16:38:28,016 INFO sqlalchemy.engine.Engine [generated in 0.00019s] {'param_1': 'ahauser17'}
2024-04-26 16:38:28,017 INFO sqlalchemy.engine.Engine ROLLBACK
```

---

`127.0.0.1 - - [26/Apr/2024 16:38:28] "GET /users/ahauser17 HTTP/1.1" 200 -`

10. This is another log entry from Flask's development server. It shows that a GET request was made to the `/users/ahauser17` route and the server responded with a 200 status code, which indicates success.

---

### ADD FEEDBACK

After registering and logging into the application the user is presented with the choice of adding feedback.  Clicking the `add feedback` button the user is brought to the url: `http://127.0.0.1:5000/users/ahauser17/feedback/new` and the console displays `127.0.0.1 - - [26/Apr/2024 16:51:46] "GET /users/ahauser17/feedback/new HTTP/1.1" 200 -`.

The screen displays two inputs: one for the title of the feedback and one for the content of the feedback.  I entered text and clicked the `Add!` button.  I successfully added the feedback to the database and received the following output from my console.

---

1. SQLAlchemy is starting a new transaction. This is the start of a series of database operations that are treated as a single unit of work.

`BEGIN (implicit)`

---

2. SQLAlchemy is executing an SQL INSERT command to add a new record to the `feedback` table. The values for the new record are provided in the following dictionary.

`INSERT INTO feedback (title, content, username) VALUES (%(title)s, %(content)s, %(username)s) RETURNING feedback.id`

---

3. These are the values that are being inserted into the new record.

`{'title': 'first note of many', 'content': 'this is my first note', 'username': 'ahauser17'}`

---

4. SQLAlchemy is committing the transaction. This makes all changes made during the transaction permanent.

`COMMIT`

---

5. SQLAlchemy is executing an SQL SELECT command to retrieve the record for the feedback with the id `1` from the `feedback` table.

`SELECT feedback.id AS feedback_id, feedback.title AS feedback_title, feedback.content AS feedback_content, feedback.username AS feedback_username FROM feedback WHERE feedback.id = %(pk_1)s`

---

6. This is the parameter being passed to the SELECT command.

`{'pk_1': 1}`

---

7. SQLAlchemy is rolling back the transaction. This undoes all changes made during the transaction. This is likely happening because the transaction is being managed by Flask's request handling code, which rolls back the transaction if no unhandled exceptions occurred during the request.

`ROLLBACK`

---

8.  This is a log entry from Flask's development server. It shows that a POST request was made to the `/users/ahauser17/feedback/new` route and the server responded with a 302 status code, which indicates a redirect.
    
`127.0.0.1 - - [26/Apr/2024 16:56:55] "POST /users/ahauser17/feedback/new HTTP/1.1" 302 -`

---

9. The next few lines are similar to the previous ones, but this time SQLAlchemy is executing a SELECT command to retrieve the user and feedback for the user 'ahauser17' from the `users` and `feedback` tables.

---

10. This is another log entry from Flask's development server. It shows that a GET request was made to the `/users/ahauser17` route and the server responded with a 200 status code, which indicates success.

`127.0.0.1 - - [26/Apr/2024 16:56:55] "GET /users/ahauser17 HTTP/1.1" 200 -`

### FLASK MIGRATION

# Flask-Migrate handles the creation and management of my database schema.

Now, I can use the command line to manage my database. 

1. First, I can initialize my migration repository with the terminal command: `flask db init`.  

2. Then, whenever I make changes to my models, I can generate a migration script with the command: `flask db migrate`. 

3. Finally, I can apply the changes to my database with: `flask db upgrade`.

As part of adding and committing migration scripts it's important to track these changes using Git.  My github workflow would follow the following protocol: 

   1. First, initialize a Git repository in your project directory, if you haven't already. You can do this with the command `git init`. This only needs to be done once per project.

   2. After you've created a migration script using `flask db migrate`, you can add it to Git with the command `git add migrations`. This tells Git that you want to include the latest changes in the `migrations` directory in your next commit.
   
   3. Then, you can create a commit with the command `git commit -m "Your message here"`. Replace `"Your message here"` with a short description of the changes you made. For example, if you just created a migration script for adding a new table, you might write `"Add migration for new table"`.
   
   4. If you're using a remote repository (like on GitHub), you can then push your changes to the remote repository with `git push`.

Here's a "cheat sheet" of the terminal commands cross referenced with the common phases of workflow:

```
git init  # Only needed once per project
git add migrations
git commit -m "Add migration for new table"
git push  # If using a remote repository
```