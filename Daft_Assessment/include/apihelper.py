import os
import logging
import json
import requests

class APIHelper:
    def __init__(self):
        '''
            The default constructor.
        '''
        logging.debug("APIHelper: Inside init.")
        try:
            #Global variables
            #self.headers={"Vary": "X-Origin; Origin,Accept-Encoding","Content-Type": "application/json; charset=UTF-8","Date": "Mon, 26 Sep 2016 16:44:30 GMT","Expires": "Mon, 26 Sep 2016 16:44:30 GMT","Cache-Control": "private, max-age=0","X-Content-Type-Options": "nosniff","X-Frame-Options": "SAMEORIGIN","X-Xss-Protection": "1; mode=block","Server": "GSE","Alt-Svc": "quic=\":443\"; ma=2592000; v=\"36,35,34,33,32\"","Accept-Ranges": "none","Transfer-Encoding": "chunked"}
            self.headers ={}
            #self.headers={"Cache-Control": "no-cache, no-store, max-age=0, must-revalidate","Pragma": "no-cache","Expires": "Mon, 01 Jan 1990 00:00:00 GMT","Date": "Wed, 28 Sep 2016 08:24:21 GMT","Vary": "X-Origin; Origin,Accept-Encoding","Content-Type": "application/json; charset=UTF-8","X-Content-Type-Options": "nosniff","X-Frame-Options": "SAMEORIGIN","X-Xss-Protection": "1; mode=block","Server": "GSE","Alt-Svc": "quic=\":443\";ma=2592000; v=\"36,35,34,33,32\"","Accept-Ranges": "none","Transfer-Encoding": "chunked"}
        except:
            logging.exception("APIHelper: Exception occurred in init: ")
        finally:
            logging.debug("APIHelper: Leaving init.")
            
    def getResponseMsg(self,url=None,jsonpara=None):
        '''
            Function for get Response from url
            Parameters:
            @param url: url.
            @param jsonpara: json parameter.
        '''
        try:
            logging.debug("APIHelper: Inside getResponseMsg.")
            data = json.dumps(jsonpara)
            responseOutput = requests.post(url, data=json.dumps(jsonpara), headers=self.headers)
            #print responseOutput.history
            #print responseOutput.raw
            #print responseOutput.elapsed
            #print responseOutput.content
            #print responseOutput.json
            #print responseOutput.text
            #print responseOutput.raise_for_status
            #For successful API call, response code will be 200 (OK)
            if responseOutput.ok:
                logging.debug("APIHelper: Leaving getResponseMsg.")
                return(responseOutput.content)
            else:
                logging.error("APIHelper: Got error in response message.")
                logging.debug("APIHelper: Leaving getResponseMsg.")
                return(responseOutput.content)
        except:
            logging.exception("APIHelper: Exception occurred in getResponseMsg: ")
            return False
    
    def validateResponse(self, expecte_output=None, actule_output=None):
        '''
            Function for validate the output
            Parameters:
            @param expecte_output: 
            @param actule_output:
        '''
        try:
            logging.debug("APIHelper: Inside validateResponse.")
            expecte_output = json.loads(expecte_output)
            actule_output  = json.loads(actule_output) 
            
            for key in set(expecte_output) & set(actule_output):
                if expecte_output[key] == actule_output[key]:
                    logging.debug("Successfully matched both the response message")
                    return True
                else:
                    logging.debug("Failed to matched both the response message")
                    return False        
        except:
            logging.exception("APIHelper: Exception occurred in validateResponse: ")
            return False
            
if __name__ == "__main__":
    apiobj = APIHelper()
    #ret = apiobj.test()
    #print ret
  
    jsonPara = {"homeMobileCountryCode": 310,"homeMobileNetworkCode": 260,
                "radioType": "gsm",
                "carrier": "T-Mobile",
                "cellTowers": [
                               {
                                "cellId": 39627456,
                                "locationAreaCode": 40495,
                                "mobileCountryCode": 310,
                                "mobileNetworkCode": 260,
                                "age": 0,
                                "signalStrength": -95
                                }
                               ],
                "wifiAccessPoints": [
                                     {
                                      "macAddress": "01:23:45:67:89:AB",
                                      "signalStrength": 8,
                                      "age": 0,
                                      "signalToNoiseRatio": -65,
                                      "channel": 8
                                      }
                                     ]
}

    ret = apiobj.getResponseMsg(url="https://www.googleapis.com/geolocation/v1/geolocate?key= AIzaSyAKC3sgc1iixalipAnijFc6pL2CflpTg24", jsonpara=jsonPara)
    print ret
