import keras


class CustomCallback(keras.callbacks.Callback):

    def on_epoch_begin(self, epoch, logs=None):
        # keys = list(logs.keys())
        # print("Start epoch {} of training; got log keys: {}".format(epoch, keys))
        # print("Start epoch {} of training; counter: {}".format(epoch, epoch_counter))
        pass

    def on_epoch_end(self, epoch, logs=None):
        global epoch_counter
        # keys = list(logs.keys())
        epoch_counter = epoch + 1
        # print("End epoch {} of training; got log keys: {}".format(epoch, epoch_counter))