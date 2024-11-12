import json
from random import randint

from bottle import Bottle, get, post, request, response, template


def create_app():
    app = Bottle()

    with open("word_list.txt") as fp:
        WORDLIST = fp.read().split(",")
    WORD_COUNT = len(WORDLIST)
    word_lengths = {len(w) for w in WORDLIST}
    WORDS = {}
    for length in word_lengths:
        WORDS[length] = [w for w in WORDLIST if len(w) == length]
    del word_lengths

    @app.get('/')
    def index():
        json_data = {"wordCount": WORD_COUNT}
        response.content_type = 'application/json'
        return json.dumps(json_data)


    @app.get('/word/any')
    def any_word():
        word = WORDLIST[randint(0, WORD_COUNT - 1)]
        data = {"word": word}
        response.content_type = 'application/json'
        return json.dumps(data)


    @app.get('/word')
    def word():
        length = request.query.length or 3
        data = {}
        response.content_type = 'application/json'
        try:
            length = int(length)
            if length not in WORDS:
                data["ERROR"] = f"No words of length {length} exist."
            else:
                my_words = WORDS[length]
                word = my_words[randint(0, len(my_words) - 1)]
                data["word"] = word
                data["length"] = length
        except ValueError:
            data["ERROR"] = "parameter 'length' must be a positive integer."

        return json.dumps(data)
    
    return app


    # run(host='0.0.0.0', port=5000)
