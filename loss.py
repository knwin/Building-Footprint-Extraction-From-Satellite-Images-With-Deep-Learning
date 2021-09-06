import tensorflow as tf
import tensorflow.keras.backend as K


def dice_coef(y_true, y_pred):
    
    # explicit cast
    y_true = tf.cast(y_true, tf.float32)
    
    y_true = K.flatten(y_true)
    y_pred = K.flatten(y_pred)
    intersection = K.sum(y_true * y_pred)
    
    return 2.0 * intersection / (K.sum(y_true) + K.sum(y_pred) + 1.)


def dice_coef_loss(y_true, y_pred):
    
    # explicit cast
    y_true = tf.cast(y_true, tf.float32)
    
    return 1.0 - dice_coef(y_true, y_pred)


def bce_dice_loss(y_true, y_pred):
    
    # explicit cast
    y_true = tf.cast(y_true, tf.float32)
    
    a = 0.5
    b = 1-a
    loss = a * K.binary_crossentropy(y_true, y_pred) + b * dice_coef_loss(y_true, y_pred)
    
    return loss