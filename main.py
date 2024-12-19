
from pymongo.client_session import ClientSession

import certifi
from menu_definitions import (menu_mainME, add_select, delete_select, list_select, select_select,
                              update_select, debug_select,
                              yes_no)

from Menu import Menu
from CommandLogger import CommandLogger, log
from pymongo import monitoring, MongoClient
from Department import Department
from Course import Course
from Catalog import Catalog
from RequirementType import RequirementType
from CourseRequirement import CourseRequirement
from DegreeCatalog import *
from CatalogCourse import CatalogCourse
from Exclusive import Exclusive
from Inclusive import Inclusive
from Total import Total
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
            department = Department(name, abbreviation)
            department.save()
            valid = True
        except NotUniqueError as NUID:
            print(f'You violated a uniqueness constraint: {NUID}.  Try again')
        except ValidationError as VEND:
            print(f'You violated a validation constraint: {VEND}.')

def add_course(session: Session):
    valid: bool = False
    while not valid:
        department = select_department(session)
        course_num = input_int("Enter course number -->")
        course_name = input("Enter course name -->")
        units = input_int("Enter amount of units -->")
        lecture_hours = input_int("Enter number of lecture hours per week -->")

        try:
            course = Course(course_num, lecture_hours, course_name, units, department, department.abbreviation)
            course.save()
            department.add_course(course)
            department.save()
            valid = True
        except NotUniqueError as NUID:
            print(f'You violated a uniqueness constraint: {NUID}.  Try again')
        except ValidationError as VEND:
            print(f'You violated a validation constraint: {VEND}.')     

def add_degreeCatalog(session: Session):
    valid: bool = False
    while not valid:
        department = select_department(session)
        department.save()
        degreeType = input("Enter the title of the degree")
        totalUnits = input_int("How many units are Required for this Degree")

        try:
            catalog = DegreeCatalog(degree_type=degreeType,total_units=totalUnits,department=department, abbreviation= department.abbreviation)
            catalog.save()
            department.add_degreeCatalog(catalog)
            department.save()
            valid=True
        except NotUniqueError as NUID:
            print(f'You violated a uniqueness constraint: {NUID}.  Try again')
        except ValidationError as VEND:
            print(f'You violated a validation constraint: {VEND}.')   

def add_CourseRequirement(session:Session):
    valid: bool = False
    while not valid:
        degreeCat = select_degree_catalog(session)
        degreeCat.save()
        requirement_name = input("Enter the name of the requirement")
        total_points = input("Enter how many points the requirement is")
        try:
            courseRequirement = CourseRequirement(total_points=total_points, name=requirement_name,degree_catalog=degreeCat, degreeType= degreeCat.degreeType)
            courseRequirement.save()
            degreeCat.add_course_requirement()
            degreeCat.save()
            valid = True
        except NotUniqueError as NUID:
            print(f'You violated a uniqueness constraint: {NUID}.  Try again')
        except ValidationError as VEND:
            print(f'You violated a validation constraint: {VEND}.')   
def add_requirementType(session:Session):
    valid: bool = False
    while not valid:
        requirement_name = input("Enter the name of the requirement")
        try:
            requirementType = RequirementType(name=requirement_name)
            requirementType.save()
            valid = True
        except NotUniqueError as NUID:
            print(f'You violated a uniqueness constraint: {NUID}.  Try again')
        except ValidationError as VEND:
            print(f'You violated a validation constraint: {VEND}.')   


def add_Catalog(session:Session):
    vaild = False
    while not vaild:
        course_requirement = select_course_requirement(session)
        title = input("Enter a name")
        catalogType = input_int_range('Enter 1 for a Exclusive, 2 for an Inclusive, 3 for a Total')
        try:
            if catalogType == 1:
                catalog = Exclusive(title, course_requirement,course_requirement.name, course_requirement.degreeType, course_requirement.requirementTypeName)
            if catalogType == 2:
                catalog = Inclusive(title, course_requirement,course_requirement.name, course_requirement.degreeType, course_requirement.requirementTypeName)
            else:
                remainingUnit = input_int('Enter an amount of unit left')
                catalog = Exclusive(title, course_requirement,course_requirement.name, course_requirement.degreeType, course_requirement.requirementTypeName, remainingUnit)
            catalog.save()
            course_requirement.add_catalog(catalog)
            course_requirement.save()
        except NotUniqueError as NUID:
            print(f'You violated a uniqueness constraint: {NUID}.  Try again')
        except ValidationError as VEND:
            print(f'You violated a validation constraint: {VEND}.')   

def add_CatalogCourse(session:Session):
    vaild = False
    while not vaild:
        course = select_course(session)
        catalog = select_catalog(session)

        try:
            catalogCourse = CatalogCourse(catalog, course,catalog.title, 
                                          course.courseNum, course.abbreviation,
                                          catalog.name, catalog.degreeType, 
                                          catalog.requirementTypeName)
            catalogCourse.save()
            course.add_course_catalog(catalogCourse)
            course.save()
            catalog.add_catalog_course(catalogCourse)
            course.save()
        except NotUniqueError as NUID:
            print(f'You violated a uniqueness constraint: {NUID}.  Try again')
        except ValidationError as VEND:
            print(f'You violated a validation constraint: {VEND}.')   


def delete_department(session: Session):
    ok: bool = False
    while not ok:
        department: Department = select_department(session)
        
    
        pipeline = [
            {"$match": {"department": department.name}}
        ]
        course_count: int = len(list(Course.objects().aggregate(pipeline)))
        degree_count = len(list(DegreeCatalog.objects().aggregate(pipeline)))

        if course_count > 0 or degree_count > 0:
            print('Error, you cannot delete that department, there are child relationships to it.')
        else:
            department.delete()
            ok = True

def delete_department(session: Session):
    ok: bool = False
    while not ok:
        department: Department = select_department(session)
        
    
        pipeline = [
            {"$match": {"department": department.name}}
        ]
        course_count: int = len(list(Course.objects().aggregate(pipeline)))
        degree_count = len(list(DegreeCatalog.objects().aggregate(pipeline)))

        if course_count > 0 or degree_count > 0:
            print('Error, you cannot delete that department, there are child relationships to it.')
        else:
            department.delete()
            ok = True

#if this version doesn't work then replace with the above type of way 
def delete_course(session: Session):
    course: Course = select_course(session)
    if len(course.course_catologs) < 1:
        course.delete()

def delete_degreeCatalog(session: Session):
    degreeCatalog = select_degree_catalog(session)
    if len(degreeCatalog.course_requirement) < 1:
        degreeCatalog.delete()

def delete_catalog(session: Session):
    catalog:Catalog = select_catalog(session)
    if len(catalog.catalog_courses) < 1:
        catalog.delete()

def delete_course_requirement(session: Session):
    courseRequirement:CourseRequirement = select_course_requirement(session)
    if len(courseRequirement.catalogs) < 1:
        courseRequirement.delete()

def delete_catalogCourse(session:Session):
    catalogCourse = select_catalog_course()
    catalogCourse.delete()

def delete_requirementType(session: Session):
    requirementType:RequirementType = select_requirement_type(session)
    if len(requirementType.course_requirements) < 1:
        requirementType.delete()

def update_department(session: Session):
    department = select_department(session)
    newName = input(f'Current name is: {department.name}.  Enter new name -->')
    pipeline = [
        {"$match": {"department": department.name}}
    ]
    course_count: int = len(list(Course.objects().aggregate(pipeline)))
    degree_count = len(list(DegreeCatalog.objects().aggregate(pipeline)))

    if course_count > 0 or degree_count > 0:
         print('Error, you cannot delete that department, there are child relationships to it.')
         
    else:
        department.name = newName
        department.save()

def update_course(session: Session):
    course = select_department(session)
    newName = input(f'Current name is: {course.name}.  Enter new name -->')
    pipeline = [
        {"$match": {"department": course.name}}
    ]
    child_count: int = len(list(CatalogCourse.objects().aggregate(pipeline)))

    if child_count > 0:
        print('Error, you cannot update that course, there are courseCatalog related to it.')
    else:
        course.name = newName
        course.save()

def update_courseRequirement(session: Session):
    courseRequirement = select_course_requirement(session)
    newName = input(f'Current name is: {courseRequirement.name}.  Enter new name -->')
    pipeline = [
        {"$match": {"department": courseRequirement.name}}
    ]
    child_count: int = len(list(Catalog.objects().aggregate(pipeline)))

    if child_count > 0:
        print('Error, you cannot update that courseRequirement, there are catalogs that relate to it.')
    else:
        courseRequirement.name = newName
        courseRequirement.save()


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

def select_requirement_type(session: Session):
    found: bool = False
    while not found:
        requirmentName = input('Enter a requirementName')
        pipeline = [
            {"$match": {"name": requirmentName}}
        ]
        name_count = len(list(RequirementType.objects().aggregate(pipeline)))

        if name_count != 0:
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
    for requirementType in RequirementType.objects().aggregate(pipeline):
        return RequirementType.objects(id=requirementType.get('_id')).first()
    
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
def select_course_requirement(session: Session):
    found: bool = False
    while not found:
        degreeType = input("Degree type of the course requirement that you're looking for-->")
        requirementName = input("Enter a requirement name")
        courseRequirementName = input("Enter a course requirement name")
        pipeline = [
            {"$match": {'$and':[{"degreeType": degreeType},
                {'requirementTypeName' : requirementName},
                {'name': courseRequirementName}]}
             }
        ]
        courseRequirement_count = len(list(CourseRequirement.objects().aggregate(pipeline)))

        if courseRequirement_count != 0:
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
    for courseRequirement in CourseRequirement.objects().aggregate(pipeline):
        return CourseRequirement.objects(id=courseRequirement.get('_id')).first()
    
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

def select_degree_catalog(session:Session):
    found: bool = False
    while not found:
        
        degreetype = input('Enter a degree type')
        pipeline = [
            {"$match": {"degreeType": degreetype}}
        ]
        degreetype_count = len(list(DegreeCatalog.objects().aggregate(pipeline)))

        if degreetype_count != 0:
            found = True
        else:
            print("That degreeCatalog could not be found.  Try again.")
    """
    MongoEngine returns an iterable of documents (Python dictionaries) from the aggregate 
    function.  But I need the actual object to operate on.  The document includes the _id 
    value, so I perform yet another query, but this time NOT using the aggregate pipeline,
    to return just the first object that comes back from looking for the manufacturer by 
    the _id value.  MongoDB makes sure that _id is always unique.  Note that MongoENGINE
    knows the _id field as just 'id'."""
    for degreeCatalog in DegreeCatalog.objects().aggregate(pipeline):
        return DegreeCatalog.objects(id=degreeCatalog.get('_id')).first()


def select_catalog(session: Session):
    found: bool = False
    while not found:
        courseRequirement = select_course_requirement(session)
        title = input('Enter the title')
        pipeline = [
            {"$match": {"$and": [{"degreeType": courseRequirement.degreeType},
                                 {"requirementTypeName": courseRequirement.requirementTypeName},
                                 {"course_requirementName": courseRequirement.name},
                                 {'title': title}
                                 ]}}
        ]
        catalog_count = len(list(Catalog.objects().aggregate(pipeline)))

        if catalog_count != 0:
            found = True
        else:
            print ("That course could not be found.  Try again.")
    """
    MongoEngine returns an iterable of documents (Python dictionaries) from the aggregate
    function.  But I need the actual object to operate on.  The document includes the _id
    value, so I perform yet another query, but this time NOT using the aggregate pipeline,
    to return just the first object that comes back from looking for the manufacturer by
    the _id value.  MongoDB makes sure that _id is always unique.  Note that MongoENGINE
    knows the _id field as just 'id'."""
    for catalog in Catalog.objects().aggregate(pipeline):
        return Catalog.objects(id=catalog.get('_id')).first()

def select_catalog_course(session: Session):
    found: bool = False
    while not found:
        course = select_course(session)
        catalog = select_catalog(session)
        pipeline = [
            {"$match": {"$and": [{"degreeType": catalog.degreeType},
                                 {"requirementTypeName": catalog.requirementTypeName},
                                 {"course_requirementName": catalog.name},
                                 {'title': catalog.title},
                                 {'abbreviation': course.abbreviation},
                                 {'courseNum': course.courseNum}
                                 ]}}
        ]
        catalogCourse_count = len(list(CatalogCourse.objects().aggregate(pipeline)))

        if catalogCourse_count != 0:
            found = True
        else:
            print ("That course could not be found.  Try again.")
    """
    MongoEngine returns an iterable of documents (Python dictionaries) from the aggregate
    function.  But I need the actual object to operate on.  The document includes the _id
    value, so I perform yet another query, but this time NOT using the aggregate pipeline,
    to return just the first object that comes back from looking for the manufacturer by
    the _id value.  MongoDB makes sure that _id is always unique.  Note that MongoENGINE
    knows the _id field as just 'id'."""
    for catalogCourse in CatalogCourse.objects().aggregate(pipeline):
        return CatalogCourse.objects(id=catalogCourse.get('_id')).first()

def list_departments(session: Session):
    departments: [Department] = Department.objects().order_by('+name')
    for department in departments:
        print(department)

def list_courses(session: Session):
    courses: [Course] = Course.objects().order_by('+courseNum')
    for course in courses:
        print(course)

def list_degree_catalogs(session: Session):
    degree_catalogs: [DegreeCatalog] = DegreeCatalog.objects().order_by('+abbreviation')
    for degree_catalog in degree_catalogs:
        print(degree_catalog)

def list_course_requirements(session: Session):
    course_requirements: [CourseRequirement] = CourseRequirement.objects().order_by('+name')
    for course_requirement in course_requirements:
        print(course_requirement)

def list_catalog_courses(session: Session):
    catalog_courses: [CatalogCourse] = CatalogCourse.objects().order_by('+title')
    for catalog_course in catalog_courses:
        print(catalog_course)

def list_catalogs(session: Session):
    catalogs: [Catalog] = Catalog.objects().order_by('+title')
    for catalog in catalogs:
        print(catalog)

def list_requirement_types(session: Session):
    requirement_types: [RequirementType] = RequirementType.objects().order_by('+name')
    for requirement_type in requirement_types:
        print(requirement_type)



if __name__ == '__main__':
    print('Starting in main.')
    # client = pymongo.MongoClient('mongodb+srv://eduardomartinez215:Supertruck1!@323-fall.kchj8.mongodb.net/?retryWrites=true&w=majority&appName=323-Fall', tlsCAFile=certifi.where())
    monitoring.register(CommandLogger())
    # mongoengine.connect('Demonstration', host='mongodb+srv://shawnlin26:QkPN3GaNpM7blXXr@cluster0.rndwk.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0')
    mongoengine.connect('MECluster',
                        host='mongodb+srv://bryantieu41:AXW42FenGyxSnMGr@mecluster.zuxps.mongodb.net/?retryWrites=true&w=majority&appName=MECluster',
                        tlsCAFile=certifi.where())
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
