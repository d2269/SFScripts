"""
The script is created for cleaning profiles and permsets. If it does not find a component in the project that has a permission, permission is deleted.
The script logs all its actions by output information to the console.
The script creates a corresponding file for each metadata with the data that it deleted.
To work correctly, specify the full path to the project in the pathDX variable.
"""

import os
from os import path
import xml.dom.minidom as minidom

# path dx project
pathDX = "C:\\dx-project"
pathScript = os.path.dirname(os.path.abspath(__file__))+ '\\'

# get name of titeles
def getTitles(xml , typeFile):
    sections = {
        "applicationVisibilities":["application", "\\applications\\", ".app-meta.xml"] , 
        "classAccesses":["apexClass", "\\classes\\", ".cls-meta.xml"], 
        "fieldPermissions":["field","\\objects\\", "\\fields\\", ".field-meta.xml"], 
        "flowAccesses":["flow" , "\\flows\\", ".flow-meta.xml"], 
        "layoutAssignments":["layout", "\\layouts\\", ".layout-meta.xml"], 
        "objectPermissions":["object", "\\objects\\"], 
        "pageAccesses":["apexPage", "\\pages\\", ".page-meta.xml"], 
        "recordTypeVisibilities":["recordType", "\\objects\\","\\recordTypes\\",".recordType-meta.xml"], 
        "tabVisibilities":["tab", "\\tabs\\", ".tab-meta.xml"]
        }
    doc = minidom.parse(xml)
    node = doc.documentElement    
       
    for section in sections.keys():
        tegs = doc.getElementsByTagName(section) 
        for teg in tegs:            
            titleObj = teg.getElementsByTagName(sections.get(section)[0])[0]
            nodes = titleObj.childNodes
            for node in nodes:
                if node.nodeType == node.TEXT_NODE:
                    check = checking(node.data , sections.get(section)) #check file and dir exist 
                    if check == "False":
                        # create log file 
                        fullName = path.basename(xml)
                        name = path.splitext(fullName)[0]
                        index = name.index('.')                        
                        with open(pathScript + typeFile + "_" +name[:index]+"_log.txt", 'a+') as f:                       
                            f.writelines(node.data + " "+ section +"\n")                    
                            f.close()
                            teg.parentNode.removeChild(teg)                       
    
        # edit profile    
        with open(xml,"w") as fs:
            fs.write(doc.toxml())
            fs.close()        
    
# checking for file availability
def checking(name, section):
    if len(section) == 2:
        pathdir = pathDX + section[1] + name
        if os.path.isdir(pathdir): # does the file exist?
            return "True"
    elif len(section) == 3:
        pathfile = pathDX + section[1] + name + section[2]
        if os.path.isfile (pathfile): # does the file exist?
            return "True"
    elif len(section) == 4:
        names = name.split('.')    
        pathdir = pathDX + section[1] + names[0]
        #print(pathdir)        
        if os.path.isdir (pathdir):    # does the dir exist?
            pathfile = pathdir + section[2] + names[1] + section[3]
            if os.path.isfile (pathfile): # does the file exist?
                return "True"        
    return "False"

def processTheProfile():
    pathProfile = pathDX +"\\profiles\\"
    profiles = os.listdir(pathProfile)
    print(len(profiles)," profiles found")
    c = 0
    for profile in profiles:
        c += 1
        print (profile , " in progress ", len(profiles)-c, "profiles left" )
        fullPathProfile = pathProfile + profile

        from_file = open(fullPathProfile) 
        lineOld = from_file.readline() # save 1st string
        lineOld2 = from_file.readline() # save 2nd string 

        '''
        beginning of the file content:
        <?xml version="1.0" encoding="utf-8"?><Profile xmlns="http://soap.sforce.com/2006/04/metadata">
        or
        <?xml version="1.0" encoding="utf-8"?>
        <Profile xmlns="http://soap.sforce.com/2006/04/metadata">        
        '''
        if  "soap.sforce.com" in lineOld2:
            lineOld = lineOld + '\n' + lineOld2

        getTitles(fullPathProfile, "profile") # start script

        to_file = open(fullPathProfile) 
        lineNew = to_file.readline() #save 1st string - new

        with open (fullPathProfile, 'r') as f:
            newData = f.read()
        
        newData = newData.replace(lineNew, lineOld) # replace 1st string
        
        with open (fullPathProfile, 'w') as f:
            f.write(newData)
            f.close()
        
        # deleting blank lines
        with open(fullPathProfile) as xmlfile:
            lines = [line for line in xmlfile if line.strip() != ""]

        with open(fullPathProfile, "w") as xmlfile:
            xmlfile.writelines(lines)

def processThePermissionsets():
    pathPermissionsets = pathDX +"\\permissionsets\\"
    permissionsets = os.listdir(pathPermissionsets)
    print(len(permissionsets)," permissionsets found")
    c = 0
    for permissionset in permissionsets:
        c += 1
        print (permissionset , " in progress ", len(permissionsets)-c, "permissionsets left" )
        fullPathPermissionsets = pathPermissionsets + permissionset

        from_file = open(fullPathPermissionsets) 
        lineOld = from_file.readline() # save 1st string
        lineOld2 = from_file.readline() # save 2nd string 

        '''
        beginning of the file content:
        <?xml version="1.0" encoding="utf-8"?><Profile xmlns="http://soap.sforce.com/2006/04/metadata">
        or
        <?xml version="1.0" encoding="utf-8"?>
        <Profile xmlns="http://soap.sforce.com/2006/04/metadata">        
        '''
        if  "soap.sforce.com" in lineOld2:
            lineOld = lineOld + '\n' + lineOld2
        

        getTitles(fullPathPermissionsets, "permissionset") # start script

        to_file = open(fullPathPermissionsets) 
        lineNew = to_file.readline() #save 1st string - new

        with open (fullPathPermissionsets, 'r') as f:
            newData = f.read()
        
        newData = newData.replace(lineNew, lineOld) # replace 1st string
        
        with open (fullPathPermissionsets, 'w') as f:
            f.write(newData)
            f.close()
        
        # deleting blank lines
        with open(fullPathPermissionsets) as xmlfile:
            lines = [line for line in xmlfile if line.strip() != ""]

        with open(fullPathPermissionsets, "w") as xmlfile:
            xmlfile.writelines(lines)

# START 
if __name__ == "__main__":
    processTheProfile()  # run for Profiles
    processThePermissionsets() # run for Permissionsets
    
    
    