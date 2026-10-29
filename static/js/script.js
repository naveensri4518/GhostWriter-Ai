/**
 * GhostWriter AI - Client-side Application Script
 * Vanilla JavaScript implementation for horror story generation with Ollama
 */

document.addEventListener('DOMContentLoaded', () => {
  // DOM Elements
  const form = document.getElementById('story-form');
  const promptInput = document.getElementById('prompt-input');
  const charCount = document.getElementById('char-count');
  const generateBtn = document.getElementById('generate-btn');
  const loadingSection = document.getElementById('loading-section');
  const loadingStage = document.getElementById('loading-stage');
  const storySection = document.getElementById('story-section');
  const storyTitle = document.getElementById('story-title');
  const storyBody = document.getElementById('story-body');
  const storyCategoryBadge = document.getElementById('story-category-badge');
  const storyEndingBadge = document.getElementById('story-ending-badge');
  const storyModelBadge = document.getElementById('story-model-badge');
  const storyStatsBadge = document.getElementById('story-stats-badge');
  const copyStoryBtn = document.getElementById('copy-story-btn');
  const copyBtnText = document.getElementById('copy-btn-text');
  const downloadStoryBtn = document.getElementById('download-story-btn');
  const regenerateBtn = document.getElementById('regenerate-btn');
  const promptChips = document.querySelectorAll('.prompt-chip');
  const categoryRadios = document.querySelectorAll('input[name="category"]');
  const endingRadios = document.querySelectorAll('input[name="ending"]');
  const categorySelectedTag = document.getElementById('category-selected-tag');
  const endingSelectedTag = document.getElementById('ending-selected-tag');

  // Status Elements
  const statusDot = document.getElementById('status-dot');
  const statusLabel = document.getElementById('status-label');
  const statusModelBadge = document.getElementById('status-model-badge');
  const refreshStatusBtn = document.getElementById('refresh-status-btn');
  const serviceBanner = document.getElementById('service-banner');
  const serviceBannerTitle = document.getElementById('service-banner-title');
  const serviceBannerMessage = document.getElementById('service-banner-message');

  // Error Banner & Toast Elements
  const errorBanner = document.getElementById('error-banner');
  const errorMessage = document.getElementById('error-message');
  const errorCloseBtn = document.getElementById('error-close-btn');
  const toast = document.getElementById('toast');

  // State
  let currentStoryData = null;
  let isGenerating = false;
  let stageInterval = null;

  const STAGES = [
    'Communing with local neural weights...',
    'Channeling shadows from the abyss...',
    'Whispering dread into the prose...',
    'Forging the chilling climax...',
    'Sealing the tale in ink...'
  ];

  /* ==========================================================================
     1. Ambient Fog & Floating Particles Canvas
     ========================================================================== */
  function initAmbientParticles() {
    const canvas = document.getElementById('ambient-fog');
    if (!canvas) return;
    const ctx = canvas.getContext('2d');

    let width = (canvas.width = window.innerWidth);
    let height = (canvas.height = window.innerHeight);

    window.addEventListener('resize', () => {
      width = canvas.width = window.innerWidth;
      height = canvas.height = window.innerHeight;
    });

    const particles = [];
    const count = Math.min(35, Math.floor(width / 35));

    for (let i = 0; i < count; i++) {
      particles.push({
        x: Math.random() * width,
        y: Math.random() * height,
        radius: Math.random() * 2.5 + 0.8,
        speedX: (Math.random() - 0.5) * 0.35,
        speedY: -Math.random() * 0.45 - 0.15,
        alpha: Math.random() * 0.45 + 0.1,
        color: Math.random() > 0.6 ? 'rgba(230, 57, 70,' : 'rgba(139, 92, 246,'
      });
    }

    function render() {
      ctx.clearRect(0, 0, width, height);

      particles.forEach((p) => {
        p.x += p.speedX;
        p.y += p.speedY;

        if (p.y < -10) {
          p.y = height + 10;
          p.x = Math.random() * width;
        }
        if (p.x < -10) p.x = width + 10;
        if (p.x > width + 10) p.x = -10;

        ctx.beginPath();
        ctx.arc(p.x, p.y, p.radius, 0, Math.PI * 2);
        ctx.fillStyle = `${p.color} ${p.alpha})`;
        ctx.shadowBlur = 10;
        ctx.shadowColor = p.color === 'rgba(230, 57, 70,' ? '#E63946' : '#8B5CF6';
        ctx.fill();
      });

      requestAnimationFrame(render);
    }

    render();
  }

  /* ==========================================================================
     2. Health Check & AI Service Status
     ========================================================================== */
  async function checkHealth() {
    statusDot.className = 'status-dot pulse';
    statusLabel.textContent = 'Checking AI...';

    try {
      const response = await fetch('/api/health');
      const data = await response.json();

      if (data.status === 'healthy') {
        statusDot.className = 'status-dot online';
        statusLabel.textContent = 'Ollama Ready';
        statusModelBadge.textContent = data.configured_model;
        serviceBanner.classList.add('hidden');
      } else if (data.status === 'degraded') {
        statusDot.className = 'status-dot degraded';
        statusLabel.textContent = 'Model Missing';
        statusModelBadge.textContent = data.configured_model;
        showServiceBanner(
          'Model Not Found in Ollama',
          `The configured model "${data.configured_model}" is missing. In PowerShell, run: ollama pull ${data.configured_model}`
        );
      } else {
        statusDot.className = 'status-dot offline';
        statusLabel.textContent = 'Ollama Offline';
        showServiceBanner(
          'Ollama Service Not Detected',
          data.message || 'Please start the Ollama service by running: ollama serve'
        );
      }
    } catch (err) {
      statusDot.className = 'status-dot offline';
      statusLabel.textContent = 'Backend Offline';
      showServiceBanner(
        'Backend Connection Error',
        'Could not communicate with the local GhostWriter server. Ensure app.py is running.'
      );
    }
  }

  function showServiceBanner(title, message) {
    serviceBannerTitle.textContent = title;
    serviceBannerMessage.textContent = message;
    serviceBanner.classList.remove('hidden');
  }

  refreshStatusBtn.addEventListener('click', () => {
    checkHealth();
    showToast('Checking Ollama status...');
  });

  /* ==========================================================================
     3. Form Interactions & UI Feedback
     ========================================================================== */
  // Character counter
  promptInput.addEventListener('input', () => {
    const len = promptInput.value.length;
    charCount.textContent = `${len} / 1000`;
  });

  // Prompt chips fill
  promptChips.forEach((chip) => {
    chip.addEventListener('click', () => {
      const text = chip.getAttribute('data-prompt');
      promptInput.value = text;
      promptInput.dispatchEvent(new Event('input'));
      promptInput.focus();
    });
  });

  // Category change indicator
  categoryRadios.forEach((radio) => {
    radio.addEventListener('change', () => {
      if (radio.checked) {
        categorySelectedTag.textContent = radio.value;
      }
    });
  });

  // Ending change indicator
  endingRadios.forEach((radio) => {
    radio.addEventListener('change', () => {
      if (radio.checked) {
        endingSelectedTag.textContent = radio.value;
      }
    });
  });

  // Keyboard shortcut: Ctrl+Enter / Cmd+Enter
  promptInput.addEventListener('keydown', (e) => {
    if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
      e.preventDefault();
      form.requestSubmit();
    }
  });

  /* ==========================================================================
     4. Story Generation Execution
     ========================================================================== */
  form.addEventListener('submit', async (e) => {
    e.preventDefault();
    if (isGenerating) return;

    const prompt = promptInput.value.trim();
    if (!prompt) {
      showError('Please enter a premise or choose an inspiration chip first.');
      promptInput.focus();
      return;
    }

    const selectedCategory = document.querySelector('input[name="category"]:checked')?.value || 'Ghost Stories';
    const selectedEnding = document.querySelector('input[name="ending"]:checked')?.value || 'Terrifying';

    hideError();
    startLoading();

    try {
      const response = await fetch('/api/generate', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          prompt: prompt,
          category: selectedCategory,
          ending: selectedEnding
        })
      });

      const data = await response.json();

      if (!response.ok || !data.success) {
        throw new Error(data.error || 'Failed to generate story.');
      }

      currentStoryData = data;
      renderStory(data);
    } catch (err) {
      showError(err.message);
    } finally {
      stopLoading();
    }
  });

  // Regenerate button
  regenerateBtn.addEventListener('click', () => {
    form.requestSubmit();
  });

  /* ==========================================================================
     5. Loading State Management
     ========================================================================== */
  function startLoading() {
    isGenerating = true;
    generateBtn.disabled = true;
    generateBtn.querySelector('.btn-text').textContent = 'Summoning...';
    
    // Hide previous story, show loading
    storySection.classList.add('hidden');
    loadingSection.classList.remove('hidden');
    loadingSection.scrollIntoView({ behavior: 'smooth', block: 'center' });

    let stageIdx = 0;
    loadingStage.textContent = STAGES[0];
    stageInterval = setInterval(() => {
      stageIdx = (stageIdx + 1) % STAGES.length;
      loadingStage.textContent = STAGES[stageIdx];
    }, 2800);
  }

  function stopLoading() {
    isGenerating = false;
    generateBtn.disabled = false;
    generateBtn.querySelector('.btn-text').textContent = 'Summon Story';
    loadingSection.classList.add('hidden');
    if (stageInterval) {
      clearInterval(stageInterval);
      stageInterval = null;
    }
  }

  /* ==========================================================================
     6. Story Rendering
     ========================================================================== */
  function renderStory(data) {
    storyTitle.textContent = data.title || 'Untitled Horror';
    storyCategoryBadge.textContent = data.category;
    storyEndingBadge.textContent = data.ending;
    storyModelBadge.textContent = data.model;
    storyStatsBadge.textContent = `${data.word_count} words • ${data.reading_time_minutes} min read`;

    // Format paragraphs
    const paragraphs = data.story
      .split(/\n\s*\n/)
      .map((p) => p.trim())
      .filter((p) => p.length > 0);

    storyBody.innerHTML = '';
    paragraphs.forEach((pText) => {
      const pElem = document.createElement('p');
      pElem.textContent = pText;
      storyBody.appendChild(pElem);
    });

    storySection.classList.remove('hidden');
    storySection.scrollIntoView({ behavior: 'smooth', block: 'start' });
    showToast('Your horror story has materialized. 🦇');
  }

  /* ==========================================================================
     7. Copy & Download Features
     ========================================================================== */
  copyStoryBtn.addEventListener('click', async () => {
    if (!currentStoryData) return;

    const fullText = `${currentStoryData.title}\n\nCategory: ${currentStoryData.category} | Ending: ${currentStoryData.ending} | Model: ${currentStoryData.model}\n\n${currentStoryData.story}\n\n-- Generated by GhostWriter AI`;

    try {
      await navigator.clipboard.writeText(fullText);
      const originalText = copyBtnText.textContent;
      copyBtnText.textContent = 'Copied to Clipboard! 🦇';
      showToast('Story copied to clipboard!');
      setTimeout(() => {
        copyBtnText.textContent = originalText;
      }, 2500);
    } catch (err) {
      // Fallback
      const ta = document.createElement('textarea');
      ta.value = fullText;
      document.body.appendChild(ta);
      ta.select();
      document.execCommand('copy');
      document.body.removeChild(ta);
      showToast('Story copied to clipboard!');
    }
  });

  downloadStoryBtn.addEventListener('click', () => {
    if (!currentStoryData) return;

    const fullText = `${currentStoryData.title.toUpperCase()}\n========================================\nCategory: ${currentStoryData.category}\nEnding:   ${currentStoryData.ending}\nModel:    ${currentStoryData.model}\nDate:     ${new Date().toLocaleString()}\n========================================\n\n${currentStoryData.story}\n\n---\nGenerated locally by GhostWriter AI (Hacktoberfest Week 4)`;

    const blob = new Blob([fullText], { type: 'text/plain;charset=utf-8' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    const safeTitle = currentStoryData.title.toLowerCase().replace(/[^a-z0-9]+/g, '-').slice(0, 30);
    a.href = url;
    a.download = `ghostwriter-${safeTitle || 'horror'}.txt`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
    showToast('Story downloaded as .txt file 📜');
  });

  /* ==========================================================================
     8. Error & Toast Notifications
     ========================================================================== */
  function showError(msg) {
    errorMessage.textContent = msg;
    errorBanner.classList.remove('hidden');
    errorBanner.scrollIntoView({ behavior: 'smooth', block: 'center' });
  }

  function hideError() {
    errorBanner.classList.add('hidden');
  }

  errorCloseBtn.addEventListener('click', hideError);

  let toastTimer = null;
  function showToast(msg) {
    if (toastTimer) clearTimeout(toastTimer);
    toast.textContent = msg;
    toast.classList.remove('hidden');
    toastTimer = setTimeout(() => {
      toast.classList.add('hidden');
    }, 3200);
  }

  /* ==========================================================================
     9. Initialization
     ========================================================================== */
  initAmbientParticles();
  checkHealth();
  // Periodic status poll every 20 seconds
  setInterval(checkHealth, 20000);
});
