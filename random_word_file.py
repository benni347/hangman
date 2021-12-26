import requests


def random_word_fn():
    # make a request to the url and get the response as a json object https://random-word-api.herokuapp.com/word?number=1
    response = requests.get(
        "https://random-word-api.herokuapp.com/word?number=1&swear=0")
    # cut the response at the first "
    response = response.text[2:-2]
    # print the response as a string
    return response


if __name__ == '__main__':
    # print the word
    print(random_word_fn())
