# CancerDetect AI — Détection du Cancer du Sein

Mini projet universitaire · Deep Learning · Django · TensorFlow

---

## Démarrage rapide

```bash
# 1. Installer les dépendances
python3 -m venv venv
source venv/bin/activate          # Windows: venv\Scripts\activate
pip install -r requirements.txt

# 2. Migrations
python manage.py makemigrations detector
python manage.py migrate

# 3. Lancer le serveur
python manage.py runserver
```

Ouvrir → **http://127.0.0.1:8000**

---

## Entraîner le modèle (optionnel)

Téléchargez le **BUSI Dataset** depuis Kaggle :  
`aryashah2k/breast-ultrasound-images-dataset`

```bash
cd detector/ai_model
python train_model.py --dataset /path/to/Dataset_BUSI_with_GT --epochs 30
```

Le modèle est sauvegardé dans `detector/ai_model/breast_cancer_model.h5`.  
Sans modèle entraîné, l'application fonctionne en **mode démo** (poids aléatoires).

---

## Structure du projet

```
mini projet/
├── manage.py
├── requirements.txt
├── setup.sh
├── breast_cancer_detector/      # Config Django
│   ├── settings.py
│   └── urls.py
├── detector/                    # Application principale
│   ├── models.py                # Modèle Analysis (SQLite)
│   ├── views.py                 # Logique métier
│   ├── urls.py
│   ├── forms.py
│   ├── admin.py
│   └── ai_model/
│       ├── predictor.py         # CNN + Grad-CAM
│       └── train_model.py       # Script d'entraînement
├── templates/
│   └── detector/
│       ├── home.html
│       ├── upload.html
│       ├── result.html
│       ├── history.html
│       └── about.html
├── static/
│   ├── css/style.css
│   └── js/
└── media/                       # Images uploadées + Grad-CAM
```

---

## Architecture CNN

| Couche | Détail |
|--------|--------|
| Input | 224 × 224 × 3 |
| Conv2D (×2) + BN | 32 filtres, ReLU |
| Conv2D (×2) + BN | 64 filtres, ReLU |
| Conv2D (×2) + BN | 128 filtres, ReLU |
| GlobalAvgPool | — |
| Dense(256) + Dropout(0.5) | ReLU |
| Dense(1) | **Sigmoid** |

- Optimizer : **Adam** (lr=0.0001)  
- Loss : **binary_crossentropy**  
- Métriques : Accuracy, AUC

---

## Avertissement

Ce système est développé à des fins **éducatives uniquement**.  
Il ne constitue pas un dispositif médical et ne remplace pas un diagnostic médical professionnel.
