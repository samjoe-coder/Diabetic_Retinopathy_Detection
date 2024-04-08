import numpy as np
import PIL
from tensorflow.keras.layers import Dense, Conv2D, MaxPool2D , Flatten, BatchNormalization, Activation, Add, MaxPooling2D, ZeroPadding2D, AveragePooling2D, Input
from tensorflow.keras.initializers import glorot_uniform

def load_model():

    def res_block(X, filter, stage):
        X_copy = X

        f1 , f2, f3 = filter
            
        X = Conv2D(f1, (1,1),strides = (1,1), name ='res_'+str(stage)+'_conv_a', kernel_initializer= glorot_uniform(seed = 0))(X)
        X = MaxPool2D((2,2))(X)
        X = BatchNormalization(axis =3, name = 'bn_'+str(stage)+'_conv_a')(X)
        X = Activation('relu')(X) 

        X = Conv2D(f2, kernel_size = (3,3), strides =(1,1), padding = 'same', name ='res_'+str(stage)+'_conv_b', kernel_initializer= glorot_uniform(seed = 0))(X)
        X = BatchNormalization(axis =3, name = 'bn_'+str(stage)+'_conv_b')(X)
        X = Activation('relu')(X) 

        X = Conv2D(f3, kernel_size = (1,1), strides =(1,1),name ='res_'+str(stage)+'_conv_c', kernel_initializer= glorot_uniform(seed = 0))(X)
        X = BatchNormalization(axis =3, name = 'bn_'+str(stage)+'_conv_c')(X)

        X_copy = Conv2D(f3, kernel_size = (1,1), strides =(1,1),name ='res_'+str(stage)+'_conv_copy', kernel_initializer= glorot_uniform(seed = 0))(X_copy)
        X_copy = MaxPool2D((2,2))(X_copy)
        X_copy = BatchNormalization(axis =3, name = 'bn_'+str(stage)+'_conv_copy')(X_copy)

        X = Add()([X,X_copy])
        X = Activation('relu')(X)

        X_copy = X

        X = Conv2D(f1, (1,1),strides = (1,1), name ='res_'+str(stage)+'_identity_1_a', kernel_initializer= glorot_uniform(seed = 0))(X)
        X = BatchNormalization(axis =3, name = 'bn_'+str(stage)+'_identity_1_a')(X)
        X = Activation('relu')(X) 

        X = Conv2D(f2, kernel_size = (3,3), strides =(1,1), padding = 'same', name ='res_'+str(stage)+'_identity_1_b', kernel_initializer= glorot_uniform(seed = 0))(X)
        X = BatchNormalization(axis =3, name = 'bn_'+str(stage)+'_identity_1_b')(X)
        X = Activation('relu')(X) 

        X = Conv2D(f3, kernel_size = (1,1), strides =(1,1),name ='res_'+str(stage)+'_identity_1_c', kernel_initializer= glorot_uniform(seed = 0))(X)
        X = BatchNormalization(axis =3, name = 'bn_'+str(stage)+'_identity_1_c')(X)

        X = Add()([X,X_copy])
        X = Activation('relu')(X)

        X_copy = X

        X = Conv2D(f1, (1,1),strides = (1,1), name ='res_'+str(stage)+'_identity_2_a', kernel_initializer= glorot_uniform(seed = 0))(X)
        X = BatchNormalization(axis =3, name = 'bn_'+str(stage)+'_identity_2_a')(X)
        X = Activation('relu')(X) 

        X = Conv2D(f2, kernel_size = (3,3), strides =(1,1), padding = 'same', name ='res_'+str(stage)+'_identity_2_b', kernel_initializer= glorot_uniform(seed = 0))(X)
        X = BatchNormalization(axis =3, name = 'bn_'+str(stage)+'_identity_2_b')(X)
        X = Activation('relu')(X) 

        X = Conv2D(f3, kernel_size = (1,1), strides =(1,1),name ='res_'+str(stage)+'_identity_2_c', kernel_initializer= glorot_uniform(seed = 0))(X)
        X = BatchNormalization(axis =3, name = 'bn_'+str(stage)+'_identity_2_c')(X)

        X = Add()([X,X_copy])
        X = Activation('relu')(X)

        return X

    input_shape = (256,256,3)

    X_input = Input(input_shape)

    X = ZeroPadding2D((3,3))(X_input)

    X = Conv2D(64, (7,7), strides= (2,2), name = 'conv1', kernel_initializer= glorot_uniform(seed = 0))(X)
    X = BatchNormalization(axis =3, name = 'bn_conv1')(X)
    X = Activation('relu')(X)
    X = MaxPooling2D((3,3), strides= (2,2))(X)

    X = res_block(X, filter= [64,64,256], stage= 2)

    X = res_block(X, filter= [128,128,512], stage= 3)

    X = res_block(X, filter= [256,256,1024], stage= 4)

    X = AveragePooling2D((2,2), name = 'Averagea_Pooling')(X)

    X = Flatten()(X)
    X = Dense(5, activation = 'softmax', name = 'Dense_final', kernel_initializer= glorot_uniform(seed=0))(X)

    return (X_input, X)

def predict(img_path, model):
    
    labels = {0: 'Mild', 1: 'Moderate', 2: 'No_DR', 3:'Proliferate_DR', 4: 'Severe'}
   
    image = []

    img0 = img_path
    img= PIL.Image.open(img0)
    img = img.resize((256,256))
    image.append(img)

    img = np.asarray(img, dtype= np.float32)
    img = img / 255
    img = img.reshape(-1,256,256,3)
    predict = model.predict(img)
    predict = np.argmax(predict)
    
    return labels[predict]
