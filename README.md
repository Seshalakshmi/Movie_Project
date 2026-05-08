# Movie Database App

A command-line movie database application built with Python. The app allows users to manage a personal movie collection, fetch movie details from the OMDb API, store movie data in a SQLite database, view movie statistics, and generate a simple static HTML movie website.

## Features

- Add movies by title using OMDb API data
- Store movie information in a SQLite database
- List all saved movies
- Delete movies from the database
- Update movie ratings
- Search movies by title
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
- OMDb API
- HTML/CSS for static website generation

## Requirements

Install the required Python packages:

You can get an API key from:
text [https://www.omdbapi.com/apikey.aspx](https://www.omdbapi.com/apikey.aspx)

> Note: The `.env` file is ignored by Git and should not be committed.

## Database

The application uses SQLite as its database.

By default, the database is stored at:

text data/movies.db

The database table is created automatically when the storage module is loaded.

bash python movie_phase2.py

You will see an interactive menu:

text ********** My Movies Database **********
Menu:
1. Exit
2. List Movies
3. Add Movie
4. Delete Movie
5. Update Movie
6. Stats
7. Random Movie
8. Search Movie
9. Movies sorted by rating
10. Movies sorted by year
11. Filter Movies
12. Generate Website``` 

Enter the number of the action you want to perform.

## Generate the Website

To generate the static movie website, choose option:
```

text
Generate Website``` 

The generated website will be written to:
```

text _static/index.html``` 

Open this file in a browser to view your movie collection as a web page.

## Example Workflow

1. Start the application:
```

bash python movie_phase2.py``` 

2. Choose option `2` to add a movie.

3. Enter a movie title.

4. The app fetches movie details from OMDb and stores them in the database.

5. Choose option `1` to list saved movies.

6. Choose option `11` to generate the HTML website.

## Notes

- Movie data is fetched from the OMDb API.
- Ratings are stored locally and can be updated.
- Movie posters are used when generating the static website.
- The application requires an active internet connection when adding movies through the API.

## Security

Do not commit sensitive information such as API keys.

The `.gitignore` file should include:
```

text .env``` 

## Future Improvements

Possible improvements for future versions:

- Add unit tests for storage and API modules
- Improve error handling for missing API data
- Add support for editing movie titles and years
- Add a graphical user interface
- Add export/import functionality
- Improve generated website styling
- Add pagination or categories for larger movie collections

## License

This project is intended for educational purposes. You may modify and extend it as needed.
```

