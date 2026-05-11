from sqlalchemy import create_engine, text


engine = create_engine("sqlite:///./data/movies.db", pool_pre_ping=True)


# Create the movies table if it does not exist
with engine.connect() as connection:
    connection.execute(text("""
                            CREATE TABLE IF NOT EXISTS users
                            (id INTEGER PRIMARY KEY AUTOINCREMENT,
                             name TEXT UNIQUE NOT NULL,
                            password TEXT NOT NULL)
                            """))

    connection.execute(text("""
                            CREATE TABLE IF NOT EXISTS movies
                            (id INTEGER PRIMARY KEY AUTOINCREMENT,
                            title TEXT UNIQUE NOT NULL,
                            year INTEGER NOT NULL,
                            rating REAL NOT NULL,
                            poster TEXT NOT NULL)
                            """))

    connection.execute(text("""
                            CREATE TABLE IF NOT EXISTS user_movies
                            (user_id INTEGER NOT NULL,
                            movie_id INTEGER NOT NULL,
                            note TEXT,
                            PRIMARY KEY (user_id, movie_id),
                            FOREIGN KEY (user_id) REFERENCES users(id),
                            FOREIGN KEY (movie_id) REFERENCES movies(id))"""))


    connection.commit()


def list_users():
    """Retrieve all users from the database."""
    with engine.connect() as connection:
        result = connection.execute(
            text("SELECT id, name, password FROM users"))
        users = result.fetchall()

    return {row[0]: {"name": row[1], "password": row[2]} for row in users}


def get_user_name(user_id):
    """Retrieve all users from the database."""
    with engine.connect() as connection:
        params = {"user_id": user_id}
        result = connection.execute(
            text("SELECT id, name FROM users WHERE id = :user_id"), params)
        users = result.fetchall()

    return {row[0]: {"name": row[1]} for row in users}


def add_users(user_name, password):
    """Add a new user to the database"""
    with engine.connect() as connection:
        try:
            params = {"user_name": user_name, "password": password}
            result = connection.execute(text("INSERT INTO users (name, password) "
                                    "VALUES (:user_name, :password)"),
                               params)

            connection.commit()
            return result.lastrowid

        except Exception as e:
            print(f"Error: {e}")


def list_all_movies():
    with engine.connect() as connection:
        result = connection.execute(
            text("""SELECT * FROM movies"""))
        movies = result.fetchall()

    return {row[0]: {"title": row[1], "year": row[2], "rating": row[3],
                     "poster": row[4]} for row in movies}

def list_movies(user_id):
    """Retrieve all movies from the database."""
    with engine.connect() as connection:
        params = {
            "id": user_id
        }
        result = connection.execute(
            text("""SELECT 
                        movies.id, 
                        movies.title, 
                        movies.year, 
                        movies.rating, 
                        movies.poster,
                        user_movies.note
                    FROM users 
                    JOIN user_movies ON user_movies.user_id = users.id
                    JOIN movies ON user_movies.movie_id = movies.id
                    WHERE users.id = :id"""), params)
        movies = result.fetchall()

    return {row[0]: {"title": row[1], "year": row[2], "rating": row[3],
                     "poster": row[4], "note": row[5]} for row in movies}


def add_movie(title, year, rating, poster, user_id):
    """Add a new movie to the database."""
    with engine.connect() as connection:
        try:
            params = {"title": title, "year": year, "rating": rating,
                      "poster": poster, "user_id": user_id}
            result = connection.execute(
                text("INSERT INTO movies (title, year, rating, poster) "
                     "VALUES (:title, :year, :rating, :poster)"),
                params)
            params["movie_id"] = result.lastrowid
            connection.execute(
                text("INSERT INTO user_movies (user_id, movie_id) "
                     "VALUES (:user_id, :movie_id)"),
                params)
            connection.commit()
        except Exception as e:
            print(f"Error: {e}")

def add_existing_movie_user(movie_id, user_id):
    with engine.connect() as connection:
        try:
            params = {"movie_id": movie_id, "user_id": user_id}
            connection.execute(
                text("INSERT INTO user_movies (user_id, movie_id) "
                     "VALUES (:user_id, :movie_id)"), params)
            connection.commit()
        except Exception as e:
            print(f"Error: {e}")


def delete_movie(title, user_id):
    """Delete a movie from the database."""
    with engine.connect() as connection:
        try:
            params = {'title': title, 'user_id': user_id}
            connection.execute(text(
                 """DELETE FROM user_movies
                    WHERE movie_id IN (
                        SELECT id
                        FROM movies
                        WHERE title = :title
                    )
                        AND user_id = :user_id"""
            ), params)
            connection.commit()
        except Exception as e:
            print(f"Error: {e}")


def update_movie(title, note, user_id):
    """Update a movie's rating in the database."""
    with engine.connect() as connection:
        try:
            params = {"note": note, "title": title, "user_id": user_id}
            connection.execute(text("""
                UPDATE user_movies
                SET note = :note
                WHERE user_id = :user_id
                  AND movie_id = (
                      SELECT id FROM movies WHERE title = :title
                  )
            """),
                params)
            connection.commit()
        except Exception as e:
            print(f"Error: {e}")
