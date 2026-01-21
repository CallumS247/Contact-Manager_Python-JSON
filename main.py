import json
import os
from datetime import date

if not os.path.exists("contacts.json"):
    people = []
else:
    with open("contacts.json", "r") as f:
        try:
            data = json.load(f)
            people = data.get("contacts", [])
        except json.JSONDecodeError:        #File exists but is empty or invalid       
            people = []

def add_person():
    name = input("Name: ")

    while True:
        dob = input("Date of Birth (DD-MM-YYYY): ").strip()
        try:                                #Correct formatting of DoB
            d, m, y = map(int, dob.split("-"))
            date(y, m, d)                   #Validates it's a real date
            break
        except:
            print("Invalid date. Use DD-MM-YYYY (e.g., 14-09-2006).")

    tag = input("Tag (Friend/Family/Work): ")

    person = {"name": name, "dob": dob, "tag": tag}
    return person

def calculate_age(dob_str: str) -> int:     #Calculates age based on the DoB stored
    d, m, y = map(int, dob_str.split("-"))  #DD-MM-YYYY
    born = date(y, m, d)
    today = date.today()
    return today.year - born.year - ((today.month, today.day) < (born.month, born.day))

def display_people(people):
    if not people:
        print("No contacts found.")
        return

    for i, person in enumerate(people):
        age = calculate_age(person["dob"])
        print(i + 1, "-", person["name"], "|", age, "|", person["dob"], "|", person["tag"])

def delete_contact(people):
    display_people(people)

    while True:
        number = input("Enter a number to delete: ")
        try:
            number = int(number)
            if number <= 0 or number > len(people):
                print("Invalid number, out of range.")
            else:
                break
        except:
            print("Invalid number")

    people.pop(number - 1)
    print("Person deleted.")

def search(people):
    query = input("Search name or tag: ").lower().strip()
    results = []

    for person in people:
        if query in person["name"].lower() or query in person["tag"].lower():
            results.append(person)

    display_people(results)

print("Hi, welcome to the Contact Management System.")
print()

with open("contacts.json", "r") as f:
    people = json.load(f)["contacts"]

while True:
    print()
    print("Contact list size:", len(people))
    command = input("You can 'Add', 'Delete' or 'Search' and 'Q' for quit: ").lower()

    if command == "add":
        person = add_person()
        people.append(person)
        print("Person added!")
    elif command == "delete":
        delete_contact(people)
    elif command == "search":
        search(people)
    elif command == "q":
        break
    else:
        print("Invalid command.")

with open("contacts.json", "w") as f:
    json.dump({"contacts": people}, f)