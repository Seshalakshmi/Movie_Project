import random
import sys
from statistics import median

from thefuzz import process

from movie_storage.movie_storage_API import get_movie_details
from movie_storage import movie_storage_sql as storage

HTML_FILE_PATH = "_static/index_template.html"
GENERATE_HTML_WEBSITE = "_static/index.html"

######################## HELPER FUNCTIONS ##############################
def get_valid_rating():
    """
        Prompt the user for a valid movie rating between 0 and 10.

        Returns:
            float: A validated rating value.
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
        Prompt the user for a unique movie name.

        Args:
            movie_database (dict): Existing movie database to check duplicates.

        Returns:
            str: A validated, non-duplicate movie name.
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
        Prompt the user for an optional minimum rating filter.

        Returns:
            float | str: Minimum rating or empty string if not provided.
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
        Prompt the user for an optional start year filter.

        Returns:
            int | str: Start year or empty string if not provided.
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
        Prompt the user for an optional end year filter.

        Returns:
            int | str: End year or empty string if not provided.
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


def serialization_movie(movie_database):
    """
        Convert movie database entries into HTML list items.

        Args:
            movie_database (dict): Movie database.

        Returns:
            str: Serialized HTML string representing movies.
    """
    output = [f'''<li class="movie">
                <div>
                <img class="movie-poster" src="{details["poster"]}">
                {f'<div class="tooltip">{details["note"]}</div>' 
    if details.get("note") and details["note"] != "None" else ''}
                <div class="movie-title">{details["title"]}</div>
                <div class="movie-rating">IMDB Rating: {details["rating"]}</div>
                <div class="movie-year">{details["year"]}</div>
                </div>
            </li>
            ''' for movie, details in movie_database.items()]

    return '\n'.join(output)

######################## END OF HELPER FUNCTION ############################



def exit_app(user_id):
    """
    Exit the application gracefully.

    Args:
        user_id (int): Current user ID.
    """
    user_name = storage.get_user_name(user_id)
    for u_name in user_name.values():
        print(f"{u_name['name']}!, Thank You.")
        print("Bye!")
        sys.exit()


def list_of_movies(user_id):
    """
        Print all movies belonging to the user.

        Args:
            user_id (int): Current user ID.
    """
    movie_database = storage.list_movies(user_id)

    if movie_database:
        total_movies = len(movie_database)

        print(f"{total_movies} movies in total")
        for detail in movie_database.values():
            print(f"{detail['title']} ({detail.get('rating')}): "
                  f"{detail.get('year')}")
    else:
        print("There is no movies, please add a movie")


def get_movie_data(user_id):
    """
        Fetch and prepare movie metadata from external API.

        Args:
            user_id (int): Current user ID.

        Returns:
            tuple: (title, year, rating, poster URL)
    """
    movie_database = storage.list_movies(user_id)

    new_movie = get_valid_movie_name(movie_database)

    fetch_movie_details = get_movie_details(new_movie)
    movie_title = fetch_movie_details.get('Title', 0)
    movie_year = fetch_movie_details.get('Year', 0)
    movie_rating = fetch_movie_details.get('imdbRating', 0)
    movie_poster = fetch_movie_details.get('Poster',
                                "https://placehold.co/380x562?text=No+Poster")

    return movie_title, movie_year, movie_rating, movie_poster


def add_movie(user_id):
    """
        Add a new movie to the database or link it to an existing entry.

        Args:
            user_id (int): Current user ID.
    """
    movie_database = storage.list_all_movies()
    new_movie, new_movie_year, new_movie_rating, new_movie_poster \
        = get_movie_data(user_id)
    for movie_id, details in movie_database.items():
        if new_movie == details['title']:
            storage.add_existing_movie_user(movie_id, user_id)
            print(f"Movie {new_movie} successfully added")
            return

    storage.add_movie(
        new_movie,
        new_movie_year,
        new_movie_rating,
        new_movie_poster,
        user_id
    )
    print(f"Movie {new_movie} successfully added")


def delete_movie(user_id):
    """
        Delete a movie from the user's collection.

        Args:
            user_id (int): Current user ID.
    """
    movie_database = storage.list_movies(user_id)
    if not movie_database:
        print("There is no data to delete the movie")
        return

    movie_name_delete = input(
        "\033[34mEnter movie name to delete: \033[0m")
    movie_exits = False
    for details in movie_database.values():
        if movie_name_delete.lower() == details['title'].lower():
            movie_exits = True
            break

    if not movie_exits:
        print(f"{movie_name_delete} doesn't exist!")
        return

    storage.delete_movie(movie_name_delete, user_id)
    print(f"Movie {movie_name_delete} successfully deleted")


def update_movie(user_id):
    """
        Update a movie note in the database.

        Args:
            user_id (int): Current user ID.
    """
    movie_database = storage.list_movies(user_id)
    if not movie_database:
        print("There is no data to update the movie")
        return

    movie_name = input("\033[34mEnter movie name: \033[0m")
    movie_note = input("\033[34mEnter movie note: \033[0m")
    movie_exits = False
    for details in movie_database.values():
        if movie_name.lower() == details['title'].lower():
            movie_exits = True
            break
    if not movie_exits:
        print(f"Movie '{movie_name}' doesn't exist!")
        return
    storage.update_movie(movie_name, movie_note, user_id)
    print(f"Movie '{movie_name}' successfully updated")


def stats(user_id):
    """
        Display statistical analysis of the movie collection.

        Args:
            user_id (int): Current user ID.
    """
    movie_database = storage.list_movies(user_id)
    if not movie_database:
        print("There is no data about movies")
        return

    list_of_rating = [rating['rating'] for rating in movie_database.values()]

    average_rating = round(sum(list_of_rating) / len(movie_database), 1)
    print("Average rating: ", average_rating)

    median_rating = round(median(sorted(list_of_rating)), 1)
    print("Median rating: ", median_rating)

    max_rating = max(details['rating']
                     for details in movie_database.values())
    for movie_rating in movie_database.values():
        if max_rating == movie_rating['rating']:
            print(f"Best Movie: {movie_rating['title']}, {movie_rating['rating']}")

    min_rating = min(details['rating']
                     for details in movie_database.values())
    for movie_rating in movie_database.values():
        if min_rating == movie_rating['rating']:
            print(f"Worst Movie: {movie_rating['title']}, {movie_rating['rating']}")



def random_movie(user_id):
    """
        Select and display a random movie from the user's collection.

        Args:
            user_id (int): Current user ID.
    """
    movie_database = storage.list_movies(user_id)
    if not movie_database:
        print("There is no data about movies")
        return

    movie_name, rating = random.choice(list(movie_database.items()))
    print(f"Your movie for tonight: {rating['title']} "
          f"({rating['year']}), it's rated {rating['rating']}")



def search_movie(user_id):
    """
        Search for a movie by name or partial match.

        Uses fuzzy matching to suggest similar titles if an exact match is not found.

        Args:
            user_id (int): Current user ID.
    """
    movie_database = storage.list_movies(user_id)
    if not movie_database:
        print("There is no data about movies")
        return
    while True:
        searching = input("\033[34mEnter part of movie name: \033[0m")
        list_of_movie = [detail['title'] for detail in movie_database.values()]

        if searching == "":
            print("Please provide part of movie name")
        elif searching in list_of_movie:
            for detail in movie_database.values():
                if detail['title'] == searching:
                    print(f"{detail['title']}, {detail['rating']}")
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



def sort_by_rating(user_id):
    """
        Display movies sorted by rating in descending order.

        Args:
            user_id (int): Current user ID.

        Returns:
    """
    movie_database = storage.list_movies(user_id)
    if not movie_database:
        print("There is no data about movies")
        return
    sorted_movie_database = sorted(movie_database.items(),
                                   key=lambda item: item[1]['rating'],
                                   reverse=True)
    for movies, rating in sorted_movie_database:
        print(f"{rating['title']} ({rating['year']}): "
              f"{rating['rating']}")



def sort_by_year(user_id):
    """
        Display movies sorted by release year.

        Allows user to choose ascending or descending order.

        Args:
            user_id (int): Current user ID.
    """
    movie_database = storage.list_movies(user_id)
    if not movie_database:
        print("There is no data about movies")
        return
    while True:
        latest_sort = input("Do you want the latest movies first? (Y/N): ")
        print()
        if latest_sort.capitalize() == "Y":
            sorted_movie_database = sorted(movie_database.items(),
                                           key=lambda item: item[1][
                                               'year'],
                                           reverse=True)
            for movies, rating in sorted_movie_database:
                print(
                    f"{rating['title']} ({rating['year']}): "
                    f"{rating['rating']}")
            break
        elif latest_sort.capitalize() == "N":
            sorted_movie_database = sorted(movie_database.items(),
                                           key=lambda item: item[1][
                                               'year'])
            for movies, rating in sorted_movie_database:
                print(
                    f"{rating['title']} ({rating['year']}): "
                    f"{rating['rating']}")
            break
        else:
            print('Please enter "Y" or "N"')


def filter_movies(user_id):
    """
        Filter movies based on optional criteria such as rating and year range.

        Users can filter by:
        - Minimum rating
        - Start year
        - End year

        Args:
            user_id (int): Current user ID.
    """
    movie_database = storage.list_movies(user_id)
    if not movie_database:
        print("There is no data about movies")
        return

    minimum_rating = get_minimum_rating()
    start_year = get_start_year()
    end_year = get_end_year()

    list_of_filtered_movies = []


    if minimum_rating == "" and start_year == "" and end_year == "":
        for detail in movie_database.values():
            result = (f"{detail['title']} ({detail['year']}): "
                      f"{detail['rating']}")
            list_of_filtered_movies.append(result)

    elif minimum_rating and start_year == "" and end_year == "":
        for detail in movie_database.values():
            if detail['rating'] >= minimum_rating:
                result = (f"{detail['title']} ({detail['year']}): "
                          f"{detail['rating']}")
                list_of_filtered_movies.append(result)

    elif minimum_rating == "" and start_year and end_year == "":
        for detail in movie_database.values():
            if detail['year'] >= start_year:
                result = (f"{detail['title']} ({detail['year']}): "
                          f"{detail['rating']}")
                list_of_filtered_movies.append(result)

    elif minimum_rating == "" and start_year =="" and end_year:
        for detail in (movie_database.values()):
            if detail['year'] <= end_year:
                result = (f"{detail['title']} ({detail['year']}): "
                          f"{detail['rating']}")
                list_of_filtered_movies.append(result)

    else:
        for detail in movie_database.values():
            if (detail['rating'] >= minimum_rating and
                    start_year <= detail['year'] <= end_year):
                result = (f"{detail['title']} ({detail['year']}): "
                          f"{detail['rating']}")
                list_of_filtered_movies.append(result)

    if len(list_of_filtered_movies) != 0:
        print("\n".join(list_of_filtered_movies))
    else:
        print("No movies match your criteria.")


def generate_website(user_id):
    """
       Generate a static HTML website representing the user's movie collection.

       Reads an HTML template, injects movie data, and writes the output to a file.

       Args:
           user_id (int): Current user ID.
    """
    movie_database = storage.list_movies(user_id)
    user_detail = storage.get_user_name(user_id)
    user_name = {}
    for u_name in user_detail.values():
        user_name = u_name
    if not movie_database:
        serialized_movie = (f"<h2>{user_name['name']}, your movie collection is empty. "
                            f"Add some movies!</h2>")
    else:
        serialized_movie = serialization_movie(movie_database)

    with (open(HTML_FILE_PATH, "r") as read_file):
        tags = read_file.read().replace("__TEMPLATE_TITLE__",
                                        "Masterschool's Movie App"
                                        ).replace("__TEMPLATE_MOVIE_GRID__"
                                                  , serialized_movie)

    with open(GENERATE_HTML_WEBSITE, "w", encoding='UTF-8') as write_html:
        write_html.write(tags)
    print("Website was generated successfully.")

def create_user():
    """
        Create a new user in the system.

        Prompts for username and password, then stores the user in the database.

        Returns:
            int: Newly created user ID.
    """
    user_name = input("Enter user name: ")
    password = input("Enter new password: ")
    user_id = storage.add_users(user_name, password)
    return user_id

def movie_suggestion(user_id):
    """
        Display the main menu and handle user interaction for movie operations.

        Provides options such as adding, deleting, searching, and analyzing movies.

        Args:
            user_id (int): Current user ID.
    """
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
                choice = input("Enter choice (0-11): ")
                if not choice.isdigit():
                    print("Please provide a valid number")
                    continue

                choice = int(choice)
                print()
                action = menu.get(choice)
                if action is None:
                    print("Invalid Choice")
                else:
                    action(user_id)
                input("\nPress enter to continue")
                break
            except ValueError:
                print("Please provide a valid number")


def main():
    """
        Entry point of the application.

        Displays available users, allows user selection or creation,
        and starts the movie management menu loop.
    """
    first_line = '*' * 10
    print(f"{first_line} My Movies Database {first_line}")

    users = storage.list_users()

    for user_id, user in users.items():
        print(f"{user_id}. {user['name']}")
    print(f"{len(users) + 1}. Create new user")
    while True:
        select_user = input("Enter choice: ")
        if not select_user.isdigit():
            print("Please provide a number")
            continue

        select_user = int(select_user)
        if select_user in users.keys():
            print(f"Hello, {users[select_user]['name']}")
            movie_suggestion(select_user)
            break
        elif select_user == len(users) + 1:
            print("Create New user")
            user_id = create_user()
            movie_suggestion(user_id)
            break
        else:
            print("Invalid choice")

if __name__ == "__main__":
    main()
