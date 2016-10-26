import numpy as np
import tensorflow as tf
import math
from matplotlib import pyplot as plt

class InputLayer:

    def __init__(self, name, order, input_size, condition_data = False):

        self.name = name
        self.order = order
        self.input_size = input_size
        self.hidden_size = input_size           #this is not a hidden layer BUT the pre processing of the data can be though of as a layer R^i = R^o
        self.condition_data = condition_data
        self.layer_type = "Input"

        self.init = None
        self.tf_session = None
        self.encode = None
        self._input_data = None


    def build_model(self):
        self._create_placeholders()

        self._create_encode_layer()


    def _create_placeholders(self):
        print 'creating input layer of size,', self.input_size
        self._input_data = tf.placeholder(tf.float32, [None, self.input_size], name='x-raw-input')
    

    def _create_encode_layer(self):
        #Encoding in the input layer is just pre processing of data
        with tf.name_scope(self.name+"pre_process"):
            self.encode = tf.mul(self._input_data,1) #should be updated in the future but for now we need to avoid the feed / fetch problem in TF
            #future pre processing stuff here

    def encode_data(self,session,data):
        self.tf_session = session
        return self.tf_session.run(self.encode, feed_dict={self._input_data: data})

