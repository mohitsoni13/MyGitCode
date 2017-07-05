'''
TC_005 - Removed 3 parameters(age,signalStrength,timingAdvance) from cellTowers

'''
import sys
import logging
import traceback
import time
import os
import json
CURRENT_PATH = os.getcwd()
if "include" in CURRENT_PATH:
    LIB_PATH = CURRENT_PATH.split("include")[0] + "include"
elif "bin" in CURRENT_PATH:
    LIB_PATH = CURRENT_PATH.split("bin")[0] + "include"
elif "TestCase" in CURRENT_PATH:
    LIB_PATH = CURRENT_PATH.split("TestCase")[0] + "include"
if LIB_PATH not in sys.path:
    sys.path.append(LIB_PATH)
from config import Config
from commonhelper import CommonHelp
from apihelper import APIHelper

# Highlevel steps for this automation
'''
Removed 3 parameters (age,signalStrength,timingAdvance) from cellTowers
Verify the response message
'''
TEST_CASE_NAME = "Removed 3 parameters(age,signalStrength,timingAdvance) from cellTowers"
TEST_SCRIPT = os.path.basename(__file__).split(".")[0]
START_TIME = None
END_TIME = None
config = Config(["config"])
class TC_005():
    ''' TC_005_1726293 '''
    def __init__(self):
        ''' __init__ function '''        
        print TEST_SCRIPT+":Removed 3 parameters(age,signalStrength,timingAdvance) from cellTowers."
        
    def init(self):
        ''' init function:  '''
        logging.debug(TEST_SCRIPT+": Inside init()")
        if config.parenttest == "":
            config.parenttest = TEST_SCRIPT
        # Get the object of the helper class
        self.commonHelpObj = CommonHelp()
        self.apihelperobj = APIHelper()
        self.execute_msg = ""
        self.output = {"location":{"lat":1.352083,"lng":103.819836},"accuracy":16850.0}        
        self.output = json.dumps(self.output)
        logging.debug(TEST_SCRIPT+": Leaving init()")
        return True
                          
    def execute(self):
        ''' execute function '''
        logging.debug(TEST_SCRIPT+": Inside execute()")
        try: 
            self.urlResult = self.apihelperobj.getResponseMsg(config.url, jsonpara=config.remove3Para)
            if self.urlResult:
                logging.debug("Successfully get the response message")
                return True
            else:
                self.execute_msg += "Failed to get the response message."
                logging.debug("Failed to get the response message.")
                return False
        except:
            self.execute_msg += "Exception occurred in execute."
            logging.exception(TEST_SCRIPT+": Exception occurred in execute:")
            return False
        finally:
            logging.debug(TEST_SCRIPT+": Leaving execute()")
        
    
    def verify(self):
        ''' verify function'''
        logging.debug(TEST_SCRIPT+": Inside verify()")
        try:
            urlResult = self.apihelperobj.validateResponse(self.urlResult,self.output)
            if urlResult:
                logging.debug("Successfully matched the response message")
                return True
            else:
                self.execute_msg += "Failed to matched the error response message."
                logging.debug("Failed to matched the error response message")
                return False
        except:
            self.execute_msg += "Exception occurred in verify."
            logging.exception(TEST_SCRIPT+": Exception occurred in verify:")
            return False
        finally:
            logging.debug(TEST_SCRIPT+": Leaving verify()")
            
    def cleanup(self):
        ''' cleanup function'''
        logging.debug(TEST_SCRIPT+": Inside cleanup()")
        if config.parenttest == TEST_SCRIPT:
            config.parenttest = ""
        self.execute_msg += "Cleanup Successful."
        logging.debug(TEST_SCRIPT+": Leaving cleanup()")
        return True

if __name__ == "__main__":
    TEST_STATUS = "Failed"
    OLD_FMT = '%d/%m/%y %H:%M:%S'
    START_TIME = time.strftime(OLD_FMT)
    try:
        TESTOBJ = TC_005()
        commonhelperobj = CommonHelp()
        # Logging the message in to log file 
        commonhelperobj.writeToLogFile(TEST_SCRIPT)
        # Perform test case operations
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
        TB_FORMAT = traceback.format_exc()
        REPLACES = TB_FORMAT.replace("\n", "")
        logging.debug("TC_005 test case: Exception: " + REPLACES)
    logging.info("Result of testcase %s: %s" % (TEST_CASE_NAME, TEST_STATUS))
    commonhelperobj.saveResultsOfTestcase(TEST_SCRIPT, START_TIME, TEST_STATUS, END_TIME, TESTOBJ.execute_msg)
    sys.exit(RETURN_VAL)