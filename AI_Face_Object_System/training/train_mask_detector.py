import os
import cv2
import numpy as np
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout
from tensorflow.keras.utils import to_categorical
from sklearn.model_selection import train_test_split

DATASET = 'dataset'
CATEGORIES = ['with_mask', 'without_mask']
data, labels = [], []

for cat in CATEGORIES:
    path = os.path.join(DATASET, cat)
    label = CATEGORIES.index(cat)
    for img in os.listdir(path):
        image = cv2.imread(os.path.join(path, img))
        image = cv2.resize(image, (224,224))
        data.append(image/255.0)
        labels.append(label)

data = np.array(data)
labels = to_categorical(labels, 2)

X_train, X_test, y_train, y_test = train_test_split(data, labels, test_size=0.2)

model = Sequential([
    Conv2D(32,(3,3),activation='relu',input_shape=(224,224,3)),
    MaxPooling2D(2,2),
    Conv2D(64,(3,3),activation='relu'),
    MaxPooling2D(2,2),
    Flatten(),
    Dense(128,activation='relu'),
    Dropout(0.5),
    Dense(2,activation='softmax')
])

model.compile(optimizer='adam',loss='categorical_crossentropy',metrics=['accuracy'])
model.fit(X_train,y_train,epochs=10,validation_data=(X_test,y_test))
model.save("mask_detector.model")
