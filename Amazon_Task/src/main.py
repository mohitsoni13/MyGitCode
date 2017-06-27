import os
import logging
import config
import csv
import re

class Student(object):
    ''' Student class '''
    def getDataFromFile(self, filepath=config.path):
        '''
        getDataFromFile() : Read the student ID, date and score from the CSV file and return a list
        @param CSV file path
        @return: List
        '''
        try:
            with open(filepath, 'rU') as f:
                reader = csv.reader(f)
                list = []
                for row in reader:
                    dict = {}
                    l = len(list)
                    #for i in range(1,l):
                    dict["ID"] = row[0]
                    dict["Date"] = row[1]
                    dict["Score"] = row[2]
                    #newList.append(dict)
                    list.append(dict)
                return list
        except:
            logging.exception("Student::exception in getDataFromFile")
            return None
        finally:
            logging.debug("Student::exit getDataFromFile")
       
       
    def getStudentScore(self, id, list):
        '''
        getStudentScore() : return the score
        @param list
        @return: score
        '''
        try:
            score = []
            for i in list:
                if id in i['ID']:
                    score.append(int (i['Score']))
            score.sort()
            return score
        except:
            logging.exception("Student::exception in getStudentScore")
            return None
        finally:
            logging.debug("Student::exit getStudentScore")        
    
    def getAverage(self, scoreList):
        '''
        getStudentScore() : return the average
        @param score list
        @return: average score
        '''
        try:
            scoreCount = 0
            totalScore = 0
            if scoreList == None:
                return False
            else:
                l =  len(scoreList)
                if l < 5:
                    scoreCount = l
                else:
                    scoreCount = 5
                for i in range(0, scoreCount):
                    totalScore = totalScore+ scoreList[i]
                averageScore = float (totalScore / scoreCount)
                return averageScore
        except:
            logging.exception("Student::exception in getAverage")
            return None
        finally:
            logging.debug("Student::exit getAverage")
            
    def checkFormat(self,studentID):
        '''
        Function for check the student id format
        @para student id
        @return: return True if id is successful
        '''
        try:
            if re.search('STD', studentID):
                return True
            else:
                return False
        except:
            logging.exception("Student::exception in checkFormat")
            return None
        finally:
            logging.debug("Student::exit checkFormat")
                   
if __name__ == '__main__':
    Studobj = Student()
    file_output = Studobj.getDataFromFile()
    print "~~~~~ Student id sample STD1, STD2, STD3 ~~~~~~"
    student_id = raw_input("Enter student id: ")
    if Studobj.checkFormat(student_id):
        student_score = Studobj.getStudentScore(student_id,file_output)
        average_score = Studobj.getAverage(student_score)
        print average_score
    else:
        print "Improper format please try again later"
    