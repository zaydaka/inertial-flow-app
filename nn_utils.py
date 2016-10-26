import numpy as np
import tensorflow as tf

def extract_data(filename, x_data=None, y_data=None, input_size=None):
    fvecs = []
    labels = []
    if input_size is None:
        for line in file(filename):
            row = line.split(",")
            fvecs.append([float(x) for x in row[0:]])
        fvecs_np = np.matrix(fvecs).astype(np.float32)
        if x_data is None:
            return fvecs_np
        else:
            return np.concatenate((x_data, fvecs_np), axis=0)
    else:
        for line in file(filename):
            row = line.split(",")
            labels.append(int(row[0]))
            fvecs.append([float(x) for x in row[1:]])
        fvecs_np = np.matrix(fvecs).astype(np.float32)
        labels_np = np.array(labels).astype(dtype=np.uint8)
        labels_onehot = (np.arange(input_size) == labels_np[:, None]).astype(np.float32)
        if x_data is None:
            return fvecs_np, labels_onehot
        else:
            return np.concatenate((x_data, fvecs_np), axis=1),np.concatenate((y_data, labels_onehot), axis=1)

def get_samples(data, sample_size):
    return data[np.random.randint(data.shape[0],size=sample_size)]

def get_activation_function(func):
    if func == "tanh":
        return tf.nn.tanh
    elif func == "sigmoid":
        return tf.nn.sigmoid
    elif func == "softmax":
        return tf.nn.softmax
    elif func == "relu":
        return tf.nn.relu
    elif func == "relu6":
        return tf.nn.relu6
    elif func == "crelu":
        return tf.nn.crelu
    elif func == "elu":
        return tf.nn.elu
    elif func == "softplus":
        return tf.nn.softplus
    elif fucn == "softsign":
        return tf.nn.softsign

def get_optimizer_function(func):
    if func == "GradientDescent":
        return tf.train.GradientDescentOptimizer
    elif func == "Adam":
        return tf.train.AdamOptimizer
    elif func == "RMSProp":
        return tf.train.RMSPropOptimizer
    elif func == "Ftrl":
        return tf.train.FtrlOptimizer
    elif func == "Adagrad":
        return tf.train.AdagradOptimizer
    elif func == "Adadelta":
        return tf.train.AdadeltaOptimizer

def random_seed_np_tf(seed):
    """Seed numpy and tensorflow random number generators.
    :param seed: seed parameter
    """
    if seed >= 0:
        np.random.seed(seed)
        tf.set_random_seed(seed)
        return True
    else:
        return False