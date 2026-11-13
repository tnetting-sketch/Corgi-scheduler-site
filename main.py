from drafter import *
from dataclasses import dataclass

set_website_title("Corgi Scheduler")
set_site_information(
    author = "Tyler Netting",
    description = "Schedulerer that finds days all members of a group are available",
    sources = "Drafter Docs,",
    planning = "plan.pdf",
    links = []
    )
# -------------------------
# DATA CLASSES
# -------------------------

@dataclass
class Person:
    name: str
    schedule: list[str]
    
@dataclass
class State:
    group_name: str
    people: list[Person]
    meeting_purpose: str
    meeting_location: str


# -------------------------
# HOME PAGE
# -------------------------

@route
def index(state: State) -> Page:
    return Page(state, [
        Header("Group Availability Scheduler"),
        "Find days when your whole group is free!",
        "Group: " + state.group_name,
        "Number of people: " + str(len(state.people)),
        Button("Create / Rename Group", "create_group_page"),
        Button("Add Person", "add_person_page"),
        Button("View Group", "view_group"),
        Button("Edit Availability", "edit_page"),
        Button("Remove Person", "remove_page"),
        Button("Check Group Availability", "available"),
        Button("Edit Group Details", "group_details_page")
    ])


# -------------------------
# CREATE GROUP
# -------------------------

@route
def create_group_page(state: State) -> Page:
    return Page(state, [
        Header("Create a Group"),
        "Enter your group name:",
        TextBox("group_name", state.group_name),
        Button("Save Group", "create_group"),
        Button("Home", "index")
    ])


@route
def create_group(state: State, group_name: str) -> Page:
    if group_name.strip() != "":
        state.group_name = group_name.strip()

    return index(state)


# -------------------------
# ADD PERSON
# -------------------------

@route
def add_person_page(state: State) -> Page:
    return Page(state, [
        Header("Add a Person"),
        "Enter the person's name:",
        TextBox("name"),
        "Enter available days separated by commas:",
        "Example: Monday, Wednesday, Friday",
        TextBox("days"),
        Button("Add Person", "add_person"),
        Button("Home", "index")
    ])


@route
def add_person(state: State, name: str, days: str) -> Page:

    if name.strip() == "":
        return Page(state, [
            "Please enter a name.",
            Button("Try Again", "add_person_page")
        ])

    # Convert the days into a list
    new_schedule = []

    for day in days.split(","):
        if day.strip() != "":
            new_schedule.append(day.strip().title())

    # Create a new Person
    new_person = Person(name.strip(), new_schedule)

    # Add the person to the group
    state.people.append(new_person)

    return view_group(state)


# -------------------------
# VIEW GROUP
# -------------------------

@route
def view_group(state: State) -> Page:

    content = [
        Header("Group Members"),
        "Group: " + state.group_name,
        "Number of people: " + str(len(state.people))
    ]

    if len(state.people) == 0:
        content.append("There are no people in this group.")

    for person in state.people:
        content.append("Name: " + person.name)
        content.append(
            "Available days: " + ", ".join(person.schedule)
        )

    content.append(Button("Home", "index"))

    return Page(state, content)


# -------------------------
# EDIT AVAILABILITY
# -------------------------

@route
def edit_page(state: State) -> Page:
    return Page(state, [
        Header("Edit Availability"),
        "Enter the name of the person you want to edit:",
        TextBox("target_name"),
        "Enter their new available days:",
        "Example: Monday, Tuesday, Thursday",
        TextBox("new_days"),
        Button("Save Changes", "edit"),
        Button("Home", "index")
    ])


@route
def edit(state: State, target_name: str,
         new_days: str) -> Page:

    for person in state.people:
        if person.name.lower() == target_name.strip().lower():

            new_schedule = []

            for day in new_days.split(","):
                if day.strip() != "":
                    new_schedule.append(day.strip().title())

            person.schedule = new_schedule

            return view_group(state)

    return Page(state, [
        "Person not found. Check the name and try again.",
        Button("Try Again", "edit_page"),
        Button("Home", "index")
    ])


# -------------------------
# REMOVE PERSON
# -------------------------

@route
def remove_page(state: State) -> Page:
    return Page(state, [
        Header("Remove a Person"),
        "Enter the name of the person to remove:",
        TextBox("target_name"),
        Button("Remove Person", "remove"),
        Button("Home", "index")
    ])


@route
def remove(state: State, target_name: str) -> Page:

    new_list = []

    for person in state.people:
        if person.name.lower() != target_name.strip().lower():
            new_list.append(person)

    state.people = new_list

    return view_group(state)

@route
def save_details(state: State,
                 meeting_purpose: str,
                 meeting_location: str) -> Page:

    if meeting_purpose.strip() != "":
        state.meeting_purpose = meeting_purpose

    if meeting_location.strip() != "":
        state.meeting_location = meeting_location

    return index(state)
    # Display the results
    content = [
        Header("Group Availability"),
        "Days when everyone is available:"
    ]

    if len(common_days) == 0:
        content.append("There are no days when everyone is available.")
    else:
        for day in common_days:
            content.append(day)

    content.append(Button("Home", "index"))

    return Page(state, content)

# -------------------------
# CHECK AVAILABILITY
# -------------------------

@route
def available(state: State) -> Page:

    if len(state.people) == 0:
        return Page(state, [
            Header("Group Availability"),
            "You need to add people first!",
            Button("Add Person", "add_person_page"),
            Button("Home", "index")
        ])

    # Start with the first person's available days
    common_days = state.people[0].schedule.copy()

    # Compare their days with everybody else's
    for person in state.people:

        days_to_keep = []

        for day in common_days:
            if day in person.schedule:
                days_to_keep.append(day)

        common_days = days_to_keep
      # Display the results
    content = [
        Header("Group Availability"),
        "Days when everyone is available:"
    ]

    if len(common_days) == 0:
        content.append("There are no days when everyone is available.")
    else:
        for day in common_days:
            content.append(day)

    content.append(Button("Home", "index"))

    return Page(state, content)
# -------------------------
# START APPLICATION
# -------------------------

start_server(State("", [],"",""))
