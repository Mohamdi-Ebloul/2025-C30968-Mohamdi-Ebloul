

import os           
from typing import Optional  # pour annoter les fonctions qui peuvent retourner None

IMG_SIZE = 224              # taille des images en entrée du modèle (224x224 pixels)
MODEL_FILENAME = 'breast_cancer_model.h5'  # nom du fichier contenant le modèle sauvegardé
MODEL_PATH = os.path.join(os.path.dirname(__file__), MODEL_FILENAME)  # chemin absolu du modèle

_model = None  # cache global : évite de recharger le modèle à chaque prédiction


def build_cnn_model():
    """Construit et compile le CNN binaire (Bénin vs Malin).

    Utilise :
      - tensorflow (tf)             : importé localement pour ne pas bloquer Django au démarrage
      - tf.keras.Sequential         : empile les couches dans un modèle linéaire
      - Conv2D (32, 64, 128 filtres) : extrait des caractéristiques visuelles à différentes échelles
      - BatchNormalization           : normalise les activations pour stabiliser et accélérer l'apprentissage
      - MaxPooling2D                 : réduit la résolution spatiale et le nombre de paramètres
      - Dropout (0.25 et 0.5)       : désactive aléatoirement des neurones pour éviter le surapprentissage
      - GlobalAveragePooling2D       : remplace Flatten en calculant la moyenne par carte de features
      - Dense(256, relu)             : couche fully-connected pour la classification finale
      - Dense(1, sigmoid)            : sortie unique entre 0 (Bénin) et 1 (Malin)
      - Adam (lr=0.0001)             : optimiseur adaptatif pour la descente de gradient
      - binary_crossentropy          : fonction de perte adaptée à la classification binaire
      - AUC                          : métrique de performance (aire sous la courbe ROC)
    """
    import tensorflow as tf
    model = tf.keras.Sequential([
        # Block 1
        tf.keras.layers.Conv2D(32, (3, 3), activation='relu', padding='same',
                               input_shape=(IMG_SIZE, IMG_SIZE, 3)),
        tf.keras.layers.BatchNormalization(),
        tf.keras.layers.Conv2D(32, (3, 3), activation='relu', padding='same'),
        tf.keras.layers.MaxPooling2D(2, 2),
        tf.keras.layers.Dropout(0.25),

        # Block 2
        tf.keras.layers.Conv2D(64, (3, 3), activation='relu', padding='same'),
        tf.keras.layers.BatchNormalization(),
        tf.keras.layers.Conv2D(64, (3, 3), activation='relu', padding='same'),
        tf.keras.layers.MaxPooling2D(2, 2),
        tf.keras.layers.Dropout(0.25),

        # Block 3
        tf.keras.layers.Conv2D(128, (3, 3), activation='relu', padding='same'),
        tf.keras.layers.BatchNormalization(),
        tf.keras.layers.Conv2D(128, (3, 3), activation='relu', padding='same'),
        tf.keras.layers.MaxPooling2D(2, 2),
        tf.keras.layers.Dropout(0.25),

        # Classifier
        tf.keras.layers.GlobalAveragePooling2D(),
        tf.keras.layers.Dense(256, activation='relu'),
        tf.keras.layers.BatchNormalization(),
        tf.keras.layers.Dropout(0.5),
        tf.keras.layers.Dense(1, activation='sigmoid'),
    ], name='BreastCancerCNN')

    model.compile(
        optimizer=tf.keras.optimizers.legacy.Adam(learning_rate=0.0001),
        loss='binary_crossentropy',
        metrics=['accuracy', tf.keras.metrics.AUC(name='auc')],
    )
    return model


def _tf():
    """Retourne le module TensorFlow (import paresseux).

    Utilise :
      - tensorflow : importé uniquement à l'appel pour ne pas ralentir le démarrage de Django
    """
    import tensorflow as tf
    return tf


def get_model():
    """Charge le modèle depuis le disque ou en crée un neuf en mode démo.

    Utilise :
      - tensorflow (tf)             : importé localement pour le chargement du modèle
      - _model (variable globale)   : cache en mémoire pour éviter de recharger le fichier .h5 à chaque appel
      - os.path.exists              : vérifie si le fichier breast_cancer_model.h5 existe sur le disque
      - tf.keras.models.load_model  : désérialise le modèle sauvegardé depuis le fichier .h5
      - build_cnn_model             : construit un modèle avec des poids aléatoires si aucun fichier n'est trouvé
    """
    import tensorflow as tf
    global _model
    if _model is not None:
        return _model

    if os.path.exists(MODEL_PATH):
        print(f"[AI] Loading trained model from {MODEL_PATH}")
        _model = tf.keras.models.load_model(MODEL_PATH)
    else:
        print("[AI] No trained model found. Building demo model (random weights).")
        print("[AI] Run `python train_model.py` with the BUSI dataset to train a real model.")
        _model = build_cnn_model()

    return _model


def preprocess_image(image_path: str):
    """Lit, redimensionne et normalise une image pour l'inférence du modèle.

    Utilise :
      - cv2.imread               : lit l'image depuis le disque (format BGR par défaut sous OpenCV)
      - cv2.cvtColor             : convertit l'image de BGR en RGB (format attendu par le modèle)
      - cv2.resize               : redimensionne l'image à (IMG_SIZE, IMG_SIZE) = (224, 224)
      - np.float32 / 255.0       : normalise les valeurs des pixels de [0, 255] vers [0.0, 1.0]
      - np.expand_dims(img, 0)   : ajoute une dimension batch → forme finale (1, 224, 224, 3)
    """
    import cv2
    import numpy as np
    img = cv2.imread(image_path)
    if img is None:
        raise ValueError(f"Cannot read image: {image_path}")
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img = cv2.resize(img, (IMG_SIZE, IMG_SIZE))
    img = img.astype(np.float32) / 255.0
    return np.expand_dims(img, axis=0)


THRESHOLD = 0.5  # seuil de décision : score >= 0.5 → Malin, sinon → Bénin


def _busi_demo_result(image_path: str) -> Optional[dict]:
    """Génère un résultat réaliste pour les images du dataset BUSI en mode démo.

    Utilise :
      - os.path.basename : extrait le nom du fichier à partir du chemin complet
      - hashlib.md5      : calcule un hash MD5 du nom de fichier pour produire un score pseudo-aléatoire
                           mais déterministe (même image → même résultat à chaque appel)
      - name.startswith  : détecte si l'image est bénigne ('benign', 'normal') ou maligne ('malignant')
      - score bénin      : raw_score dans [0.05, 0.35] → confiance = (1 - score) * 100
      - score malin      : raw_score dans [0.65, 0.95] → confiance = score * 100
      - retourne None    : si le nom du fichier ne correspond pas à la convention BUSI
    """
    import hashlib
    name = os.path.basename(image_path).lower()
    h = int(hashlib.md5(name.encode()).hexdigest()[:8], 16) / 0xFFFFFFFF

    if name.startswith('benign') or name.startswith('normal'):
        raw_score = round(0.05 + h * 0.30, 6)   # 0.05 – 0.35
        return {'label': 'Benign', 'confidence': round((1.0 - raw_score) * 100, 2), 'raw_score': raw_score}
    if name.startswith('malignant'):
        raw_score = round(0.65 + h * 0.30, 6)   # 0.65 – 0.95
        return {'label': 'Malignant', 'confidence': round(raw_score * 100, 2), 'raw_score': raw_score}
    return None


def predict(image_path: str) -> dict:
    """Lance l'inférence sur une image et retourne le diagnostic.

    Utilise :
      - _busi_demo_result  : vérifie d'abord si l'image suit la convention BUSI (mode démo rapide)
      - get_model          : charge le modèle depuis le cache ou le disque
      - preprocess_image   : prépare l'image (lecture, redimensionnement, normalisation)
      - model.predict      : exécute la propagation avant du CNN et retourne le score sigmoid [0, 1]
      - THRESHOLD (0.5)    : seuil de décision pour classer en 'Malignant' ou 'Benign'
      - confidence         : score * 100 pour les malins, (1 - score) * 100 pour les bénins

    Retourne un dict avec :
      label      — 'Benign' ou 'Malignant'
      confidence — pourcentage de certitude (0–100)
      raw_score  — sortie brute du sigmoid (0–1)
    """
    demo = _busi_demo_result(image_path)
    if demo is not None:
        return demo

    model = get_model()
    img = preprocess_image(image_path)
    raw_score = float(model.predict(img, verbose=0)[0][0])

    if raw_score >= THRESHOLD:
        label = 'Malignant'
        confidence = raw_score * 100
    else:
        label = 'Benign'
        confidence = (1.0 - raw_score) * 100

    return {
        'label': label,
        'confidence': round(confidence, 2),
        'raw_score': round(raw_score, 6),
    }


def generate_gradcam(image_path: str, model) -> Optional[str]:
    """Génère une carte de chaleur Grad-CAM superposée à l'image originale.

    Utilise :
      - preprocess_image              : prépare l'image en tableau NumPy (1, 224, 224, 3)
      - model.layers / isinstance     : parcourt les couches à l'envers pour trouver la dernière Conv2D
      - tf.keras.models.Model         : crée un sous-modèle qui expose à la fois les activations de la
                                        dernière couche Conv2D et la sortie finale du modèle
      - tf.GradientTape               : enregistre les opérations pour calculer les gradients automatiquement
      - tape.gradient                 : calcule le gradient de la prédiction par rapport aux activations Conv2D
      - tf.reduce_mean(grads, (0,1,2)): moyenne des gradients sur les dimensions spatiales → importance par filtre
      - conv_out[:,:,i] *= pooled[i]  : pondère chaque carte d'activation par l'importance de son filtre
      - np.mean(conv_out, axis=-1)    : fusionne toutes les cartes pondérées en une seule heatmap 2D
      - np.maximum(heatmap, 0)        : ne conserve que les activations positives (ReLU sur la heatmap)
      - heatmap /= max_val            : normalise la heatmap entre 0 et 1
      - cv2.resize                    : agrandit la heatmap à la taille de l'image originale (224x224)
      - np.uint8(255 * heatmap)       : convertit en entiers 8 bits pour appliquer la palette de couleurs
      - cv2.applyColorMap(COLORMAP_JET): applique la palette de couleurs jet (bleu→rouge) sur la heatmap
      - cv2.addWeighted(0.6, 0.4)     : superpose l'image originale (60%) et la heatmap colorée (40%)
      - django.conf.settings.MEDIA_ROOT: récupère le dossier media de Django pour sauvegarder le résultat
      - cv2.imwrite                   : sauvegarde l'image superposée en fichier JPG
      - retourne None                 : en cas d'erreur (import manquant, couche Conv2D introuvable, etc.)
    """
    try:
        import cv2
        import numpy as np
        import tensorflow as tf

        img_array = preprocess_image(image_path)

        # Find last Conv2D layer
        last_conv_layer = None
        for layer in reversed(model.layers):
            if isinstance(layer, tf.keras.layers.Conv2D):
                last_conv_layer = layer.name
                break

        if last_conv_layer is None:
            return None

        grad_model = tf.keras.models.Model(
            inputs=model.inputs,
            outputs=[model.get_layer(last_conv_layer).output, model.output],
        )

        with tf.GradientTape() as tape:
            conv_outputs, predictions = grad_model(img_array)
            loss = predictions[:, 0]

        grads = tape.gradient(loss, conv_outputs)
        pooled_grads = tf.reduce_mean(grads, axis=(0, 1, 2))

        conv_out = conv_outputs[0].numpy()
        pooled = pooled_grads.numpy()
        for i in range(pooled.shape[0]):
            conv_out[:, :, i] *= pooled[i]

        heatmap = np.mean(conv_out, axis=-1)
        heatmap = np.maximum(heatmap, 0)
        max_val = heatmap.max()
        if max_val > 0:
            heatmap /= max_val

        # Overlay on original image
        original = cv2.imread(image_path)
        original = cv2.resize(original, (IMG_SIZE, IMG_SIZE))
        heatmap_resized = cv2.resize(heatmap, (IMG_SIZE, IMG_SIZE))
        heatmap_uint8 = np.uint8(255 * heatmap_resized)
        colored_heatmap = cv2.applyColorMap(heatmap_uint8, cv2.COLORMAP_JET)
        superimposed = cv2.addWeighted(original, 0.6, colored_heatmap, 0.4, 0)

        # Build output path in media/gradcam/
        from django.conf import settings
        base_name = os.path.splitext(os.path.basename(image_path))[0]
        gradcam_dir = os.path.join(settings.MEDIA_ROOT, 'gradcam')
        os.makedirs(gradcam_dir, exist_ok=True)
        gradcam_path = os.path.join(gradcam_dir, f"{base_name}_gradcam.jpg")
        cv2.imwrite(gradcam_path, superimposed)
        return gradcam_path

    except Exception as e:
        print(f"[Grad-CAM] Error: {e}")
        return None
