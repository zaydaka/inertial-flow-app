import tensorflow as tf
import numpy as np
import os
import math
import json
import nn_utils
from datetime import datetime
from matplotlib import pyplot as plt
flags = tf.app.flags
FLAGS = flags.FLAGS

flags.DEFINE_string('json_file','sample.json','JSON file to be processed')

if __name__ == '__main__':

    with open(FLAGS.json_file,'r') as f:
        options = json.load(f)

    nn_utlis.random_seed_np_tf(-1)
    root_logdir = options['dir']
    project_name = options['name']
    now = datetime.utcnow().strftime("%Y%m%d%H%M%S")
    logdir = "{}/{}-{}/".format(root_logdir,project_name, now)

    if 'training_data' in options['data']:
        for training_file in options['data']['training_data']:
            print "Loading training set ", training_file['file_name']
            if 'trX' in locals():
                trX, trRef = nn_utils.extract_data(training_file['file_name'], trX, trRef)
            else:
                trX, trRef = nn_utils.extract_data(training_file['file_name'])
    if 'validation_data' in options['data']:
        for validation_file in options['data']['validation_data']:
            print "Loading validation set ", validation_file['file_name']
            if 'vlX' in locals():
                vlX, vlRef = nn_utils.extract_data(validation_file['file_name'], vlX, vlRef)
            else:
                vlX, vlRef = nn_utils.extract_data(validation_file['file_name'])
    if 'testing_data' in options['data']:
        for testing_data in options['data']['testing_data']:
            print "Loading testing set ", testing_data['file_name']
            if 'teX' in locals():
                teX = nn_utils.extract_data(testing_data['file_name'], teX)
            else:
                teX = nn_utils.extract_data(testing_data['file_name'])

    #pre training methods
    layer = options['layers'][0]
    if layer['pre_train'] == "true":
        print "Doing pre training on layer 0..."
        n_samp, input_size = teX.shape
        x_preTrain = tf.placeholder("float",[None,teX.shape[1]])
        Wh = tf.Variable(tf.random_uniform((input_size,layer['hidden_size']),-1.0/math.sqrt(input_size),1.0/math.sqrt(input_size)))
        bh = tf.Variable(tf.zeros([layer['hidden_size']]))
        if layer['activation'] == 'tanh':
            h = tf.nn.tanh(tf.matmul(x_preTrain,Wh) + bh)
            if layer['tied_weights']:
                print 'Setting up tied weights...'
                Wo = tf.transpose(Wh) #tied Weights
            else:
                Wo = tf.Variable(tf.random_uniform((layer['hidden_size'],input_size),-1.0/math.sqrt(input_size),1.0/math.sqrt(input_size)))
            bo = tf.Variable(tf.zeros([input_size]))
            y = tf.nn.tanh(tf.matmul(h,Wo) + bo)
            evalAutoEncoder = tf.nn.tanh(tf.matmul(h,Wo) + bo)
        elif FLAGS.activation == 'sigmoid':
            h = tf.nn.sigmoid(tf.matmul(x,Wh) + bh)
            if FLAGS.tied_weights:
                print 'Setting up tied weights...'
                Wo = tf.transpose(Wh) #tied Weights
            else:
                Wo = tf.Variable(tf.random_uniform((layer['hidden_size'],input_size),-1.0/math.sqrt(input_size),1.0/math.sqrt(input_size)))
            bo = tf.Variable(tf.zeros([input_size]))
            y = tf.nn.sigmoid(tf.matmul(h,Wo) + bo)
            evalAutoEncoder = tf.nn.sigmoid(tf.matmul(h,Wo) + bo)

        #Objective functions
        y_ = tf.placeholder("float",[None,input_size])
        with tf.name_scope("pre_train_cost") as scope:
            if layer['pre_train_cost'] == "MSE":
                meansq = tf.reduce_mean(tf.square(y_-y))
                mse_summary = tf.scalar_summary('MSE', meansq)
        if layer['pre_train_optimizer'] == "Adam":
            train_step = tf.train.AdamOptimizer(layer['pre_train_learning_rate']).minimize(meansq)

        init = tf.initialize_all_variables()
        saver = tf.train.Saver()
        merged_summary_op = tf.merge_all_summaries()
        sess = tf.Session()

        sess.run(init)
        summary_writer = tf.train.SummaryWriter(logdir, graph_def=sess.graph_def)
        n_rounds = layer['pre_train_rounds']
        batch_size = min(layer['pre_train_batch_size'],n_samp)
        error = []
        for i in range(n_rounds):
            sample = np.random.randint(n_samp, size=batch_size)
            batch_xs = teX[sample][:]
            batch_ys = teX[sample][:]
            sess.run(train_step, feed_dict={x_preTrain: batch_xs, y_:batch_ys})
            if i % 50 == 0:
                summary_str = sess.run(merged_summary_op, feed_dict={x_preTrain: batch_xs, y_:batch_ys})
                summary_writer.add_summary(summary_str,i)
            if i % 100 == 0:
                error.append(sess.run(meansq, feed_dict={x_preTrain: batch_xs, y_:batch_ys}))
                print i, sess.run(meansq, feed_dict={x_preTrain: batch_xs, y_:batch_ys})

        print "Final weights (input => hidden layer)"
        print sess.run(Wh)
        print "Final biases (input => hidden layer)"
        print sess.run(bh)

        saved_path = saver.save(sess,options['name']+"ckpt")
        print saved_path
        summary_writer.close()
        example_x = teX[10000][:]
        plt.plot(range(300),np.transpose(example_x))
        plt.plot(range(300),np.transpose(sess.run(evalAutoEncoder, feed_dict={x_preTrain: example_x})))
        plt.grid()
        plt.show()


        example_x = teX[1000][:]
        plt.plot(range(300),np.transpose(example_x))
        plt.plot(range(300),np.transpose(sess.run(evalAutoEncoder, feed_dict={x_preTrain: example_x})))
        plt.grid()
        plt.show()

        example_x = teX[20000][:]
        plt.plot(range(300),np.transpose(example_x))
        plt.plot(range(300),np.transpose(sess.run(evalAutoEncoder, feed_dict={x_preTrain: example_x})))
        plt.grid()
        plt.show()

        plt.plot(error)
        plt.show()
        plt.savefig("name.jpg")
    quit()




    #cross_entropy = -tf.reduce_sum(y_*tf.log(y))



    #def evalAutoEncoder(input_x):
    #    print sess.run(evalAutoEncoder, feed_dict={x: input_x}).shape
    #    plt.plot(input_x)
    #    plt.plot(sess.run(evalAutoEncoder, feed_dict={x: input_x}))
    #    plt.show()
