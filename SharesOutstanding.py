#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
Takes stock-symbol and goes to sec.gov,
finds the last 10-Q report for that company and
returns back 'shares outstanding' info, like:

- ex1:   "AMD'" the result is "999,407,216"
- ex2:   "KTOS" the result is " 103,297,525 "
- ex3    "INTC" the result is "4,564" etc
'''

import sys
from PyQt5 import QtWidgets, QtGui, uic
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import pandas as pd
import re
import os


# Import UI file created in QtDesigner
qtCreatorFile = "SharesOutstanding.ui"
Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)
 
class MyApp(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)
        self.pushButton.clicked.connect(self.getSharesOutstanding)
        # Button and lineEdit emits clicked signal when ENTER pressed
        self.pushButton.setAutoDefault(True)
        self.lineEdit.returnPressed.connect(self.getSharesOutstanding)
    
    def getSharesOutstanding(self):
        company = self.lineEdit.text()
        self.label_5.setText(company)

        #launch url
        url = "https://www.sec.gov"

        # create a new Firefox session
        driverPath = r'chromedriver_win32\chromedriver.exe'
        driver = webdriver.Chrome(driverPath)
        driver.implicitly_wait(30)
        driver.get(url)
        assert 'SEC.gov | HOME' in driver.title
        elem = driver.find_element_by_id('company-name')
        elem.clear()
        elem.send_keys(company)
        elem.send_keys(Keys.RETURN)

        # Scrap web page
        soup = BeautifulSoup(driver.page_source, 'lxml')
        # Grab the table from HTML page
        myTable = soup.find_all("table", {"class": "tableFile2"})[0]
        level1 = myTable.find('tbody')
        level2 = level1.findChildren()

        # If the row has 10-Q, click Interactive Data link
        for i in range(len(level2)):
            if level2[i].string == '10-Q':
                theALink = level2[i+3]
                break
        theHref = theALink['href']
        interactiveDocLink = url + theHref
        
        # Take 'share outstanding' from 2nd page
        driver.get(interactiveDocLink)
        soup = BeautifulSoup(driver.page_source, 'lxml')
        myTable2 = soup.find_all('table', {'class': 'report'})[0]
        allFromTable = myTable2.descendants
        
        for item in allFromTable:
            if item.string == 'Entity Common Stock, Shares Outstanding':
                theRow = item.parent
                theTdTag = theRow.find('td', {'class': 'nump'} )
                sharesOutstanding = theTdTag.next_element
                break
        # Get shares outstanding data in label
        self.label_3.setText(sharesOutstanding)
        driver.close()

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())