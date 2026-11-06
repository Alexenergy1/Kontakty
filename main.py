
import json
import os

FILE_NAME = "contacts.json"


def load_contacts():
    if not os.path.exists(FILE_NAME):
        return []

    try:
        with open(FILE_NAME, "r", encoding="utf-8") as file:
            data = json.load(file)
            return data if isinstance(data, list) else []
    except (json.JSONDecodeError, OSError):
        return []


def save_contacts(contacts):
    with open(FILE_NAME, "w", encoding="utf-8") as file:
        json.dump(contacts, file, indent=4, ensure_ascii=False)


def add_contact(contacts):
    first_name = input("First name: ").strip()
    last_name = input("Last name: ").strip()
    phone = input("Phone number: ").strip()
    email = input("Email: ").strip()

    if not first_name or not last_name or not phone:
        print("Error: Required fields cannot be empty.")
        return

    contact = {
        "id": max((c["id"] for c in contacts), default=0) + 1,
        "first_name": first_name,
        "last_name": last_name,
        "phone": phone,
        "email": email,
        "group": "General"
    }

    contacts.append(contact)
    save_contacts(contacts)
    print("Contact added successfully.")


def list_contacts(contacts):
    if not contacts:
        print("No contacts found.")
        return

    for contact in contacts:
        print(
            f'{contact["id"]}. '
            f'{contact["first_name"]} {contact["last_name"]} | '
            f'{contact["phone"]} | {contact["email"]}'
        )


def main():
    contacts = load_contacts()

    while True:
        print("\nCONTACT MANAGEMENT")
        print("1. Add contact")
        print("2. List contacts")
        print("0. Exit")

        choice = input("Choose an option: ").strip()

        if choice == "1":
            add_contact(contacts)
        elif choice == "2":
            list_contacts(contacts)
        elif choice == "0":
            print("Goodbye!")
            break
        else:
            print("Invalid menu option.")


if __name__ == "__main__":
    main()
