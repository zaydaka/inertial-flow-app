import tensorflow as tf
import numpy as np
import os
import math
import json
import nn_utils
from datetime import datetime
from matplotlib import pyplot as plt
import auto_encoder
import input_layer

flags = tf.app.flags
FLAGS = flags.FLAGS
base_path = os.path.dirname(__file__)



def writeToTemp(s):
    fil_path = base_path + "/temp/out_temp.txt"
    f_t = open(fil_path,'a')
    f_t.write(s+"\n")
    f_t.close()

def run_network(jsn_file, project_save_path,evaluate=None):

    if evaluate is None:
        evaluate = False        #do not train
    else:
        evaluete = True         # do training

    fil_path = base_path + "/temp/out_temp.txt"
    print "filPath = ",fil_path
    open(fil_path, 'w').close()
    with open(jsn_file,'r') as f:
        options = json.load(f)

    print "just loaded options"
    

# Create a working directory
    nn_utils.random_seed_np_tf(-1)
    root_logdir = options['dir']
    project_name = options['name']
    now = datetime.utcnow().strftime("%Y%m%d%H%M%S")
    logdir = "{}/{}-{}/".format(root_logdir,project_name, now)

    if evaluate==False:
        # Load data sets
        if 'training_data' in options['data']:
            for training_file in options['data']['training_data']:
                ##print "Loading training set ", training_file['file_name']
                writeToTemp("Loading training set " + training_file['file_name'])
                if 'trX' in locals():
                    trX, trRef = nn_utils.extract_data(training_file['file_name'], trX, trRef, input_size=2)
                else:
                    trX, trRef = nn_utils.extract_data(training_file['file_name'], input_size=2)
        if 'validation_data' in options['data']:
            for validation_file in options['data']['validation_data']:
                ##print "Loading validation set ", validation_file['file_name']
                writeToTemp("Loading validation set " + validation_file['file_name'])
                if 'vlX' in locals():
                    vlX, vlRef = nn_utils.extract_data(validation_file['file_name'], vlX, vlRef)
                else:
                    vlX, vlRef = nn_utils.extract_data(validation_file['file_name'])
        if 'testing_data' in options['data']:
            for testing_data in options['data']['testing_data']:
                ##print "Loading testing set ", testing_data['file_name']
                writeToTemp("Loading testing set " + testing_data['file_name'])
                if 'teX' in locals():
                    teX = nn_utils.extract_data(testing_data['file_name'], teX)
                else:
                    teX = nn_utils.extract_data(testing_data['file_name'])
    else:
        n_sampe = 1
        input_size = 17 #hardcoded

# Stack and build the layers
    if evaluate==False:
        n_samp, input_size = teX.shape

    net_layers = []
    layerNumber = -1
    print "Stacking layers..."
    writeToTemp("Stacking layers...")
    for layer in options['layers']:
        layerNumber = layerNumber + 1
        if layer['layer_type'] == "input":
            print "Adding input layer ", layer['layer_name']
            writeToTemp("adding input layer " + layer['layer_name'])
            net_layers.append(input_layer.InputLayer(layer['layer_name'],layer['layer_order'],input_size,False))
            print "Building graph for ", layer['layer_name']
            writeToTemp("Building graph for " + layer['layer_name'])
            net_layers[layerNumber].build_model()
        elif layer['layer_type'] == "autoencoder":
            print "Adding autoencoder layer ", layer['layer_name']
            writeToTemp("Adding autoencoder layer " + layer['layer_name'])
            net_layers.append(auto_encoder.AutoEncoder(layer['layer_name'], layer['layer_order'], layer['hidden_size'], layer['activation'], options['dir'],net_layers[layerNumber-1].encode,  layer['pre_train'], layer['tied_weights'], "FULL", 
            layer['pre_train_rounds'], layer['pre_train_batch_size'], layer['pre_train_cost'],layer['pre_train_optimizer'],layer['pre_train_learning_rate']))
            writeToTemp("Building graph for " + layer['layer_name'])
            print "Building graph for ", layer['layer_name']
            net_layers[layerNumber].build_model(net_layers[layerNumber-1].hidden_size)
        else:
            print "Adding fully connected layer ", layer['layer_name']
            writeToTemp("Adding fully connected layer " + layer['layer_name'])
            net_layers.append(auto_encoder.AutoEncoder(layer['layer_name'], layer['layer_order'], layer['hidden_size'], layer['activation'], options['dir'],net_layers[layerNumber-1].encode))
            print "Building graph for ", layer['layer_name']
            writeToTemp("Building graph for " + layer['layer_name'])
            net_layers[layerNumber].build_model(net_layers[layerNumber-1].hidden_size)

# Setup overall network to train
    if 'trX' in locals() and 'trRef' in locals():
        print "trRef.shpe=",trRef.shape
        print "outsize=",net_layers[len(net_layers)-1].hidden_size
        assert (net_layers[len(net_layers)-1].hidden_size == trRef.shape[1]), "Your final layer hidden size should be equal to your labels size!" 
        writeToTemp("Building full network training model...")
        y_ = tf.placeholder(tf.float32, [None, trRef.shape[1]])  #holds the truth data
        #create the cost function
        if options['cost'] == 'MSE':
            cost =  tf.reduce_mean(tf.square(net_layers[len(net_layers)-1].encode-y_))
        else:
            cost =  tf.reduce_mean(tf.square(net_layers[len(net_layers)-1].encode-y_))
       # train_step = nn_utils.get_optimizer_function(options['optimizer']).minimize(cost)  #fix this bug
        train_step = tf.train.AdamOptimizer(options['learning_rate']).minimize(cost)

        correct_prediction = tf.equal(tf.argmax(net_layers[len(net_layers)-1].encode, 1), tf.argmax(y_, 1))
        evaluate_full = net_layers[len(net_layers)-1].encode
        accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))
    elif evaluate==True:
        writeToTemp("Creating evaluation network")
        evaluate_full = net_layers[len(net_layers)-1].encodea



# Start the session
    init = tf.initialize_all_variables()
    sess = tf.Session()
    
    saver = tf.train.Saver()


    sess.run(init)

    if evaluate==False:
    # Do pretraining // asuume first layer is input layer
        pre_training_data = net_layers[0].encode_data(sess,teX)
        for i in range(1,len(net_layers),1):
            ae = net_layers[i]
            if ae.layer_type == "Autoencoder":
                if net_layers[i-1].layer_type == "Input" and ae.pre_train:
                    ##print "Pre Training encoder ", ae.name
                    writeToTemp("Pre training encoder " + ae.name)
                    ae.pre_train_model(sess,pre_training_data)
                    pre_training_data = ae.encode_data(sess,pre_training_data)
                elif ae.pre_train:
                    if net_layers[i-1].pre_train != True:
                        k = [] ##remove
                        ##print "WARNING: Cannot pre-train ", ae.name, " because a previous layer is not pre-trained."
                        writeToTemp("WARNING: Cannot pre-train " + ae.name + " because a previous layer is not pre-trained")
                    else:
                        ##print "Pre Training encoder ", ae.name
                        writeToTemp("Pre training encoder " + ae.name)
                        ae.pre_train_model(sess,pre_training_data)
                        pre_training_data = ae.encode_data(sess,pre_training_data)
                        ##print "size of pre_training_data ", pre_training_data.shape
    else:
        print "Restoring the past session"
        saver.restore(sess,project_save_path + options['name'] + ".ckpt")

# Run the training
    outputs = ""
    
    if evaluate==False:
        if 'trX' in locals() and 'trRef' in locals():
            ##print "Starting network training..."
            writeToTemp("Starting network training..")
            n_samp, n_input = trX.shape
            batch_size = min(options['batch_size'],n_samp)
            for i in range(options['training_rounds']):
                sample = np.random.randint(n_samp, size=batch_size)
                batch_xs = trX[sample][:]
                batch_ys = trRef[sample][:]
                sess.run(train_step, feed_dict={net_layers[0]._input_data: batch_xs, y_: batch_ys})
                if i % 100 == 0:
                    print "Round:",i, " Accuracy: ",sess.run(accuracy, feed_dict={net_layers[0]._input_data: trX,y_: trRef})
                    acc = sess.run(accuracy, feed_dict={net_layers[0]._input_data: trX,y_: trRef})
                    outputs = "Accuracy: " + str(acc)
                    #writeToTemp(outputs)
                    #print "Round:",i, " Accuracy: ",sess.run(accuracy, feed_dict={net_layers[0]._input_data: trX,y_: trRef})
            acc = sess.run(accuracy, feed_dict={net_layers[0]._input_data: trX,y_: trRef})
            outputs = "Final network accuracy: " + str(acc)
            writeToTemp(outputs)
    else:
        res = sess.run(evaluate_full, feed_dict={net_layers[0]._input_data: test})
        print "Result is " + str(trX)
    
    
    
############## train full network


   
   
# Close out session
    if evaluate==False:
        print "Saving network... "
        save_path = saver.save(sess, project_save_path + options['name'] + ".ckpt")
        print "Saving network to ", save_path
        sess.close()

        dirs = os.listdir(project_save_path)

    #for file in dirs:
    #    os.chmod(file,0777)

    #plt.show()
    #quit()
    return outputs


        #plt.plot(range(300),np.transpose(example_x))
        #plt.plot(range(300),np.transpose(sess.run(evalAutoEncoder, feed_dict={x_preTrain: example_x})))
        #plt.grid()
        #plt.show()


        #example_x = teX[1000][:]
        #plt.plot(range(300),np.transpose(example_x))
        #plt.plot(range(300),np.transpose(sess.run(evalAutoEncoder, feed_dict={x_preTrain: example_x})))
        #plt.grid()
        #plt.show()

        #example_x = teX[20000][:]
        #plt.plot(range(300),np.transpose(example_x))
        #plt.plot(range(300),np.transpose(sess.run(evalAutoEncoder, feed_dict={x_preTrain: example_x})))
        #plt.grid()
        #plt.show()

        #plt.plot(error)
        #plt.show()
        #plt.savefig("name.jpg")
