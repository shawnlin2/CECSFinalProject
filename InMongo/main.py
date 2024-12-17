import logging
from datetime import date

from mongoengine import NotUniqueError, OperationError, ValidationError
from pymongo.client_session import ClientSession

from Catalog import Catalog
from InMongo.CourseRequirement import CourseRequirement
from menu_definitions import (menu_mainME, add_select, delete_select, list_select, select_select,
                              update_select, debug_select,
                              yes_no)
# Note that until you import your SQLAlchemy declarative classes, such as Manufacturer, Python
# will not execute that code, and SQLAlchemy will be unaware of the mapped table.
from Menu import Menu
from CommandLogger import CommandLogger, log
from pymongo import monitoring, MongoClient
from Department import Department
from Course import Course

from DegreeCatalog import *
from input_utilities import *

import mongoengine

class Session(ClientSession):
    """I'm hoping to be able to actually use the Session in the transactions in this eventually,
    so I'm faking it here with this class definition."""
    pass

def menu_loop(menu: Menu, sess: Session):
    """Little helper routine to just keep cycling in a menu until the user signals that they
    want to exit.
    :param  menu:   The menu that the user will see.
    :param  sess:   The database connect session that the operation selected will use."""
    action: str = ''
    while action != menu.last_action():
        action = menu.menu_prompt()
        print('next action: ', action)
        exec(action)


def add(session: Session):
    """Top level menu prompt for any add operation."""
    menu_loop(add_select, session)


def list_members(session: Session):
    """Top level menu prompt for any list members operation."""
    menu_loop(list_select, session)


def select(session: Session):
    """Top level menu prompt for any select operation."""
    menu_loop(select_select, session)


def delete(session: Session):
    """Top level menu prompt for any delete operation."""
    menu_loop(delete_select, session)

def update(session: Session):
    """Top level menu prompt for any update operation."""
    menu_loop(update_select, session)
# ------------------------------------------------------------------------------------
def add_department(session: Session):
    valid: bool = False
    while not valid:
        name = input("Enter department's name -->")
        abbreviation = input("Enter department's abbreviation -->")

        try:
            department = Department(name, abbreviation,)
            department.save()
            valid = True
        except NotUniqueError as NUID:
            print(f'You violated a uniqueness constraint: {NUID}.  Try again')

def add_course(session: Session):
    valid: bool = False
    while not valid:
        department = select_department(session)
        department.save()
        course_num = input_int("Enter course number -->")
        course_name = input("Enter course name -->")
        units = input_int("Enter amount of units -->")
        lecture_hours = input_int("Enter number of lecture hours per week -->")

        try:
            course = Course(course_num, lecture_hours, course_name, units, department)
            course.save()
            valid = True
        except NotUniqueError as NUID:
            print(f'You violated a uniqueness constraint: {NUID}.  Try again')

def add_degreeCatalog(session: Session):
    valid: bool = False
    while not valid:
        department = select_department(session)
        department.save()
        degreeType = input("Enter the title of the degree")
        totalUnits = input_int("How many units are Required for this Degree")


        try:
            catalog = DegreeCatalog(degree_type=degreeType,total_units=totalUnits,department=department)
            catalog.save()
            valid=True
        except NotUniqueError as NUID:
            print(f'You violated a uniquenss constrains: {NUID} Try again')

def add_CourseRequirement(session:Session):
    valid: bool = False
    while not valid:
        degreeCat = select_degree_catalogs(session)
        degreeCat.save()
        requirement_name = input("Enter the name of the requirement")
        total_points = input("Enter how many points the requirement is")
        try:
            courseRequirement = CourseRequirement(total_points=total_points, name=requirement_name,degree_catalog=degreeCat)
            courseRequirement.save()
            valid = True
        except NotUniqueError as NUID:
            print(f'You violated a uniquenss constrains {NUID} try again')


def delete_department(session: Session):
    ok: bool = False
    while not ok:
        department: Department = select_department(session)
        pipeline = [
            {"$match": {"abbreviation": department.abbreviation}}
        ]
        abbreviation_count = len(list(Department.objects().aggregate(pipeline)))
        print(department)
        try:
            department.delete()
            ok = True
            print(f'Department {department.name} deleted.')
        except OperationError as VE:
            print(f"Error: {VE}")


def delete_course(session: Session):
    course: Course = select_course(session)
    course.delete()

def update_department(session: Session):
    department = select_department(session)
    newName = input(f'Current name is: {department.name}.  Enter new name -->')
    pipeline = [
        {"$match": {"department": department.name}}
    ]
    child_count: int = len(list(Course.objects().aggregate(pipeline)))

    if child_count > 0:
        print('Error, you cannot update that department, there are courses offered by it.')
    else:
        department.name = newName
        department.save()

def select_department(session: Session) -> Department:
    found: bool = False
    while not found:
        abbreviation = input("Abbreviation of the department that you're looking for-->")
        pipeline = [
            {"$match": {"abbreviation": abbreviation}}
        ]
        abbreviation_count = len(list(Department.objects().aggregate(pipeline)))

        if abbreviation_count != 0:
            found = True
        else:
            print("That department could not be found.  Try again.")
    """
    MongoEngine returns an iterable of documents (Python dictionaries) from the aggregate 
    function.  But I need the actual object to operate on.  The document includes the _id 
    value, so I perform yet another query, but this time NOT using the aggregate pipeline,
    to return just the first object that comes back from looking for the manufacturer by 
    the _id value.  MongoDB makes sure that _id is always unique.  Note that MongoENGINE
    knows the _id field as just 'id'."""
    for department in Department.objects().aggregate(pipeline):
        return Department.objects(id=department.get('_id')).first()


# def select_office(session:Session):
#     print("Searching for that specific office:  ")
#     buildingName = input("Enter the name of the building por favor: ")
#     officeNum = input("Enter that office num")
#     try:
#         building = Building.objects(name = buildingName).first()
#         office = Office.objects(number = officeNum).first()
#
#         if building and office:
#             print("Office found")
#             return office
#         else:
#             print("No office was found with thos details")
#     except Exception as e:
#         print(f"Error locating {e}")

def select_course(session: Session):
    print("Searching for that specific course: ")
    department_name = input("Enter the department name --> ")
    course_num = input("Enter the course number --> ")
    try:
        department = Department.objects(name=department_name).first()
        course = Course.objects(courseNum=course_num).first()

        if department and course:
            print("Course found")
            return course
        else:
            print("No course was found with those details")
    except Exception as e:
        print(f"Error locating course: {e}")

def select_degree_catalogs(session:Session):
    print("Searching for a Degree Catalog")
    department_name = input("Enter the Department")
    degreeCat = input("Enter the Degree Type")
    try:
        department = Department.objects(name = department_name).first()
        degreeCat = DegreeCatalog.objects(degree_type= degreeCat).first()

        if department and degreeCat:
            print("Degree Catalog Found")
            return degreeCat
        else:
            print("No Degree Catalog was found")
    except Exception as e:
        print(f'Error Occured {e}')


# def select_course(session: Session) -> Course:
#     found: bool = False
#     while not found:
#         department = select_department(sess)
#         course_num = input_int("Number of course you're looking for -->")
#         pipeline = [
#             {"$match": {"$and": [{"department": department.id},
#                                  {"course_num": course_num},
#                                  ]}}
#         ]
#         course_count = len(list(Course.objects().aggregate(pipeline)))
#
#         if course_count != 0:
#             found = True
#         else:
#             print ("That course could not be found.  Try again.")
#     """
#     MongoEngine returns an iterable of documents (Python dictionaries) from the aggregate
#     function.  But I need the actual object to operate on.  The document includes the _id
#     value, so I perform yet another query, but this time NOT using the aggregate pipeline,
#     to return just the first object that comes back from looking for the manufacturer by
#     the _id value.  MongoDB makes sure that _id is always unique.  Note that MongoENGINE
#     knows the _id field as just 'id'."""
#     for course in Course.objects().aggregate(pipeline):
#         return Course.objects(id=course.get('_id')).first()






if __name__ == '__main__':
    print('Starting in main.')
    # client = pymongo.MongoClient('mongodb+srv://eduardomartinez215:Supertruck1!@323-fall.kchj8.mongodb.net/?retryWrites=true&w=majority&appName=323-Fall', tlsCAFile=certifi.where())
    monitoring.register(CommandLogger())
    mongoengine.connect('Demonstration', host='mongodb+srv://eduardomartinez215:Supertruck1!@323-fall.kchj8.mongodb.net/?retryWrites=true&w=majority&tlsInsecure=true&appName=323-Fall')
    db = mongoengine.connection.get_db()
    """This actually initiates a session at the PyMongo layer of the software architecture, but
    I cannot get MongoEngine to actually use it.  So I'm paving the way to do that eventually 
    (since I'm hoping that MongoEngine eventually supports passing the Session in to the 
    save method) to be prepared, and to look as much like the SQLAlchemy code as I can."""
    sess: Session = db.client.start_session()
    main_action: str = ''
    while main_action != menu_mainME.last_action():
        main_action = menu_mainME.menu_prompt()
        print('next action: ', main_action)
        exec(main_action)
    log.info('All done for now.')