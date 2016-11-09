from shutil import copyfile
import os

def copy_default_to_new_user():
	copyfile(src, dst)


def setup_new_account(base_path, user):
	print "in fuctions"
	u_name = user.replace("@","_")
	u_name = u_name.replace(".","_")
	path = base_path + "/data/User/" + u_name
	print path
	if not os.path.exists(path):
		os.makedirs(path)
	path = base_path + "/data/User/" + u_name + "/Projects"
	print path
	if not os.path.exists(path):
		os.makedirs(path)
	path = path + "/Sample"
	print path
	if not os.path.exists(path):
		os.makedirs(path)
	path = base_path + "/data/User/" + u_name + "/Data"
	print path
	if not os.path.exists(path):
		os.makedirs(path)

    #move default projects and data....
	copyfile(base_path+"/data/Sample/iris.data",base_path+"/data/User/"+u_name+"/Data")
	copyfile(base_path+"/data/Sample/iris.json",base_path+"/data/User/"+u_name+"Projects/Sample")