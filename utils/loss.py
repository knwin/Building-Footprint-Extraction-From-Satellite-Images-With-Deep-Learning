
import keras.backend as k
def dice_coef(y_true, y_pred):
    y_true = tf.cast(y_true, tf.float32)  # -------------------------------------------------- explicit cast
    y_true = K.flatten(y_true)
    y_pred = K.flatten(y_pred)
    intersection = K.sum(y_true * y_pred)
    return 2.0 * intersection / (K.sum(y_true) + K.sum(y_pred) + 1.)

    ## function for measuring loss value
def dice_coef_loss(y_true, y_pred):
    y_true = tf.cast(y_true, tf.float32)  # -------------------------------------------------- explicit cast
    return 1.0 - dice_coef(y_true, y_pred)

    ## Merge loss
def bce_dice_loss(y_true, y_pred):
    y_true = tf.cast(y_true, tf.float32)  # -------------------------------------------------- explicit cast
    a = 0.5
    b = 1-a
    loss = a * K.binary_crossentropy(y_true, y_pred) + b * dice_coef_loss(y_true, y_pred)
    return loss
