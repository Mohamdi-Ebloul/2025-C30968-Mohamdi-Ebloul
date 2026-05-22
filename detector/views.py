import time
import os
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.conf import settings
from .forms import AnalysisForm
from .models import Analysis
from .ai_model import predictor as ai_predictor


def home(request):
    recent_analyses = Analysis.objects.all()[:6]
    total_analyses = Analysis.objects.count()
    benign_count = Analysis.objects.filter(result='Benign').count()
    malignant_count = Analysis.objects.filter(result='Malignant').count()

    context = {
        'recent_analyses': recent_analyses,
        'total_analyses': total_analyses,
        'benign_count': benign_count,
        'malignant_count': malignant_count,
    }
    return render(request, 'detector/home.html', context)


def upload(request):
    if request.method == 'POST':
        form = AnalysisForm(request.POST, request.FILES)
        if form.is_valid():
            analysis = form.save(commit=False)
            analysis.save()

            image_path = analysis.image.path
            start_time = time.time()

            try:
                prediction = ai_predictor.predict(image_path)
                analysis.result = prediction['label']
                analysis.confidence = prediction['confidence']
                analysis.raw_score = prediction['raw_score']
                analysis.processing_time = round(time.time() - start_time, 3)

                # Generate Grad-CAM heatmap
                try:
                    model = ai_predictor.get_model()
                    gradcam_abs_path = ai_predictor.generate_gradcam(image_path, model)
                    if gradcam_abs_path and os.path.exists(gradcam_abs_path):
                        rel_path = os.path.relpath(gradcam_abs_path, settings.MEDIA_ROOT)
                        analysis.gradcam_image = rel_path
                except Exception as gradcam_error:
                    print(f"[Grad-CAM] Non-critical error: {gradcam_error}")

                analysis.save()
                messages.success(request, 'Analyse effectuée avec succès.')
                return redirect('detector:result', pk=analysis.pk)

            except Exception as e:
                analysis.delete()
                messages.error(request, f'Erreur lors de l\'analyse : {str(e)}')
                return redirect('detector:upload')
    else:
        form = AnalysisForm()

    return render(request, 'detector/upload.html', {'form': form})


def result(request, pk):
    analysis = get_object_or_404(Analysis, pk=pk)
    return render(request, 'detector/result.html', {'analysis': analysis})


def history(request):
    analyses = Analysis.objects.all()
    total = analyses.count()
    benign_count = analyses.filter(result='Benign').count()
    malignant_count = analyses.filter(result='Malignant').count()
    benign_pct = round(benign_count / total * 100) if total else 0
    malignant_pct = round(malignant_count / total * 100) if total else 0

    context = {
        'analyses': analyses,
        'total': total,
        'benign_count': benign_count,
        'malignant_count': malignant_count,
        'benign_pct': benign_pct,
        'malignant_pct': malignant_pct,
    }
    return render(request, 'detector/history.html', context)


def delete_analysis(request, pk):
    analysis = get_object_or_404(Analysis, pk=pk)
    if request.method == 'POST':
        # Remove associated files
        if analysis.image and os.path.exists(analysis.image.path):
            os.remove(analysis.image.path)
        if analysis.gradcam_image:
            gradcam_path = os.path.join(settings.MEDIA_ROOT, str(analysis.gradcam_image))
            if os.path.exists(gradcam_path):
                os.remove(gradcam_path)
        analysis.delete()
        messages.success(request, 'Analyse supprimée avec succès.')
    return redirect('detector:history')


def about(request):
    techs = ['Python 3.9', 'Django 4.2', 'TensorFlow 2.15', 'Keras', 'OpenCV', 'Bootstrap 5', 'SQLite']
    return render(request, 'detector/about.html', {'techs': techs})
