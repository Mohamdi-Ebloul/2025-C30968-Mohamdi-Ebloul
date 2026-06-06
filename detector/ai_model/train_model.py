import os          # pour construire les chemins de dossiers et vérifier leur existence
import sys         # pour quitter le programme avec sys.exit() en cas d'erreur
import argparse    # pour lire les arguments passés en ligne de commande (--dataset, --epochs, --lr)
import numpy as np # pour convertir les listes d'images/labels en tableaux numériques
import cv2         # pour lire, convertir et redimensionner les images (OpenCV)
import tensorflow as tf  # pour construire le pipeline de données et entraîner le modèle
from sklearn.model_selection import train_test_split  # pour diviser les données en train/validation
import matplotlib.pyplot as plt  # pour tracer et sauvegarder les courbes d'entraînement

IMG_SIZE = 224       # taille cible de chaque image (224x224 pixels)
BATCH_SIZE = 16      # nombre d'images traitées à chaque étape d'entraînement
MODEL_SAVE_PATH = os.path.join(os.path.dirname(__file__), 'breast_cancer_model.h5')  # chemin de sauvegarde du modèle


def load_dataset(dataset_path: str):
    """Charge les images bénignes et malignes depuis le dossier du dataset BUSI.

    Utilise :
      - os.path.join / os.path.exists / os.listdir : pour parcourir les dossiers benign et malignant
      - cv2.imread         : lit chaque fichier image depuis le disque
      - cv2.cvtColor       : convertit l'image de BGR (format OpenCV) en RGB
      - cv2.resize         : redimensionne l'image à IMG_SIZE x IMG_SIZE
      - np.float32 / 255.0 : normalise les pixels dans l'intervalle [0, 1]
      - np.array           : convertit les listes Python en tableaux NumPy pour TensorFlow
    """
    images, labels = [], []

    benign_dir = os.path.join(dataset_path, 'benign')
    malignant_dir = os.path.join(dataset_path, 'malignant')

    for directory, label in [(benign_dir, 0), (malignant_dir, 1)]:
        if not os.path.exists(directory):
            print(f"[WARNING] Directory not found: {directory}")
            continue
        for filename in sorted(os.listdir(directory)):
            if '_mask' in filename:
                continue  # ignore les images de masques (annotations)
            if not filename.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp')):
                continue
            img_path = os.path.join(directory, filename)
            img = cv2.imread(img_path)
            if img is None:
                continue
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            img = cv2.resize(img, (IMG_SIZE, IMG_SIZE))
            img = img.astype(np.float32) / 255.0
            images.append(img)
            labels.append(label)

    return np.array(images), np.array(labels)


def build_model():
    """Construit et retourne le modèle CNN défini dans predictor.py.

    Utilise :
      - sys.path.insert : ajoute le dossier courant au chemin de recherche des modules Python
      - predictor.build_cnn_model : importe et appelle la fonction de construction du CNN
    """
    import sys
    sys.path.insert(0, os.path.dirname(__file__))
    from predictor import build_cnn_model
    return build_cnn_model()


def plot_history(history, output_dir='.'):
    """Trace les courbes de Loss, Accuracy et AUC et les sauvegarde en image PNG.

    Utilise :
      - matplotlib.pyplot.subplots : crée une figure avec 3 sous-graphiques côte à côte
      - axes[i].plot              : trace les valeurs d'entraînement et de validation pour chaque métrique
      - axes[i].set_title / legend: ajoute un titre et une légende à chaque graphique
      - plt.tight_layout          : ajuste automatiquement l'espacement entre les sous-graphiques
      - plt.savefig               : sauvegarde la figure dans le fichier training_history.png
      - history.history.get       : accède à l'AUC (peut être absent si non calculé)
    """
    fig, axes = plt.subplots(1, 3, figsize=(16, 4))

    axes[0].plot(history.history['loss'], label='Train Loss')
    axes[0].plot(history.history['val_loss'], label='Val Loss')
    axes[0].set_title('Loss')
    axes[0].legend()

    axes[1].plot(history.history['accuracy'], label='Train Acc')
    axes[1].plot(history.history['val_accuracy'], label='Val Acc')
    axes[1].set_title('Accuracy')
    axes[1].legend()

    axes[2].plot(history.history.get('auc', []), label='Train AUC')
    axes[2].plot(history.history.get('val_auc', []), label='Val AUC')
    axes[2].set_title('AUC')
    axes[2].legend()

    plt.tight_layout()
    plot_path = os.path.join(output_dir, 'training_history.png')
    plt.savefig(plot_path)
    print(f"[Training] Plot saved to {plot_path}")


def main():
    """Point d'entrée principal : charge les données, configure et lance l'entraînement.

    Utilise :
      - argparse.ArgumentParser : lit les arguments --dataset, --epochs, --lr depuis le terminal
      - load_dataset            : charge et prépare les images X et les labels y
      - train_test_split        : divise X/y en 80% train et 20% validation (stratifié)
      - tf.keras.Sequential     : pipeline d'augmentation de données (flip, rotation, zoom, contraste)
      - tf.data.Dataset         : crée des datasets optimisés avec shuffle, map, batch et prefetch
      - build_model             : instancie le CNN
      - tf.keras.callbacks      : EarlyStopping (arrêt anticipé), ReduceLROnPlateau (ajustement du taux
                                  d'apprentissage) et ModelCheckpoint (sauvegarde du meilleur modèle)
      - class_weight            : calcule les poids pour compenser le déséquilibre bénin/malin
      - model.fit               : lance l'entraînement sur les données augmentées
      - model.evaluate          : évalue le modèle final sur le jeu de validation
      - plot_history            : sauvegarde les courbes d'entraînement
    """
    parser = argparse.ArgumentParser(description='Train Breast Cancer CNN')
    parser.add_argument('--dataset', required=True, help='Path to BUSI dataset folder')
    parser.add_argument('--epochs', type=int, default=30)
    parser.add_argument('--lr', type=float, default=0.0001)
    args = parser.parse_args()

    print(f"[Training] Loading dataset from: {args.dataset}")
    X, y = load_dataset(args.dataset)

    if len(X) == 0:
        print("[ERROR] No images loaded. Check your dataset path and structure.")
        sys.exit(1)

    print(f"[Training] Loaded {len(X)} images — "
          f"Benign: {(y == 0).sum()}, Malignant: {(y == 1).sum()}")

    X_train, X_val, y_train, y_val = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    # Data augmentation
    data_augmentation = tf.keras.Sequential([
        tf.keras.layers.RandomFlip('horizontal'),
        tf.keras.layers.RandomRotation(0.1),
        tf.keras.layers.RandomZoom(0.1),
        tf.keras.layers.RandomContrast(0.1),
    ])

    train_ds = tf.data.Dataset.from_tensor_slices((X_train, y_train))
    train_ds = (train_ds
                .shuffle(buffer_size=len(X_train))
                .map(lambda x, y: (data_augmentation(x, training=True), y),
                     num_parallel_calls=tf.data.AUTOTUNE)
                .batch(BATCH_SIZE)
                .prefetch(tf.data.AUTOTUNE))

    val_ds = (tf.data.Dataset.from_tensor_slices((X_val, y_val))
              .batch(BATCH_SIZE)
              .prefetch(tf.data.AUTOTUNE))

    model = build_model()
    model.summary()

    callbacks = [
        tf.keras.callbacks.EarlyStopping(
            monitor='val_auc', patience=8, restore_best_weights=True, mode='max'
        ),
        tf.keras.callbacks.ReduceLROnPlateau(
            monitor='val_loss', factor=0.5, patience=4, min_lr=1e-6
        ),
        tf.keras.callbacks.ModelCheckpoint(
            MODEL_SAVE_PATH, monitor='val_auc', save_best_only=True, mode='max'
        ),
    ]

    # Compensate for class imbalance (benign >> malignant in BUSI)
    n_total = len(y_train)
    class_weight = {
        0: n_total / (2.0 * (y_train == 0).sum()),
        1: n_total / (2.0 * (y_train == 1).sum()),
    }
    print(f"[Training] Class weights: {class_weight}")

    print(f"[Training] Starting training for up to {args.epochs} epochs...")
    history = model.fit(
        train_ds,
        validation_data=val_ds,
        epochs=args.epochs,
        callbacks=callbacks,
        class_weight=class_weight,
    )

    # Evaluate
    loss, acc, auc = model.evaluate(val_ds, verbose=0)
    print(f"\n[Training] Final validation — Loss: {loss:.4f} | Accuracy: {acc:.4f} | AUC: {auc:.4f}")
    print(f"[Training] Model saved to: {MODEL_SAVE_PATH}")

    plot_history(history, output_dir=os.path.dirname(__file__))


if __name__ == '__main__':
    main()
