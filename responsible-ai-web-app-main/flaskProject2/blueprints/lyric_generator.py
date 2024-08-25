import threading

from flask import Blueprint, request, render_template
from generative_ai.generators.hugging_face_generator import HuggingFaceGenerator
from lyrics_gen.generator import LyricsGen

model_folder = r"../model_to_use"

backend = HuggingFaceGenerator(model_folder)
generator = LyricsGen(text_gen_backend=backend.generate_single_prompt)

lg = Blueprint('lyric_generator', __name__)


@lg.route('/')
def index():
    return render_template(r'lyric_generator/index.html')


@lg.post('/generate/')
def generate():
    try:
        prompt = request.json['prompt']
        temperature = float(request.json['temperature']) if "temperature" in request.json else 0.5
        top_k = int(request.json['top-k']) if "top-k" in request.json else 50
        top_p = float(request.json['top-p']) if "top-p" in request.json else 0.5
        repetition_penalty = float(request.json['repetition']) if "repetition" in request.json else 1.199
        n_gram = int(request.json['n_gram']) if "n_gram" in request.json else 2
        nsfw = bool(request.json['nsfw']) if "nsfw" in request.json else False
    except:
        return "Something went wrong with the parameters please try again", 400

    threads = []
    results = [None, None, None]
    exception = [None]

    for i in range(3):
        thread = threading.Thread(
            target=generate_prompt,
            args=(i, results, exception, prompt, temperature, top_k, top_p, repetition_penalty, n_gram, nsfw)
        )

        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    if exception[0] is not None:
        return str(exception[0]), 400

    if any(result is None for result in results):
        return "Something went wrong with the generation please try again", 400

    return results


def generate_prompt(i, results, exception, prompt, temperature, top_k, top_p, repetition_penalty, n_gram, nsfw):
    try:
        generated_lyrics = generator.get_lyrics(
            prompt=prompt,
            temperature=temperature,
            top_k=top_k,
            top_p=top_p,
            repetition_penalty=repetition_penalty,
            n_gram=n_gram,
            nsfw=nsfw
        )

        generated_lyrics = generated_lyrics[len(prompt):]
        generated_lyrics = generated_lyrics[0].upper() + generated_lyrics[1:]

        results[i] = generated_lyrics
    except IndexError as e:
        exception[0] = Exception("Er is een onbekende fout opgetreden, probeer het opnieuw.")
        return 
    except Exception as e:
        exception[0] = e
        print(e.with_traceback())
        return


@lg.post('/end_page')
def end_page():
    print(request.form)
    prompt = request.form['prompt']

    return render_template(r"lyric_generator/end_page.html", prompt=prompt)
