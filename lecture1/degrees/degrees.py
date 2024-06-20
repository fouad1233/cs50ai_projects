import csv
import sys , os

from util import Node, StackFrontier, QueueFrontier

# Maps names to a set of corresponding person_ids
names = {}

# Maps person_ids to a dictionary of: name, birth, movies (a set of movie_ids)
people = {}

# Maps movie_ids to a dictionary of: title, year, stars (a set of person_ids)
movies = {}


def load_data(directory):
    """
    Load data from CSV files into memory.
    """
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


def main():
    if len(sys.argv) > 2:
        sys.exit("Usage: python degrees.py [directory]")
    file_path = os.path.dirname(os.path.abspath(__file__))

    directory = os.path.join( file_path, (sys.argv[1] if len(sys.argv) == 2 else "large"))
    print(directory)

    # Load data from files into memory
    print("Loading data...")
    load_data(directory)
    print("Data loaded.")
    print("people: ", people)
    print("movies: ", movies)
    print("names: ", names)

    source = person_id_for_name(input("Name: "))
    if source is None:
        sys.exit("Person not found.")
    target = person_id_for_name(input("Name: "))
    if target is None:
        sys.exit("Person not found.")

    path = shortest_path(source, target)

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


def shortest_path(source, target):
    """
    Returns the shortest list of (movie_id, person_id) pairs
    that connect the source to the target.

    If no possible path, returns None.
    """
    deggrees_of_seperation = DegreesOfSeperation(source, target)
    deggrees_of_seperation.solve()
    return deggrees_of_seperation.solution
    

class DegreesOfSeperation():
    def __init__(self, sourceid , targetid ):
        self.source = sourceid
        self.target = targetid
        self.start = sourceid
        self.goal = targetid
        self.solution = None
        self.explored = set()
    def solve(self):
        
        # Keep track of number of states explored
        self.num_explored = 0
        
        # Initialize frontier to just the starting position
        start = Node(state=self.start, parent=None, action=None)
        frontier = StackFrontier()
        frontier.add(start)
        
        while True:
            # If nothing left in frontier, then no path
            if frontier.empty():
                return None

            # Choose a node from the frontier
            node = frontier.remove()
            self.num_explored += 1

            # If node is the goal, then we have a solution
            if node.state == self.goal:
                previous_nodes = []
                while node.parent is not None:
                    previous_nodes.append(node)
                    node = node.parent
                previous_nodes.reverse()
                movies_and_persons = []
                for node in previous_nodes:
                    movies_and_persons.append((node.action, node.state))
                self.solution = movies_and_persons
                return
            #if the goal is in the frontier
            is_sol_in_frontier = is_solution_in_frontier(frontier, self.goal)
            if is_sol_in_frontier[0]:
                node = is_sol_in_frontier[1]
                previous_nodes = []
                while node.parent is not None:
                    previous_nodes.append(node)
                    node = node.parent
                previous_nodes.reverse()
                movies_and_persons = []
                for node in previous_nodes:
                    movies_and_persons.append((node.action, node.state))
                self.solution = movies_and_persons
                return

            # Mark node as explored
            self.explored.add(node.state)

            # Add neighbors to frontier
            for action, state in self.neighbors(node.state):
                if not frontier.contains_state(state) and state not in self.explored:
                    child = Node(state=state, parent=node, action=action)
                    frontier.add(child)
    def neighbors(self,state):
        return neighbors_for_person(state)
def is_solution_in_frontier(frontier, goal):
    for node in frontier.frontier:
        if node.state == goal:
            return True , node
    return False , None

def person_id_for_name(name):
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


def neighbors_for_person(person_id):
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


if __name__ == "__main__":
    main()
