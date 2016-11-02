import os
import requests
import operator
import re
import json
from rq import Queue
from rq.job import Job
from worker import conn
from flask import Flask, render_template, request, jsonify
from werkzeug.utils import secure_filename
import inertial_flow


app = Flask(__name__)

# This is the path to the upload directory
app.config['DATA_UPLOAD_FOLDER'] = '/data'
app.config['JSON_UPLOAD_FOLDER'] = '/JSON'
# These are the extension that we are accepting to be uploaded
app.config['ALLOWED_EXTENSIONS'] = set(['txt', 'csv','json'])

base_path = os.path.dirname(__file__)

# For a given file, return whether it's an allowed type or not
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']

q = Queue(connection=conn)


def run_network(f):
    print "in count functin", f
    errors = []
    result = inertial_flow.run_network(f)
    return result


@app.route('/api/getDataFiles',methods=['POST'])
def r_p_getData_Files():
    print "Getting filesss"
   # path = os.getcwd() + "/data"
    path = base_path + "/data"
    dirs = os.listdir( path )
    results = {}
    i = 0
    # This would print all the files and directories
    for file in dirs:
        i = i + 1
        results[i] = file
        print file

    return jsonify(results)

@app.route('/api/getJSONFiles',methods=['POST'])
def r_p_get_JSON_Files():
    print "Getting filesss"
    #path = os.getcwd() + "/JSON"
    path = base_path + "/JSON"
    dirs = os.listdir( path )
    results = {}
    i = 0
    # This would print all the files and directories
    for file in dirs:
        i = i + 1
        results[i] = file
        print file

    return jsonify(results)


@app.route('/api/runnetwork', methods=['POST'])
def r_net_post():
    # run the json file
    print "in running network"
    data = json.loads(request.data.decode())
    json_file = data["file"]
    # start job
    fil_path = base_path + "/temp/out_temp.txt"
    open(fil_path, 'w').close()       #clear inter comm file
    job = q.enqueue_call(
        func="__init__.run_network", args=(json_file,), result_ttl=5000
    )
    # return created job id
    return job.get_id()

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

@app.route('/uploaddata', methods=['POST'])
def uploaddata():
    # Get the name of the uploaded file
    file = request.files['file']
    # Check if the file is one of the allowed types/extensions
    if file and allowed_file(file.filename):
        print "Allowed to save this file in folder", app.config['DATA_UPLOAD_FOLDER']
        # Make the filename safe, remove unsupported chars
        filename = secure_filename(file.filename)
        # Move the file form the temporal folder to
        # the upload folder we setup
        fil_path = base_path + "/data/" + filename
        file.save(fil_path)
        # Redirect the user to the uploaded_file route, which
        # will basicaly show on the browser the uploaded file
    #    return redirect(url_for('uploaded_file',
    #                            filename=filename))
    else:
        return "-1"
    return render_template('index.html')

@app.route('/uploadjson', methods=['POST'])
def uploadjson():
    # Get the name of the uploaded file
    file = request.files['file']
    # Check if the file is one of the allowed types/extensions
    if file and allowed_file(file.filename):
        print "Allowed to save this file in folder", app.config['JSON_UPLOAD_FOLDER']
        # Make the filename safe, remove unsupported chars
        filename = secure_filename(file.filename)
        # Move the file form the temporal folder to
        # the upload folder we setup
        fil_path = base_path + "/JSON/" + filename
        file.save(fil_path)

        #file.save(os.path.join(app.config['JSON_UPLOAD_FOLDER'], filename))
        # Redirect the user to the uploaded_file route, which
        # will basicaly show on the browser the uploaded file
    #    return redirect(url_for('uploaded_file',
    #                            filename=filename))
    else:
        return "-1"
    return render_template('index.html')




@app.route("/results/<job_key>", methods=['GET'])
def get_results(job_key):

    job = Job.fetch(job_key, connection=conn)
    fil_path = base_path + "/temp/out_temp.txt"
    if job.is_finished:
        print "Job Finished"

        #result = job.result
        d = {}
        i = -1
        file = open(fil_path, 'r')
        for lin in file.readlines():
            i = i + 1
            d[i] = lin
        file.close()
        return jsonify(d), 200
    else:
        d = {}
        i = -1
        file = open(fil_path, 'r')
        for lin in file.readlines():
            i = i + 1
            d[i] = lin
        file.close()
        return jsonify(d), 202


if __name__ == '__main__':
    app.run()
