import os

class ProjectInfo:

    def __init__(self):
        self.name = ""
        self.description = ""

        
    def open_project(self, file_name):
        with open(file_name) as f:
            for i,line in enumerate(fp):
                if i == 0:
                    self.name = line
                elif i == 1:
                    self.description = line

    def create_new_project(self,path,project_name):
        fileName = path + "/" + project_name + ".info"
        f = open(fileName,"w")
        f.write(project_name+"\n")
        f.close()
        os.chmod(fileName,0777)
        self.name = project_name


def listValidProjects(path):
    print "in listValidProjects"
    results = {}
    i = 0
    for name in os.listdir(path):
        if os.path.isdir(name):
            print "validating ",name
            prj_name = getProjectNameFromPath(path + "/" + name + "/" + name + ".info")
            if prj_name != "None":
                i = i + 1
                results[i] = prj_name


def getProjectNameFromPath(path):
    results = "None"
    print "in getProjectnameFromPath",path
    with open(path) as f:
        results = f.readline()
        print "getProjectnameFromPath",results
    return results


    

    