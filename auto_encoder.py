import numpy as np
import tensorflow as tf
import nn_utils
import math
from matplotlib import pyplot as plt

class AutoEncoder:

    def __init__(self, name, order, hidden_size, activation, path, input_layer = None, pre_train = False, tied_weights = True, verbose = "FULL",
        num_pre_train_epochs=2000, pre_train_batch_size=5000, pre_train_cost="MSE",pre_train_optimizer="Adam",pre_train_learning_rate=0.001):

        self.path = path
        self.name = name
        self.order = order
        self.hidden_size = hidden_size
        self.activation_function = nn_utils.get_activation_function(activation)
        self.pre_train = pre_train
        self.tied_weights = tied_weights
        self.num_pre_train_epochs = num_pre_train_epochs
        self.pre_train_batch_size = pre_train_batch_size
        self.pre_train_cost = pre_train_cost
        self.pre_train_optimizer_function = nn_utils.get_optimizer_function(pre_train_optimizer)
        self.pre_train_learning_rate = pre_train_learning_rate
        self.verbose = verbose
        self.input_layer = input_layer
        self.layer_type = "Autoencoder"

        self.init = None
        self.tf_session = None
        self.pre_train_step = None
        self.encode = None
        self.pre_train_encode = None
        self.pre_train_decode = None
        self._input_data = None
        self._output_data = None
        self._input_labels = None
        self.Wi = None
        self.bi = None
        self.Wo = None
        self.bo = None
        self.cost = None

    #def train_model(self, session,train_set, validation_set=None, train_ref=None, Validation_ref=None):
        #should_init=False
    #    self.tf_session = session
    #    self._run_train_step(train_set)
    #    if self.verbose == "FULL":
    #        index = np.random.randint(train_set.shape[0],size=1)
    #        example_x = train_set[index][:]
    #        plt.figure()
    #        plt.plot(range(train_set.shape[1]),np.transpose(example_x))
    #        plt.plot(range(train_set.shape[1]),np.transpose(self.tf_session.run(self.pre_train_decode, feed_dict={self._input_data: example_x})))
    #        plt.grid()
    #        plt.draw()

        #for i in range(self.num_pre_train_epochs):
        #    self._run_train_step(train_set)

            # validation code here !!!
            #if validation_set is not None:
            #    feed = {self.input_data_orig: validation_set,self.input_data: validation_set}
            #    self._run_validation_error_and_summaries(i, feed)

    #def _init_node():
    #    self.init = tf.initialize_all_variables()  #question the scope of this
    def encode_data(self,session,data):
        self.tf_session = session
        return self.tf_session.run(self.pre_train_encode, feed_dict={self._input_data: data})

    def pre_train_model(self, session, train_set):
        if self.pre_train:
            self.tf_session = session
            self._run_pre_train_step(train_set)
            if self.verbose == "FULL":
                index = np.random.randint(train_set.shape[0],size=1)
                example_x = train_set[index][:]
                plt.figure()
                plt.plot(range(train_set.shape[1]),np.transpose(example_x))
                plt.plot(range(train_set.shape[1]),np.transpose(self.tf_session.run(self.pre_train_decode, feed_dict={self._input_data: example_x})))
                plt.title("Pre-trained Layer: "+self.name+" Example")
                plt.grid()
                plt.draw()

    def _run_pre_train_step(self, train_set):
        n_samp, n_input = train_set.shape
        batch_size = min(self.pre_train_batch_size, n_samp)

        for i in range(self.num_pre_train_epochs):
            sample = np.random.randint(n_samp, size=batch_size)
            batch_xs = train_set[sample][:]
            self.tf_session.run(self.pre_train_step, feed_dict={self._input_data: batch_xs, self._output_data: batch_xs})
            #if i % 50 == 0:
            #    summary_str = sess.run(merged_summary_op, feed_dict={x: batch_xs, y_:batch_ys})
            #    summary_writer.add_summary(summary_str,i)
            if i % 100 == 0:
                if self.verbose == "FULL" or self.verbose == "MEDIUM":
                    print "Pre-training Round:",i, self.tf_session.run(self.cost, feed_dict={self._input_data: batch_xs, self._output_data: batch_xs})

    def _create_pre_train_step_node(self):
        with tf.name_scope(self.name+"train"):
            self.pre_train_step = self.pre_train_optimizer_function(self.pre_train_learning_rate).minimize(self.cost)

    def build_model(self, n_features):
        self._create_placeholders(n_features)
        self._create_variables(n_features)

        if self.input_layer is not None:
            self._create_encode_layer()

        if self.pre_train:
            self._create_pre_train_encode_layer()
            self._create_pre_train_decode_layer()
            self._create_pre_train_cost_function_node()
            self._create_pre_train_step_node()

        #vars = [self.Wi, self.bi, self.Wo, self.bo]
        #regterm = self.compute_regularization(vars)
        

    def _create_pre_train_cost_function_node(self):
        with tf.name_scope(self.name+"pre_train_cost"):
            if self.pre_train_cost == 'MSE':
                self.cost = tf.reduce_mean(tf.square(self._output_data-self.pre_train_decode))

    def _create_placeholders(self, n_features):
        self._input_data = tf.placeholder(tf.float32, [None, n_features], name=self.name+'_x-input')
        self._output_data = tf.placeholder(tf.float32, [None, n_features], name=self.name+'y-input')
        self._input_labels = tf.placeholder(tf.float32)

    def _create_variables(self, n_features):
        self.Wi = tf.Variable(tf.random_uniform((n_features,self.hidden_size),-1.0/math.sqrt(n_features),1.0/math.sqrt(n_features)),name=self.name+'_enc-wi')
        self.bi = tf.Variable(tf.zeros([self.hidden_size]),name=self.name+'_enc-bi')
        if self.tied_weights:
            self.Wo = tf.transpose(self.Wi, name=self.name+'_enc-wo') #tied Weight
        else:
            self.Wo = tf.Variable(tf.random_uniform((self.hidden_size,n_features),-1.0/math.sqrt(self.hidden_size),1.0/math.sqrt(self.hidden_size)),name=self.name+'_enc-wo')
        self.bo = tf.Variable(tf.zeros([n_features]),name=self.name+'_enc-bo')

    def _create_pre_train_encode_layer(self):
        with tf.name_scope(self.name+"pretrain_encoder"):
            activation = tf.matmul(self._input_data, self.Wi) + self.bi
            self.pre_train_encode = self.activation_function(activation)

    def _create_encode_layer(self):
        with tf.name_scope(self.name+"encoder"):
            activation = tf.matmul(self.input_layer, self.Wi) + self.bi
            self.encode = self.activation_function(activation)

    def _create_pre_train_decode_layer(self):
        with tf.name_scope(self.name+"pretrain_decoder"):
            activation = tf.matmul(self.pre_train_encode, self.Wo) + self.bo
            self.pre_train_decode = self.activation_function(activation)

    def get_model_parameters(self, session, graph=None):
        #Return the model parameters in the form of numpy arrays.
        self.session = session
        g = graph
        with g.as_default():
            with tf.Session() as self.tf_session:
                self.tf_saver.restore(self.tf_session, self.model_path)
                return {
                    name+'_enc-Wi': self.Wi.eval(),
                    name+'_enc-bi': self.bi.eval(),
                    name+'_enc-Wo': self.Wo.eval(),
                    name+'_enc-bo': self.bo.eval()
                }
