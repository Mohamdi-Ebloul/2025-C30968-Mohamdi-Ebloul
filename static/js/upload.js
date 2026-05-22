// CancerDetect AI — Upload page interactions

(function () {
  'use strict';

  const dropZone     = document.getElementById('dropZone');
  const fileInput    = document.getElementById('imageUpload');
  const dropContent  = document.getElementById('dropContent');
  const imagePreview = document.getElementById('imagePreview');
  const imageInfo    = document.getElementById('imageInfo');
  const fileName     = document.getElementById('fileName');
  const fileSize     = document.getElementById('fileSize');
  const removeBtn    = document.getElementById('removeImage');
  const submitBtn    = document.getElementById('submitBtn');
  const form         = document.getElementById('analysisForm');
  const progressOvl  = document.getElementById('progressOverlay');
  const mainBar      = document.getElementById('mainProgressBar');

  if (!dropZone) return;

  // Drag & drop events
  ['dragenter', 'dragover'].forEach(evt => {
    dropZone.addEventListener(evt, e => {
      e.preventDefault();
      dropZone.classList.add('drag-over');
    });
  });

  ['dragleave', 'drop'].forEach(evt => {
    dropZone.addEventListener(evt, e => {
      e.preventDefault();
      dropZone.classList.remove('drag-over');
    });
  });

  dropZone.addEventListener('drop', e => {
    const file = e.dataTransfer.files[0];
    if (file) setFile(file);
  });

  // File input change
  fileInput.addEventListener('change', () => {
    if (fileInput.files.length > 0) setFile(fileInput.files[0]);
  });

  function setFile(file) {
    // Validate type
    const allowed = ['image/jpeg', 'image/png', 'image/bmp', 'image/tiff'];
    if (!allowed.includes(file.type) && !file.name.match(/\.(jpg|jpeg|png|bmp|tiff|tif)$/i)) {
      showError('Format non supporté. Formats acceptés : JPG, PNG, BMP, TIFF');
      return;
    }
    if (file.size > 10 * 1024 * 1024) {
      showError("L'image ne doit pas dépasser 10 MB.");
      return;
    }

    const reader = new FileReader();
    reader.onload = e => {
      imagePreview.src = e.target.result;
      imagePreview.classList.remove('d-none');
      dropContent.classList.add('d-none');
      dropZone.classList.add('has-file');

      // Info bar
      fileName.textContent = file.name;
      fileSize.textContent = formatBytes(file.size);
      imageInfo.classList.remove('d-none');

      submitBtn.disabled = false;
    };
    reader.readAsDataURL(file);
  }

  function showError(msg) {
    const div = document.createElement('div');
    div.className = 'alert alert-danger alert-dismissible fade show mt-2 py-2';
    div.innerHTML = `<i class="bi bi-exclamation-triangle me-1"></i>${msg}
      <button type="button" class="btn-close" data-bs-dismiss="alert"></button>`;
    dropZone.insertAdjacentElement('afterend', div);
    setTimeout(() => bootstrap.Alert.getOrCreateInstance(div).close(), 4000);
  }

  // Remove image
  removeBtn && removeBtn.addEventListener('click', () => {
    fileInput.value = '';
    imagePreview.src = '#';
    imagePreview.classList.add('d-none');
    dropContent.classList.remove('d-none');
    dropZone.classList.remove('has-file');
    imageInfo.classList.add('d-none');
    submitBtn.disabled = true;
  });

  // Form submission — show progress overlay
  form.addEventListener('submit', () => {
    submitBtn.querySelector('#btnNormal').classList.add('d-none');
    submitBtn.querySelector('#btnLoading').classList.remove('d-none');
    submitBtn.disabled = true;

    progressOvl.classList.remove('d-none');
    animateSteps();
  });

  // Animated progress steps
  function animateSteps() {
    const steps = document.querySelectorAll('.step-item');
    const durations = [400, 600, 900, 700, 400]; // ms per step
    let delay = 0;
    steps.forEach((step, i) => {
      setTimeout(() => {
        if (i > 0) steps[i - 1].classList.replace('active', 'done');
        step.classList.add('active');
        const pct = Math.round(((i + 1) / steps.length) * 100);
        mainBar.style.width = pct + '%';
      }, delay);
      delay += durations[i];
    });
  }

  function formatBytes(bytes) {
    if (bytes < 1024) return bytes + ' B';
    if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(1) + ' KB';
    return (bytes / (1024 * 1024)).toFixed(2) + ' MB';
  }

})();
