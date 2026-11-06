
import json
import os
import re

FILE_NAME = "contacts.json"


def load_contacts():
    if not os.path.exists(FILE_NAME):
        return []
    try:
        with open(FILE_NAME, "r", encoding="utf-8") as file:
            data = json.load(file)
            return data if isinstance(data, list) else []
    except (OSError, json.JSONDecodeError):
        print("Error loading contacts.")
        return []


def save_contacts(contacts):
    try:
        with open(FILE_NAME, "w", encoding="utf-8") as file:
            json.dump(contacts, file, indent=4, ensure_ascii=False)
        return True
    except OSError:
        print("Error saving contacts.")
        return False


def valid_phone(phone):
    return bool(re.fullmatch(r"\+?[0-9]{7,15}", phone))


def valid_email(email):
    return not email or bool(
        re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", email)
    )


def find_by_id(contacts, contact_id):
    for contact in contacts:
        if contact["id"] == contact_id:
            return contact
    return None


def get_contact_id():
    try:
        return int(input("Enter contact ID: "))
    except ValueError:
        print("Invalid ID.")
        return None


def add_contact(contacts):
    first_name = input("First name: ").strip()
    last_name = input("Last name: ").strip()
    phone = input("Phone number: ").strip()
    email = input("Email: ").strip()
    group = input("Group (default General): ").strip() or "General"

    if not first_name or not last_name:
        print("First name and last name are required.")
        return

    if not valid_phone(phone):
        print("Invalid phone number.")
        return

    if not valid_email(email):
        print("Invalid email address.")
        return

    contact = {
        "id": max((c["id"] for c in contacts), default=0) + 1,
        "first_name": first_name,
        "last_name": last_name,
        "phone": phone,
        "email": email,
        "group": group
    }

    updated = contacts + [contact]
    if save_contacts(updated):
        contacts.append(contact)
        print("Contact added successfully.")


def list_contacts(contacts):
    if not contacts:
        print("No contacts found.")
        return

    for contact in contacts:
        print(
            f'{contact["id"]}. '
            f'{contact["first_name"]} {contact["last_name"]} | '
            f'{contact["phone"]} | {contact["email"]} | '
            f'{contact["group"]}'
        )


def edit_contact(contacts):
    contact_id = get_contact_id()
    if contact_id is None:
        return

    contact = find_by_id(contacts, contact_id)
    if contact is None:
        print("Contact not found.")
        return

    print("Press Enter to keep the current value.")

    first_name = input("First name: ").strip() or contact["first_name"]
    last_name = input("Last name: ").strip() or contact["last_name"]
    phone = input("Phone number: ").strip() or contact["phone"]
    email = input("Email: ").strip() or contact["email"]
    group = input("Group: ").strip() or contact["group"]

    if not valid_phone(phone) or not valid_email(email):
        print("Invalid phone number or email.")
        return

    updated = [dict(c) for c in contacts]
    for item in updated:
        if item["id"] == contact_id:
            item.update({
                "first_name": first_name,
                "last_name": last_name,
                "phone": phone,
                "email": email,
                "group": group
            })
            break

    if save_contacts(updated):
        contacts[:] = updated
        print("Contact updated successfully.")


def delete_contact(contacts):
    contact_id = get_contact_id()
    if contact_id is None:
        return

    contact = find_by_id(contacts, contact_id)
    if contact is None:
        print("Contact not found.")
        return

    confirm = input("Delete this contact? (yes/no): ").strip().lower()
    if confirm != "yes":
        print("Deletion cancelled.")
        return

    updated = [c for c in contacts if c["id"] != contact_id]
    if save_contacts(updated):
        contacts[:] = updated
        print("Contact deleted successfully.")


def search_contacts(contacts):
    query = input("Search by name or phone: ").strip().lower()

    if not query:
        print("Search query cannot be empty.")
        return

    results = [
        c for c in contacts
        if query in c["first_name"].lower()
        or query in c["last_name"].lower()
        or query in c["phone"].lower()
    ]
    list_contacts(results)


def sort_contacts(contacts):
    print("1. Sort by first name")
    print("2. Sort by last name")
    choice = input("Choose an option: ").strip()

    if choice == "1":
        result = sorted(contacts, key=lambda c: c["first_name"].lower())
    elif choice == "2":
        result = sorted(contacts, key=lambda c: c["last_name"].lower())
    else:
        print("Invalid menu option.")
        return

    list_contacts(result)


def filter_contacts(contacts):
    group = input("Enter group: ").strip().lower()

    if not group:
        print("Group cannot be empty.")
        return

    results = [
        c for c in contacts
        if c["group"].lower() == group
    ]
    list_contacts(results)


def main():
    contacts = load_contacts()

    while True:
        print("\nCONTACT MANAGEMENT")
        print("1. Add contact")
        print("2. List contacts")
        print("3. Edit contact")
        print("4. Delete contact")
        print("5. Search contacts")
        print("6. Sort contacts")
        print("7. Filter by group")
        print("0. Exit")

        choice = input("Choose an option: ").strip()

        if choice == "1":
            add_contact(contacts)
        elif choice == "2":
            list_contacts(contacts)
        elif choice == "3":
            edit_contact(contacts)
        elif choice == "4":
            delete_contact(contacts)
        elif choice == "5":
            search_contacts(contacts)
        elif choice == "6":
            sort_contacts(contacts)
        elif choice == "7":
            filter_contacts(contacts)
        elif choice == "0":
            print("Goodbye!")
            break
        else:
            print("Invalid menu option.")


if __name__ == "__main__":
    main()
