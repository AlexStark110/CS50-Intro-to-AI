"""
Degrees of Separation

Find the shortest path between actors using breadth-first search
(like "Six Degrees of Kevin Bacon")
"""

import csv
import sys
from collections import deque


def load_data(directory):
    """
    Load data from CSV files into memory.
    """
    # Data structures to hold movies and actors
    names = {}
    people = {}
    movies = {}

    # Load people
    with open(f"{directory}/people.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            people[row["id"]] = {
                "name": row["name"],
                "birth": row["birth"],
                "movies": set()
            }
            if row["name"].lower() not in names:
                names[row["name"].lower()] = {row["id"]}
            else:
                names[row["name"].lower()].add(row["id"])

    # Load movies
    with open(f"{directory}/movies.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            movies[row["id"]] = {
                "title": row["title"],
                "year": row["year"],
                "stars": set()
            }

    # Load stars
    with open(f"{directory}/stars.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                people[row["person_id"]]["movies"].add(row["movie_id"])
                movies[row["movie_id"]]["stars"].add(row["person_id"])
            except KeyError:
                pass

    return names, people, movies


def person_id_for_name(name, names, people):
    """
    Returns the IMDB id for a person's name,
    resolving ambiguities as needed.
    """
    person_ids = list(names.get(name.lower(), set()))
    if len(person_ids) == 0:
        return None
    elif len(person_ids) > 1:
        print(f"Which '{name}'?")
        for person_id in person_ids:
            person = people[person_id]
            name = person["name"]
            birth = person["birth"]
            print(f"ID: {person_id}, Name: {name}, Birth: {birth}")
        try:
            person_id = input("Intended Person ID: ")
            if person_id in person_ids:
                return person_id
        except ValueError:
            pass
        return None
    else:
        return person_ids[0]


def neighbors_for_person(person_id, people, movies):
    """
    Returns (movie_id, person_id) pairs for people
    who starred with a given person.
    """
    movie_ids = people[person_id]["movies"]
    neighbors = set()
    for movie_id in movie_ids:
        for person_id in movies[movie_id]["stars"]:
            neighbors.add((movie_id, person_id))
    return neighbors


def shortest_path(source, target, people, movies):
    """
    Returns the shortest list of (movie_id, person_id) pairs
    that connect the source to the target.

    If no possible path, returns None.
    """
    # Initialize frontier to source
    start = source
    frontier = deque([(start, [])])
    
    # Keep track of explored nodes
    explored = set()
    
    # Keep searching until no more nodes in frontier
    while frontier:
        node, path = frontier.popleft()
        
        # If we've reached the target, return path
        if node == target:
            return path
            
        # Mark node as explored
        explored.add(node)
        
        # Add neighbors to frontier
        for movie_id, person_id in neighbors_for_person(node, people, movies):
            if person_id not in explored:
                new_path = path + [(movie_id, person_id)]
                frontier.append((person_id, new_path))
    
    return None


def main():
    if len(sys.argv) > 2:
        sys.exit("Usage: python degrees.py [directory]")
    directory = sys.argv[1] if len(sys.argv) == 2 else "large"

    # Load data from files into memory
    print("Loading data...")
    names, people, movies = load_data(directory)
    print("Data loaded.")

    source = person_id_for_name(input("Name: "), names, people)
    if source is None:
        sys.exit("Person not found.")
    target = person_id_for_name(input("Name: "), names, people)
    if target is None:
        sys.exit("Person not found.")

    path = shortest_path(source, target, people, movies)

    if path is None:
        print("Not connected.")
    else:
        degrees = len(path)
        print(f"{degrees} degrees of separation.")
        path = [(None, source)] + path
        for i in range(degrees):
            person1 = people[path[i][1]]["name"]
            person2 = people[path[i + 1][1]]["name"]
            movie = movies[path[i + 1][0]]["title"]
            print(f"{i + 1}: {person1} and {person2} starred in {movie}")


if __name__ == "__main__":
    main()