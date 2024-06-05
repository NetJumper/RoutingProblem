# Author: Jose Iriarte Garduno
# Student ID: 010724242
# Title: WGUPS Project
# Submission 2: 05/20/2024

import csv
import datetime

# Helper function to read a CSV file and return its content as a list of lists
def read_csv_to_list(file_path):
    with open(file_path, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.reader(file)
        return list(reader)

# Paths to the CSV files
address_file = 'CSV/Address_File.csv'
distance_file = 'CSV/Distance_File.csv'
package_file = 'CSV/Package_File.csv'

# Read the files using the helper function
address_data = read_csv_to_list(address_file)
distance_data = read_csv_to_list(distance_file)
package_data = read_csv_to_list(package_file)

# HashTable class using chaining
class ChainingHashTable:
    def __init__(self, initial_capacity=10):
        # Initialize the hash table with empty bucket list entries
        self.table = []
        for i in range(initial_capacity):
            self.table.append([])
      
    def insert(self, key, item):
        # Insert or update the key-item pair in the hash table
        bucket = hash(key) % len(self.table)
        bucket_list = self.table[bucket]
        for kv in bucket_list:
            if kv[0] == key:
                kv[1] = item
                return True
        key_value = [key, item]
        bucket_list.append(key_value)
        return True

    def search(self, key):
        # Search for an item with the matching key in the hash table
        bucket = hash(key) % len(self.table)
        bucket_list = self.table[bucket]
        for kv in bucket_list:
            if kv[0] == key:
                return kv[1]
        return None

    def remove(self, key):
        # Remove an item with the matching key from the hash table
        bucket = hash(key) % len(self.table)
        bucket_list = self.table[bucket]
        for kv in bucket_list:
            if kv[0] == key:
                bucket_list.remove(kv)
                return True
        return False

# Package class to store package information
class Package:
    def __init__(self, ID, street, city, state, zip_code, deadline, weight, notes, status="At the hub"):
        # Initialize package attributes
        self.ID = ID
        self.street = street
        self.city = city
        self.state = state
        self.zip_code = zip_code
        self.deadline = deadline
        self.weight = weight
        self.notes = notes
        self.status = status
        self.departure_time = None 
        self.delivery_time = None   
        self.truck_id = None  # Add truck ID attribute

    def __str__(self):
        # String representation of the Package object
        departure = self.departure_time.strftime("%H:%M:%S") if isinstance(self.departure_time, datetime.datetime) else "Not yet departed"
        delivery = self.delivery_time.strftime("%H:%M:%S") if isinstance(self.delivery_time, datetime.datetime) else "Not yet delivered"
        return (f"ID: {self.ID}, {self.street:20s}, {self.city}, {self.state}, {self.zip_code}, "
                f"Deadline: {self.deadline}, Weight: {self.weight}, Status: {self.status}, "
                f"Departure Time: {departure}, Delivery Time: {delivery}, Truck ID: {self.truck_id}")

    def update_status(self, current_time):
        # Update the address for Package #9 after 10:20 AM
        if self.ID == 9 and current_time >= datetime.datetime.combine(datetime.date.today(), datetime.time(10, 20)):
            self.street = "410 S State St"
            self.city = "Salt Lake City"
            self.state = "UT"
            self.zip_code = "84111"
        # Update the status of the package based on the current time
        if self.departure_time and isinstance(self.departure_time, datetime.datetime) and current_time >= self.departure_time:
            self.status = "En route" if not self.delivery_time or (isinstance(self.delivery_time, datetime.datetime) and current_time < self.delivery_time) else "Delivered"
        else:
            self.status = "At the hub"

# Function to load package data from a CSV file and insert it into the hash table
def load_package_data(filename, hash_table):
    with open(filename, mode='r', newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        next(reader)  # Skip the header row
        for package in reader:
            ID = int(package[0])
            street = package[1]
            city = package[2]
            state = package[3]
            zip_code = package[4]
            deadline = package[5]
            weight = package[6]
            notes = package[7]
            status = "At the Hub"

            # Create a Package instance and insert it into the hash table
            p = Package(ID, street, city, state, zip_code, deadline, weight, notes, status)
            hash_table.insert(ID, p)

# Truck class to store truck information and manage package deliveries
class Truck:
    def __init__(self, id, speed, miles, current_location, depart_time, packages):
        # Initialize truck attributes
        self.id = id  # Truck ID
        self.speed = speed
        self.miles = miles
        self.current_location = current_location
        self.depart_time = depart_time  
        self.time = depart_time  
        self.packages = packages

    def __str__(self):
        # String representation of the Truck object
        return (f"Truck Info - ID: {self.id}, Speed: {self.speed} mph, Mileage: {self.miles} mi, Location: {self.current_location}, "
                f"Departure Time: {self.depart_time.strftime('%H:%M:%S') if self.depart_time else 'Not Set'}, "
                f"Packages: {', '.join(str(p) for p in self.packages)}")

    def list_packages(self):
        # Print the list of packages assigned to the truck
        for package_id in self.packages:
            package = package_hash_table.search(package_id)
            if package:
                package.truck_id = self.id  # Set the truck ID for the package
                print(package)

# Function to find the index of an address in the address data
def find_address_index(address, address_data):
    for row in address_data:
        if address.strip().lower() in row[2].lower():
            return int(row[0])
    return -1  # Return -1 or consider raising an exception if address not found

# Function to get the distance between two addresses using their indices
def get_distance_between(index1, index2, distance_matrix):
    try:
        distance = distance_matrix[index1][index2]
        if distance == '':
            distance = distance_matrix[index2][index1]
        return float(distance)
    except IndexError:
        raise ValueError(f"Distance data at indices {index1}, {index2} is not a valid float.")

# Get the current date and time
current_datetime = datetime.datetime.now()

# Define departure times for the trucks
truck1_depart_time = datetime.datetime.combine(datetime.date.today(), datetime.time(8, 0, 0))
truck2_depart_time = datetime.datetime.combine(datetime.date.today(), datetime.time(8, 0, 0))
truck3_depart_time = datetime.datetime.combine(datetime.date.today(), datetime.time(8, 0, 0))

# Create instances of the Truck class
truck1 = Truck(1, 18, 0, "4001 South 700 East", truck1_depart_time, [1, 13, 14, 15, 16, 20, 29, 30, 31, 34, 37, 40])
truck2 = Truck(2, 18, 0, "4001 South 700 East", truck2_depart_time, [3, 6, 12, 17, 18, 19, 21, 22, 23, 24, 26, 27, 35, 36, 38, 39])
truck3 = Truck(3, 18, 0, "4001 South 700 East", truck3_depart_time, [2, 4, 5, 7, 8, 9, 10, 11, 25, 28, 32, 33])

# Create an instance of ChainingHashTable and load package data
package_hash_table = ChainingHashTable()
load_package_data("CSV/Package_File.csv", package_hash_table)

# Function to extract the index of an address from the address data
def extract_address_index(address, address_data):
    for index, data in enumerate(address_data):
        if address in data:
            return index
    raise ValueError("Address not found")

# Function to calculate distances between addresses and store them in a matrix
def calculate_distances(address_data, distance_data):
    distances = [[0.0] * len(address_data) for _ in address_data]
    for i, row in enumerate(distance_data):
        for j, dist in enumerate(row):
            if dist:
                distances[i][j] = distances[j][i] = float(dist)
    return distances

# Precompute distances
distances = calculate_distances(address_data, distance_data)

# Function to deliver packages and update the truck's time
def delivering_packages(truck, address_data, distances):
    # Get the list of packages not yet delivered
    not_delivered = [package_hash_table.search(packageID) for packageID in truck.packages]
    truck.packages.clear()
    current_address_index = extract_address_index(truck.current_location, address_data)
    current_time = truck.depart_time

    while not_delivered:
        # Sort packages based on distance from current location
        not_delivered.sort(key=lambda pkg: distances[current_address_index][extract_address_index(pkg.street, address_data)])

        next_package = not_delivered.pop(0)
        next_address_index = extract_address_index(next_package.street, address_data)
        next_distance = distances[current_address_index][next_address_index]

        # Update truck and package details
        truck.packages.append(next_package)
        truck.miles += next_distance
        truck.current_location = next_package.street # Update the truck's current location
        current_address_index = next_address_index
        travel_time = datetime.timedelta(hours=next_distance / truck.speed)
        current_time += travel_time # Update the time
        # Update the package's departure and delivery time
        next_package.departure_time = truck.depart_time
        next_package.delivery_time = current_time
        next_package.truck_id = truck.id  # Set the truck ID for the package
        # Update the truck's time
        truck.time = current_time

# Deliver packages for all trucks
delivering_packages(truck1, address_data, distances)
delivering_packages(truck2, address_data, distances)
truck3.depart_time = min(truck1.time, truck2.time)
delivering_packages(truck3, address_data, distances)

# Main class to manage the overall process and user interaction
class Main:
    def __init__(self, truck1, truck2, truck3, package_hash_table):
        # Initialize main class with truck instances and package hash table
        self.truck1 = truck1
        self.truck2 = truck2
        self.truck3 = truck3
        self.package_hash_table = package_hash_table

    def display_total_mileage(self):
        # Display the total mileage of all trucks
        total_mileage = self.truck1.miles + self.truck2.miles + self.truck3.miles
        print("Western Governors University Parcel Service")
        print(f"The overall miles are: {total_mileage:.1f}")

    def handle_time_entry(self):
        # Handle user input for time entry
        user_time = input("Please enter a time for which you'd like to see the status of each package. Format: HH:MM: ")
        try:
            h, m = map(int, user_time.split(":"))
            input_time = datetime.datetime.now().replace(hour=h, minute=m, second=0, microsecond=0)
            self.display_packages(input_time)
        except ValueError:
            print("Invalid time format. Please use the format HH:MM.")
    
    # Display the status of all packages, individually or all together.
    def display_packages(self, current_time):
        print("Enter the Package ID or press Enter to display all packages.")
        package_id = input("Package ID: ")
        if package_id:
            package = self.package_hash_table.search(int(package_id))
            if package:
                package.update_status(current_time)
                self.print_package_info(package)
            else:
                print(f"Package ID {package_id} not found.")
        else:
            for package_id in range(1, 41):  # package IDs range from 1 to 40
                package = self.package_hash_table.search(package_id)
                if package:
                    package.update_status(current_time)
                    self.print_package_info(package)
            exit() # Exit the program after displaying all packages.

    def print_package_info(self, package):
        departure = package.departure_time.strftime("%H:%M") if package.departure_time else "Not yet departed"
        delivery = package.delivery_time.strftime("%H:%M") if package.delivery_time else "Not yet delivered"
        print(f"ID: {package.ID}, {package.street:20s}, {package.city}, {package.state}, {package.zip_code}, "
              f"Deadline: {package.deadline}, {package.weight}, {package.status}, "
              f"Departure Time: {departure}, Delivery Time: {delivery}, Truck ID: {package.truck_id}")

    def request_time_input(self):
        # Request user input to start or exit the program
        while True:
            text = input("To start please type the word 'start' (typing 'exit' will close the program): ")
            if text.lower() == "start":
                self.handle_time_entry()
                break
            elif text.lower() == "exit":
                print("Exiting program.")
                break
            else:
                print("Invalid input, please type 'start' to continue or 'exit' to quit.")

# Main execution block
if __name__ == "__main__":
    main = Main(truck1, truck2, truck3, package_hash_table)
    main.display_total_mileage()
    main.request_time_input()

  