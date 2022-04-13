# -*- coding: utf-8 -*-
"""
Created on Wed Apr 13 17:46:37 2022

@author: Steven Najem
"""
import os
import dataserver, app, testclient, videoclient



#Simple initial attribute variables 
CurrentWorkingDirectory = os.getcwd()
ListStringAccepts = ["","y","yes","yeet", "yeah", "yt", "yu"]
ListStringDecline = ["n","no",""]
ConfigFile = ""
#Simple initial attribute variables

#Introduction and config file selection
inputSelectConfigFile = input("Hello! \n Please enter the name of the config" +
                              " file you would like to use:\n" +
                              "(If you would like to do a test just press enter)\n")

if inputSelectConfigFile == "":
    ConfigFile = "test.json"

else:
    ConfigFile = inputSelectConfigFile 
    print("Custom Input selected")
    
print("You have selected this as the config file:\n " 
      + CurrentWorkingDirectory + "/" + ConfigFile
      + "Would you like to use the same config file for all of the files?\n")
#Introduction and config file selection

ConfigFile = CurrentWorkingDirectory + "/" + ConfigFile

#Use a single config file for all files being opened
isUseForAll = input("(Press enter for yes or type 'N' for no")
isUseForAll = isUseForAll.lower()

if (isUseForAll == "") or (isUseForAll in ListStringAccepts):
    isUseForAll = 1
elif isUseForAll in ListStringDecline:
    isUseForAll = 0
    

dataserver #--config = ConfigFile
app #--config = ConfigFile
testclient #--config = ConfigFile
videoclient #--config = ConfigFile