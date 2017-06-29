'''
Verify daft.ie website end to end scenario
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
2- Click on sale tab
3- Select Dublin city
4- Click on advance search tab
5- Add random price range, bedroom and bathrooms
6- Select any random property
7- Verify bathrooms and bedroom equals to the search criteria. 
'''
TEST_CASE_NAME = "Verify daft.ie website end to end scenario"
TEST_SCRIPT = "TC_02_EndToEndScenario"
START_TIME = None
END_TIME = None
config = Config(["config"])

class TC_02_EndToEndScenario(BaseTest):
    
    def __init__(self):
        ''' __init__ function '''
        print "Verify daft.ie website end to end scenario"
    
    def init(self):
        ''' init function:  '''
        logging.debug("TC_02_EndToEndScenario: Inside init()")
        if config.parenttest == "":
            config.parenttest = "TC_02_EndToEndScenario"
        # Get the object of the helper class
        self.baseuihelpobj = BaseUIHelper()
        self.execute_msg = ""
        logging.debug("TC_02_EndToEndScenario: Leaving init()")
        return True
    
    def execute(self):
        ''' execute function '''
        logging.debug("TC_02_EndToEndScenario: Inside execute()")
        result = self.baseuihelpobj.clickOnRandomProperty(config.sale_tab)
        if result:
            logging.info("Successfully got the random property")
        else:
            self.execute_msg += "Failed not able to got the random property."
            logging.debug("Failed not able to got the random property")
            return False
        logging.debug("TC_02_EndToEndScenario: Leaving execute()")
        return True
        
    def verify(self):
        ''' verify function'''
        logging.debug("TC_02_EndToEndScenario: Inside verify()")
        result = self.baseuihelpobj.validateBedAndBath(bed=config.bedroom ,bath=config.bathroom)
        if result:
            logging.info("Successfully got the random property")
        else:
            self.execute_msg += "Failed not able to got the random property."
            logging.debug("Failed not able to got the random property")
            return False
        logging.debug("TC_02_EndToEndScenario: Leaving verify()")
        return True
        
    def cleanup(self):
        ''' cleanup function'''
        logging.debug("TC_02_EndToEndScenario: Inside cleanup()")
        if config.parenttest == "TC_02_EndToEndScenario":
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
        logging.debug("TC_02_EndToEndScenario: Leaving cleanup()")
        self.execute_msg += "Cleanup successful."
        return True
        
if __name__ == "__main__":
    TEST_STATUS = "Failed"
    OLD_FMT = '%d/%m/%y %H:%M:%S'
    START_TIME = time.strftime(OLD_FMT)
    try:
        TESTOBJ = TC_02_EndToEndScenario()
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