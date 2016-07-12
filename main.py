from pygit2 import discover_repository
from argparse import ArgumentParser
from os import path
import logging
import sys

from scheduler import Scheduler
from gui.root import VisualBlame
from events import EventManager
from modules.module_event_config import module_events
from gui.widget_event_config import widget_event_listeners
from gui.widget_event_config import widget_event_triggers


# Function handling the input of the application. The application expects
# one command line argument containing the file path of the file to open
# the application with
def handle_argv():
    parser = ArgumentParser()
    parser.add_argument("file_path", type=str,
                        help="Path to the file to start the application with")

    file_path = parser.parse_args().file_path

    if not path.isfile(file_path):
        logging.error("Input: invalid file path")
        sys.exit()

    return file_path


def read_file(file_path):
    with open(file_path) as f:
        return f.read().splitlines()

# TODO remove this comment if not used
# 1. Get input file path - 2. Get absolute file path - 3. Get pygit2
# git dir using input file path. - 4. get file path rel to git dir path
# - 5. Init event manager - 6. Init scheduler with event manager, pygit2
# git dir and module config - 7. Get file contents using absolute path -
# 8. Init GUI with file contents, rel file path, event manager, event
# listen config and event trigger config
# CONCLUSION - Too much stuff going on here, should ideally be limited
# to handling input and initializing event manager/scheduler/gui
if __name__ == '__main__':
    file_path = handle_argv()
    file_path_abs = path.abspath(file_path)
    git_dir = discover_repository(file_path)
    file_path_rel = file_path_abs[len(git_dir) - 5:]

    event_manager = EventManager()
    scheduler = Scheduler(git_dir, event_manager, module_events)

    data = read_file(file_path_abs)

    gui = VisualBlame(data=data, file_path_rel=file_path_rel,
                      event_manager=event_manager,
                      widget_event_listeners=widget_event_listeners,
                      widget_event_triggers=widget_event_triggers)
    gui.run()
