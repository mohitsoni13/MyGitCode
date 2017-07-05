import logging
import sys
import os

class BaseTest:
    """
    BaseTest is abstract base class for Testcase objects and each
    Testcase class must derive from this class.  If derived class
    do not define any of the functions, an exception of type
    NotImplementedException will be thrown
    """
    def __init__(self):
        pass

    def init(self):
        logging.debug("Checking if user is 'root'")
        if os.getuid() != 0 :
            logging.error("Script must be run as root")
            return 1
        
        return 0

    def execute(self):
        raise NotImplementedException("Must be implemented in subclass")

    def verify(self):
        raise NotImplementedException("Must be implemented in subclass")

    def cleanup(self):
        raise NotImplementedException("Must be implemented in subclass")

    def __del__(self):
        pass