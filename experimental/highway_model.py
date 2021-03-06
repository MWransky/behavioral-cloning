import time
import os
import numpy as np

from keras.optimizers import *
from keras.callbacks import *

from highway_network import *
from data_helpers import *
from model_helpers import *


def train():
    print('Loading data...')
    train_dataset, valid_dataset, train_outputs, valid_outputs = get_training_data()

    # define loss function and training metric

    loss = 'mse'
    metric = 'mse'

    print('Building network ...')
    model = build_network()
    model.summary()

    model.compile(optimizer='adam',
                  loss=loss, metrics=[metric])

    # save model to json file
    saving = 'highway_model'
    if not os.path.exists('./experiment'):
        os.makedirs('./experiment')
    fModel = open('experiment/' + saving + '.json', 'w')
    json_str = model.to_json()
    fModel.write(json_str)

    print('Training...')
    path = './experiment'
    if not os.path.exists(path):
        os.makedirs(path)

    start_time = time.time()

    fParams = '{0}/{1}.h5'.format(path, saving)
    saveParams = ModelCheckpoint(fParams, monitor='loss', save_best_only=True)

    callbacks = [saveParams]

    model.fit(train_dataset, train_outputs, verbose=1,
              validation_data=(valid_dataset, valid_outputs),
              nb_epoch=15, batch_size=32, callbacks=callbacks)

    end_time = time.time()

    print('training time: %.2f' % (end_time - start_time))


def main():
    train()

if __name__ == "__main__":
    main()
