from django.contrib import admin
from django.utils.html import format_html
from .models import Analysis


@admin.register(Analysis)
class AnalysisAdmin(admin.ModelAdmin):
    list_display = ('id', 'result_badge', 'confidence_display', 'created_at', 'processing_time_display')
    list_filter = ('result', 'created_at')
    search_fields = ('result', 'notes')
    readonly_fields = ('created_at', 'raw_score', 'processing_time', 'image_preview', 'gradcam_preview')
    ordering = ('-created_at',)

    fieldsets = (
        ('Image', {'fields': ('image', 'image_preview')}),
        ('Résultat IA', {'fields': ('result', 'confidence', 'raw_score', 'processing_time')}),
        ('Grad-CAM', {'fields': ('gradcam_image', 'gradcam_preview')}),
        ('Informations', {'fields': ('notes', 'created_at')}),
    )

    def result_badge(self, obj):
        color = 'red' if obj.result == 'Malignant' else 'green'
        return format_html(
            '<span style="color:white;background:{};padding:3px 8px;border-radius:4px;">{}</span>',
            color, obj.result
        )
    result_badge.short_description = 'Résultat'

    def confidence_display(self, obj):
        return f"{obj.confidence:.1f}%"
    confidence_display.short_description = 'Confiance'

    def processing_time_display(self, obj):
        return f"{obj.processing_time:.3f}s"
    processing_time_display.short_description = 'Durée'

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-height:200px;"/>', obj.image.url)
        return '—'
    image_preview.short_description = 'Aperçu image'

    def gradcam_preview(self, obj):
        if obj.gradcam_image:
            return format_html('<img src="{}" style="max-height:200px;"/>', obj.gradcam_image.url)
        return '—'
    gradcam_preview.short_description = 'Aperçu Grad-CAM'
