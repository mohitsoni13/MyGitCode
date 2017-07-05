import sys
import platform
import re
import os
import urllib2
if not re.search("bin", os.getcwd()):
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
if (platform.system() == "Linux"):
    sys.path.append('../..')
    sys.path.insert( 0, '..//include' )
else:
    sys.path.append('../..')
    sys.path.insert( 0, '..\\include' )
from config import Config
import unittest
import subprocess
import time
import traceback
import shutil
import logging
from commonhelper import CommonHelp
import concurrent.futures
import glob
import datetime
from lockfile import FileLock, AlreadyLocked, LockTimeout, linklockfile
config = Config(["all"])
currentpath =  os.getcwd()
print currentpath
if re.search("bin",currentpath):
    respath = currentpath.split("bin")[0]
lockfile=respath + "autoprog"
lock = FileLock(lockfile)
windows_flag = True if platform.system() == "Windows" else False
#checking and enabling the lock 
if lock.is_locked():
    print "Mutex lock present task in progress"
    print lock.path, 'is locked.'
    sys.exit(0)
else:
    logging.info("file is unlock - acquireing the lock")
    #acquire the lock 
    lock.acquire()
    print "Mutex Lock acquired on file"
    print lock.path, 'is locked.'

def info():
    logging.info("Starting script to parse  and run the test")
            
# Execute Test Case(s) in the test suite path                
def executetestcasenew(testsuite, testsuitepath, testcaselist):
    logging.debug("Inside executetestcasenew.")
    currentpath =  os.getcwd()
    if re.search("bin",currentpath):
        respath = currentpath.split("bin")[0]
    finaltestsuitepath = respath +  testsuitepath
    if type(testcaselist) is list:
        gettestcaselist = testcaselist
    else:
        gettestcaselist = testcaselist.split(",")
    for testcase in gettestcaselist:
        testcasefile = testcase + ".py"
        testcase = finaltestsuitepath + testcasefile
        logging.info("Executing Test Case " + testcasefile + " in " + finaltestsuitepath)    
        try:
            print "Running test script:%s" % testcasefile
            retval=subprocess.call( ["python", testcase],\
                    stdout=subprocess.PIPE, stderr=subprocess.PIPE,shell=False)
            if retval:
                print "%s script passed" % testcasefile
                logging.info("%s script passed" % testcasefile)
            else:
                print "%s script failed" % testcasefile
                logging.info("%s script failed" % testcasefile)
            print "sleep for 5 sec - before next test start"
            time.sleep(5)
        except:
            print "Test Case Suite " + testsuite + " was not loaded from the path " + testsuitepath
            logging.exception("Test Case Suite " + testsuite + " was not loaded from the path " + testsuitepath)
    logging.debug("Leaving executetestcasenew.")

testCaseExecutionTimes = {"total": "", "API" : "", "UI" : ""}

def Task_API():
    logging.info("Start API test cases" )
    start_time = datetime.datetime.now().replace(microsecond = 0)
    if "api" in config.api_testcase_csv:
        api_testcase_list = get_test_cases("api_suite", config.testsuitepath, config.api_testcase_csv, config.api_exclude_tests)
    executetestcasenew(config.testsuite, config.testsuitepath, api_testcase_list)
    end_time = datetime.datetime.now().replace(microsecond = 0)
    testCaseExecutionTimes["API"] = str(end_time - start_time)   
    
def Task_UI():
    logging.info("Start UI test cases" )
    start_time = datetime.datetime.now().replace(microsecond = 0)
    if "ui" in config.ui_testcase_csv:
        ui_testcase_list = get_test_cases("ui_suite", config.testsuitepathui, config.ui_testcase_csv, config.ui_exclude_tests)
    executetestcasenew(config.testsuite, config.testsuitepathui, ui_testcase_list)
    end_time = datetime.datetime.now().replace(microsecond = 0)
    testCaseExecutionTimes["UI"] = str(end_time - start_time) 

def get_test_cases(test_suite_name, test_suite_path, test_csv_file, exclude_test_cases):
    """ Read the test case from csv file and execute the test case
        Parameters:
            @param test_suite_name: Test suite name 
            @param test_suite_path: Test suite path
            @param test_csv_file: test csv file name
            @param exclude_test_cases: exclude test suite
        Return Values:
            Test case list if able to get the test case list from csv file
            Otherwise return None.
        """
    try:
        logging.debug("Start: Inside get_test_cases")
        testcase_list = []
        csv_file_path = os.getcwd().split("bin")[0] + test_suite_path + test_csv_file
        file_handle = open(csv_file_path, "r")
        test_cases = file_handle.read()
        test_case_list = test_cases.split("\n")
        for test in test_case_list:
            if re.match(r'\s|\#', test):
                continue
            if test and test.split("\\")[0] not in exclude_test_cases:
                testcase_list.append(test)
        print testcase_list
        return testcase_list
    except:
        logging.exception("Start: found exception in get_test_cases")
        return None
    finally:
        logging.debug("Start: Leaving get_test_cases")

def is_function_exist(func_name, func_dict):
    try:
        if func_dict[func_name]:
            return True
    except KeyError:
        logging.error("%s is wrong task function, check the task function name" % func_name)
        return False
    except:
        tb = traceback.format_exc()
        replaces = tb.replace("\n", "")
        logging.error("exception:" + replaces)
        return False

def sequential_task(prod_list):
    ''' This function will run the task in a sequence'''
    logging.debug("Inside sequential_task()")
    for product in prod_list:
        if is_function_exist(product,func_dict):
            eval(product+'()')
    logging.debug("Leaving sequential_task()")

def testcaseRunner():
    try:
        commonhelperobj = CommonHelp()
        commonhelperobj.writeToLogFile("starttest")
        info()
        currentpath = os.getcwd()
        respath = currentpath.split("bin")[0]
        if platform.system() == "Windows":
            finalresultpath = respath + "log\\"
        else:
            finalresultpath = respath + "log//"
        resultsfile = finalresultpath + config.g_resultfile + "-" + time.strftime("%d-%m-%Y")+ ".log"
        filehandle = open(resultsfile, "w")
        filehandle.close()
        try:
            logging.debug("Inside ThreadPoolExecutor try block()")
            total_product_list = []
            temp_seq_product_list = []
            if config.g_sequential_product:
                if type(config.g_sequential_product) == list:
                    total_product_list.append(config.g_sequential_product)
                else:
                    temp_seq_product_list.append(config.g_sequential_product)
                    total_product_list.append(temp_seq_product_list)
            if config.g_concurrent_product:
                if type(config.g_concurrent_product) == list:
                    total_product_list.extend(config.g_concurrent_product)
                else:
                    total_product_list.append(config.g_concurrent_product)
            print "Complete product list to run the test:  " + str(total_product_list)
            total_threads_required = len(total_product_list)
            with concurrent.futures.ThreadPoolExecutor(max_workers = total_threads_required) as executor:
                for product in total_product_list:
                    if str(type(product)) == "<type 'list'>" and config.g_sequential == True:
                        sequential_task(product)
                    elif str(type(product)) == "<type 'str'>" and config.g_concurrent == True:
                        if is_function_exist(product,func_dict):
                            executor.submit(eval(product))
            logging.debug("Leaving ThreadPoolExecutor try block()")
        except:
            tb_format = traceback.format_exc()
            excepstr = tb_format.replace("\n", "")
            print excepstr
            logging.error("Thread Pool Executor: Exception :" + str(excepstr))
    except:
        tb_format = traceback.format_exc()
        excepstr = tb_format.replace("\n", "")
        print excepstr
        logging.error("testcaseRunner :" + str(excepstr))
        
#--------------------Begining of the Test execution --------------------------
try:
    #The start time of the test suite
    TEST_SUITE_START_TIME = datetime.datetime.now().replace(microsecond = 0)
    # Before executing the test, capturing all function name define in the Start.py
    func_dict = {}
    func_dict = locals()
    testcaseRunner()        
    #The end time of the test suite
    TEST_SUITE_END_TIME = datetime.datetime.now().replace(microsecond = 0)
    testCaseExecutionTimes['total'] = str(TEST_SUITE_END_TIME - TEST_SUITE_START_TIME)
finally:
    #Release the Lock
    lock.release()