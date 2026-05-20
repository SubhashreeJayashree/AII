from flask import Flask, request, jsonify, send_from_directory
import sqlite3
import os
from translator import translate_to_robot_commands
from safety_rules import is_task_safe

APP = Flask(__name__, static_folder="../frontend", static_url_path="/")

DB_PATH = os.path.join(os.path.dirname(__file__), "commands.db")

def init_db_if_missing():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("""
      CREATE TABLE IF NOT EXISTS commands (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        task TEXT NOT NULL,
        is_safe INTEGER NOT NULL,
        details TEXT,
        translation TEXT,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP
      )
    """)
    conn.commit()
    conn.close()

def save_command_to_db(task_text, is_safe, details=None, translation=None):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO commands (task, is_safe, details, translation)
        VALUES (?, ?, ?, ?)
    """, (task_text, 1 if is_safe else 0, details, str(translation) if translation else None))
    conn.commit()
    conn.close()

init_db_if_missing()

@APP.route("/")
def index():
    return send_from_directory(APP.static_folder, "index.html")


# Serve assets from the frontend 'assests' folder (typo in folder name).
@APP.route('/assets/<path:filename>')
def serve_assets(filename):
    # Map '/assets/...' requests to the existing frontend/assests directory
    return send_from_directory(os.path.join(APP.static_folder, "assests"), filename)
@APP.route("/process", methods=["POST"])
def process():
    data = request.get_json()
    task_text = data.get("task", "").strip()
    mode = data.get("mode") if data else None
    options = data.get("options") if data else {}

    if not task_text:
        return jsonify({"error": "Task cannot be empty."}), 400

    safe, message = is_task_safe(task_text)
    
    if not safe:
        save_command_to_db(task_text, False, message, None)
        return jsonify({
            "status": "unsafe",
            "message": "❌ Dangerous Task: " + message
        })

    # Log the incoming task for debugging
    print(f"[PROCESS] task={task_text!r}, mode={mode!r}, options={options!r}")

    translation = translate_to_robot_commands(task_text, mode, options)

    # Log translation result for debugging
    print(f"[TRANSLATION] {translation}")

    save_command_to_db(task_text, True, "safe", translation)

    return jsonify({
        "status": "safe",
        "message": "Task is safe.",
        "translation": translation
    })

if __name__ == "__main__":
    APP.run(debug=True, host="127.0.0.1", port=5000)




import random
import html
import pyttsx3


def translate_to_robot_commands(task_text, mode=None, options=None):
    """
    Translate a human task into robot steps. `mode` adjusts tone/behavior and
    `options` can include:
      - language: 'en', 'ta', 'es', 'fr', or 'any'
      - emotion: sub-emotion for emotional mode ('happy','sad','angry')
      - story_count: number of different stories to generate (1-5)
    """
    task = (task_text or '').strip()
    low = task.lower()
    options = options or {}
    language = options.get('language', 'any')
    emotion = options.get('emotion', 'default')
    story_count = int(options.get('story_count', 1) or 1)
    story_count = max(1, min(5, story_count))
    subject = options.get("subject", "").lower()

    def make_song_links(query):
        q = html.escape(query.replace(' ', '+'))
        youtube = f"https://www.youtube.com/results?search_query={q}"
        spotify = f"https://open.spotify.com/search/{q}"
        return youtube, spotify

    # === Storyteller Mode ===
    if mode == 'storyteller' or 'story' in low:
        stories = []
        langs = [language] if language != 'any' else ['en', 'ta', 'es', 'fr']
        templates = {
            'en': [
                "Once upon a time there was a {adj} little robot named {name} who loved to explore.",
                "In a small town, {name} the robot discovered a secret that changed everything.",
                "{name} was a curious robot who traveled beyond the city to meet new friends."
            ],
            'ta': [
                "ஒரு சிறிய நகரில் {name} என்ற ரோபோ ஒரு சுவாரஸ்யமான அத்தியாயத்தை கண்டுபிடித்தான்.",
                "ஒரு இனிய நாள், {name} ரோபோ மனிதர்களை புரிந்து கொள்ள தொடங்கினான்.",
                "{name} ரோபோ சுற்றுலாவிற்கு சென்று புதிய நண்பர்களைப் பெற்றது."
            ],
            'es': [
                "Érase una vez un robot llamado {name} que tenía un corazón curioso.",
                "En una aldea, {name} encontró una puerta hacia un mundo nuevo.",
                "{name} era un robot pequeño que soñaba con ir más allá del horizonte."
            ],
            'fr': [
                "Il était une fois un robot appelé {name} qui aimait écouter le vent.",
                "Dans un village, {name} découvrit un secret ancien.",
                "{name} était un petit robot qui rêvait d'aventures."
            ]
        }
        names = ['Robo', 'Ari', 'Kavi', 'Mika', 'Luna', 'Tiko']
        adjs = ['brave', 'curious', 'playful', 'kind', 'clever']

        for i in range(story_count):
            lang = langs[i % len(langs)]
            tmpl = random.choice(templates.get(lang, templates['en']))
            story = tmpl.format(name=random.choice(names), adj=random.choice(adjs))
            if len(story) > 180:
                story = story[:180].rsplit(' ', 1)[0].rstrip(' ,.;:') + '...'
            stories.append({'lang': lang, 'text': story})

        speech = "Here are some short stories I've created for you."
        return {
            'steps': ['Understand request: tell stories', 'Activate storytelling module',
                      f'Generate {len(stories)} story(ies)', 'Present stories to user'],
            'speech': speech,
            'output': {'stories': stories}
        }

    # === Teacher Mode (Q&A with references) ===
    if mode == 'teacher' or any(q in low for q in ['quiz','question','what is','define','explain']):
        import difflib
        import re
        def normalize_text(s):
            s = (s or '').lower().strip()
            s = re.sub(r'[^\w\s]', '', s)
            s = re.sub(r'\s+', ' ', s)
            return s

        subjects_questions = {
            'tamil': [{"q": "தமிழ் மொழி எது?", "a": "தமிழ் ஒரு திராவிட மொழி, உலகின் பழமையான மொழிகளில் ஒன்று."}],
            'english': [{"q": "What is the meaning of happy?", "a": "Happy means feeling or showing pleasure, satisfaction, or contentment."}],
            'maths': [{"q": "State Pythagoras theorem.", "a": "In a right triangle, square of hypotenuse = sum of squares of other two sides."}, {"q": "What is the square root of 144?", "a": "12"}],
            'physics': [{"q": "State Newton’s first law of motion.", "a": "A body remains at rest or in uniform motion unless acted upon by an external force."}, {"q": "State Newton’s second law.", "a": "Force equals mass times acceleration (F = ma)."}],
            'chemistry': [{"q": "Define atom.", "a": "An atom is the smallest unit of matter that retains the properties of an element."}, {"q": "What is H2O?", "a": "H2O is water, composed of two hydrogen atoms and one oxygen atom."}],
            'botany': [{"q": "Define photosynthesis.", "a": "Photosynthesis is the process by which plants produce food (glucose) using sunlight, carbon dioxide, and water."}, {"q": "Role of chlorophyll?", "a": "Chlorophyll absorbs light energy used in photosynthesis."}, {"q": "What is xylem?", "a": "Xylem is the plant vascular tissue that transports water and dissolved minerals from the roots upward to the shoots and leaves."}],
            'zoology': [{"q": "Define zoology.", "a": "The scientific study of animals."}, {"q": "What is a vertebrate?", "a": "An animal that has a backbone."}],
            'computer_applications': [{"q": "What is an operating system?", "a": "An operating system manages computer hardware and software resources."}, {"q": "Define compiler.", "a": "A compiler translates source code into machine code."}],
            'accountancy': [{"q": "Define accounting.", "a": "Accounting is the process of recording, summarizing, and reporting financial transactions."}, {"q": "What is a balance sheet?", "a": "A balance sheet shows a company’s assets, liabilities, and equity at a specific time."}],
            'economics': [{"q": "Define economics.", "a": "Economics is the study of production, distribution, and consumption of goods and services."}, {"q": "What is demand?", "a": "Demand is the quantity of a good consumers are willing to buy at a given price."}],
            'commerce': [{"q": "Define commerce.", "a": "Commerce is the activity of buying and selling goods and services."}, {"q": "What is trade?", "a": "Trade is the exchange of goods and services between people or countries."}],
            'gen_ai': [{"q": "What is Generative AI?", "a": "Generative AI refers to AI systems that can create new content such as text, images, or music."}],
            'ai_ml': [{"q": "What is Machine Learning?", "a": "Machine Learning is a subset of AI that enables systems to learn from data."}, {"q": "Define Artificial Intelligence.", "a": "Simulation of human intelligence by machines"}],
            'deep_learning': [{"q": "What is CNN in Deep Learning?", "a": "CNN (Convolutional Neural Network) is used for image and pattern recognition."}, {"q": "What are the layers in CNN?", "a": "Typical CNN layers include convolutional, pooling, fully connected, and output layers."}],
        }

        subj = subject or options.get("subject", "") or ""
        subj = subj.lower().strip()
        if not subj:
            for s in subjects_questions.keys():
                if s in low:
                    subj = s
                    break

        def build_index(pool):
            idx = {}
            for item in pool:
                k = normalize_text(item.get('q', ''))
                if k:
                    idx[k] = item.get('a', '')
            return idx

        if subj and subj in subjects_questions:
            pool_index = build_index(subjects_questions[subj])
            query_norm = normalize_text(task)
            if query_norm in pool_index:
                answer = pool_index[query_norm]
            else:
                qcore = re.sub(r'^(what is|define|explain|who is|tell me about)\s+', '', query_norm)
                matches = difflib.get_close_matches(qcore, list(pool_index.keys()), n=1, cutoff=0.6)
                if matches:
                    answer = pool_index[matches[0]]
                else:
                    top_candidates = list(pool_index.items())[:5]
                    enriched = [f"Q: {k}\nA: {v}" for k, v in top_candidates]
                    speech_output = 'I do not have an exact match. Here are related Q/A from ' + subj + ':\n\n' + '\n\n'.join(enriched)
                    return {'steps': ['Identify subject', f'Subject selected: {subj}', 'No exact match', 'Provide related Q/A'], 'speech': speech_output, 'output': {'quiz': enriched}}
            speech_output = f"Q: {task}\nA: {answer}"
            return {'steps': ['Identify subject', f'Subject selected: {subj}', 'Find best match', 'Present answer'], 'speech': speech_output, 'output': {'quiz': [{'q': task, 'a': answer}]}}

        else:
            combined_index = {}
            subject_map = {}
            for sname, pool in subjects_questions.items():
                for item in pool:
                    k = normalize_text(item.get('q', ''))
                    if k:
                        combined_index[k] = item.get('a', '')
                        subject_map[k] = sname
            query_norm = normalize_text(task)
            if query_norm in combined_index:
                answer = combined_index[query_norm]
                matched_subject = subject_map[query_norm]
            else:
                qcore = re.sub(r'^(what is|define|explain|who is|tell me about)\s+', '', query_norm)
                matches = difflib.get_close_matches(qcore, list(combined_index.keys()), n=1, cutoff=0.6)
                if matches:
                    m = matches[0]
                    answer = combined_index[m]
                    matched_subject = subject_map[m]
                else:
                    shortlist = []
                    for k, v in list(combined_index.items())[:6]:
                        shortlist.append({'q': k, 'a': v, 'subject': subject_map[k]})
                    enriched_texts = [f"[{it['subject']}] Q: {it['q']}\nA: {it['a']}" for it in shortlist]
                    speech_output = "Couldn't find an exact answer. Here are some related Q/A across subjects:\n\n" + "\n\n".join(enriched_texts)
                    return {'steps': ['Identify subject (none)', 'Search across pools', 'No exact match', 'Provide related Q/A'], 'speech': speech_output, 'output': {'quiz': enriched_texts}}
            speech_output = f"[{matched_subject}] Q: {task}\nA: {answer}"
            return {'steps': ['Identify subject (inferred)', f'Matched subject: {matched_subject}', 'Present answer'], 'speech': speech_output, 'output': {'quiz': [{'q': task, 'a': answer, 'subject': matched_subject}]}}
# === Emotional Mode with Songs ===
    if mode == 'emotional' or 'feel' in low or 'emotion' in low:
        emotion_choice = emotion if emotion and emotion != 'default' else None
        if not emotion_choice:
            for e in ['happy','sad','angry']:
                if e in low: emotion_choice = e; break
        base_steps = [f'Receive input: {task}', 'Assess emotional content', 'Provide feedback', 'Offer next steps']
        songs = []
        speech = "I'm here to share how you feel and help."

        if emotion_choice == 'happy':
            queries = ['happy songs playlist', 'upbeat pop hits', 'feel good songs']
            for q in queries:
                yt, sp = make_song_links(q)
                songs.append({'title': q, 'youtube': yt, 'spotify': sp})
            speech = 'You sound happy — here are some upbeat songs you can enjoy.'

        elif emotion_choice == 'sad':
            queries = ['sad songs playlist', 'calming sad music', 'melancholic songs']
            for q in queries:
                yt, sp = make_song_links(q)
                songs.append({'title': q, 'youtube': yt, 'spotify': sp})
            speech = 'I hear you — gentle music may help. Here are some suggestions.'

        elif emotion_choice == 'angry':
            queries = ['angry rock songs', 'intense workout music', 'release anger songs']
            for q in queries:
                yt, sp = make_song_links(q)
                songs.append({'title': q, 'youtube': yt, 'spotify': sp})
            speech = 'You seem angry — here are some tracks that could match that energy.'

        else:
            queries = ['calm relaxing music', 'gentle piano music', 'ambient chill playlist']
            for q in queries:
                yt, sp = make_song_links(q)
                songs.append({'title': q, 'youtube': yt, 'spotify': sp})
            speech = "Tell me more — here are some calming tracks you might like."

        return {'steps': base_steps, 'speech': speech, 'output': {'songs': songs}}

    # === Motivational Mode ===
    if mode == 'motivational':
        plan = ['Listen to the goal','Break it into small achievable steps','Set quick wins and timeline','Cheer and encourage']
        speech = "You can do this — let's create a small plan and start now."
        return {'steps': plan, 'speech': speech, 'output': {}}


    # Default behavior: try to infer task type (cleaning, pick up, etc.)
    if 'clean' in low:
        return {
            'steps': [
                'Understanding the cleaning task',
                'Scanning the area',
                'Identifying dust and waste',
                'Activating cleaning arm',
                'Cleaning the surface',
                'Task completed successfully'
            ],
            'speech': 'Cleaning the area now.'
        }

    if 'give me' in low or 'pick' in low:
        return {
            'steps': [
                'Identifying the object',
                'Scanning location',
                'Moving arm to the object',
                'Grabbing object',
                'Bringing the object to the user',
                'Task finished'
            ],
            'speech': 'I am giving the item to you.'
        }

    # Fallback
    return {
        'steps': [
            'Understanding the task: ' + task,
            'Robot is waking up',
            'Scanning surroundings',
            'Planning safe execution',
            'Performing task',
            'Task completed successfully'
        ],
        'speech': 'Task executed.'
    }
