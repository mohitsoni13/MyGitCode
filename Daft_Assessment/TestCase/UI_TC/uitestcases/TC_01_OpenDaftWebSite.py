'''
Open the URL - Daft.ie
'''
import sys
import logging
import time
import os
current_path = os.getcwd()
if "include" in current_path:
    lib_path = current_path.split("include")[0] + "include"
elif "bin" in current_path:
    lib_path = current_path.split("bin")[0] + "include"
elif "TestCase" in current_path:
    lib_path = current_path.split("TestCase")[0] + "include"
if lib_path not in sys.path:
    sys.path.append(lib_path)
from config import Config
from CommonTest import BaseTest
from commonhelper import CommonHelp
from baseuihelper import BaseUIHelper
'''
1- Open the Daft.ie website in firefox browser
2- Verify the title page - Daft.ie - Property for sale and houses for sale or rent in Ireland
'''
TEST_CASE_NAME = "Open the URL - Daft.ie"
TEST_SCRIPT = "TC_01_OpenDaftWebsite"
START_TIME = None
END_TIME = None
config = Config(["config"])

class TC_01_OpenDaftWebsite(BaseTest):
    
    def __init__(self):
        ''' __init__ function '''
        print "Open the URL - Daft.ie"
    
    def init(self):
        ''' init function:  '''
        logging.debug("TC_01_OpenDaftWebsite: Inside init()")
        if config.parenttest == "":
            config.parenttest = "TC_01_OpenDaftWebsite"
        # Get the object of the helper class
        self.baseuihelpobj = BaseUIHelper()
        self.execute_msg = ""
        logging.debug("TC_01_OpenDaftWebsite: Leaving init()")
        return True
    
    def execute(self):
        ''' execute function '''
        logging.debug("TC_01_OpenDaftWebsite: Inside execute()")
        result = self.baseuihelpobj.openURL(url=config.daft_url)
        if result:
            logging.info("Successfully open the Daft.ie website")
        else:
            self.execute_msg += "Failed not able to open the Daft.ie website."
            logging.debug("Failed not able to open the Daft.ie website")
            return False
        logging.debug("TC_01_OpenDaftWebsite: Leaving execute()")
        return True
        
    def verify(self):
        ''' verify function'''
        logging.debug("TC_01_OpenDaftWebsite: Inside verify()")
        # TODO - Need to add code for verify the page
        return True
        logging.debug("TC_01_OpenDaftWebsite: Leaving verify()")
        
    def cleanup(self):
        ''' cleanup function'''
        logging.debug("TC_01_OpenDaftWebsite: Inside cleanup()")
        if config.parenttest == "TC_01_OpenDaftWebsite":
            config.parenttest = ""
        ret = self.baseuihelpobj.closeDriver()
        if ret == True:
            logging.info("Successfully closed the Driver")
        else:
            self.execute_msg += "Failed to closed the Driver."
            logging.info("Failed to closed the Driver")
            return False
        if self.baseuihelpobj:
            self.baseuihelpobj= None
        logging.debug("TC_01_OpenDaftWebsite: Leaving cleanup()")
        self.execute_msg += "Cleanup successful."
        return True
        
if __name__ == "__main__":
    TEST_STATUS = "Failed"
    OLD_FMT = '%d/%m/%y %H:%M:%S'
    START_TIME = time.strftime(OLD_FMT)
    try:
        TESTOBJ = TC_01_OpenDaftWebsite()
        COMMONHELP_OBJ = CommonHelp()
        # Loging the message in to log file
        COMMONHELP_OBJ.writeToLogFile(TEST_SCRIPT)
        # Perform testcase operations
        RETURN_VAL = TESTOBJ.init()
        # Perform execute once initialization succeeds...
        if RETURN_VAL == True:
            RETURN_VAL = TESTOBJ.execute()
        # Once execution succeeds, perform verification...
        if RETURN_VAL == True:
            RETURN_VAL = TESTOBJ.verify()
        # Perform testcase cleanup
        CLEANUP_RETURN_VAL = TESTOBJ.cleanup()
        if RETURN_VAL and CLEANUP_RETURN_VAL:
            TEST_STATUS = "Passed"
        END_TIME = time.strftime(OLD_FMT)
        print TEST_STATUS
    except:
        END_TIME = time.strftime(OLD_FMT)
        logging.exception(TEST_SCRIPT + ": Exception: ")
        logging.info("Result of testcase %s: %s" % (TEST_CASE_NAME, TEST_STATUS))
    COMMONHELP_OBJ.saveResultsOfTestcase(TEST_SCRIPT, START_TIME, TEST_STATUS, END_TIME, TESTOBJ.execute_msg)
    sys.exit(RETURN_VAL)
