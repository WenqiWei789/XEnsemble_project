import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils import load_externals

from models.cnn1_models import cnn1_cifar10_model
from models.cnn2_models import cnn2_cifar10_model
from models.densenet_models import densenet_cifar10_model, get_densenet_weights_path
from models.cifar10_resnet20_model import resnet20_cifar10_model, resnet32_cifar10_model, resnet44_cifar10_model, resnet56_cifar10_model, resnet110_cifar10_model
from models.cifar10_lenet_model import lenet_cifar10_model

from models.distillation_cifar10_models import distillation_cifar10_model

from keras.datasets import cifar10
from keras.utils import np_utils


class CIFAR10Dataset:
    def __init__(self):
        self.dataset_name = "CIFAR-10"
        self.image_size = 32
        self.num_channels = 3
        self.num_classes = 10

    def get_test_dataset(self):
        (X_train, y_train), (X_test, y_test) = cifar10.load_data()
        X_test = X_test.reshape(X_test.shape[0], self.image_size, self.image_size, self.num_channels)
        X_test = X_test.astype('float32')
        X_test /= 255
        Y_test = np_utils.to_categorical(y_test, self.num_classes)
        del X_train, y_train
        return X_test, Y_test

    def get_train_dataset(self):
        (X_train, y_train), (X_test, y_test) = cifar10.load_data()
        X_train = X_train.reshape(X_train.shape[0], self.image_size, self.image_size, self.num_channels)
        X_train = X_train.astype('float32')
        X_train /= 255
        Y_train = np_utils.to_categorical(y_train, self.num_classes)
        del X_test, y_test
        return X_train, Y_train

    def get_val_dataset(self):
        (X_train, y_train), (X_test, y_test) = cifar10.load_data()
        val_size = 5000
        X_val = X_train[:val_size]
        X_val = X_val.reshape(X_val.shape[0], self.image_size, self.image_size, self.num_channels)
        X_val = X_val.astype('float32') / 255
        y_val = y_train[:val_size]
        Y_val = np_utils.to_categorical(y_val, self.num_classes)
        del X_train, y_train, X_test, y_test

        return X_val, Y_val


    def load_model_by_name(self, model_name, logits=False, input_range_type=1, pre_filter=lambda x:x):
        """
        :params logits: return logits(input of softmax layer) if True; return softmax output otherwise.
        :params input_range_type: {1: [0,1], 2:[-0.5, 0.5], 3:[-1, 1]...}
        """
        if model_name not in ["cnn2", 'cnn2_adv_trained', 'cnn1', 'densenet','resnet20','resnet32','resnet44','resnet56','resnet110','lenet','distillation']:
            raise NotImplementedError("Undefined model [%s] for %s." % (model_name, self.dataset_name))
        self.model_name = model_name

        model_weights_fpath = "%s_%s.keras_weights.h5" % (self.dataset_name, model_name)
        model_weights_fpath = os.path.join('downloads/trained_models', model_weights_fpath)

        if model_name in ["cnn2", 'cnn2_adv_trained']:
            model = cnn2_cifar10_model(logits=logits, input_range_type=input_range_type, pre_filter=pre_filter)
        elif model_name == "cnn1":
            model = cnn1_cifar10_model(logits=logits, input_range_type=input_range_type, pre_filter=pre_filter)
        elif model_name == "densenet":
            model = densenet_cifar10_model(logits=logits, input_range_type=input_range_type, pre_filter=pre_filter)
            model_weights_fpath = get_densenet_weights_path(self.dataset_name)
        elif model_name == "lenet":
            model = lenet_cifar10_model(logits=logits, input_range_type=input_range_type, pre_filter=pre_filter)
        elif model_name in ['resnet20']:
            model = resnet20_cifar10_model()
        elif model_name in ['resnet32']:
            model = resnet32_cifar10_model()
        elif model_name in ['resnet44']:
            model = resnet44_cifar10_model()
        elif model_name in ['resnet56']:
            model = resnet56_cifar10_model()
        elif model_name in ['resnet110']:
            model = resnet110_cifar10_model()
        elif model_name in ['distillation']:
            model = distillation_cifar10_model()
        print("\n===Defined TensorFlow model graph.")
        #if model_name not in ['distillation']:
        model.load_weights(model_weights_fpath)
        print ("---Loaded CIFAR-10-%s model.\n" % model_name)
        return model

if __name__ == '__main__':
    dataset = CIFAR10Dataset()
    X_test, Y_test = dataset.get_test_dataset()
    print (X_test.shape)
    print (Y_test.shape)