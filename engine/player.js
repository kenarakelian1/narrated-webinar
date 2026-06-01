(function() {
  const SEGMENTS = /*SEGMENTS_JSON*/;
  const CHAPTERS = /*CHAPTERS_JSON*/;

  const startScreen = document.getElementById('start-screen');
  const app = document.getElementById('app');
  const playBtn = document.getElementById('play-btn');
  const prevBtn = document.getElementById('prev-btn');
  const nextBtn = document.getElementById('next-btn');
  const pauseBtn = document.getElementById('pause-btn');
  const iconPause = document.getElementById('icon-pause');
  const iconPlay = document.getElementById('icon-play');
  const progressFill = document.getElementById('progress-fill');
  const timeDisplay = document.getElementById('time-display');
  const chapterList = document.getElementById('chapter-list');
  const segmentChapter = document.getElementById('segment-chapter');
  const segmentTitle = document.getElementById('segment-title');
  const scenes = document.querySelectorAll('.scene');

  let currentIdx = 0;
  let currentAudio = null;
  let isPaused = false;
  let rafId = null;

  CHAPTERS.forEach((ch, i) => {
    const li = document.createElement('li');
    li.className = 'chapter-item';
    li.dataset.chapterIdx = i;
    li.dataset.firstSeg = ch.firstIdx;
    const num = document.createElement('span');
    num.className = 'chapter-num';
    num.textContent = ch.icon;
    li.appendChild(num);
    const title = document.createElement('span');
    title.className = 'chapter-title';
    title.textContent = ch.title;
    li.appendChild(title);
    li.addEventListener('click', () => { jumpToSegment(ch.firstIdx); });
    chapterList.appendChild(li);
  });
  const chapterEls = chapterList.querySelectorAll('.chapter-item');

  function updateChapterHighlight(segIdx) {
    const chNum = SEGMENTS[segIdx].chapter;
    CHAPTERS.forEach((ch, i) => {
      const el = chapterEls[i];
      el.classList.toggle('active', ch.num === chNum);
      el.classList.toggle('played', ch.num < chNum);
    });
  }

  function fmtTime(s) {
    if (!isFinite(s) || s < 0) s = 0;
    const m = Math.floor(s / 60);
    const sec = Math.floor(s % 60);
    return m + ':' + sec.toString().padStart(2, '0');
  }

  // Clear any timed classes a scene element accumulated, and deactivate it.
  function resetScene(s) {
    s.classList.remove('active');
    if (s.dataset.timedApplied) {
      s.dataset.timedApplied.split(',').forEach(c => { if (c) s.classList.remove(c); });
      s.dataset.timedApplied = '';
    }
    if (s.dataset.highlightSel) {
      s.querySelectorAll(s.dataset.highlightSel).forEach(c => {
        c.classList.remove('active', 'dim');
      });
      s.dataset.highlightSel = '';
    }
  }

  function showScene(seg) {
    scenes.forEach(resetScene);
    const el = document.querySelector('.scene[data-scene="' + seg.scene + '"]');
    if (!el) return;
    el.classList.add('active');
    if (seg.highlight) {
      const cards = el.querySelectorAll(seg.highlight.selector);
      const act = new Set(seg.highlight.activeIndices || []);
      cards.forEach((c, i) => {
        c.classList.toggle('active', act.has(i));
        c.classList.toggle('dim', act.size > 0 && !act.has(i));
      });
      el.dataset.highlightSel = seg.highlight.selector;
    }
  }

  function applyTimedClasses(seg, t) {
    if (!seg.timedClasses) return;
    const el = document.querySelector('.scene[data-scene="' + seg.scene + '"]');
    if (!el) return;
    const applied = new Set((el.dataset.timedApplied || '').split(',').filter(Boolean));
    seg.timedClasses.forEach(tc => {
      if (t >= tc.at) { el.classList.add(tc.addClass); applied.add(tc.addClass); }
      else { el.classList.remove(tc.addClass); applied.delete(tc.addClass); }
    });
    el.dataset.timedApplied = [...applied].join(',');
  }

  function updateProgress() {
    if (!currentAudio) return;
    const t = currentAudio.currentTime || 0;
    const d = currentAudio.duration || 0;
    const pct = d > 0 ? (t / d) * 100 : 0;
    progressFill.style.width = pct + '%';
    timeDisplay.textContent = fmtTime(t) + ' / ' + fmtTime(d);
    applyTimedClasses(SEGMENTS[currentIdx], t);
    if (!isPaused && !currentAudio.paused && !currentAudio.ended) {
      rafId = requestAnimationFrame(updateProgress);
    }
  }

  function playSegment(idx) {
    if (idx < 0 || idx >= SEGMENTS.length) { cancelAnimationFrame(rafId); return; }
    currentIdx = idx;
    const seg = SEGMENTS[idx];
    showScene(seg);
    updateChapterHighlight(idx);
    segmentChapter.textContent = 'Ch ' + seg.chapter + ' · ' + seg.chapterTitle;
    segmentTitle.textContent = seg.title;
    if (currentAudio) { currentAudio.pause(); currentAudio.onended = null; }
    currentAudio = new Audio('audio/' + seg.id + '.mp3');
    currentAudio.preload = 'auto';
    currentAudio.addEventListener('loadedmetadata', () => {
      timeDisplay.textContent = '0:00 / ' + fmtTime(currentAudio.duration);
    });
    currentAudio.onended = () => playSegment(idx + 1);
    // Don't hang the deck if a segment's audio can't load — advance past it.
    currentAudio.addEventListener('error', () => {
      console.warn('Audio failed to load, skipping:', seg.id);
      playSegment(idx + 1);
    });
    currentAudio.play().catch(err => console.warn('Playback failed:', err));
    cancelAnimationFrame(rafId);
    updateProgress();
    if (idx + 1 < SEGMENTS.length) {
      const next = new Audio('audio/' + SEGMENTS[idx + 1].id + '.mp3');
      next.preload = 'auto';
    }
  }

  function jumpToSegment(idx) {
    if (idx < 0 || idx >= SEGMENTS.length) return;
    playSegment(idx);
    isPaused = false;
    iconPause.classList.remove('hidden');
    iconPlay.classList.add('hidden');
  }

  playBtn.addEventListener('click', () => {
    startScreen.classList.add('hidden');
    app.classList.add('visible');
    setTimeout(() => playSegment(0), 600);
  });

  pauseBtn.addEventListener('click', () => {
    if (!currentAudio) return;
    if (currentAudio.paused) {
      currentAudio.play(); isPaused = false;
      iconPause.classList.remove('hidden'); iconPlay.classList.add('hidden');
      updateProgress();
    } else {
      currentAudio.pause(); isPaused = true;
      iconPause.classList.add('hidden'); iconPlay.classList.remove('hidden');
      cancelAnimationFrame(rafId);
    }
  });

  prevBtn.addEventListener('click', () => jumpToSegment(currentIdx - 1));
  nextBtn.addEventListener('click', () => jumpToSegment(currentIdx + 1));

  document.addEventListener('keydown', (e) => {
    if (startScreen.classList.contains('hidden')) {
      if (e.code === 'Space') { e.preventDefault(); pauseBtn.click(); }
      if (e.code === 'ArrowRight') nextBtn.click();
      if (e.code === 'ArrowLeft') prevBtn.click();
    }
  });
})();
