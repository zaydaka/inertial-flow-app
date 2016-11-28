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
        f = open("fileName","w")
        f.write(project_name+"\n")
        f.close()

        self.name = project_name



    

    