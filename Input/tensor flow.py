import tensorflow as tf

'''
input > weight > hidden layer 1

activation function > weights > hidden layer 2

repeat

(activation function) > weights > output layer

compare output to intended output using cost function (ie cross entropy)
optimization function (optimizer) - minimize cost (AdamOptimizer, SGD, AdaGrad) - back-propagation, manipulates weights

feed forward + back-prop = epoch
'''

from tensorflow.examples.tutorials.mnist import input_data

mnist = input_data.read_data_sets("/tmp/data/", one_hot = True) # only one element is on

'''
10 classes, 0-9

one_hot outputs:
[1,0,0,0,0,0,0,0,0,0] for 0
[0,1,0,0,0,0,0,0,0,0] for 1
[0,0,1,0,0,0,0,0,0,0] for 2

'''

n_nodes_hl1 = 500
n_nodes_hl2 = 500
n_nodes_hl3 = 500

n_classes = 10

batch_size = 100  # processes batches of 100 features at a time, and then manipulate weight per batch, for memory-saving


# matrix is given as height x width

# placeholder at any given time
x = tf.placeholder('float', [None, 784])  # flatten a 28x28 grid into 1x784 array
y = tf.placeholder('float')


def neural_network_model(data):
    # initializes hidden layers
    # creates a giant matrix with random values as weights
    # (input_data * weights) + biases
    # biases used for if all input data is 0, so that neurons can still fire

    hidden_1_layer = {'weights': tf.Variable(tf.random_normal([784, n_nodes_hl1])),
                      'biases': tf.Variable(tf.random_normal([n_nodes_hl1]))}

    hidden_2_layer = {'weights': tf.Variable(tf.random_normal([n_nodes_hl1, n_nodes_hl2])),  #input is number of nodes in hidden layer 1
                      'biases': tf.Variable(tf.random_normal([n_nodes_hl2]))}

    hidden_3_layer = {'weights': tf.Variable(tf.random_normal([n_nodes_hl2, n_nodes_hl3])),
                      'biases': tf.Variable(tf.random_normal([n_nodes_hl3]))}

    output_layer = {'weights': tf.Variable(tf.random_normal([n_nodes_hl3, n_classes])),
                    'biases': tf.Variable(tf.random_normal([n_classes]))} # outputs to 10 classes, so use n_classes

    # (input_data * weights) + biases
    l1 = tf.add(tf.matmul(data, hidden_1_layer['weights']),  hidden_1_layer['biases'])

    # activation function
    l1 = tf.nn.relu(l1)

    l2 = tf.add(tf.matmul(l1, hidden_2_layer['weights']),  hidden_2_layer['biases'])
    l2 = tf.nn.relu(l2)

    l3 = tf.add(tf.matmul(l2, hidden_3_layer['weights']) + hidden_3_layer['biases'])
    l3 = tf.nn.relu(l3)

    output = tf.matmul(l3, output_layer['weights']) + output_layer['biases']

    return output #outputs one hot array


def train_neural_network(x):
    prediction = neural_network_model(x)
    cost = tf.reduce_mean (tf.nn.softmax_cross_entropy_with_logits(prediction, y))
    optimizer = tf.train.AdamOptimizer().minimize(cost)

    #cycles of feed forward and back propagation
    num_epochs = 5

    with tf.Session() as sess:
        sess.run(tf.initialize_all_variables())
        for epoch in range(num_epochs):
            epoch_loss = 0
            for _ in range(int(mnist.train.num_examples/batch_size)): # divides the data into batches of appropriate sizes
                epoch_x, epoch_y = mnist.train.next_batch(batch_size) #produces the next batch
                _, c = sess.run([optimizer, cost], feed_dict={x: epoch_x, y: epoch_y})
                epoch_loss += c

            print('Epoch: ', epoch, 'completed out of ', num_epochs, ' loss: ', epoch_loss)

        correct = tf.equal(tf.argmax(prediction, 1), tf.argmax(y, 1)) #tf.equal compares the arguments
                                            # prediction and y are one-hot arrays, so if they're the same then the index
                                            # of max value (1) should be the same

        accuracy = tf.reduce_mean(tf.cast(correct, 'float'))

        print('Accuracy: ', accuracy.eval({x: mnist.test.images, y:mnist.test.labels}))


train_neural_network(x)