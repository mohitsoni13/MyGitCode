import os
import logging
import time
import re
import platform
import traceback
import ConfigParser
from config import Config
import glob
config = Config(['config'])

class CommonHelp(object):
    """Common Helper class """
    def __init__(self):
        """Return  intialized the Global variable"""
        logging.debug("CommonHelp: Inside __init__")
        logging.debug("CommonHelp: Exit __init__")
    
    def saveResultsOfTestcase(self, testcase, starttime="", teststatus="", endtime="", msg=""):
        """
        save test case result in log folder
        Parameters:
            testcase: test script name
            starttime: start time of the test case
            teststatus: test case status
            endtime: end time of the test case
        """
        logging.debug("CommonHelp: Inside saveResultsOfTestcase")
        try:
            """Function save's the results of the Test Case in the Test Case Results File in the Cache Directory."""
            if config.parenttest != "" and config.parenttest != testcase:
                testcase = config.parenttest + "_" + testcase
            logging.debug("commonhelper: Inside save_results_of_testcase() for testcase %s " % testcase)
            respath = None
            currentpath = os.getcwd()
            if re.search("thirdparty", currentpath):
                respath = currentpath.split("thirdparty")[0]
            elif re.search("include", currentpath):
                respath = currentpath.split("include")[0]
            elif re.search("TestCase", currentpath):
                respath = currentpath.split("TestCase")[0]
            elif re.search("BVT_AWS", currentpath):
                respath = currentpath.split("BVT_AWS")[0]
            elif re.search("bin", currentpath):
                respath = currentpath.split("bin")[0]
            if platform.system() == "Windows":
                finalresultpath = respath + "log\\"
            else:
                finalresultpath = respath + "log//"
            summary_file =  [file for file in  glob.glob(finalresultpath + "*.log") if re.search("summary", file)]
            if summary_file:
                resultsfile = summary_file[0]
            else:
                resultsfile = finalresultpath + config.g_resultfile + "-" + time.strftime("%d-%m-%Y")+ ".log"    
            configdata = ConfigParser.RawConfigParser(allow_no_value=True)
            configdata.add_section(testcase + '_Status')
            # Save messages with | separated
            #configdata.set(testcase + '_Status', 'Info', "|".join(map(str, message)))
            configdata.set(testcase + '_Status', 'starttime', starttime)
            configdata.set(testcase + '_Status', 'Status', teststatus)
            configdata.set(testcase + '_Status', 'ExecutionState', msg)
            configdata.set(testcase + '_Status', 'endtime', endtime)
            logging.info("commonhelper: Saving Results of Test Case " + testcase + " in the File " + resultsfile)
            try:
                filehandle = open(resultsfile, "a")
                configdata.write(filehandle)
                filehandle.close()
            except:

                logging.exception("commonhelper: Failed to save Results of Test Case " + testcase + " in the File " + resultsfile)
                logging.info("commonhelper: Parameters were")
                logging.info("commonhelper: Info = " + str(starttime))
                logging.info("commonhelper: Info = " + str(teststatus))
                logging.info("commonhelper: Info = " + str(msg))
                logging.info("commonhelper: Info = " + str(endtime))
                exit(1)
            logging.debug("commonhelper: Leaving save_results_of_testcase()")
            logging.debug("CommonHelp: Exit saveResultsOfTestcase")
        except:
            tb_format = traceback.format_exc()
            replaces = tb_format.replace("\n", "")
            print replaces
            logging.error("commonhelper-saveResultsOfTestcase: Exception :" + str(replaces))
            
    def writeToLogFile(self, scriptname):
        """ write To Log File """
        logging.debug("CommonHelp: Inside writeToLogFile")
        try:
            respath = None
            currentpath = os.getcwd()
            if re.search("thirdparty", currentpath):
                respath = currentpath.split("thirdparty")[0]
            elif re.search("include", currentpath):
                respath = currentpath.split("include")[0]
            elif re.search("TestCase", currentpath):
                respath = currentpath.split("TestCase")[0]
            elif re.search("bin", currentpath):
                respath = currentpath.split("bin")[0]
            if platform.system() == "Windows":
                finallogpath = respath + "log\\"
            else:
                finallogpath = respath + "log//"
            logformat = '%(asctime)s - %(levelname)s - %(module)s - %(funcName)s - at line:  %(lineno)d  - %(message)s'
            dateformat = "%Y-%m-%d %H:%M:%S"
            if re.search("API_TC", scriptname):
                if platform.system() == "Windows":
                    logfolderpath = finallogpath + "API_TC" + "\\" + scriptname + "\\"
                else:
                    logfolderpath = finallogpath + "API_TC" + "//" + scriptname + "//"
            elif re.search("vcenter", scriptname):
                if platform.system() == "Windows":
                    logfolderpath = finallogpath + "UI_TC" + "\\" + scriptname + "\\"
                else:
                    logfolderpath = finallogpath + "UI_TC" + "//" + scriptname + "//"
            else:
                logfolderpath = finallogpath
            if os.path.isdir(logfolderpath):
                logging.info("Directory %s is already exist" %logfolderpath)
            else:
                os.makedirs(logfolderpath)
            logfilename = logfolderpath + scriptname + ".log"
            logging.getLogger('').handlers = []
            logging.basicConfig(filename=logfilename, filemode="w", level=config.g_loglevel, format=logformat, datefmt=dateformat)
            console = logging.StreamHandler()
            console.setLevel(logging.ERROR)
            logging.getLogger('').addHandler(console)
            logging.debug("CommonHelp: leaving writeToLogFile")
        except:
            tb_format = traceback.format_exc()
            replaces = tb_format.replace("\n", "")
            print replaces
            logging.error("commonhelper-uninstallExtension: Exception :" + str(replaces))
            
if __name__ == '__main__':
    COMMON_OBJ = CommonHelp()
    res = COMMON_OBJ.writeToLogFile()
    print res