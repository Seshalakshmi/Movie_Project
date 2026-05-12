``` markdown
# Movie Database App

A command-line movie database application built with Python. It lets users manage personal movie collections, fetch movie details from the OMDb API, store data in SQLite, view collection statistics, and generate a static HTML movie website.

## Features

- Select an existing user or create a new user
- Add movies by title using OMDb API data
- Store movie information in a SQLite database
- List saved movies
- Delete movies from a user's collection
- Add or update movie notes
- Search movies by title with fuzzy matching suggestions
- View movie statistics:
  - Average rating
  - Median rating
  - Best-rated movies
  - Worst-rated movies
- Display a random movie
- Sort movies by rating
- Sort movies by year
- Filter movies by:
  - Minimum rating
  - Start year
  - End year
- Generate a static HTML website with movie posters

## Tech Stack

- Python 3
- SQLite
- SQLAlchemy
- Requests
- python-dotenv
- thefuzz / RapidFuzz
- HTML/CSS for static website generation
- OMDb API

## Project Structure
```

text Movie_Project/ ├── _static/ │ ├── index.html │ ├── index_template.html │ └── style.css ├── data/ │ └── movies.db ├── movie_storage/ │ ├── init.py │ ├── movie_storage_API.py │ └── movie_storage_sql.py ├── .env ├── .gitignore ├── main.py ├── README.md └── requirements.txt``` 

## Requirements

Install the required Python packages:
```

bash pip install -r requirements.txt``` 

The project uses the OMDb API. You can request an API key here:
```

text https://www.omdbapi.com/apikey.aspx``` 

Create a `.env` file in the `Movie_Project` directory and add your API key:
```

text API_KEY=your_api_key_here``` 

> Note: The `.env` file contains sensitive information and should not be committed to Git.

## Database

The application uses SQLite as its database.

By default, the database is stored at:
```

text data/movies.db``` 

The database tables are created and managed by the SQL storage module.

## Run the Application

From inside the `Movie_Project` directory, run:
```

bash python main.py``` 

You will first see a list of existing users and an option to create a new user.

After selecting or creating a user, the main menu appears:
```

text Menu:
Exit
List Movies
Add Movie
Delete Movie
Update Movie
Stats
Random Movie
Search Movie
Movies sorted by rating
Movies sorted by year
Filter Movies
Generate Website``` 

Enter the number of the action you want to perform.

## Generate the Website

To generate the static movie website, choose option:
```

text
Generate Website``` 

The generated website is written to:
```

text _static/index.html``` 

Open this file in a browser to view the movie collection as a web page.

## Example Workflow

1. Start the application:
```

bash python main.py``` 

2. Select an existing user or create a new user.

3. Choose option `2` to add a movie.

4. Enter a movie title.

5. The app fetches movie details from OMDb and stores them in the database.

6. Choose option `1` to list saved movies.

7. Choose option `5` to view statistics.

8. Choose option `11` to generate the HTML website.

## Notes

- Movie data is fetched from the OMDb API.
- Movie ratings, years, posters, and notes are stored locally.
- Movie notes can be updated through the update option.
- Movie posters are displayed in the generated static website.
- An active internet connection is required when adding movies through the API.

## Security

Do not commit sensitive information such as API keys.

Make sure `.gitignore` includes:
```

text .env``` 

Use a placeholder in documentation and examples instead of a real API key:
```

text API_KEY=your_api_key_here``` 

## Future Improvements

Possible improvements for future versions:

- Add unit tests for storage and API modules
- Improve error handling for missing or incomplete API data
- Add password hashing for user accounts
- Add support for editing movie titles and years
- Add export/import functionality
- Improve generated website styling
- Add pagination or categories for larger movie collections
- Add a graphical user interface

## License

This project is intended for educational purposes. You may modify and extend it as needed.
```
