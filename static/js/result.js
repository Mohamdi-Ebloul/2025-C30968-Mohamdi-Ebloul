// CancerDetect AI — Result page animations

(function () {
  'use strict';

  // Animate confidence progress bar
  const confBar = document.getElementById('confBar');
  if (confBar) {
    const value = confBar.dataset.value;
    requestAnimationFrame(() => {
      setTimeout(() => { confBar.style.width = value + '%'; }, 200);
    });
  }

  // Animate gauge counter and SVG arc
  const gaugeArc   = document.getElementById('gaugeArc');
  const gaugeValue = document.getElementById('gaugeValue');

  if (gaugeArc && gaugeValue) {
    const confidence = parseFloat(gaugeArc.dataset.confidence) || 0;
    const circumference = 339.3;
    const offset = circumference - (confidence / 100) * circumference;

    // Start at full offset (empty), animate to target
    gaugeArc.style.strokeDashoffset = circumference;

    let start = null;
    const duration = 1500;

    function animate(ts) {
      if (!start) start = ts;
      const progress = Math.min((ts - start) / duration, 1);
      const eased = 1 - Math.pow(1 - progress, 3); // ease-out-cubic

      const current = circumference - eased * (circumference - offset);
      gaugeArc.style.strokeDashoffset = current;
      gaugeValue.textContent = Math.round(eased * confidence);

      if (progress < 1) requestAnimationFrame(animate);
    }

    requestAnimationFrame(animate);
  }

})();
