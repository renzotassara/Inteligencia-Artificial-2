import numpy as np
import matplotlib.pyplot as plt
from keras.datasets import mnist

from matplotlib.colors import ListedColormap
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC

from sklearn.metrics import confusion_matrix
import pandas as pd
import seaborn as sn


# # Cargar el dataset MNIST
# (X_train, y_train), (X_test, y_test) = mnist.load_data()

# # Mostrar 15 ejemplos aleatorios
# r, c = 3, 5
# fig = plt.figure(figsize=(2*c, 2*r))
# for _r in range(r):
#     for _c in range(c):
#         ix = np.random.randint(0, len(X_train))
#         img = X_train[ix]
#         plt.subplot(r, c, _r*c + _c + 1)
#         plt.imshow(img, cmap='gray')
#         plt.axis("off")
#         plt.title(y_train[ix])
# plt.tight_layout()
# plt.show()

# Cargar el dataset MNIST
(X_train, Y_train), (X_test, Y_test) = mnist.load_data()

# Tomamos el diez por ciento de los datos para entrenamiento y prueba
X_train_s, _, Y_train_s, _ = train_test_split(X_train, Y_train, test_size=0.9, random_state=42)
X_test_s, _, Y_test_s, _ = train_test_split(X_test, Y_test, test_size=0.9, random_state=42)
print(f"X_train: {X_train_s.shape}, Y_train: {Y_train_s.shape}")
print(f"X_test: {X_test_s.shape}, Y_test: {Y_test_s.shape}")

# # Normalizar las imágenes dividiendo por 255
# X_train_norm = X_train_s.reshape(-1, 28*28) / 255.0
# X_test_norm = X_test_s.reshape(-1, 28*28) / 255.0

# Normalizar las imágenes con StandardScaler
X_train_std = X_train_s.reshape(-1, 28*28)
X_test_std = X_test_s.reshape(-1, 28*28)
scaler = StandardScaler()
X_train_std = scaler.fit_transform(X_train_std)
X_test_std = scaler.transform(X_test_std)

# # ----- Clasificador SVC ----- #
# clf = SVC(kernel='linear', C=1.0, random_state=42)

# # Dividir el dataset en entrenamiento y prueba
# clf.fit(X_train_std, Y_train_s)

# # Evaluar el clasificador
# Y_pred = clf.predict(X_test_std)
# accuracy = accuracy_score(Y_test_s, Y_pred)
# print(f"Accuracy: {accuracy:.2f}")

# ----- Clasificador de regresión logística ----- #
clf = LogisticRegression(C = 1, max_iter=6000)
clf.fit(X_train_std, Y_train_s)

# Evaluar el clasificador
Y_pred = clf.predict(X_test_std)
accuracy = accuracy_score(Y_test_s, Y_pred)
print(f"Accuracy: {accuracy:.2f}")

# Mostrar ejemplos de imágenes mal clasificadas
r, c = 3, 5
fig = plt.figure(figsize=(2*c, 2*r))
ix = 0
for _r in range(r):
    for _c in range(c):
        while Y_test_s[ix] == Y_pred[ix]:
            ix += 1
        img = X_test[ix].reshape(28, 28)
        plt.subplot(r, c, _r*c + _c + 1)
        plt.imshow(img, cmap='gray')
        plt.axis("off")
        plt.title(f"Pred: {Y_pred[ix]}\nTrue: {Y_test_s[ix]}")
        ix += 1
plt.tight_layout()
plt.show()

# Mostrar ejemplos de imágenes bien clasificadas
r, c = 3, 5
fig = plt.figure(figsize=(2*c, 2*r))
ix = 0
for _r in range(r):
    for _c in range(c):
        while Y_test_s[ix] != Y_pred[ix]:
            ix += 1
        img = X_test[ix].reshape(28, 28)
        plt.subplot(r, c, _r*c + _c + 1)
        plt.imshow(img, cmap='gray')
        plt.axis("off")
        plt.title(f"Pred: {Y_pred[ix]}\nTrue: {Y_test_s[ix]}")
        ix += 1
plt.tight_layout()
plt.show()

y_pred = Y_pred
cm = confusion_matrix(Y_test_s, y_pred)
df_cm = pd.DataFrame(cm, index = [i for i in range(0,10)], columns = [i for i in range(0,10)])
plt.figure(figsize = (10,7))
sn.heatmap(df_cm, annot=True)
plt.show()