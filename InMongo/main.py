import logging
from datetime import date

from pymongo.client_session import ClientSession
from menu_definitions import (menu_mainME, add_select, delete_select, list_select,
                              select_select, update_select, debug_select,
                              yes_no, transmission_type)
# Note that until you import your SQLAlchemy declarative classes, such as Manufacturer, Python
# will not execute that code, and SQLAlchemy will be unaware of the mapped table.
from Menu import Menu
from input_utilities import input_int_range, input_float_range
from CommandLogger import CommandLogger, log
from pymongo import monitoring, MongoClient
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



if __name__ == '__main__':
    print('Starting in main.')
    cluster = 'mongodb+srv://shawnlin26:NJOaZV3P2P9M6LXu@cluster0.whilp.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0'
    monitoring.register(CommandLogger())
    mongoengine.connect('Demonstration', host=cluster)
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
