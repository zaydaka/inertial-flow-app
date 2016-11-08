from shutil import copyfile


def copy_default_to_new_user(user):
	copyfile(src, dst)


def setup_new_account(base_path, user):
	u_name = user.replace("@","_").replace(".","_")
    path = base_path + "/data/User/" + u_name
    if not os.path.exists(path):
        os.makedirs(path)
    path = base_path + "/data/User/" + u_name + "/Projects"
    if not os.path.exists(path):
        os.makedirs(path)
    path = path + "/Sample"
    if not os.path.exists(path):
    	os.makedirs(path)
    path = base_path + "/data/User/" + u_name + "/Data"
    if not os.path.exists(path):
        os.makedirs(path)

    #move default projects and data....
