"""The Compass — a worked example for the narrated-webinar skill (single-file format).

A fictional AI-governance advisory webinar, included only as a reference for
authoring your own webinar.py.
"""

META = {
    "title": "The Compass",
    "eyebrow": "EXECUTIVE BRIEFING",
    "subtitle": "A 10-minute walk through the AI operating model your bank needs before the next board meeting.",
    "preview": [
        {"num": "PART ONE", "title": "The storm every CEO knows"},
        {"num": "PART TWO", "title": "The eight pieces of the operating model"},
        {"num": "PART THREE", "title": "Two weeks. Three artifacts. $35K."},
    ],
    "start_meta": "10 minutes · narrated · 7 segments",
    "property_line": "",
    "sidebar_eyebrow": "Executive Webinar",
    "sidebar_title": "AI in Banking",
    "stage_property": "",
}

VOICE = {
    "id": "EXAVITQu4vr4xnSDxMaL",
    "model": "eleven_multilingual_v2",
    "settings": {
        "stability": 0.55,
        "similarity_boost": 0.8,
        "style": 0.22,
        "use_speaker_boost": True,
    },
}

SCENES = {
    "coldopen": {
        "html": """
        <div class="coldopen-titlecard">
          <div class="coldopen-titlecard-text">The Compass<br><small style="color: var(--text-dim); font-size: 0.5em; letter-spacing: 0.3em;">AI GOVERNANCE</small></div>
        </div>
        <div class="coldopen-sky">
          <span class="coldopen-cloud">GEMINI</span>
          <span class="coldopen-cloud">GROK</span>
          <span class="coldopen-cloud">GPT</span>
          <span class="coldopen-cloud">CLAUDE</span>
          <span class="coldopen-cloud">COPILOT</span>
          <span class="coldopen-cloud">LLAMA</span>
        </div>

        <div class="coldopen-sea">
          <div class="coldopen-wave coldopen-wave-1"></div>
          <div class="coldopen-wave coldopen-wave-2"></div>
        </div>

        <svg class="coldopen-ship" viewBox="0 0 200 120" xmlns="http://www.w3.org/2000/svg">
          <!-- hull -->
          <path d="M 20 80 L 180 80 L 160 110 L 40 110 Z" fill="#0a1428" stroke="#d4a647" stroke-width="2"/>
          <!-- mast -->
          <line x1="100" y1="80" x2="100" y2="10" stroke="#d4a647" stroke-width="2"/>
          <!-- sail -->
          <path d="M 100 15 L 100 75 L 145 75 Z" fill="#e8eef8" opacity="0.85"/>
          <!-- flag -->
          <path d="M 100 10 L 120 14 L 100 18 Z" fill="#d4a647"/>
          <!-- ceo silhouette at helm -->
          <circle cx="80" cy="68" r="5" fill="#0a1428"/>
          <rect x="76" y="73" width="8" height="10" fill="#0a1428"/>
        </svg>

        <span class="coldopen-bubble">$50K!</span>
        <span class="coldopen-bubble">Who approved this?</span>
        <span class="coldopen-bubble">We need a CAIO!</span>
        <span class="coldopen-bubble">It's in the policy!</span>

        <div class="coldopen-compass">THE<br>COMPASS</div>

        <div class="coldopen-final">
          <div class="coldopen-final-title">The Compass</div>
          <div class="coldopen-final-sub">Decide · Govern · Invest</div>
        </div>
""",
        "css": """
  .scene-coldopen {
    position: relative;
    width: 100%; height: 100%;
    overflow: hidden;
    background: linear-gradient(180deg, #0a1428 0%, #142347 60%, #1a2a4f 100%);
    transition: background 8s ease-in-out;
  }
  .scene-coldopen.active.calm {
    background: linear-gradient(180deg, #c5d6f0 0%, #f4c869 70%, #ffb878 100%);
  }
  .coldopen-sky { position: absolute; inset: 0; }
  .coldopen-cloud {
    position: absolute;
    font-weight: 700;
    color: #1a2a4f;
    background: rgba(180, 195, 220, 0.92);
    padding: 0.35rem 0.9rem;
    border-radius: 999px;
    font-size: 0.85rem;
    letter-spacing: 0.1em;
    box-shadow: 0 8px 30px rgba(0,0,0,0.4);
    opacity: 0;
    transform: translateY(-40px);
    transition: opacity 0.8s ease, transform 1.2s ease;
  }
  .scene-coldopen.active .coldopen-cloud { opacity: 1; transform: translateY(0); }
  .scene-coldopen.active.calm .coldopen-cloud {
    opacity: 0;
    transform: translateY(-120px) scale(0.6);
    transition: opacity 1.5s ease, transform 2s ease;
  }
  .scene-coldopen.active .coldopen-cloud:nth-of-type(1) { transition-delay: 0.4s; top: 14%; left: 8%; }
  .scene-coldopen.active .coldopen-cloud:nth-of-type(2) { transition-delay: 0.9s; top: 9%;  left: 28%; }
  .scene-coldopen.active .coldopen-cloud:nth-of-type(3) { transition-delay: 1.4s; top: 18%; left: 50%; }
  .scene-coldopen.active .coldopen-cloud:nth-of-type(4) { transition-delay: 1.9s; top: 11%; left: 68%; }
  .scene-coldopen.active .coldopen-cloud:nth-of-type(5) { transition-delay: 2.4s; top: 20%; left: 84%; }
  .scene-coldopen.active .coldopen-cloud:nth-of-type(6) { transition-delay: 2.9s; top: 7%;  left: 92%; transform: translateX(-100%); }

  .coldopen-sea {
    position: absolute;
    bottom: 0; left: 0; right: 0; height: 38%;
    background: linear-gradient(180deg, transparent 0%, rgba(10,20,40,0.6) 100%);
  }
  .coldopen-wave {
    position: absolute;
    bottom: 0; left: -10%; right: -10%;
    height: 100%;
    background-repeat: repeat-x;
    background-size: 200px 80px;
    animation: waveMove 4s linear infinite;
  }
  .coldopen-wave-1 {
    background-image: radial-gradient(ellipse 100px 14px at 50% 100%, rgba(255,255,255,0.18), transparent 70%);
    bottom: 12%;
  }
  .coldopen-wave-2 {
    background-image: radial-gradient(ellipse 130px 18px at 50% 100%, rgba(255,255,255,0.12), transparent 70%);
    bottom: 6%;
    animation-duration: 6s;
    animation-direction: reverse;
  }
  .scene-coldopen.active.calm .coldopen-wave { animation-duration: 14s; opacity: 0.6; }
  @keyframes waveMove {
    from { background-position: 0 0; }
    to   { background-position: 200px 0; }
  }

  .coldopen-ship {
    position: absolute;
    bottom: 20%; left: 50%;
    transform: translateX(-50%);
    width: 200px; height: 120px;
    animation: shipRock 3.5s ease-in-out infinite;
  }
  @keyframes shipRock {
    0%, 100% { transform: translateX(-50%) rotate(-3deg); }
    50%      { transform: translateX(-50%) rotate(3deg); }
  }
  .scene-coldopen.active.calm .coldopen-ship {
    animation: shipGlide 6s ease-out forwards;
  }
  @keyframes shipGlide {
    from { transform: translateX(-50%) rotate(0deg); }
    to   { transform: translateX(20%)   rotate(0deg); }
  }

  .coldopen-bubble {
    position: absolute;
    background: rgba(231, 76, 60, 0.92);
    color: #fff;
    padding: 0.3rem 0.7rem;
    border-radius: 8px;
    font-size: 0.75rem;
    font-weight: 600;
    opacity: 0;
    animation: bubbleFlash 1.4s ease-out forwards;
  }
  @keyframes bubbleFlash {
    0%   { opacity: 0; transform: translateY(10px); }
    20%  { opacity: 1; transform: translateY(0); }
    80%  { opacity: 1; transform: translateY(0); }
    100% { opacity: 0; transform: translateY(-10px); }
  }
  .scene-coldopen.active .coldopen-bubble:nth-of-type(1) { animation-delay: 18s; bottom: 32%; left: 35%; }
  .scene-coldopen.active .coldopen-bubble:nth-of-type(2) { animation-delay: 19.5s; bottom: 36%; left: 55%; }
  .scene-coldopen.active .coldopen-bubble:nth-of-type(3) { animation-delay: 21s; bottom: 28%; left: 40%; }
  .scene-coldopen.active .coldopen-bubble:nth-of-type(4) { animation-delay: 22.5s; bottom: 38%; left: 50%; }
  .scene-coldopen.active.calm .coldopen-bubble { animation: none; opacity: 0; }

  .coldopen-compass {
    position: absolute;
    bottom: 28%; right: -20%;
    width: 90px; height: 90px;
    border-radius: 50%;
    background: radial-gradient(circle, #f4c869 0%, #d4a647 60%, #8a6a2a 100%);
    border: 3px solid #f4c869;
    display: flex; align-items: center; justify-content: center;
    font-size: 0.55rem; font-weight: 800; color: #1a2a4f;
    text-align: center;
    line-height: 1.1;
    box-shadow: 0 0 40px rgba(244, 200, 105, 0.6);
    opacity: 0;
    transition: right 2s ease, opacity 0.8s ease;
    animation: pulse 2.4s ease-out infinite;
  }
  .scene-coldopen.active .coldopen-compass {
    animation-delay: 24s;
    transition-delay: 24s;
    right: 38%;
    opacity: 1;
  }
  .scene-coldopen.active.calm .coldopen-compass {
    right: 46%;
    transition: right 2s ease;
  }

  .coldopen-final {
    position: absolute;
    inset: 0;
    display: flex; align-items: center; justify-content: center;
    flex-direction: column;
    opacity: 0;
    transition: opacity 1.5s ease;
    pointer-events: none;
  }
  .scene-coldopen.active.calm .coldopen-final { opacity: 1; }
  .coldopen-final-title {
    color: #1a2a4f;
    font-size: clamp(2rem, 4vw, 3.2rem);
    font-weight: 800;
    text-shadow: 0 4px 20px rgba(255,255,255,0.6);
  }
  .coldopen-final-sub {
    margin-top: 0.5rem;
    color: #1a2a4f;
    font-size: clamp(1rem, 1.5vw, 1.2rem);
    letter-spacing: 0.15em;
    text-transform: uppercase;
  }

  .coldopen-titlecard {
    position: absolute; inset: 0;
    background: #050a18;
    display: flex; align-items: center; justify-content: center;
    z-index: 50;
    transition: opacity 1s ease 4s;
  }
  .scene-coldopen.active .coldopen-titlecard { opacity: 0; pointer-events: none; }
  .coldopen-titlecard-text {
    color: var(--gold);
    font-size: clamp(1.5rem, 3.5vw, 2.6rem);
    font-weight: 800;
    letter-spacing: 0.05em;
    text-align: center;
    opacity: 0;
    transition: opacity 1s ease 0.6s, letter-spacing 1.4s ease 0.6s;
  }
  .scene-coldopen.active .coldopen-titlecard-text {
    opacity: 1;
    letter-spacing: 0.15em;
  }
""",
    },
    "pressures": {
        "html": """
        <div class="pressures-grid">

          <div class="pressure-tile">
            <div class="pressure-icon">$</div>
            <div class="pressure-title">P-card sprawl</div>
            <div class="pressure-body">Marketing bought a transcription tool last month. IT bought a Copilot license. Nobody is sure who approves what.</div>
            <div class="pressure-quote">"Who approved this?"</div>
          </div>

          <div class="pressure-tile">
            <div class="pressure-icon">B</div>
            <div class="pressure-title">The board wants accountability</div>
            <div class="pressure-body">Your directors started asking a question last quarter. Who is accountable for AI at this institution? And the CEO can't quite answer yet.</div>
            <div class="pressure-quote">"Who owns this?"</div>
          </div>

          <div class="pressure-tile">
            <div class="pressure-icon">!</div>
            <div class="pressure-title">Every vendor wants you to hire a CAIO</div>
            <div class="pressure-body">Each pitch implies you need a Chief AI Officer. None of them can tell you how to structure the committee that reviews their replacement.</div>
            <div class="pressure-quote">"Just hire a CAIO."</div>
          </div>

        </div>
""",
        "css": """
  .scene-pressures {
    display: flex; align-items: center; justify-content: center;
    padding: 4rem 6rem;
  }
  .pressures-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 2rem;
    max-width: 1100px;
    width: 100%;
  }
  .pressure-tile {
    background: rgba(20, 35, 71, 0.55);
    border: 1px solid rgba(212, 166, 71, 0.25);
    border-radius: 16px;
    padding: 2rem;
    opacity: 0;
    transform: translateY(30px);
    transition: opacity 0.8s ease, transform 0.8s ease;
  }
  .scene-pressures.active .pressure-tile { opacity: 1; transform: translateY(0); }
  .scene-pressures.active .pressure-tile:nth-child(1) { transition-delay: 0.4s; }
  .scene-pressures.active .pressure-tile:nth-child(2) { transition-delay: 1.4s; }
  .scene-pressures.active .pressure-tile:nth-child(3) { transition-delay: 2.4s; }
  .pressure-icon {
    width: 48px; height: 48px;
    background: linear-gradient(135deg, var(--gold-bright), var(--gold));
    border-radius: 12px;
    display: flex; align-items: center; justify-content: center;
    color: var(--navy-900);
    font-size: 1.3rem; font-weight: 800;
    margin-bottom: 1.25rem;
  }
  .pressure-title {
    font-size: 1.15rem;
    font-weight: 700;
    color: var(--text);
    margin-bottom: 0.75rem;
  }
  .pressure-body {
    font-size: 0.95rem;
    color: var(--text-dim);
    line-height: 1.55;
  }
  .pressure-quote {
    margin-top: 1rem;
    padding: 0.75rem 1rem;
    border-left: 3px solid var(--gold);
    color: var(--text);
    font-style: italic;
    font-size: 0.9rem;
  }
""",
    },
    "policy": {
        "html": """
        <div class="policy-stack">
          <div class="policy-page"><div class="policy-page-content"></div></div>
        </div>
        <div class="policy-callouts">
          <div class="policy-callout"><strong>Who</strong> enforces it?</div>
          <div class="policy-callout"><strong>What</strong> triggers committee review?</div>
          <div class="policy-callout"><strong>Who</strong> owns the incident-response call?</div>
        </div>
""",
        "css": """
  .scene-policy {
    display: flex; align-items: center; justify-content: center;
    padding: 4rem;
  }
  .policy-stack { position: relative; width: 320px; height: 420px; }
  .policy-page {
    position: absolute;
    width: 100%; height: 100%;
    background: #f5f0e6;
    border-radius: 4px;
    box-shadow: 0 20px 60px rgba(0,0,0,0.4);
    padding: 2rem 1.5rem;
    color: #1a2a4f;
    font-size: 0.7rem;
    line-height: 1.5;
    opacity: 1;
    transform: translateY(0) rotate(0);
    transition: opacity 1.5s ease 2s, transform 1.5s ease 2s;
  }
  .scene-policy.active .policy-page {
    opacity: 0.2;
    transform: translateY(60px) rotate(8deg) scale(0.9);
  }
  .policy-page::before {
    content: "AI POLICY TEMPLATE";
    display: block;
    font-weight: 800;
    font-size: 0.65rem;
    letter-spacing: 0.2em;
    margin-bottom: 1rem;
    color: #1a2a4f;
  }
  .policy-page-content {
    background-image: repeating-linear-gradient(
      0deg,
      rgba(26, 42, 79, 0.5) 0px,
      rgba(26, 42, 79, 0.5) 1px,
      transparent 1px,
      transparent 8px
    );
    height: 320px;
  }

  .policy-callouts {
    position: absolute;
    inset: 0;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    gap: 1rem;
    opacity: 0;
    transition: opacity 1s ease 3.5s;
    pointer-events: none;
  }
  .scene-policy.active .policy-callouts { opacity: 1; }
  .policy-callout {
    background: rgba(20, 35, 71, 0.85);
    border: 1px solid var(--gold);
    border-radius: 8px;
    padding: 0.65rem 1.2rem;
    color: var(--text);
    font-weight: 600;
    font-size: 0.95rem;
  }
  .policy-callout strong { color: var(--gold-bright); }
""",
    },
    "opmodel": {
        "html": """
        <div class="opmodel-grid">

          <div class="opmodel-card">
            <div class="opmodel-num">01</div>
            <div class="opmodel-title">Accountability Map</div>
            <div class="opmodel-body">Named-executive accountability for AI program oversight, policy, vendor selection, and incident response.</div>
          </div>

          <div class="opmodel-card">
            <div class="opmodel-num">02</div>
            <div class="opmodel-title">Green · Yellow · Red Lanes</div>
            <div class="opmodel-body">What any department can buy. What triggers a 5-day committee review. What requires CEO sign-off.</div>
          </div>

          <div class="opmodel-card">
            <div class="opmodel-num">03</div>
            <div class="opmodel-title">Centralized vs. Distributed</div>
            <div class="opmodel-body">Default for community banks: selection centralized, implementation distributed. New committee or existing one.</div>
          </div>

          <div class="opmodel-card">
            <div class="opmodel-num">04</div>
            <div class="opmodel-title">AI Support Model</div>
            <div class="opmodel-body">Where the support function lives. Who trains, who curates the approved tool list, who retires tools.</div>
          </div>

          <div class="opmodel-card">
            <div class="opmodel-num">05</div>
            <div class="opmodel-title">Decision Rights RACI</div>
            <div class="opmodel-body">Seven decision types — intake, renewal, exception, incident, retirement, training, board reporting.</div>
          </div>

          <div class="opmodel-card">
            <div class="opmodel-num">06</div>
            <div class="opmodel-title">Board Reporting</div>
            <div class="opmodel-body">Quarterly cadence and content. What constitutes a material AI incident requiring within-cycle escalation.</div>
          </div>

          <div class="opmodel-card">
            <div class="opmodel-num">07</div>
            <div class="opmodel-title">Talent Strategy</div>
            <div class="opmodel-body">Whether to hire a CAIO. Our default for $1–5B institutions: <strong>no.</strong> AI program manager instead.</div>
          </div>

          <div class="opmodel-card">
            <div class="opmodel-num">08</div>
            <div class="opmodel-title">Year-2 Review Triggers</div>
            <div class="opmodel-body">Regulatory shift, M&amp;A, repeated governance failures, scaling decisions on a pilot. Built in so it's not a shelf doc.</div>
          </div>

        </div>
""",
        "css": """
  .scene-opmodel {
    display: flex; align-items: center; justify-content: center;
    padding: 3rem 4rem;
  }
  .opmodel-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 1rem;
    max-width: 1200px;
    width: 100%;
  }
  .opmodel-card {
    background: rgba(20, 35, 71, 0.55);
    border: 1px solid rgba(212, 166, 71, 0.25);
    border-radius: 12px;
    padding: 1.25rem 1.1rem;
    opacity: 0;
    transform: rotateY(70deg);
    transform-origin: left center;
    transition: opacity 0.8s ease, transform 0.9s ease;
  }
  .scene-opmodel.active .opmodel-card { opacity: 1; transform: rotateY(0); }
  /* card timings — 8 cards over ~150 seconds, ~18s each */
  .scene-opmodel.active .opmodel-card:nth-child(1) { transition-delay: 2s; }
  .scene-opmodel.active .opmodel-card:nth-child(2) { transition-delay: 22s; }
  .scene-opmodel.active .opmodel-card:nth-child(3) { transition-delay: 40s; }
  .scene-opmodel.active .opmodel-card:nth-child(4) { transition-delay: 58s; }
  .scene-opmodel.active .opmodel-card:nth-child(5) { transition-delay: 76s; }
  .scene-opmodel.active .opmodel-card:nth-child(6) { transition-delay: 94s; }
  .scene-opmodel.active .opmodel-card:nth-child(7) { transition-delay: 112s; }
  .scene-opmodel.active .opmodel-card:nth-child(8) { transition-delay: 130s; }
  .opmodel-num {
    color: var(--gold);
    font-size: 0.65rem;
    letter-spacing: 0.25em;
    font-weight: 700;
    margin-bottom: 0.5rem;
  }
  .opmodel-title {
    font-size: 1rem;
    font-weight: 700;
    color: var(--text);
    margin-bottom: 0.6rem;
    line-height: 1.2;
  }
  .opmodel-body {
    font-size: 0.8rem;
    color: var(--text-dim);
    line-height: 1.5;
  }
""",
    },
    "twoweeks": {
        "html": """
        <div class="timeline">
          <div class="timeline-node">
            <div class="tnode-label">WEEK 0</div>
            <div class="tnode-title">Questionnaire &amp; kickoff</div>
            <div class="tnode-body">30-min questionnaire + 30-min scope call.</div>
          </div>
          <div class="timeline-arrow">→</div>
          <div class="timeline-node">
            <div class="tnode-label">WEEK 1</div>
            <div class="tnode-title">Discovery</div>
            <div class="tnode-body">CEO + stakeholder interviews. Anonymized peer scan.</div>
          </div>
          <div class="timeline-arrow">→</div>
          <div class="timeline-node">
            <div class="tnode-label">WEEK 2</div>
            <div class="tnode-title">Synthesis &amp; readout</div>
            <div class="tnode-body">Draft → Day 9 readout → Day 10 revisions.</div>
          </div>
        </div>

        <div class="deliverables-row">
          <div class="deliverable">
            <div class="deliverable-icon"></div>
            <div class="deliverable-title">Operating Model</div>
            <div class="deliverable-meta">~12 pages, board-adoptable</div>
          </div>
          <div class="deliverable">
            <div class="deliverable-icon"></div>
            <div class="deliverable-title">CEO Briefing Deck</div>
            <div class="deliverable-meta">~15 slides, editable .pptx</div>
          </div>
          <div class="deliverable">
            <div class="deliverable-icon"></div>
            <div class="deliverable-title">Board Memo</div>
            <div class="deliverable-meta">1 page, board-ratifiable</div>
          </div>
        </div>
""",
        "css": """
  .scene-twoweeks {
    display: flex; flex-direction: column;
    align-items: center; justify-content: center;
    padding: 3rem 4rem;
    gap: 3rem;
  }
  .timeline {
    display: flex;
    align-items: center;
    gap: 1rem;
    width: 100%;
    max-width: 900px;
  }
  .timeline-node {
    flex: 1;
    text-align: center;
    padding: 1.25rem 0.75rem;
    background: rgba(20, 35, 71, 0.55);
    border: 1px solid rgba(212, 166, 71, 0.25);
    border-radius: 12px;
    opacity: 0;
    transform: translateY(20px);
    transition: opacity 0.8s ease, transform 0.8s ease;
  }
  .scene-twoweeks.active .timeline-node { opacity: 1; transform: translateY(0); }
  .scene-twoweeks.active .timeline-node:nth-child(1) { transition-delay: 1s; }
  .scene-twoweeks.active .timeline-node:nth-child(3) { transition-delay: 14s; }
  .scene-twoweeks.active .timeline-node:nth-child(5) { transition-delay: 38s; }
  .timeline-arrow {
    color: var(--gold);
    font-size: 1.6rem;
    font-weight: 700;
    opacity: 0;
    transition: opacity 0.6s ease;
  }
  .scene-twoweeks.active .timeline-arrow { opacity: 1; }
  .scene-twoweeks.active .timeline-arrow:nth-child(2) { transition-delay: 6s; }
  .scene-twoweeks.active .timeline-arrow:nth-child(4) { transition-delay: 26s; }
  .tnode-label {
    color: var(--gold);
    font-size: 0.65rem;
    letter-spacing: 0.25em;
    font-weight: 700;
    margin-bottom: 0.4rem;
  }
  .tnode-title { font-size: 0.95rem; font-weight: 700; }
  .tnode-body { font-size: 0.8rem; color: var(--text-dim); margin-top: 0.4rem; line-height: 1.5; }

  .deliverables-row {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 1.5rem;
    width: 100%;
    max-width: 900px;
  }
  .deliverable {
    background: rgba(20, 35, 71, 0.55);
    border: 1px solid rgba(212, 166, 71, 0.4);
    border-radius: 12px;
    padding: 1.5rem;
    text-align: center;
    opacity: 0;
    transform: scale(0.85);
    transition: opacity 0.8s ease, transform 0.8s ease;
  }
  .scene-twoweeks.active .deliverable { opacity: 1; transform: scale(1); }
  .scene-twoweeks.active .deliverable:nth-child(1) { transition-delay: 60s; }
  .scene-twoweeks.active .deliverable:nth-child(2) { transition-delay: 70s; }
  .scene-twoweeks.active .deliverable:nth-child(3) { transition-delay: 80s; }
  .deliverable-icon {
    width: 64px; height: 80px;
    margin: 0 auto 1rem;
    background: linear-gradient(180deg, #f5f0e6, #e0d4b8);
    border-radius: 4px;
    position: relative;
  }
  .deliverable-icon::after {
    content: "";
    position: absolute;
    top: 8px; left: 50%;
    transform: translateX(-50%);
    width: 70%; height: 60%;
    background-image: repeating-linear-gradient(
      0deg, #1a2a4f 0, #1a2a4f 1px, transparent 1px, transparent 6px);
  }
  .deliverable-title { font-size: 0.95rem; font-weight: 700; }
  .deliverable-meta { font-size: 0.75rem; color: var(--text-dim); margin-top: 0.3rem; }
""",
    },
    "whofor": {
        "html": """
        <div class="whofor-cols">

          <div class="whofor-col yes">
            <div class="whofor-header">THIS IS FOR YOU IF</div>
            <ul class="whofor-list">
              <li>You run a community or regional bank between $200M and $5B.</li>
              <li>You want this decided in weeks, not quarters.</li>
              <li>You have no functioning AI committee — or one that has stalled.</li>
              <li>Your board is starting to ask the accountability question.</li>
            </ul>
          </div>

          <div class="whofor-col no">
            <div class="whofor-header">THIS IS NOT FOR YOU IF</div>
            <ul class="whofor-list">
              <li>You already have a CAIO and a chartered AI committee. That's a Sprint conversation.</li>
              <li>You want a vendor shortlist or a use-case workshop. Also a Sprint.</li>
              <li>You want a policy template off a shelf. We don't sell those.</li>
            </ul>
          </div>

        </div>
""",
        "css": """
  .scene-whofor {
    display: flex; align-items: center; justify-content: center;
    padding: 4rem;
  }
  .whofor-cols {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 2rem;
    max-width: 1100px;
    width: 100%;
  }
  .whofor-col {
    background: rgba(20, 35, 71, 0.55);
    border-radius: 16px;
    padding: 2rem;
    opacity: 0;
    transform: translateX(-30px);
    transition: opacity 0.8s ease, transform 0.8s ease;
  }
  .whofor-col.no { transform: translateX(30px); }
  .scene-whofor.active .whofor-col { opacity: 1; transform: translateX(0); }
  .scene-whofor.active .whofor-col.yes { transition-delay: 1s; border: 1px solid #4ade80; }
  .scene-whofor.active .whofor-col.no  { transition-delay: 3s; border: 1px solid #e74c3c; }
  .whofor-header {
    font-size: 0.7rem;
    letter-spacing: 0.3em;
    font-weight: 800;
    margin-bottom: 1.25rem;
  }
  .whofor-col.yes .whofor-header { color: #4ade80; }
  .whofor-col.no  .whofor-header { color: #e74c3c; }
  .whofor-list { list-style: none; padding: 0; }
  .whofor-list li {
    padding: 0.65rem 0;
    border-bottom: 1px solid rgba(255,255,255,0.06);
    color: var(--text);
    font-size: 0.95rem;
    line-height: 1.5;
  }
  .whofor-list li:last-child { border-bottom: none; }
""",
    },
    "close": {
        "html": """
        <div class="close-compass">THE<br>COMPASS</div>
        <div class="close-headline">The Compass</div>
        <div class="close-meta">$35,000 · 2 weeks · 3 artifacts</div>
        <a class="close-cta" href="https://example.com">Book a 1-hour Signal call</a>
        <div class="close-url">example.com/signal</div>
        <div class="close-final-line">Set your course.</div>
""",
        "css": """
  .scene-close {
    display: flex; flex-direction: column;
    align-items: center; justify-content: center;
    padding: 4rem;
    text-align: center;
    background: radial-gradient(ellipse at center, #142347 0%, #050a18 70%);
  }
  .close-compass {
    width: 140px; height: 140px;
    border-radius: 50%;
    background: radial-gradient(circle, #f4c869 0%, #d4a647 60%, #8a6a2a 100%);
    border: 4px solid #f4c869;
    box-shadow: 0 0 80px rgba(244, 200, 105, 0.5);
    margin-bottom: 2rem;
    animation: pulse 3s ease-out infinite;
    display: flex; align-items: center; justify-content: center;
    color: #1a2a4f; font-weight: 800; font-size: 0.7rem;
    letter-spacing: 0.2em;
    line-height: 1.2;
    opacity: 0;
    transition: opacity 1s ease 1s;
  }
  .scene-close.active .close-compass { opacity: 1; }
  .close-headline {
    font-size: clamp(2rem, 4vw, 3rem);
    font-weight: 800;
    color: var(--text);
    margin-bottom: 0.5rem;
    opacity: 0;
    transition: opacity 0.8s ease 2s;
  }
  .scene-close.active .close-headline { opacity: 1; }
  .close-meta {
    color: var(--gold);
    font-size: 1.1rem;
    letter-spacing: 0.15em;
    font-weight: 700;
    margin-bottom: 2rem;
    opacity: 0;
    transition: opacity 0.8s ease 3s;
  }
  .scene-close.active .close-meta { opacity: 1; }
  .close-cta {
    display: inline-block;
    padding: 1rem 2.5rem;
    border-radius: 999px;
    background: linear-gradient(135deg, var(--gold-bright), var(--gold));
    color: var(--navy-900);
    font-size: 1.1rem;
    font-weight: 800;
    letter-spacing: 0.05em;
    text-decoration: none;
    box-shadow: 0 20px 50px rgba(212, 166, 71, 0.4);
    opacity: 0;
    transform: translateY(20px);
    transition: opacity 0.8s ease 4s, transform 0.8s ease 4s;
  }
  .scene-close.active .close-cta { opacity: 1; transform: translateY(0); }
  .close-url {
    margin-top: 1rem;
    color: var(--text-dim);
    font-size: 0.85rem;
    letter-spacing: 0.1em;
    opacity: 0;
    transition: opacity 0.8s ease 4.5s;
  }
  .scene-close.active .close-url { opacity: 1; }
  .close-final-line {
    margin-top: 3rem;
    font-size: 1.4rem;
    font-style: italic;
    color: var(--gold-bright);
    opacity: 0;
    transition: opacity 1.2s ease 45s;
  }
  .scene-close.active .close-final-line { opacity: 1; }
""",
    },
}

CHAPTERS = [
    {"number": 0, "title": "Cold Open", "icon": "0", "segments": [
        {"id": "c0_00_cold_open", "scene": "coldopen",
         "narration": (
             "Every community bank CEO right now is at the helm in a storm. "
             "You are navigating the same rapidly evolving AI landscape as every other organization — "
             "working to understand what is delivering value, where uncertainty remains, "
             "and the tradeoffs required to move forward. "
             "The shifting winds have names: Gemini, Grok, ChatGPT, Copilot, Claude. "
             "And then there are countless applications with AI embedded inside them — "
             "systems already moving through your organization, often beyond your visibility or control. "
             "Below deck, the crew is shouting: budgets are tightening, a new tool appears every week, "
             "the board is asking who is accountable, and no one in the room has a clear answer. "
             "What the CEO needs is not another tool. "
             "It is not another policy template pulled from a research firm. "
             "What the CEO needs is a compass: a clear way to decide, govern, and invest with confidence. "
             "That is what the Compass provides. "
             "Built for your institution in two weeks, "
             "the Compass gives leaders the direction they need "
             "to navigate AI risk, align accountability, and chart a course forward."
         ),
         "timedClasses": [{"at": 30, "addClass": "calm"}]},
    ]},
    {"number": 1, "title": "The Storm Is Real", "icon": "1", "segments": [
        {"id": "c1_01_storm_real", "scene": "pressures",
         "narration": (
             "The storm is here, and every organization is already navigating through it. "
             "How successfully you make it through depends on how you steer. "
             "Last quarter, your marketing team bought an AI transcription tool on a P-card. "
             "Your IT department bought a Microsoft Copilot license. "
             "Your CRO asked whether Risk should have reviewed either of them — "
             "and three weeks later, that question is still open. "
             "This is the shadow IT sprawl that examiners flag. "
             "In the boardroom, your directors started asking a question last quarter "
             "that they did not ask the year before: "
             "Who is accountable for AI at this institution? "
             "And when you look around the room, the answer is not obvious. "
             "The CCO thinks Risk owns it. The CIO thinks the AI committee owns it — "
             "except there is not one yet. "
             "And the CEO has been quietly trying to figure out whether to chair it personally "
             "or appoint someone else. "
             "Meanwhile, every vendor walks in claiming their tool is compliant. "
             "They will tell you exactly how their AI works. "
             "They will not tell you where it fails, where it should not be used, "
             "what happens when it is applied outside its intended boundaries, "
             "or how to control it once it is running. "
             "Does everyone in your institution even define AI the same way? "
             "That is the storm. It is here. "
             "And it is going to keep getting louder until someone in your institution picks up a compass."
         )},
    ]},
    {"number": 2, "title": "Why Policy Isn't Enough", "icon": "2", "segments": [
        {"id": "c2_01_policy_trap", "scene": "policy",
         "narration": (
             "The first instinct is to put an AI policy in place. "
             "To move faster, that effort is often accelerated by purchasing a template from a research firm, "
             "downloading one from an industry association, or commissioning one from outside counsel. "
             "And policy is necessary. We are not telling you to skip it. "
             "But a policy is not enough. "
             "A policy tells you what the rules are. "
             "It does not tell you who enforces them. "
             "It does not tell you what triggers a committee review, or what requires CEO sign-off, "
             "or who owns the incident-response call at three in the morning "
             "when a customer-facing chatbot goes off-script. "
             "That is what an operating model does. "
             "An operating model answers who decides what — for AI, in your bank, at the scale you actually operate. "
             "Without that operating model, even the strongest policy becomes static guidance "
             "in a dynamic environment. "
             "That is what the Compass delivers."
         )},
    ]},
    {"number": 3, "title": "What an Operating Model Is", "icon": "3", "segments": [
        {"id": "c3_01_what_op_model", "scene": "opmodel",
         "narration": (
             "An AI operating model establishes decision rights, escalation paths, "
             "accountability, and response protocols. "
             "It turns governance from a document on the shelf into a system that functions under pressure. "
             "The Compass delivers eight core components, each one built for your institution. "
             "First: the Accountability Map. "
             "Named-executive accountability for AI program oversight, policy adherence, "
             "vendor selection, and incident response. "
             "We distinguish accountability from involvement. Involvement is everywhere. "
             "Accountability sits in one chair. "
             "Second: the Green, Yellow, and Red investment lanes. "
             "What any department can buy without committee review. "
             "What triggers a five-business-day committee review. "
             "What requires CEO sign-off. With dollar thresholds and data-sensitivity triggers "
             "that fit your bank. "
             "Third: the centralized-versus-distributed posture. "
             "Our standard approach for community banks is selection centralized, "
             "implementation distributed. "
             "We will tell you whether AI lives inside your existing Risk committee, "
             "your Tech committee, or if an independent structure is needed. "
             "Fourth: the AI support model. Where the support function lives in your org. "
             "Who trains new hires. Who curates the approved tool list. "
             "Who answers prompting questions from a loan officer at four o'clock on a Friday. "
             "Fifth: the Decision Rights Matrix. "
             "A RACI across seven decision types — new tool intake, vendor renewal, policy exception, "
             "incident response, model retirement, training program design, and board reporting. "
             "This is what makes the operating model executable, not aspirational. "
             "Sixth: board reporting. Quarterly cadence and content. "
             "A template for what goes to the Risk committee versus the Tech committee. "
             "And what constitutes a material AI incident requiring within-cycle escalation. "
             "Seventh: talent strategy. "
             "Including an explicit position on whether to hire a Chief AI Officer. "
             "For institutions between one and five billion in assets, "
             "our standard recommendation is no. An AI program manager is enough. "
             "This closes out the vendor pitches that assume you need a CAIO. "
             "Eighth: Year Two review triggers. "
             "Pre-committed criteria for re-opening the operating model — a regulatory shift, an M&A event, "
             "repeated governance failures, or a scaling decision on a pilot. "
             "This is not a shelf document. It establishes the foundation for today "
             "while creating a living operating model your bank can continuously evolve "
             "to keep pace with changing conditions, emerging risks, and new opportunities. "
             "Eight pieces. One operating model. Built for your institution."
         )},
    ]},
    {"number": 4, "title": "Two Weeks, Three Artifacts", "icon": "4", "segments": [
        {"id": "c4_01_two_weeks", "scene": "twoweeks",
         "narration": (
             "How does it run? Two weeks. Three artifacts. "
             "Week One begins with a brief thirty-minute pre-engagement questionnaire. "
             "We review your existing committee charters, your organizational chart, "
             "your technology stack and the list of AI-touching vendors already in place, "
             "and any current or prior AI policy drafts. "
             "We then schedule a thirty-minute kickoff call to align on scope "
             "and the interview roster, "
             "and to flag any sensitivities before discovery begins. "
             "In Week Two, we do discovery. "
             "A ninety-minute interview with the CEO, focused on authority and what you will not delegate. "
             "Sixty-minute interviews with the identified roster participants. "
             "A walkthrough of your committee landscape, "
             "and an anonymized scan of how three peer institutions have structured their AI governance. "
             "In Week Three, we translate discovery into the Compass: "
             "the board-ready operating model your institution will use to navigate AI. "
             "We draft the three integrated artifacts that comprise the Compass. "
             "On Day Nine, we present the readout and walk your leadership team through our recommendations. "
             "On Day Ten, we incorporate your revisions and finalize the deliverables. "
             "You leave with three artifacts. "
             "First, the Operating Model document — a board-adoptable framework "
             "covering all eight core sections. "
             "Second, the CEO Briefing Deck — a presentation designed for your board meeting, "
             "the deck you walk into that meeting with as your recommendation, not ours. "
             "Third, the Board Memo — designed to accelerate board ratification, "
             "ready to circulate five business days before adoption. "
             "Two weeks. Three artifacts. One Compass: "
             "the operating model that fits your institution."
         )},
    ]},
    {"number": 5, "title": "Who This Is For", "icon": "5", "segments": [
        {"id": "c5_01_who_for", "scene": "whofor",
         "narration": (
             "The Compass is built for a specific kind of institution. "
             "Let me tell you how to know if it is the right fit. "
             "It is designed for institutions at a critical AI decision point. "
             "Community or regional banks and credit unions "
             "between two hundred million and five billion dollars in assets. "
             "Leaders who want this decided in weeks, not quarters. "
             "If you do not yet have a functioning AI committee — "
             "or if the one you established has stalled — "
             "and if your board has started asking the accountability question, "
             "this gives you a clear answer before they have to ask twice. "
             "The Compass may not be the right fit for every institution. "
             "If you already have a Chief AI Officer and a chartered AI committee that meets monthly, "
             "you may already have the governance foundation Compass is designed to establish. "
             "In that case, the next step is likely selecting and launching pilots. "
             "That is a Sprint conversation and workshop rather than a Compass engagement. "
             "If you are looking for a vendor shortlist, a use-case workshop, "
             "or a productivity-tool rollout — those are valuable initiatives, "
             "but they are execution-focused sprints rather than governance and decision-rights work. "
             "And if you want a policy template you can buy off a shelf, "
             "we do not sell those. You can find one elsewhere — "
             "but it will not tell you who decides what."
         )},
    ]},
    {"number": 6, "title": "Set Your Course", "icon": "6", "segments": [
        {"id": "c6_01_close", "scene": "close",
         "narration": (
             "That is the Compass. "
             "The Compass is a fixed investment of thirty-five thousand dollars. "
             "Delivered in two weeks. Three tangible artifacts. "
             "One operating model tailored specifically to your institution — "
             "by senior advisors who have spent careers in regulated financial institutions, "
             "not by generalist consultants or templates sold by research firms. "
             "If that sounds like the right next step, "
             "schedule a complimentary Compass Navigation Call. "
             "The purpose is simple: to understand your current situation "
             "and determine whether Compass is the right fit before any engagement is proposed. "
             "If it is not the right fit, we will tell you candidly "
             "and point you toward the path that is. "
             "Use the link below to book the call. "
             "The storm is not going away. "
             "Set your course."
         )},
    ]},
]
