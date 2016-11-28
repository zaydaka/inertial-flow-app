from shutil import copyfile
import os
import csv
from projectinfo import ProjectInfo


def copy_default_to_new_user():
	copyfile(src, dst)

def create_project(base_path,project_name):
	path = base_path + project_name
	if not os.path.exists(path):
		os.makedirs(path)
		os.chmod(path,0777)

	prj = ProjectInfo()
	prj.create_new_project(path,project_name)


def setup_new_account(base_path, user):
	print "in fuctions"
	u_name = user.replace("@","_")
	u_name = u_name.replace(".","_")
	path = base_path + "/data/User/" + u_name
	print path
	if not os.path.exists(path):
		os.makedirs(path)
		os.chmod(path,0777)
	path = base_path + "/data/User/" + u_name + "/Projects"
	print path
	if not os.path.exists(path):
		os.makedirs(path)
		os.chmod(path,0777)
	path = path + "/Sample"
	print path
	if not os.path.exists(path):
		os.makedirs(path)
		os.chmod(path,0777)
	path = base_path + "/data/User/" + u_name + "/Data"
	print path
	if not os.path.exists(path):
		os.makedirs(path)
		os.chmod(path,0777)

    #move default projects and data....
    
	copyfile(base_path+"/data/Sample/iris.data",base_path+"/data/User/"+u_name+"/Data/iris.data")
	os.chmod(base_path+"/data/Sample/iris.data",base_path+"/data/User/"+u_name+"/Data/iris.data",0777)
	copyfile(base_path+"/data/Sample/iris.json",base_path+"/data/User/"+u_name+"/Projects/Sample/iris.json")
	os.chmod(base_path+"/data/Sample/iris.json",base_path+"/data/User/"+u_name+"/Projects/Sample/iris.json",077)