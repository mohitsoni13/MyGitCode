"""
helper lib to parse the ini file
"""
import os
import logging
import traceback
import glob
import re
import platform

class Config(object):
    """ config class to parse the ini files"""
    def __init__(self, products):
        '''
        The parameterized constructor.
        '''
        logging.debug("config: Inside __init__")
        if platform.system() == "Windows":
            self.windows_flag = True
        else:
            self.windows_flag = False
        self.PATH_TO_BIN = self.path_to_bin()
        if len(products) > 0 and products[0].lower() == "all":
            products = self.fetch_all_ini()
        else:
            self.append_to_config("config")
        for product in products:
            self.append_to_config(product)
        logging.debug("config: Leaving __init__")
    def fetch_all_ini(self):
        '''
            Fetches names of all ini files
            under bin.
        '''
        logging.debug("config: Inside fetch_all_ini")
        try:
            filename = (self.PATH_TO_BIN + "\\*.ini") if self.windows_flag else (self.PATH_TO_BIN + "/*.ini")
            file_list = glob.glob(filename)
            if self.windows_flag: file_list = [x.split("\\")[-1].split(".")[0] for x in file_list]
            else: file_list = [x.split("/")[-1].split(".")[0] for x in file_list]
            logging.debug("config: Leaving fetch_all_ini")
            return file_list
        except:
            tb_format = traceback.format_exc()
            replaces = tb_format.replace("\n", "")
            logging.error("config: fetch_all_ini: " + replaces)
            logging.error("config: Leaving fetch_all_ini")
    def path_to_bin(self):
        '''
            Fetches path to bin folder.
        '''
        logging.debug("config: Inside path_to_bin")
        path = os.getcwd()
        if "bin" in path: return (path + "\\") if self.windows_flag else (path + "/")
        elif "include" in path: path = path.split("include")[0]
        elif "TestCase" in path: path = path.split("TestCase")[0]
        path = (path + "bin\\") if self.windows_flag else (path + "bin/")
        logging.debug("config: Leaving path_to_bin")
        return path
    def append_to_config(self, product=None):
        '''
            Reads the data in product file and
            adds to the config file.
        '''
        logging.debug("config: Inside append_to_config")
        try:
            config_base_path = self.path_to_bin()
            product_ini = config_base_path + product + ".ini"
            config_file_handle = open(product_ini, "r")
            config_data = config_file_handle.readlines()
            value = None
            for line in config_data:
                if ":" in line:
                    if platform.system() == "Windows":
                        val = line.split(":", 1)[1].strip()
                    else:
                        val = line.split(":", 1)[1].strip().replace("\\", "/")
                    if ("list" in line.split(":", 0)[0].strip().lower() or "," in val) and not "{" in val:
                        if val == '':
                            value = []
                        else:
                            value = [x.strip() for x in val.split(",")]
                    elif re.match(r'^[0-9]+$', val):
                        value = int(val)
                    elif "true" == val.lower():
                        value = True
                    elif "false" == val.lower():
                        value = False
                    elif re.match(r'^{.+:.+}$', val):
                        value = eval(val)
                    else:
                        value = val
                    setattr(self, line.split(":")[0].strip(), value)
            config_file_handle.close()
            logging.debug("config: Inside append_to_config")
        except:
            tb_format = traceback.format_exc()
            replaces = tb_format.replace("\n", "")
            logging.error("config: append_to_config: " + replaces)
            logging.error("config: Leaving append_to_config")

if __name__ == '__main__':
    config_obj = Config(['config'])
    print config_obj.g_resultfile
