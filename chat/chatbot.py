import nltk
from nltk.stem import WordNetLemmatizer
import json
import random
import numpy as np
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout
import os

dir_actual = os.path.dirname(__file__)

# Construye la ruta al archivo datos.json
ruta_datos_json = os.path.join(dir_actual, 'datos.json')
nltk.download('punkt')
nltk.download('wordnet')

# Cargar datos desde el archivo JSON
with open(ruta_datos_json) as file:
    datos = json.load(file)

# Preprocesar los datos
lemmatizer = WordNetLemmatizer()

palabras = []
tags = []
intents = datos['intents']

entrenamiento = []

for intent in intents:
    for pattern in intent['patterns']:
        # Tokenizar y lematizar las palabras
        words = nltk.word_tokenize(pattern)
        palabras.extend(words)
        tags.append(intent['tag'])

palabras = [lemmatizer.lemmatize(word.lower()) for word in palabras if word.isalnum()]
palabras = sorted(list(set(palabras)))

tags = sorted(list(set(tags)))

for intent in intents:
    for pattern in intent['patterns']:
        # Bolsa de palabras para cada patrón
        bolsa_palabras = [lemmatizer.lemmatize(word.lower()) for word in nltk.word_tokenize(pattern) if word.isalnum()]

        # Codificación de un patrón en una matriz de entrada
        fila_entrenamiento = [1 if palabra in bolsa_palabras else 0 for palabra in palabras]

        # Codificación de la etiqueta en una matriz de salida
        etiqueta = [0] * len(tags)
        etiqueta[tags.index(intent['tag'])] = 1

        # Concatenar las listas en lugar de anidarlas
        entrenamiento.append(fila_entrenamiento + etiqueta)

random.shuffle(entrenamiento)
entrenamiento = np.array(entrenamiento)

# Separar datos de entrada y salida
X_train = np.array([entrada[:len(palabras)] for entrada in entrenamiento])
y_train = np.array([etiqueta[len(palabras):] for etiqueta in entrenamiento])

# Construir el modelo de red neuronal
modelo = Sequential()
modelo.add(Dense(128, input_shape=(len(palabras),), activation='relu'))
modelo.add(Dropout(0.5))
modelo.add(Dense(64, activation='relu'))
modelo.add(Dropout(0.5))
modelo.add(Dense(len(tags), activation='softmax'))

# Compilar el modelo
modelo.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

# Entrenar el modelo
historial_entrenamiento = modelo.fit(X_train, y_train, epochs=200, batch_size=5, verbose=1)

# Guardar el modelo entrenado
modelo.save('chatbot_modelo.h5')
print("Modelo entrenado y guardado exitosamente.")

# Función para procesar el mensaje del usuario y obtener una respuesta del chatbot
def procesar_mensaje(mensaje):
    # Bolsa de palabras para el mensaje del usuario
    bolsa_palabras = [lemmatizer.lemmatize(word.lower()) for word in nltk.word_tokenize(mensaje) if word.isalnum()]

    # Codificación del mensaje en una matriz de entrada
    entrada_usuario = np.array([1 if palabra in bolsa_palabras else 0 for palabra in palabras])

    # Predicción del modelo
    resultado = modelo.predict(entrada_usuario.reshape(1, -1))

    # Obtener la etiqueta predicha
    predicha_tag = tags[np.argmax(resultado)]

    # Buscar la respuesta asociada a la etiqueta
    for intent in intents:
        if intent['tag'] == predicha_tag:
            respuesta = random.choice(intent['responses'])
            return {
                "message":respuesta,
                "state":"recieved"
            }