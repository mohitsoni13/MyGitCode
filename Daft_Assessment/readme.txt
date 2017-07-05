Basic setup:
============
1- Install eclipse with PyDev setup.
   http://www.pydev.org/manual_101_install.html

2- Install python 2.7 (python-2.7.11.amd64.msi)
   https://www.python.org/downloads/release/python-2711/
	
3- Install PIP 
   ->Download the packege (pip-8.1.2.tar.gz (md5, pgp)) from below link
     https://pypi.python.org/pypi/pip#downloads
   ->Install PIP
	-Open command prompt and run below command
   	 Downloads\pip-8.1.2>setup.py install
4- Download python futures
   https://pypi.python.org/pypi/futures
   ->Open command prompt and run below command
     Downloads\futures-3.0.5>setup.py install

4- Now go this path "C:\Python27\Scripts" and install below packages
   Open command prompt and run below command
   - pip install lockfile
   - pip install selenium

5- Download firefox browser and installed

How to execute test cases:
=========================

1- If you want to run test cases in suite.
   Start.py - Path - Daft_Assessment\bin\Start.py
   Just run Start.py script

2- If you want to run the test cases individual.
   API_Task - TC Path - Daft_Assessment\TestCase\API_TC\testcases
   UI_TASK - TC Path - C:\Users\msoni1\workspace\Daft_Assessment\TestCase\UI_TC\uitestcases
	
Log File:
=========
Once the test run completed logs and summaryresult log will be created in below path.
Log Path - Daft_Assessment\log