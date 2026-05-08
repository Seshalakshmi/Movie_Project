import random
import sys
from statistics import median

from thefuzz import process

from movie_storage_API import get_movie_details
import movie_storage_sql as storage


HTML_FILE_PATH = "_static/index_template.html"
GENERATE_HTML_WEBSITE = "_static/index.html"

######################## HELPER FUNCTIONS ##############################
def get_valid_rating():
    """
        Prompt the user to enter a valid movie rating.

        Ensures the rating:
            - Is a numeric value
            - Falls between 0 and 10 (inclusive)

        Parameters:
            None

        Returns:
            float: A valid movie rating.
    """
    while True:
        try:
            rating = float(input("\033[34mEnter movie rating (0-10): \033[0m"))
            if 0 <= rating <= 10:
                return rating
            print(f"Rating {rating} is invalid. Must be between 0 and 10.")
        except ValueError:
            print("Please provide a rating using numbers (0-10)")


def get_valid_movie_name(movie_database):
    """
        Prompt the user to enter a valid movie name.

        Ensures that:
            - The input is not empty
            - The movie does not already exist in the database

        Parameters:
            movie_database (dict): Dictionary containing existing movies.

        Returns:
            str: A valid, unique movie name.
    """
    while True:
        name = input("\033[34mEnter movie name: \033[0m").strip()
        if not name:
            print("Please provide a movie name")
            continue
        if name in movie_database:
            print(f"Movie '{name}' already exists!")
            continue
        return name


def get_minimum_rating():
    """
        Prompt the user to enter a minimum rating filter.

        The user may:
            - Provide a numeric value between 0 and 10
            - Leave the input blank to skip filtering

        Parameters:
            None

        Returns:
            float or str: Minimum rating as float, or empty string if skipped.
    """
    while True:
        try:
            minimum_rating = input(
                "Enter minimum rating (leave blank for no minimum rating): ")
            if minimum_rating == "":
                return minimum_rating
            if 0 <= float(minimum_rating) <= 10:
                return float(minimum_rating)
            if not len(minimum_rating) == 1:
                raise ValueError("Please provide a number (0-10)")
        except ValueError:
            print("Please provide a number (0-10)")
            continue


def get_start_year():
    """
        Prompt the user to enter a starting year for filtering.

        The user may:
            - Provide a valid 4-digit year
            - Leave the input blank to skip filtering

        Parameters:
            None

        Returns:
            int or str: Start year as integer, or empty string if skipped.
    """
    while True:
        start_year = input(
                "Enter start year (leave blank for no start year): ")
        if start_year == "":
            return start_year
        if len(start_year) != 4:
            print("Invalid input. Please enter a valid year.")
            continue
        if not start_year.isdigit():
            print("Invalid input. Please enter a valid year.")
            continue
        return int(start_year)


def get_end_year():
    """
        Prompt the user to enter an ending year for filtering.

        The user may:
            - Provide a valid 4-digit year
            - Leave the input blank to skip filtering

        Parameters:
            None

        Returns:
            int or str: End year as integer, or empty string if skipped.
    """
    while True:
        end_year = input(
            "Enter end year (leave blank for no end year): ")
        print()
        if end_year == "":
            return end_year
        if len(end_year) != 4:
            print("Invalid input. Please enter a valid year.")
            continue
        if not end_year.isdigit():
            print("Invalid input. Please enter a valid year.")
            continue
        return int(end_year)
######################## END OF HELPER FUNCTION ############################



def exit_app():
    """
       Exit the application gracefully.
       Prints a goodbye message to the console and exits the Python program.
    """
    print("Bye!")
    sys.exit()


def list_of_movies():
    """
        Display all movies in the database with rating and release year.

        Retrieves movies from the `movie_storage` module and prints each
        movie's name, rating, and year of release. If no movies exist,
        an informative message is printed.

        Parameters:
            None

        Returns:
            None
    """
    movie_database = storage.list_movies()
    if movie_database:
        total_movies = len(movie_database)

        print(f"{total_movies} movies in total")
        for movie, detail in movie_database.items():
            print(f"{movie} ({detail.get("rating")}): "
                  f"{detail.get("year")}")
    else:
        print("There is no data about the movies")


def get_movie_data():
    """
        Collect validated movie details from the user.

        Uses helper functions to retrieve:
            - Movie name
            - Movie rating
            - Release year

        Parameters:
            None

        Returns:
            tuple: (movie_name (str), year (int), rating (float))
    """
    movie_database = storage.list_movies()
    new_movie = get_valid_movie_name(movie_database)
    fetch_movie_details = get_movie_details(new_movie)
    movie_title = fetch_movie_details.get('Title', 0)
    movie_year = fetch_movie_details.get('Year', 0)
    movie_rating = fetch_movie_details.get('imdbRating', 0)
    movie_poster = fetch_movie_details.get('Poster', 0)

    return movie_title, movie_year, movie_rating, movie_poster


def add_movie():
    """
        Add a new movie to the database.

        Collects validated movie data from the user and stores it
        using the movie_storage module.

        Parameters:
            None

        Returns:
            None
    """
    new_movie, new_movie_year, new_movie_rating, new_movie_poster = get_movie_data()
    storage.add_movie(
        new_movie,
        new_movie_year,
        new_movie_rating,
        new_movie_poster
    )
    print(f"Movie {new_movie} successfully added")


def delete_movie():
    """
        Delete a movie from the database.

        Prompts the user for a movie name and removes it if it exists.

        Parameters:
            None

        Returns:
            None
    """
    movie_database = storage.list_movies()
    if not movie_database:
        print("There is no data to delete the movie")
        return

    movie_name_delete = input(
        "\033[34mEnter movie name to delete: \033[0m")
    if movie_name_delete not in movie_database:
        print(f"{movie_name_delete} doesn't exist!")
    else:
        storage.delete_movie(movie_name_delete)
        print(f"Movie {movie_name_delete} successfully deleted")



def update_movie():
    """
        Update the rating of an existing movie.

        Prompts the user for a movie name and a new rating,
        then updates the movie in the database.

        Parameters:
            None

        Returns:
            None
    """
    movie_database = storage.list_movies()
    if not movie_database:
        print("There is no data to update the movie")
        return

    name = input("\033[34mEnter movie name: \033[0m")
    if name not in movie_database:
        print(f"Movie '{name}' doesn't exist!")
        return
    new_rating = get_valid_rating()
    storage.update_movie(name, new_rating)
    print(f"Movie '{name}' successfully updated")


def stats():
    """
        Display statistics about movies in the database.

        Computes and prints:
            - Average rating
            - Median rating
            - Best-rated movie(s)
            - Worst-rated movie(s)

        Parameters:
            None

        Returns:
            None
    """
    movie_database = storage.list_movies()
    if not movie_database:
        print("There is no data about movies")
        return

    list_of_rating = []
    for rating in movie_database.values():
        list_of_rating.append(rating["rating"])

    average_rating = round(sum(list_of_rating) / len(movie_database), 1)
    print("Average rating: ", average_rating)

    median_rating = round(median(sorted(list_of_rating)), 1)
    print("Median rating: ", median_rating)

    max_rating = max(details["rating"]
                     for details in movie_database.values())
    for movie_name, movie_rating in movie_database.items():
        if max_rating == movie_rating["rating"]:
            print(f"Best Movie: {movie_name}, {movie_rating["rating"]}")

    min_rating = min(details["rating"]
                     for details in movie_database.values())
    for movie_name, movie_rating in movie_database.items():
        if min_rating == movie_rating["rating"]:
            print(f"Worst Movie: {movie_name}, {movie_rating["rating"]}")



def random_movie():
    """
        Display a random movie from the database.

        Selects a random movie from the database and prints its name, year and
        rating.

        Parameters:
            None

        Returns:
            None
    """
    movie_database = storage.list_movies()
    if not movie_database:
        print("There is no data about movies")
        return

    movie_name, rating = random.choice(list(movie_database.items()))
    print(f"Your movie for tonight: {movie_name} "
          f"({rating["year"]}), it's rated {rating["rating"]}")



def search_movie():
    """
        Search for a movie by name or partial name.

        If the exact movie is found, prints its name and rating. If not
        found, suggests
        close matches using fuzzy string matching (`thefuzz.process.extract`).

        Parameters:
            None

        Returns:
            None
    """
    movie_database = storage.list_movies()
    if not movie_database:
        print("There is no data about movies")
        return
    while True:
        searching = input("\033[34mEnter part of movie name: \033[0m")
        list_of_movie = movie_database.keys()

        if searching == "":
            print("Please provide part of movie name")
        elif searching in list_of_movie:
            for movie, detail in movie_database.items():
                if movie == searching:
                    print(f"{movie}, {detail["rating"]}")
            break
        else:
            matching_movies = process.extract(searching, list_of_movie)
            if matching_movies:
                print(
                    f"The movie {searching} does not exist. Did you "
                    f"mean: ")
                for suggested_movie, rating in matching_movies:
                    if rating > 75:
                        print(suggested_movie)
                break
            else:
                print(f"The movie {searching} does not exist")



def sort_by_rating():
    """
        Display all movies sorted by rating in descending order.

        Parameters:
            None

        Returns:
            None
    """
    movie_database = storage.list_movies()
    if not movie_database:
        print("There is no data about movies")
        return
    sorted_movie_database = sorted(movie_database.items(),
                                   key=lambda item: item[1]["rating"],
                                   reverse=True)
    for movies, rating in sorted_movie_database:
        print(f"{movies} ({rating["year"]}): "
              f"{rating["rating"]}")



def sort_by_year():
    """
        Display all movies sorted by release year.

        Prompts the user whether they want the latest movies first.
        Displays movies sorted either from newest to oldest or oldest to
        newest.

        Parameters:
            None

        Returns:
            None
    """
    movie_database = storage.list_movies()
    if not movie_database:
        print("There is no data about movies")
        return
    while True:
        latest_sort = input("Do you want the latest movies first? (Y/N): ")
        print()
        if latest_sort.capitalize() == "Y":
            sorted_movie_database = sorted(movie_database.items(),
                                           key=lambda item: item[1][
                                               "year"],
                                           reverse=True)
            for movies, rating in sorted_movie_database:
                print(
                    f"{movies} ({rating["year"]}): "
                    f"{rating["rating"]}")
            break
        elif latest_sort.capitalize() == "N":
            sorted_movie_database = sorted(movie_database.items(),
                                           key=lambda item: item[1][
                                               "year"])
            for movies, rating in sorted_movie_database:
                print(
                    f"{movies} ({rating["year"]}): "
                    f"{rating["rating"]}")
            break
        else:
            print('Please enter "Y" or "N"')


def filter_movies():
    """
        Filter and display movies based on user-defined criteria.

        Supports filtering by:
            - Minimum rating
            - Start year
            - End year

        The user may provide any combination of filters or skip them.

        Parameters:
            None

        Returns:
            None
    """
    movie_database = storage.list_movies()
    if not movie_database:
        print("There is no data about movies")
        return

    minimum_rating = get_minimum_rating()
    start_year = get_start_year()
    end_year = get_end_year()

    list_of_filtered_movies = []


    if minimum_rating == "" and start_year == "" and end_year == "":
        for movie, detail in (movie_database.items()):
            result = (f"{movie} ({detail["year"]}): "
                      f"{detail["rating"]}")
            list_of_filtered_movies.append(result)

    elif minimum_rating and start_year == "" and end_year == "":
        for movie, detail in (movie_database.items()):
            if detail["Rating"] >= minimum_rating:
                result = (f"{movie} ({detail["year"]}): "
                          f"{detail["rating"]}")
                list_of_filtered_movies.append(result)

    elif minimum_rating == "" and start_year and end_year == "":
        for movie, detail in (movie_database.items()):
            if detail["year"] >= start_year:
                result = (f"{movie} ({detail["year"]}): "
                          f"{detail["rating"]}")
                list_of_filtered_movies.append(result)

    elif minimum_rating == "" and start_year =="" and end_year:
        for movie, detail in (movie_database.items()):
            if detail["year"] <= end_year:
                result = (f"{movie} ({detail["year"]}): "
                          f"{detail["rating"]}")
                list_of_filtered_movies.append(result)

    else:
        for movie, detail in (movie_database.items()):
            if (detail["rating"] >= minimum_rating and
                    start_year <= detail["year"] <= end_year):
                result = (f"{movie} ({detail["year"]}): "
                          f"{detail["rating"]}")
                list_of_filtered_movies.append(result)

    if len(list_of_filtered_movies) != 0:
        print("\n".join(list_of_filtered_movies))
    else:
        print("No movies match your criteria.")


def serialization_movie(movie, details):
    parts = [
        '<li class="movie">',
        f'<img class="movie-poster" src="{details["poster"]}">',
        f'<div class="movie-title">{movie}</div>',
        f'<div class="movie-year">{details["year"]}</div>',
        '</li>',
    ]
    return ''.join(parts)


def movie_poster_cards():
    movie_database = storage.list_movies()
    if not movie_database:
        print("There is no data about movies")
        return

    output = []
    for movie, details in movie_database.items():
        output.append(serialization_movie(movie, details))

    return ''.join(output)


def replacing_tags(result):
    with (open(HTML_FILE_PATH, "r") as read_file):
        tags = read_file.read().replace("__TEMPLATE_TITLE__",
                                        "Masterschool's Movie App"
                                        ).replace("__TEMPLATE_MOVIE_GRID__"
                                                  , result)

    with open(GENERATE_HTML_WEBSITE, "w") as write_html:
        write_html.write(tags)

def generate_website():
    serialized_movie = movie_poster_cards()
    replacing_tags(serialized_movie)
    print("Website was generated successfully.")


def main():
    generate_website()
    """
        Launch the Movie Database application and handle user interaction.

        This function displays the main menu of the application and
        continuously
        prompts the user to choose an action until they decide to exit.
        Available actions include listing, adding, deleting, updating,
        and filtering
        movies, viewing statistics, selecting a random movie, and sorting
        movies
        by rating or year.

        The function maps each menu option (0-10) to its corresponding handler
        function and validates user input to ensure only valid choices are
        accepted.

        Workflow:
            1. Display a welcome banner.
            2. Show the menu of options.
            3. Prompt the user to select an option.
            4. Execute the corresponding function based on user choice.
            5. Continue prompting until the user selects 'Exit'.

        Parameters:
            None

        Returns:
            None

        Raises:
            ValueError: If the user input for menu selection cannot be
            converted to an integer.
            TypeError: If the user input is not a valid menu key.
            SystemExit: When the user chooses the 'Exit' option (0).
    """
    first_line = '*' * 10
    print(f"{first_line} My Movies Database {first_line}")

    while True:
        print("\n\033[35mMenu: \n"
              "0. Exit \n"
              "1. List Movies \n"
              "2. Add Movie \n"
              "3. Delete Movie \n"
              "4. Update Movie \n"
              "5. Stats \n"
              "6. Random Movie \n"
              "7. Search Movie \n"
              "8. Movies sorted by rating \n"
              "9. Movies sorted by year \n"
              "10. Filter Movies \n"
              "11. Generate Website \n\033[0m")

        menu = {
            0: exit_app,
            1: list_of_movies,
            2: add_movie,
            3: delete_movie,
            4: update_movie,
            5: stats,
            6: random_movie,
            7: search_movie,
            8: sort_by_rating,
            9: sort_by_year,
            10: filter_movies,
            11: generate_website
        }

        while True:
            try:
                choice = int(input("Enter choice (0-11): "))
                print()
                menu.get(choice)()
                input("\nPress enter to continue")
                break
            except ValueError:
                print("Invalid choice")
            except TypeError:
                print("Please provide a number")


if __name__ == "__main__":
    main()
