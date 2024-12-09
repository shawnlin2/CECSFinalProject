from Menu import Menu
from Option import Option

#Main menu
menu_main = Menu('main', 'Please select one of the following options:', [
    Option("Add new instance", "add(sess)"),
    Option("Delete existing instance", "delete(sess)"),
    Option("List existing instances", "list_members(sess)"),
    Option("Update existing instance", "update(sess)"),
    Option("Exit", "pass")
])

#Add Instances
add_select = Menu('add select', 'Which type of object do you want to add?:', [
    Option("Building", "add_building(sess)"),
    Option("A Shared Room Office", "add_shared_room(sess)"),
    Option("A Single Room Office", "add_single_room(sess)"),
    Option("Full Time Instructor", "add_full_timer(sess)"),
    Option("Part Time Instructor", "add_part_timer(sess)"),
    Option("Exit", "pass")
])

#Delete Instances
delete_select = Menu('delete select', 'Which type of object do you want to delete?:', [
    Option("Building", "delete_building(sess)"),
    Option("A Shared Room Office", "delete_shared_room(sess)"),
    Option("A Single Room Office", "delete_single_room(sess)"),
    Option("Full Time Instructor", "delete_full_timer(sess)"),
    Option("Part Time Instructor", "delete_part_timer(sess)"),
    Option("Exit", "pass")
])

# List Instructuors In an Office
list_select = Menu('list select', 'Which type of object do you want to list?:', [
    Option("Instructors In Office", "list_employee_in_office(sess)"),
])

# Updating Instances
update_select = Menu('update select', 'Which type of object do you want to update:', [
    Option("Update Building", "update_building_name(sess)"),
    Option("Update Instructor Name", "update_instructor_name(sess)"),
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
