from Menu import Menu
from Option import Option

#Main menu
menu_mainME = Menu('main', 'Please select one of the following options:', [
    Option("Add new instance", "add(sess)"),
    Option("Delete existing instance", "delete(sess)"),
    Option("List existing instances", "list_members(sess)"),
    Option("Select existing instance", "select(sess)"),
    Option("Update existing instance", "update(sess)"),
    Option("Exit", "pass")
])

#Add Instances
add_select = Menu('add select', 'Which type of object do you want to add?:', [
    Option("Department", "add_department(sess)"),
    Option("Course", "add_course(sess)"),
    Option("Catalog", "add_degreeCatalog(sess)"),
    Option("Course Requirement", "add_CourseRequirement(sess)"),
    Option("Exit", "pass")
])

#Delete Instances
delete_select = Menu('delete select', 'Which type of object do you want to delete?:', [
    Option("Department", "delete_department(sess)"),
    Option("Course", "delete_course(sess)"),
    Option("Degree Catalog", "delete_degree_catalog(sess)"),
    Option("Full Time Instructor", "delete_full_timer(sess)"),
    Option("Part Time Instructor", "delete_part_timer(sess)"),
    Option("Exit", "pass")
])

# List Instructuors In an Office
list_select = Menu('list select', 'Which type of object do you want to list?:', [
    Option("Departments", "list_departments(sess)"),
    Option("Courses", "list_courses(sess)"),
    Option("Degree Catalogs", "list_degree_catalogs(sess)")


])

# Select instances
select_select = Menu('select select', 'Which type of object do you want to select:', [
    Option("Departments", "print(select_department(sess))"),
    Option("Courses", "print(select_course(sess))"),
    Option("Degree Catalogs", "print(select_degree_catalogs(sess))"),
    Option("Exit", "pass")
])


# Updating Instances
update_select = Menu('update select', 'Which type of object do you want to update:', [
    Option("Update Department", "update_department(sess)"),
    Option("Update Course", "update_course(sess)"),
    Option("Exit", "pass")
])

# A menu to prompt for the amount of logging information to go to the console.
debug_select = Menu('debug select', 'Please select a debug level:', [
    Option("Informational", "logging.INFO"),
    Option("Debug", "logging.DEBUG"),
    Option("Error", "logging.ERROR")
])

# A menu to prompt for the amount of logging information for MongoEngine.
menu_logging = Menu('debug', 'Please select the logging level from the following:', [
    Option("Debugging", "logging.DEBUG"),
    Option("Informational", "logging.INFO"),
    Option("Error", "logging.ERROR")
])

yes_no = Menu("yes/no", 'Answer yes or no:', [
    Option('Yes', 'yes'),
    Option('No', 'no')
])