from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
import logging
import time
from config import Config
config = Config(["config"])

DEFAULT_WAIT = 30

class BaseUIHelper:
    def __init__(self):
        '''
            The default constructor.
        '''
        logging.debug("BaseUIHelper: Inside init.")
        try:
            pass
        except:
            logging.exception("BaseUIHelper: Exception occurred in init: ")
        finally:
            logging.debug("BaseUIHelper: Leaving init.")
    
    def openURL(self, url=config.daft_url):
        '''
            Function to open Daft.ie site
            Parameters:
            @param url: Daft.ie url.
        '''
        logging.debug("BaseUIHelper: Inside openURL.")
        try:
            # Create a new instance of the Firefox driver
            self.driver = webdriver.Firefox()
            self.driver.get(url)
            self.driver.maximize_window()
            assert "No results found." not in self.driver.page_source
            expectedTitle = config.expectedtitle
            actualTitle = str(self.driver.title)
            #Matched both the title
            if expectedTitle == actualTitle:
                logging.info("Successfully open the Daft.ie site and matched the title also")
            else:
                logging.debug("Failed open the Daft.ie site and matched the title also")
                return False
            logging.debug("BaseUIHelper: Leaving openURL.")
            return True
        except:
            logging.exception("BaseUIHelper: Exception occurred in openURL: ")
            return None

    def clickOnSaleTab(self, xpath=None):
        '''
            Function to click on sale tab
            Parameters:
            @param xpath: need to pass xpath 
        '''
        logging.debug("BaseUIHelper: Inside clickOnSaleTab.")
        try:
            #open the page
            self.openURL()
            time.sleep(15)            
            #Click on sale tab
            element = WebDriverWait(self.driver, 20).until(EC.element_to_be_clickable((By.XPATH, xpath)));
            element.click();
            logging.debug("BaseUIHelper: Leaving clickOnSaleTab.")
            return True
        except:
            logging.exception("BaseUIHelper: Exception occurred in clickOnSaleTab: ")
            return None
        
    def clickOnCityOrCounty(self, xpath=None):
        '''
            Function to click on select city or county
            Parameters:
            @param xpath: need to pass xpath 
        '''
        logging.debug("BaseUIHelper: Inside clickOnCityOrCounty.")
        try:
            #Click on sale tab
            self.clickOnSaleTab(config.sale_tab)
            #Click city or country tab
            element = WebDriverWait(self.driver, 20).until(EC.element_to_be_clickable((By.XPATH, config.city_tab)));
            element.click();
            time.sleep(15)
            #Select Area (Dublin)
            selectArea_xpath = config.area_tab
            element = WebDriverWait(self.driver, 20).until(EC.element_to_be_clickable((By.XPATH, selectArea_xpath)));
            element.click();
            logging.debug("BaseUIHelper: Leaving clickOnCityOrCounty.")
            return True
        except:
            logging.exception("BaseUIHelper: Exception occurred in clickOnCityOrCounty: ")
            return None
    
    def clickOnAdvanceSearch(self, xpath=None):
        '''
            Function to click on advance search
            Parameters:
            @param xpath: need to pass xpath 
        '''
        logging.debug("BaseUIHelper: Inside clickOnAdvanceSearch.")
        try:
            #Click on city tab
            self.clickOnCityOrCounty(xpath)
            time.sleep(5)
            #Click on advance serach tab
            advanceSearch_xpath = config.advance_tab
            element = WebDriverWait(self.driver, 20).until(EC.element_to_be_clickable((By.XPATH, advanceSearch_xpath)));
            element.click();
            logging.debug("BaseUIHelper: Leaving clickOnAdvanceSearch.")
            return True
        except:
            logging.exception("BaseUIHelper: Exception occurred in clickOnAdvanceSearch: ")
            return None
    
    def selectPriceRang(self, xpath=None):
        '''
            Function to select price range
            Parameters:
            @param xpath: need to pass xpath 
        '''
        logging.debug("BaseUIHelper: Inside selectPriceRang.")
        try:
            #Click on advance search
            self.clickOnAdvanceSearch(xpath)
            time.sleep(5)
            #select min value
            element = WebDriverWait(self.driver, 20).until(EC.element_to_be_clickable((By.XPATH, config.min_tab)));
            element.click();
            #select min range
            element = WebDriverWait(self.driver, 20).until(EC.element_to_be_clickable((By.XPATH, config.priceMin_tab)));
            element.click();
            #select max value
            element = WebDriverWait(self.driver, 20).until(EC.element_to_be_clickable((By.XPATH, config.max_tab)));
            element.click();
            #select min range
            element = WebDriverWait(self.driver, 20).until(EC.element_to_be_clickable((By.XPATH, config.priceMax_tab)));
            element.click(); 
            logging.debug("BaseUIHelper: Leaving selectPriceRang.")
            return True
        except:
            logging.exception("BaseUIHelper: Exception occurred in selectPriceRang: ")
            return None
    
    def selectBedroomAndBathrooms(self, xpath=None):
        '''
            Function to select number of bedroom and bethroom
            Parameters:
            @param xpath: need to pass xpath 
        '''
        logging.debug("BaseUIHelper: Inside selectBedroomAndBathrooms.")
        try:
            #Click on price range
            self.selectPriceRang(xpath)
            time.sleep(5)
            #select bedroom tab
            element = WebDriverWait(self.driver, 20).until(EC.element_to_be_clickable((By.XPATH, config.bedroom_tab)));
            element.click();
            #select bedroom range
            element = WebDriverWait(self.driver, 20).until(EC.element_to_be_clickable((By.XPATH, config.bedroomNo_tab)));
            element.click();
            #select bathroom tab
            element = WebDriverWait(self.driver, 20).until(EC.element_to_be_clickable((By.XPATH, config.bathroom_tab)));
            element.click();
            #select bathroom range
            element = WebDriverWait(self.driver, 20).until(EC.element_to_be_clickable((By.XPATH, config.bathroomNo_tab)));
            element.click();
            #Click on search button
            element = WebDriverWait(self.driver, 20).until(EC.element_to_be_clickable((By.XPATH, config.search_tab)));
            element.click();
            time.sleep(30)
            logging.debug("BaseUIHelper: Leaving selectBedroomAndBathrooms.")
            return True
        except:
            logging.exception("BaseUIHelper: Exception occurred in selectBedroomAndBathrooms: ")
            return None
    
    def clickOnRandomProperty(self, xpath=None):
        '''
            Function to click on random property by xpath
            Parameters:
            @param xpath: need to pass xpath 
        '''
        logging.debug("BaseUIHelper: Inside clickOnRandomProperty.")
        try:
            #Select number of bedroom and bathroom
            self.selectBedroomAndBathrooms(xpath)
            time.sleep(5)
            #Click on random property  y xpath
            element = WebDriverWait(self.driver, 20).until(EC.element_to_be_clickable((By.XPATH, config.Random_tab)));
            element.click();
            time.sleep(30)
            logging.debug("BaseUIHelper: Leaving clickOnRandomProperty.")
            return True
        except:
            logging.exception("BaseUIHelper: Exception occurred in clickOnRandomProperty: ")
            return None
    
    def validateBedAndBath(self, bed=None ,bath=None):
        '''
            Function to validate bedroom and bathroom
            Parameters:
            @param xpath: need to pass string bed and bath
        '''
        try:
            #Verify 1Bath and 1Bed
            
            pageSourceOutput = self.driver.page_source
            #if "1 Bed" and "1 Bath" in pageSourceOutput:
            if bed and bath in pageSourceOutput:
                return True
            else:
                return False
            logging.debug("BaseUIHelper: Leaving clickOnSaleTab.")
            return True
        except:
            logging.exception("BaseUIHelper: Exception occurred in clickOnSaleTab: ")
            return None
    
    def closeDriver(self):
        '''
            Closes the driver.
        '''
        try:
            logging.debug("BaseUIHelper: Inside closeDriver.")
            self.driver.quit()
            logging.debug("BaseUIHelper: Leaving closeDriver.")
            return True
        except:
            logging.exception("BaseUIHelper: Exception occurred in closeDriver: ")
            return False


if __name__ == '__main__':
    objhelp = BaseUIHelper()
    #xpath = '/html/body/div[1]/div/div/main/div[1]/div[2]/div/div[2]/div/div/div[1]/ul[1]/li[2]/a'
    #xpath_1 = '/html/body/div[1]/div/div/header/div/div[2]/div/nav/div/ul[1]/li[2]/a'
    #xpath = '/html/body/div[3]/div[1]/div/form/span/div[1]/span[2]/div/dl/dt'
                    
    res = objhelp.clickOnRandomProperty(config.sale_tab)
    print res
    res2 = objhelp.validateBedAndBath(bed=config.bedroom ,bath=config.bathroom)
    print res2