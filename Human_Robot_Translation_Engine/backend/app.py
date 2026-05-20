# translator.py

import random
import html


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

    # Helper to build search links for songs
    def make_song_links(query):
        q = html.escape(query.replace(' ', '+'))
        youtube = f"https://www.youtube.com/results?search_query={q}"
        spotify = f"https://open.spotify.com/search/{q}"
        return youtube, spotify

    # Storyteller: generate multiple short stories, possibly in a chosen language
    if mode == 'storyteller' or 'story' in low:
        stories = []
        langs = []
        if language != 'any':
            langs = [language]
        else:
            langs = ['en', 'ta', 'es', 'fr']

        # Simple templates per language to create different variants
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

        # Generate up to `story_count` stories distributed over selected languages
        for i in range(story_count):
            lang = langs[i % len(langs)]
            tmpl = random.choice(templates.get(lang, templates['en']))
            story = tmpl.format(name=random.choice(names), adj=random.choice(adjs))
            # Ensure stories are brief: truncate to ~180 chars and keep whole sentence if possible
            max_len = 180
            if len(story) > max_len:
                truncated = story[:max_len].rsplit(' ', 1)[0].rstrip(' ,.;:') + '...'
            else:
                truncated = story
            stories.append({'lang': lang, 'text': truncated})

        speech = "Here are some short stories I've created for you."
        return {
            'steps': [
                'Understand request: tell stories',
                'Activate storytelling module',
                f'Generate {len(stories)} story(ies)',
                'Present stories to user'
            ],
            'speech': speech,
            'output': {'stories': stories}
        }

    # Teacher mode: code, grammar, math as before
    if mode == 'teacher' or 'program' in low or 'c program' in low or 'c program' in task:
        # Example: C program to add two numbers
        if 'c program' in low and 'add' in low and 'two' in low:
            code = (
                '#include <stdio.h>\n'
                'int main() {\n'
                '    int a, b, sum;\n'
                '    printf("Enter two integers: ");\n'
                '    scanf("%d %d", &a, &b);\n'
                '    sum = a + b;\n'
                '    printf("Sum = %d\n", sum);\n'
                '    return 0;\n'
                '}'
            )
            return {
                'steps': ['Interpret the task', 'Write example code', 'Return code'],
                'speech': "Here's a simple C program that adds two numbers.",
                'output': {'code': code}
            }

        if 'grammar' in low or 'english grammar' in low:
            explanation = (
                "English grammar overview:\n"
                "- Sentence = Subject + Verb + Object.\n"
                "- Tenses: past, present, future.\n"
                "- Articles: 'a', 'an', 'the'.\n"
                "- Ask for a specific example for more detail."
            )
            return {
                'steps': ['Analyze grammar request', 'Provide explanation'],
                'speech': 'Here is a brief grammar overview.',
                'output': {'explanation': explanation}
            }

        # Safe math evaluator
        import ast, operator, math

        allowed_names = {k: getattr(math, k) for k in ['sqrt', 'sin', 'cos', 'tan', 'log', 'exp', 'pi', 'e']}

        def safe_eval(expr):
            node = ast.parse(expr, mode='eval')
            ops = {
                ast.Add: operator.add,
                ast.Sub: operator.sub,
                ast.Mult: operator.mul,
                ast.Div: operator.truediv,
                ast.Pow: operator.pow,
                ast.USub: operator.neg,
                ast.UAdd: operator.pos,
                ast.Mod: operator.mod
            }

            def _eval(n):
                if isinstance(n, ast.Expression):
                    return _eval(n.body)
                if isinstance(n, ast.Num):
                    return n.n
                if isinstance(n, ast.Constant):
                    return n.value
                if isinstance(n, ast.BinOp):
                    l = _eval(n.left); r = _eval(n.right)
                    op = type(n.op)
                    if op in ops: return ops[op](l, r)
                if isinstance(n, ast.UnaryOp):
                    val = _eval(n.operand); op = type(n.op)
                    if op in ops: return ops[op](val)
                if isinstance(n, ast.Call):
                    if isinstance(n.func, ast.Name):
                        fname = n.func.id
                        if fname in allowed_names:
                            args = [_eval(a) for a in n.args]
                            return allowed_names[fname](*args)
                if isinstance(n, ast.Name):
                    if n.id in allowed_names: return allowed_names[n.id]
                raise ValueError('Unsupported expression')

            return _eval(node)

        math_keywords = ['+', '-', '*', '/', 'sqrt', 'sin', 'cos', 'tan', 'log', 'pi', 'e', '^']
        if any(k in low for k in math_keywords):
            expr = low.replace('^', '**')
            try:
                res = safe_eval(expr)
                return {
                    'steps': ['Parse math expression', 'Compute result'],
                    'speech': f'The result is {res}.',
                    'output': {'result': str(res)}
                }
            except Exception:
                pass

    # Emotional mode with sub-emotions and song suggestions
    if mode == 'emotional' or 'feel' in low or 'emotion' in low:
        emotion_choice = emotion if emotion and emotion != 'default' else None
        # Detect some emotion words from task if not provided
        if not emotion_choice:
            for e in ['happy', 'sad', 'angry']:
                if e in low:
                    emotion_choice = e
                    break

        base_steps = [f'Receive input: {task}', 'Assess emotional content', 'Provide feedback', 'Offer next steps']
        songs = []
        speech = "I'm here to share how you feel and help."

        if emotion_choice == 'happy':
            # Recommend upbeat songs / playlists
            queries = ['happy songs playlist', 'upbeat pop hits', 'feel good songs']
            for q in queries[:3]:
                yt, sp = make_song_links(q)
                songs.append({'title': q, 'youtube': yt, 'spotify': sp})
            speech = 'You sound happy — here are some upbeat songs you can enjoy.'

        elif emotion_choice == 'sad':
            queries = ['sad songs playlist', 'calming sad music', 'melancholic songs']
            for q in queries[:3]:
                yt, sp = make_song_links(q)
                songs.append({'title': q, 'youtube': yt, 'spotify': sp})
            speech = 'I hear you — gentle music may help. Here are some suggestions.'

        elif emotion_choice == 'angry':
            queries = ['angry rock songs', 'intense workout music', 'release anger songs']
            for q in queries[:3]:
                yt, sp = make_song_links(q)
                songs.append({'title': q, 'youtube': yt, 'spotify': sp})
            speech = 'You seem angry — here are some tracks that could match that energy.'

        else:
            # generic emotional support: provide gentle/calm music suggestions by default
            queries = ['calm relaxing music', 'gentle piano music', 'ambient chill playlist']
            for q in queries[:3]:
                yt, sp = make_song_links(q)
                songs.append({'title': q, 'youtube': yt, 'spotify': sp})
            speech = "Tell me more — here are some calming tracks you might like."

        return {
            'steps': base_steps,
            'speech': speech,
            'output': {'songs': songs}
        }

    # Motivational mode
    if mode == 'motivational':
        plan = [
            'Listen to the goal',
            'Break it into small achievable steps',
            'Set quick wins and timeline',
            'Cheer and encourage'
        ]
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
