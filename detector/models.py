from django.db import models
from django.utils import timezone


class Analysis(models.Model):
    RESULT_CHOICES = [
        ('Benign', 'Benign'),
        ('Malignant', 'Malignant'),
    ]

    image = models.ImageField(upload_to='uploads/%Y/%m/%d/')
    result = models.CharField(max_length=20, choices=RESULT_CHOICES, blank=True)
    confidence = models.FloatField(default=0.0)
    raw_score = models.FloatField(default=0.0)
    gradcam_image = models.ImageField(upload_to='gradcam/%Y/%m/%d/', null=True, blank=True)
    notes = models.TextField(blank=True, verbose_name='Notes du médecin')
    created_at = models.DateTimeField(default=timezone.now)
    processing_time = models.FloatField(default=0.0, help_text='Temps de traitement en secondes')

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Analyse'
        verbose_name_plural = 'Analyses'

    def __str__(self):
        return f"Analyse #{self.id} — {self.result} ({self.confidence:.1f}%)"

    @property
    def result_color(self):
        return 'danger' if self.result == 'Malignant' else 'success'

    @property
    def result_icon(self):
        return 'exclamation-triangle' if self.result == 'Malignant' else 'check-circle'

    @property
    def confidence_color(self):
        if self.confidence >= 90:
            return 'success'
        elif self.confidence >= 70:
            return 'warning'
        return 'danger'
