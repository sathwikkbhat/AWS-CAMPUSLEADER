// Presentation Navigation & Interactivity
document.addEventListener('DOMContentLoaded', () => {
  const slides = document.querySelectorAll('.slide');
  const totalSlides = slides.length;
  let currentSlide = 1;

  const btnPrev = document.getElementById('btn-prev');
  const btnNext = document.getElementById('btn-next');
  const slideIndicator = document.getElementById('slide-indicator');
  const progressBar = document.getElementById('progress-bar');
  const dots = document.querySelectorAll('.dot-btn');
  const btnFullscreen = document.getElementById('btn-fullscreen');
  const btnNotes = document.getElementById('btn-notes');
  const btnCloseNotes = document.getElementById('btn-close-notes');
  const notesDrawer = document.getElementById('notes-drawer');
  const noteBoxes = document.querySelectorAll('.note-box');

  function updateSlide(newSlide) {
    if (newSlide < 1) newSlide = 1;
    if (newSlide > totalSlides) newSlide = totalSlides;

    currentSlide = newSlide;

    // Update active slide class
    slides.forEach((slide) => {
      const slideNum = parseInt(slide.dataset.slide, 10);
      if (slideNum === currentSlide) {
        slide.classList.add('active');
      } else {
        slide.classList.remove('active');
      }
    });

    // Update indicator and progress bar
    if (slideIndicator) {
      slideIndicator.textContent = `Slide ${currentSlide} of ${totalSlides}`;
    }

    if (progressBar) {
      const pct = (currentSlide / totalSlides) * 100;
      progressBar.style.width = `${pct}%`;
    }

    // Update dots
    dots.forEach((dot) => {
      const dotIndex = parseInt(dot.dataset.index, 10);
      if (dotIndex === currentSlide) {
        dot.classList.add('active');
      } else {
        dot.classList.remove('active');
      }
    });

    // Update Prev / Next button states
    if (btnPrev) {
      btnPrev.disabled = currentSlide === 1;
      btnPrev.style.opacity = currentSlide === 1 ? '0.5' : '1';
    }

    if (btnNext) {
      if (currentSlide === totalSlides) {
        btnNext.innerHTML = `<span>Finished</span>`;
      } else {
        btnNext.innerHTML = `<span>Next</span><svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="9 18 15 12 9 6"></polyline></svg>`;
      }
    }

    // Highlight corresponding notes box
    noteBoxes.forEach((box) => {
      box.classList.remove('active-note');
    });
    const activeNoteBox = document.getElementById(`note-slide-${currentSlide}`);
    if (activeNoteBox) {
      activeNoteBox.classList.add('active-note');
      activeNoteBox.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    }
  }

  // Event Listeners for Buttons
  if (btnPrev) {
    btnPrev.addEventListener('click', () => updateSlide(currentSlide - 1));
  }

  if (btnNext) {
    btnNext.addEventListener('click', () => {
      if (currentSlide < totalSlides) {
        updateSlide(currentSlide + 1);
      }
    });
  }

  // Dots click
  dots.forEach((dot) => {
    dot.addEventListener('click', () => {
      const idx = parseInt(dot.dataset.index, 10);
      updateSlide(idx);
    });
  });

  // Keyboard navigation
  document.addEventListener('keydown', (e) => {
    if (e.target.tagName === 'INPUT' || e.target.tagName === 'TEXTAREA') return;

    if (e.key === 'ArrowRight' || e.key === 'PageDown' || e.key === ' ') {
      e.preventDefault();
      if (currentSlide < totalSlides) updateSlide(currentSlide + 1);
    } else if (e.key === 'ArrowLeft' || e.key === 'PageUp') {
      e.preventDefault();
      if (currentSlide > 1) updateSlide(currentSlide - 1);
    } else if (e.key === 'f' || e.key === 'F') {
      toggleFullscreen();
    } else if (e.key === 's' || e.key === 'S' || e.key === 'n' || e.key === 'N') {
      toggleNotes();
    } else if (e.key >= '1' && e.key <= '6') {
      updateSlide(parseInt(e.key, 10));
    }
  });

  // Fullscreen Toggle
  function toggleFullscreen() {
    if (!document.fullscreenElement) {
      document.documentElement.requestFullscreen().catch((err) => {
        console.error(`Error attempting to enable fullscreen: ${err.message}`);
      });
    } else {
      if (document.exitFullscreen) {
        document.exitFullscreen();
      }
    }
  }

  if (btnFullscreen) {
    btnFullscreen.addEventListener('click', toggleFullscreen);
  }

  // Notes Drawer Toggle
  function toggleNotes() {
    if (notesDrawer) {
      notesDrawer.classList.toggle('open');
    }
  }

  if (btnNotes) {
    btnNotes.addEventListener('click', toggleNotes);
  }

  if (btnCloseNotes) {
    btnCloseNotes.addEventListener('click', () => {
      if (notesDrawer) notesDrawer.classList.remove('open');
    });
  }

  // Touch / Swipe Navigation for Mobile
  let touchStartX = 0;
  let touchStartY = 0;
  let touchEndX = 0;
  let touchEndY = 0;

  const deckContainer = document.getElementById('deck-container');
  if (deckContainer) {
    deckContainer.addEventListener('touchstart', (e) => {
      touchStartX = e.changedTouches[0].screenX;
      touchStartY = e.changedTouches[0].screenY;
    }, { passive: true });

    deckContainer.addEventListener('touchend', (e) => {
      touchEndX = e.changedTouches[0].screenX;
      touchEndY = e.changedTouches[0].screenY;
      handleSwipe();
    }, { passive: true });
  }

  function handleSwipe() {
    const deltaX = touchEndX - touchStartX;
    const deltaY = touchEndY - touchStartY;

    // Trigger if horizontal swipe is > 45px and dominant over vertical scroll
    if (Math.abs(deltaX) > 45 && Math.abs(deltaX) > Math.abs(deltaY)) {
      if (deltaX < 0) {
        // Swiped Left -> Next Slide
        if (currentSlide < totalSlides) updateSlide(currentSlide + 1);
      } else {
        // Swiped Right -> Previous Slide
        if (currentSlide > 1) updateSlide(currentSlide - 1);
      }
    }
  }

  // Initial setup
  updateSlide(1);
});
