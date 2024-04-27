# Project Title

## Description

A brief description of your project goes here.

## Installation

1. To run this application first make sure your virtual environment is activated. If it's not, activate it with the command `source venv/bin/activate` 

2. Then set the environment variable FLASK_APP to your application. For example, if your application is in a file named app.py, you would run `export FLASK_APP=app.py`.

3. Run the application with the Flask command `flask run`.

4. This will start a development web server, and Flask will give you the address where your application is running (usually `http://127.0.0.1:5000/`).


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

---

### JesseB notes:

For future reference, you will run into this a lot where their `requirements.txt` file has much older versions of things, meant for an older version of Python like 3.7 or 3.8. You will find that newer versions of Python often aren't compatible. In that case, when you get a new project, you can use `sed` to take out all of the `==1.0.2` from the requirements file, like this:

`sed -i 's/==[0-9]*\.[0-9]*\.[0-9]*//g' requirements2.txt`

So that is creating a new file called `requirements2.txt` and leaving the old one alone, and then you can run `pip install -r requirements2.txt`.  `Flask==1.0.2` becomes `Flask`.

---

### Flask-Migrate Notes

#### 1. Create the `migrations` directory by running the command `flask db init`.
#### 2. After running this command, you should see a message indicating that the `migrations` directory was created successfully. Then, you can run the `flask db migrate` command.  After running `flask db migrate`, remember to review the generated script in the `migrations/versions` directory.
#### 3. If everything looks correct, you can apply the migration with `flask db upgrade`. This will update your database schema to match the current state of your models.
#### 4. NB Below is sample console-output after running `flask db upgrade` with notes:

- `INFO [alembic.runtime.migration] Running upgrade -> d064aef74b2f, empty message:` 
  - This line indicates that Alembic is starting to apply the migration with the revision ID d064aef74b2f.

- `CREATE TABLE user_types (...):` 
  - This is the SQL command that was executed to create the user_types table.

- `ALTER TABLE users ADD COLUMN user_type_id INTEGER:` 
  - This is the SQL command that was executed to add the user_type_id column to the users table.

- `ALTER TABLE users ADD UNIQUE (username):` 
  - This is the SQL command that was executed to add a unique constraint to the username column of the users table.

- `ALTER TABLE users ADD FOREIGN KEY(user_type_id) REFERENCES user_types (id):` 
  - This is the SQL command that was executed to add a foreign key from users.user_type_id to user_types.id.

- `INSERT INTO alembic_version (version_num) VALUES ('d064aef74b2f') RETURNING alembic_version.version_num:` 
  - This is the SQL command that was executed to update the alembic_version table with the revision ID of the applied migration. This table is used by Alembic to keep track of which migrations have been applied.

- `COMMIT:` 
  - This is the SQL command that was executed to commit the changes to the database.  The fact that you're seeing COMMIT at the end, and no error messages, indicates that the migration was applied successfully. Your database schema should now match the current state of your SQLAlchemy models.

#### 5. The alembic_version table explained:

At the time of this note there are four tables listed in the `enotary_db` database (see below).  The table named `alembic_version` table is used by Alembic, the database migration tool used by Flask-Migrate.  This table keeps track of the current state of your database schema. It does this by storing the version number of the last migration script that was applied to your database.

Each time you run a migration with `flask db upgrade`, Alembic updates the `alembic_version` table with the version number of the migration script. This allows Alembic to know which migration scripts have been applied and which haven't, so it can correctly apply new migration scripts in the future.  You generally don't need to interact with this table directly. Alembic will manage it for you.

```
enotary_db=# \dt
            List of relations
 Schema |      Name       | Type  | Owner 
--------+-----------------+-------+-------
 public | alembic_version | table | haus  
 public | feedback        | table | haus  
 public | user_types      | table | haus  
 public | users           | table | haus  
(4 rows)
```