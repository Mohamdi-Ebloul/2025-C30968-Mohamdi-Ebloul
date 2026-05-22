#!/usr/bin/env bash
# ─────────────────────────────────────────────────────────────────────────────
# CancerDetect AI — Quick Setup Script
# Run once after cloning: bash setup.sh
# ─────────────────────────────────────────────────────────────────────────────
set -e

echo ""
echo "╔══════════════════════════════════════════════════════╗"
echo "║      CancerDetect AI — Setup & Launch                ║"
echo "╚══════════════════════════════════════════════════════╝"
echo ""

# 1. Virtual environment
if [ ! -d "venv" ]; then
  echo "[1/5] Creating virtual environment..."
  python3 -m venv venv
fi

source venv/bin/activate
echo "[1/5] Virtual environment activated."

# 2. Install dependencies
echo "[2/5] Installing dependencies (this may take a few minutes)..."
pip install --upgrade pip -q
pip install -r requirements.txt -q
echo "[2/5] Dependencies installed."

# 3. Django migrations
echo "[3/5] Applying database migrations..."
python manage.py makemigrations detector
python manage.py migrate
echo "[3/5] Database ready."

# 4. Create superuser (optional)
echo ""
echo "[4/5] (Optional) Create an admin superuser?"
read -p "       Create superuser? [y/N] " yn
case $yn in
  [Yy]* ) python manage.py createsuperuser ;;
  * ) echo "       Skipped." ;;
esac

# 5. Collect static files
echo "[5/5] Collecting static files..."
python manage.py collectstatic --noinput -v 0
echo "[5/5] Done."

echo ""
echo "──────────────────────────────────────────────────────"
echo " Setup complete! Start the server with:"
echo ""
echo "   source venv/bin/activate"
echo "   python manage.py runserver"
echo ""
echo " Then open: http://127.0.0.1:8000"
echo "──────────────────────────────────────────────────────"
echo ""
echo " To train the AI model with the BUSI dataset:"
echo "   cd detector/ai_model"
echo "   python train_model.py --dataset /path/to/Dataset_BUSI_with_GT --epochs 30"
echo "──────────────────────────────────────────────────────"
