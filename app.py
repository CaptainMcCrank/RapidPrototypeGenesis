"""
Rapid Prototype Genesis - Complete Flask PWA
Ready-to-run Flask application with all required files
"""

from flask import Flask, render_template, request, jsonify, make_response
from flask_cors import CORS
from datetime import datetime
import json
import os
from pathlib import Path

app = Flask(__name__)
CORS(app)

# Create storage directory for PRDs
PRD_DIR = Path("generated_prds")
PRD_DIR.mkdir(exist_ok=True)

# HTML Template (embedded for single-file deployment)
HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>Rapid Prototype Genesis</title>
    
    <!-- PWA Meta Tags -->
    <meta name="theme-color" content="#000000">
    <meta name="apple-mobile-web-app-capable" content="yes">
    <meta name="apple-mobile-web-app-status-bar-style" content="black">
    <link rel="manifest" href="/manifest.json">
    
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        :root {
            --primary: #000;
            --accent: #00ff41;
            --danger: #ff3b30;
            --bg: #ffffff;
            --text: #1d1d1f;
            --gray: #86868b;
            --light-gray: #f2f2f7;
            --shadow: 0 4px 24px rgba(0,0,0,0.08);
        }
        
        @media (prefers-color-scheme: dark) {
            :root {
                --bg: #000000;
                --text: #f5f5f7;
                --light-gray: #1c1c1e;
                --gray: #8e8e93;
            }
        }
        
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'SF Pro Text', 'Segoe UI', sans-serif;
            background: var(--bg);
            color: var(--text);
            line-height: 1.5;
            overflow-x: hidden;
            min-height: 100vh;
        }
        
        .container {
            max-width: 680px;
            margin: 0 auto;
            padding: 20px;
            min-height: 100vh;
            display: flex;
            flex-direction: column;
        }
        
        .header {
            padding: 40px 0 20px;
            border-bottom: 1px solid var(--light-gray);
            margin-bottom: 40px;
            animation: slideDown 0.6s cubic-bezier(0.34, 1.56, 0.64, 1);
        }
        
        h1 {
            font-size: 32px;
            font-weight: 700;
            letter-spacing: -0.02em;
            margin-bottom: 8px;
        }
        
        .subtitle {
            color: var(--gray);
            font-size: 16px;
            font-weight: 400;
        }
        
        .progress-bar {
            height: 4px;
            background: var(--light-gray);
            border-radius: 2px;
            margin: 30px 0;
            overflow: hidden;
            position: relative;
        }
        
        .progress-fill {
            height: 100%;
            background: linear-gradient(90deg, var(--accent) 0%, #00ff88 100%);
            border-radius: 2px;
            transition: width 0.4s cubic-bezier(0.34, 1.56, 0.64, 1);
            box-shadow: 0 0 20px rgba(0, 255, 65, 0.5);
        }
        
        .question-card {
            background: var(--bg);
            border: 1px solid var(--light-gray);
            border-radius: 16px;
            padding: 30px;
            margin-bottom: 20px;
            box-shadow: var(--shadow);
            animation: slideUp 0.5s cubic-bezier(0.34, 1.56, 0.64, 1);
            flex: 1;
            display: flex;
            flex-direction: column;
        }
        
        .section-label {
            color: var(--accent);
            font-size: 12px;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.1em;
            margin-bottom: 12px;
        }
        
        .question-number {
            color: var(--gray);
            font-size: 14px;
            margin-bottom: 8px;
        }
        
        .question-text {
            font-size: 20px;
            font-weight: 600;
            margin-bottom: 8px;
            line-height: 1.3;
        }
        
        .question-hint {
            color: var(--gray);
            font-size: 14px;
            margin-bottom: 24px;
            font-style: italic;
        }
        
        .answer-input {
            width: 100%;
            padding: 16px;
            font-size: 16px;
            border: 2px solid var(--light-gray);
            border-radius: 12px;
            background: var(--bg);
            color: var(--text);
            resize: vertical;
            min-height: 120px;
            font-family: inherit;
            transition: all 0.2s;
            margin-bottom: 20px;
        }
        
        .answer-input:focus {
            outline: none;
            border-color: var(--accent);
            box-shadow: 0 0 0 4px rgba(0, 255, 65, 0.1);
        }
        
        .controls {
            display: flex;
            gap: 12px;
            margin-top: auto;
        }
        
        .btn {
            flex: 1;
            padding: 16px 24px;
            font-size: 16px;
            font-weight: 600;
            border: none;
            border-radius: 12px;
            cursor: pointer;
            transition: all 0.2s;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 8px;
            text-transform: none;
            letter-spacing: -0.01em;
        }
        
        .btn-primary {
            background: var(--primary);
            color: white;
        }
        
        .btn-primary:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 24px rgba(0,0,0,0.2);
        }
        
        .btn-secondary {
            background: var(--light-gray);
            color: var(--text);
        }
        
        .btn-voice {
            background: var(--danger);
            color: white;
        }
        
        .btn-voice.recording {
            background: var(--accent);
            animation: pulse 1.5s infinite;
        }
        
        .btn:disabled {
            opacity: 0.5;
            cursor: not-allowed;
        }
        
        .final-screen {
            text-align: center;
            padding: 60px 20px;
            animation: fadeIn 0.8s;
        }
        
        .success-icon {
            width: 80px;
            height: 80px;
            margin: 0 auto 30px;
            background: var(--accent);
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 40px;
            animation: scaleIn 0.6s cubic-bezier(0.34, 1.56, 0.64, 1);
        }
        
        .toast {
            position: fixed;
            bottom: 30px;
            left: 50%;
            transform: translateX(-50%);
            background: var(--primary);
            color: white;
            padding: 12px 24px;
            border-radius: 24px;
            font-size: 14px;
            font-weight: 600;
            opacity: 0;
            pointer-events: none;
            transition: opacity 0.3s;
            z-index: 1000;
        }
        
        .toast.show {
            opacity: 1;
        }
        
        @keyframes slideDown {
            from { transform: translateY(-20px); opacity: 0; }
            to { transform: translateY(0); opacity: 1; }
        }
        
        @keyframes slideUp {
            from { transform: translateY(20px); opacity: 0; }
            to { transform: translateY(0); opacity: 1; }
        }
        
        @keyframes fadeIn {
            from { opacity: 0; }
            to { opacity: 1; }
        }
        
        @keyframes scaleIn {
            from { transform: scale(0); }
            to { transform: scale(1); }
        }
        
        @keyframes pulse {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.7; }
        }
        
        @media (max-width: 640px) {
            h1 { font-size: 28px; }
            .question-text { font-size: 18px; }
            .controls { flex-direction: column; }
            .btn { width: 100%; }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>Rapid Prototype Genesis™</h1>
            <p class="subtitle">From Vision to Lovable Prototype in One Day</p>
        </div>
        
        <div class="progress-bar">
            <div class="progress-fill" id="progress"></div>
        </div>
        
        <div id="questionContainer"></div>
    </div>
    
    <div class="toast" id="toast"></div>
    
    <script>
        const questions = [
            // Part 1: The Soul of the Product
            {
                section: "The Soul of the Product",
                number: 1,
                text: "The One-Liner",
                hint: "In 10 words or less, what does this thing DO?",
                timer: "30 seconds - no overthinking"
            },
            {
                section: "The Soul of the Product",
                number: 2,
                text: "The Emotional Hook",
                hint: "What feeling should users have in the first 10 seconds of interaction?"
            },
            {
                section: "The Soul of the Product",
                number: 3,
                text: "The 'Holy Shit' Moment",
                hint: "What's the ONE feature that makes someone text their friend about this?"
            },
            {
                section: "The Soul of the Product",
                number: 4,
                text: "The Non-Negotiable",
                hint: "What's the single quality that, if compromised, kills the entire product?"
            },
            {
                section: "The Beautiful Constraint",
                number: 5,
                text: "Primary Interface",
                hint: "What's the MAIN way users interact? (touch/voice/gesture/CLI/web/physical)"
            },
            {
                section: "The Beautiful Constraint",
                number: 6,
                text: "The 80% Use Case",
                hint: "What will 80% of users do 80% of the time?"
            },
            {
                section: "The Beautiful Constraint",
                number: 7,
                text: "The Deletion Test",
                hint: "If you could only ship THREE features, which three?"
            },
            {
                section: "The Beautiful Constraint",
                number: 8,
                text: "The Grandma Test",
                hint: "Can you explain this to a grandma in one sentence? (If no, simplify)"
            },
            // Part 2: The Experience Architecture
            {
                section: "User Journey Crystallization",
                number: 9,
                text: "First Touch",
                hint: "Describe the EXACT first 60 seconds of user experience (every tap, every screen)"
            },
            {
                section: "User Journey Crystallization",
                number: 10,
                text: "The Learning Cliff",
                hint: "What does the user need to know BEFORE they start? (aim for: nothing)"
            },
            {
                section: "User Journey Crystallization",
                number: 11,
                text: "The Payoff Timeline",
                hint: "How long until they get value? (Target: <2 minutes)"
            },
            {
                section: "User Journey Crystallization",
                number: 12,
                text: "The Daily Ritual",
                hint: "Why would someone use this tomorrow? And next week?"
            },
            {
                section: "Technical Beauty Standards",
                number: 13,
                text: "Response Religion",
                hint: "Maximum acceptable latency for primary action? (OP-1: instant, Tesla: <100ms)"
            },
            {
                section: "Technical Beauty Standards",
                number: 14,
                text: "Failure Grace",
                hint: "When things break, what's the user experience? (Don't say 'it won't break')"
            },
            {
                section: "Technical Beauty Standards",
                number: 15,
                text: "The Ambient State",
                hint: "What does it look/do when nobody's using it?"
            },
            {
                section: "Technical Beauty Standards",
                number: 16,
                text: "Physical Presence",
                hint: "Any physical indicators/feedback? (LEDs, sounds, haptics, display)"
            },
            // Part 3: The Build Specification
            {
                section: "System Architecture Lightning Round",
                number: 17,
                text: "Hardware Stack",
                hint: "List every physical component needed (be exhaustive)"
            },
            {
                section: "System Architecture Lightning Round",
                number: 18,
                text: "Software Services",
                hint: "List every daemon/service/process that must run"
            },
            {
                section: "System Architecture Lightning Round",
                number: 19,
                text: "Network Topology",
                hint: "Draw the network in words (who talks to what, how)"
            },
            {
                section: "System Architecture Lightning Round",
                number: 20,
                text: "Data Flows",
                hint: "What information moves where? (user input → processing → output)"
            },
            {
                section: "State & Persistence",
                number: 21,
                text: "State Management",
                hint: "What needs to be remembered between sessions?"
            },
            {
                section: "State & Persistence",
                number: 22,
                text: "Reset Behavior",
                hint: "What happens after power cycle?"
            },
            {
                section: "State & Persistence",
                number: 23,
                text: "Multi-User Reality",
                hint: "Can multiple people use simultaneously? How?"
            },
            {
                section: "State & Persistence",
                number: 24,
                text: "Progress Indicators",
                hint: "How does the system show what's happening? (visual/audio/network)"
            },
            // Part 4: The Implementation Accelerators
            {
                section: "Concrete Deliverables",
                number: 25,
                text: "File System Layout",
                hint: "Where does everything live? (/etc/, /var/, /opt/, etc.)"
            },
            {
                section: "Concrete Deliverables",
                number: 26,
                text: "Configuration Baseline",
                hint: "List every config file and its primary purpose"
            },
            {
                section: "Concrete Deliverables",
                number: 27,
                text: "Security Posture",
                hint: "Default passwords? Open ports? Intentional vulnerabilities?"
            },
            {
                section: "Concrete Deliverables",
                number: 28,
                text: "Testing Victory",
                hint: "How do you know it works? (specific, measurable outcomes)"
            },
            {
                section: "Automation Prerequisites",
                number: 29,
                text: "Environment Variables",
                hint: "What must be configurable?"
            },
            {
                section: "Automation Prerequisites",
                number: 30,
                text: "Bootstrap Sequence",
                hint: "Order of operations from blank Pi to working product?"
            },
            {
                section: "Automation Prerequisites",
                number: 31,
                text: "Dependency Chain",
                hint: "What must exist before what? (network before services, etc.)"
            },
            {
                section: "Automation Prerequisites",
                number: 32,
                text: "Health Checks",
                hint: "How does the system verify it's working correctly?"
            },
            // Part 5: The Lovability Layer
            {
                section: "The Polish That Matters",
                number: 33,
                text: "The Delight Detail",
                hint: "One small thing that's unnecessarily perfect (OP-1's knobs, iPhone's rubber-band scroll)"
            },
            {
                section: "The Polish That Matters",
                number: 34,
                text: "The Power User Secret",
                hint: "One hidden feature for advanced users to discover"
            },
            {
                section: "The Polish That Matters",
                number: 35,
                text: "The Personality Tell",
                hint: "How does this product's personality show? (error messages, waiting states, success celebrations)"
            },
            {
                section: "The Polish That Matters",
                number: 36,
                text: "The Unboxing",
                hint: "First boot experience - what happens when it powers on fresh?"
            },
            {
                section: "The Reality Check",
                number: 37,
                text: "The Minimum Lovable",
                hint: "Below what threshold does this become unusable/unlovable?"
            },
            {
                section: "The Reality Check",
                number: 38,
                text: "The Expansion Hook",
                hint: "What's the OBVIOUS next feature you're intentionally NOT building now?"
            },
            {
                section: "The Reality Check",
                number: 39,
                text: "The Success Metric",
                hint: "ONE number that tells you if this worked"
            },
            {
                section: "The Reality Check",
                number: 40,
                text: "The Kill Switch",
                hint: "How does someone gracefully stop/reset everything?"
            }
        ];
        
        let currentQuestion = 0;
        let answers = {};
        let recognition = null;
        let isRecording = false;
        
        // Initialize speech recognition
        if ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window) {
            const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
            recognition = new SpeechRecognition();
            recognition.continuous = true;
            recognition.interimResults = true;
            recognition.lang = 'en-US';
            
            recognition.onresult = (event) => {
                let finalTranscript = '';
                let interimTranscript = '';
                
                for (let i = event.resultIndex; i < event.results.length; i++) {
                    const transcript = event.results[i][0].transcript;
                    if (event.results[i].isFinal) {
                        finalTranscript += transcript + ' ';
                    } else {
                        interimTranscript += transcript;
                    }
                }
                
                const input = document.getElementById('answerInput');
                if (finalTranscript) {
                    input.value += finalTranscript;
                    answers[currentQuestion] = input.value;
                }
            };
            
            recognition.onerror = (event) => {
                console.error('Speech recognition error', event.error);
                stopRecording();
                showToast('Voice recognition error. Please try again.');
            };
        }
        
        function renderQuestion() {
            const container = document.getElementById('questionContainer');
            const q = questions[currentQuestion];
            const progress = ((currentQuestion + 1) / questions.length) * 100;
            
            document.getElementById('progress').style.width = progress + '%';
            
            container.innerHTML = `
                <div class="question-card">
                    <div class="section-label">${q.section}</div>
                    <div class="question-number">Question ${q.number} of ${questions.length}</div>
                    <h2 class="question-text">${q.text}</h2>
                    <p class="question-hint">${q.hint}</p>
                    ${q.timer ? `<p class="question-hint" style="color: var(--danger);">⏱ ${q.timer}</p>` : ''}
                    
                    <textarea 
                        id="answerInput" 
                        class="answer-input" 
                        placeholder="Type your answer or use voice input..."
                        onchange="saveAnswer()"
                        onkeyup="saveAnswer()"
                    >${answers[currentQuestion] || ''}</textarea>
                    
                    <div class="controls">
                        ${currentQuestion > 0 ? 
                            `<button class="btn btn-secondary" onclick="previousQuestion()">
                                ← Previous
                            </button>` : ''}
                        
                        ${recognition ? 
                            `<button id="voiceBtn" class="btn btn-voice" onclick="toggleRecording()">
                                🎤 ${isRecording ? 'Stop' : 'Voice'}
                            </button>` : ''}
                        
                        <button class="btn btn-primary" onclick="nextQuestion()">
                            ${currentQuestion < questions.length - 1 ? 'Next →' : 'Generate PRD'}
                        </button>
                    </div>
                </div>
            `;
            
            // Focus on textarea
            setTimeout(() => {
                document.getElementById('answerInput').focus();
            }, 100);
        }
        
        function saveAnswer() {
            const input = document.getElementById('answerInput');
            answers[currentQuestion] = input.value;
            localStorage.setItem('rpg_answers', JSON.stringify(answers));
        }
        
        function nextQuestion() {
            saveAnswer();
            
            if (currentQuestion < questions.length - 1) {
                currentQuestion++;
                renderQuestion();
            } else {
                generatePRD();
            }
        }
        
        function previousQuestion() {
            saveAnswer();
            if (currentQuestion > 0) {
                currentQuestion--;
                renderQuestion();
            }
        }
        
        function toggleRecording() {
            if (!recognition) return;
            
            const btn = document.getElementById('voiceBtn');
            
            if (isRecording) {
                stopRecording();
            } else {
                startRecording();
            }
        }
        
        function startRecording() {
            if (!recognition) return;
            
            recognition.start();
            isRecording = true;
            const btn = document.getElementById('voiceBtn');
            btn.classList.add('recording');
            btn.innerHTML = '⏹ Stop';
            showToast('Listening... Speak now');
        }
        
        function stopRecording() {
            if (!recognition) return;
            
            recognition.stop();
            isRecording = false;
            const btn = document.getElementById('voiceBtn');
            if (btn) {
                btn.classList.remove('recording');
                btn.innerHTML = '🎤 Voice';
            }
        }
        
        function showToast(message) {
            const toast = document.getElementById('toast');
            toast.textContent = message;
            toast.classList.add('show');
            setTimeout(() => {
                toast.classList.remove('show');
            }, 3000);
        }
        
        function generatePRD() {
            const container = document.getElementById('questionContainer');
            
            // Generate markdown
            let markdown = '# Rapid Prototype Genesis - Product Requirements Document\\n\\n';
            markdown += '*Generated: ' + new Date().toLocaleString() + '*\\n\\n';
            markdown += '---\\n\\n';
            
            let currentSection = '';
            questions.forEach((q, index) => {
                if (q.section !== currentSection) {
                    currentSection = q.section;
                    markdown += `## ${currentSection}\\n\\n`;
                }
                
                markdown += `### ${q.number}. ${q.text}\\n`;
                markdown += `*${q.hint}*\\n\\n`;
                markdown += `**Answer:** ${answers[index] || '(No answer provided)'}\\n\\n`;
            });
            
            markdown += '---\\n\\n';
            markdown += '## The Rapid Prototype Commitment\\n\\n';
            markdown += '- **NO additional features** beyond what\\'s specified\\n';
            markdown += '- **NO perfect-seeking** that delays shipping\\n';
            markdown += '- **NO committees** - one vision, one decision-maker\\n';
            markdown += '- **YES to opinionated defaults**\\n';
            markdown += '- **YES to surprising delight**\\n';
            markdown += '- **YES to shipping TODAY**\\n\\n';
            markdown += '*"Real artists ship."* - Steve Jobs\\n';
            
            // Create download link
            const blob = new Blob([markdown], { type: 'text/markdown' });
            const url = URL.createObjectURL(blob);
            const timestamp = new Date().toISOString().replace(/[:.]/g, '-').slice(0, -5);
            const filename = `PRD-${timestamp}.md`;
            
            container.innerHTML = `
                <div class="final-screen">
                    <div class="success-icon">✓</div>
                    <h2 style="margin-bottom: 16px;">PRD Generated!</h2>
                    <p style="color: var(--gray); margin-bottom: 32px;">
                        Your Rapid Prototype Genesis document is ready.
                    </p>
                    
                    <a href="${url}" download="${filename}" class="btn btn-primary" style="width: 200px; margin: 0 auto 16px;">
                        📄 Download PRD
                    </a>
                    
                    <button onclick="startOver()" class="btn btn-secondary" style="width: 200px; margin: 0 auto;">
                        Start New Project
                    </button>
                    
                    <div style="margin-top: 40px; padding: 20px; background: var(--light-gray); border-radius: 12px; text-align: left;">
                        <h3 style="margin-bottom: 12px;">Next Steps:</h3>
                        <ol style="padding-left: 20px; color: var(--gray);">
                            <li>Review your PRD for completeness</li>
                            <li>Share with your implementation team</li>
                            <li>Generate your Ansible playbook</li>
                            <li>Ship today!</li>
                        </ol>
                    </div>
                </div>
            `;
            
            // Save to backend
            fetch('/save-prd', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ 
                    markdown: markdown,
                    answers: answers,
                    timestamp: new Date().toISOString()
                })
            }).then(() => {
                showToast('PRD saved successfully!');
            }).catch(err => {
                console.error('Error saving PRD:', err);
            });
        }
        
        function startOver() {
            if (confirm('Start a new project? Current answers will be saved.')) {
                currentQuestion = 0;
                answers = {};
                localStorage.removeItem('rpg_answers');
                renderQuestion();
            }
        }
        
        // Load saved answers from localStorage
        const saved = localStorage.getItem('rpg_answers');
        if (saved) {
            answers = JSON.parse(saved);
        }
        
        // Keyboard shortcuts
        document.addEventListener('keydown', (e) => {
            if (e.ctrlKey || e.metaKey) {
                if (e.key === 'Enter') {
                    e.preventDefault();
                    nextQuestion();
                } else if (e.key === 'ArrowLeft') {
                    e.preventDefault();
                    previousQuestion();
                } else if (e.key === 'ArrowRight') {
                    e.preventDefault();
                    nextQuestion();
                } else if (e.key === ' ') {
                    e.preventDefault();
                    toggleRecording();
                }
            }
        });
        
        // Initialize
        renderQuestion();
        
        // Register service worker for PWA
        if ('serviceWorker' in navigator) {
            navigator.serviceWorker.register('/sw.js').then(reg => {
                console.log('Service Worker registered');
            }).catch(err => {
                console.error('Service Worker registration failed:', err);
            });
        }
    </script>
</body>
</html>"""

@app.route('/')
def index():
    """Serve the main PWA application"""
    return HTML_TEMPLATE

@app.route('/manifest.json')
def manifest():
    """Serve PWA manifest"""
    manifest_data = {
        "name": "Rapid Prototype Genesis",
        "short_name": "RPG",
        "description": "From Vision to Lovable Prototype in One Day",
        "start_url": "/",
        "display": "standalone",
        "theme_color": "#000000",
        "background_color": "#ffffff",
        "orientation": "portrait",
        "icons": [
            {
                "src": "/icon-192.png",
                "sizes": "192x192",
                "type": "image/png",
                "purpose": "any maskable"
            },
            {
                "src": "/icon-512.png",
                "sizes": "512x512",
                "type": "image/png"
            }
        ]
    }
    response = make_response(json.dumps(manifest_data, indent=2))
    response.headers['Content-Type'] = 'application/manifest+json'
    return response

@app.route('/sw.js')
def service_worker():
    """Serve service worker for offline functionality"""
    sw_content = """
const CACHE_NAME = 'rpg-v1';
const urlsToCache = [
    '/',
    '/manifest.json'
];

self.addEventListener('install', event => {
    event.waitUntil(
        caches.open(CACHE_NAME)
            .then(cache => cache.addAll(urlsToCache))
    );
});

self.addEventListener('fetch', event => {
    event.respondWith(
        caches.match(event.request)
            .then(response => {
                if (response) {
                    return response;
                }
                return fetch(event.request);
            })
    );
});

self.addEventListener('activate', event => {
    event.waitUntil(
        caches.keys().then(cacheNames => {
            return Promise.all(
                cacheNames.filter(cacheName => {
                    return cacheName !== CACHE_NAME;
                }).map(cacheName => {
                    return caches.delete(cacheName);
                })
            );
        })
    );
});
"""
    response = make_response(sw_content)
    response.headers['Content-Type'] = 'application/javascript'
    response.headers['Service-Worker-Allowed'] = '/'
    return response

@app.route('/icon-<int:size>.png')
def icon(size):
    """Generate PWA icons dynamically (SVG placeholder)"""
    svg_content = f"""
<svg width="{size}" height="{size}" viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">
    <rect width="100" height="100" fill="#000000"/>
    <text x="50" y="50" font-family="SF Pro Display, -apple-system, sans-serif" 
          font-size="40" font-weight="bold" fill="#00ff41" 
          text-anchor="middle" dominant-baseline="middle">⚡</text>
</svg>
"""
    response = make_response(svg_content)
    response.headers['Content-Type'] = 'image/svg+xml'
    return response

@app.route('/save-prd', methods=['POST'])
def save_prd():
    """Save generated PRD to server"""
    try:
        data = request.json
        markdown = data.get('markdown', '')
        answers = data.get('answers', {})
        timestamp = data.get('timestamp', datetime.now().isoformat())
        
        # Generate filename
        filename = f"PRD_{timestamp.replace(':', '-').replace('.', '-')}.md"
        filepath = PRD_DIR / filename
        
        # Save markdown file
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(markdown)
        
        # Save answers as JSON for potential reuse
        json_filename = f"answers_{timestamp.replace(':', '-').replace('.', '-')}.json"
        json_filepath = PRD_DIR / json_filename
        with open(json_filepath, 'w', encoding='utf-8') as f:
            json.dump({
                'timestamp': timestamp,
                'answers': answers,
                'markdown_file': filename
            }, f, indent=2)
        
        return jsonify({
            'success': True,
            'message': 'PRD saved successfully',
            'filename': filename
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'prd_count': len(list(PRD_DIR.glob('*.md')))
    })

if __name__ == '__main__':
    print("🚀 Rapid Prototype Genesis Server Starting...")
    print("📱 Access at: http://localhost:5000")
    print("🎤 Voice input requires HTTPS in production")
    print("💾 PRDs will be saved to: ./generated_prds/")
    print("\nKeyboard shortcuts:")
    print("  Ctrl+Enter: Next question")
    print("  Ctrl+←/→: Navigate questions")
    print("  Ctrl+Space: Toggle voice input\n")
    
    app.run(
        host='0.0.0.0',
        port=5005,
        debug=True
    )
