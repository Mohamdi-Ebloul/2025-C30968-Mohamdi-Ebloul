from django.apps import AppConfig


class DetectorConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'detector'
    verbose_name = 'Breast Cancer Detector'

    def ready(self):
        # Pre-load the AI model when Django starts (only if TF is available)
        try:
            import tensorflow  # noqa: F401 — trigger ImportError early if missing
            from .ai_model.predictor import get_model
            get_model()
            print("[AI] Model loaded successfully at startup.")
        except ImportError:
            print("[AI] TensorFlow not installed — AI features disabled until installed.")
        except Exception as e:
            print(f"[AI] Warning: Could not pre-load model at startup: {e}")
