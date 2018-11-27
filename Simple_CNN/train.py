# -- coding: utf-8 --
import tensorflow as tf
from keras.models import Sequential
from keras.layers import Dense, Dropout, Activation, Flatten
from keras.layers import Conv2D, MaxPooling2D
import keras
from keras.datasets import cifar10
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from keras.preprocessing.image import ImageDataGenerator


classes_num = 10
batch_size = 20
epochs_num = 200

def quality_classify_model():
    model = Sequential()
    model.add(Conv2D(32, (3, 3), padding='same', input_shape=(32,32,3)))
    model.add(Activation('relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Conv2D(32, (3, 3)))
    model.add(Activation('relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))

    model.add(Conv2D(64, (3, 3), padding='same'))
    model.add(Activation('relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))

    model.add(Flatten())
    model.add(Dense(64))
    model.add(Activation('relu'))
    model.add(Dropout(0.5))
    model.add(Dense(classes_num))
    model.add(Activation('softmax'))

    opt = keras.optimizers.rmsprop(lr=0.0001, decay=1e-6)
    model.compile(loss='categorical_crossentropy', optimizer=opt, metrics=['accuracy'])
    return model

def train():
    # 数据载入
    (x_train, y_train), (x_test, y_test) = cifar10.load_data()

    # 多分类标签生成
    y_train = keras.utils.to_categorical(y_train, classes_num)
    y_test = keras.utils.to_categorical(y_test, classes_num)
    # 生成训练数据
    x_train = x_train.astype('float32')
    x_test = x_test.astype('float32')
    x_train /= 255
    x_test /= 255

    model = quality_classify_model()
    hist = model.fit(x_train, y_train, batch_size=64, epochs=epochs_num, validation_data=(x_test, y_test), shuffle=True)

    model.save('./change_model/cifar10_model.hdf5') 
    model.save_weights('./change_model/cifar10_model_weight.hdf5')

    hist_dict = hist.history
    print("train acc:")
    print(hist_dict['acc'])
    print("validation acc:")
    print(hist_dict['val_acc'])

    train_acc = hist.history['acc']
    val_acc = hist.history['val_acc']
    train_loss = hist.history['loss']
    val_loss = hist.history['val_loss']

    # 绘图
    epochs = range(1, len(train_acc)+1)
    plt.plot(epochs, train_acc, 'bo', label = 'Training acc')
    plt.plot(epochs, val_acc, 'r', label = 'Validation acc')
    plt.title('Training and validation accuracy')
    plt.legend()
    plt.savefig("accuracy.png")
    plt.figure() # 新建一个图
    plt.plot(epochs, train_loss, 'bo', label = 'Training loss')
    plt.plot(epochs, val_loss, 'r', label = 'Validation loss')
    plt.title('Training and validation loss')
    plt.legend()
    plt.savefig("loss.png")
    