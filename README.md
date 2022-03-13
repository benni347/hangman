# Hangman
## Overview
This is an hangman game that generates a random word. Then it get multithreaded so that the definitons already get ready and a showcase of GitHub Copilot.
## API keys
To get the used APIs go to: 
1. [Wordsapi](https://rapidapi.com/dpventures/api/wordsapi/) and register with a free account.
2. [Lingua Robot](https://rapidapi.com/rokish/api/lingua-robot/) the same here.

Create an hangman.yml file. With this format:
```
apis:
  wordsapi:
    apikey: {your-key}
    host: {your-host}
  linguarobot:
    apikey: {your-key}
    host: {your-host}
```
## Hot wo use
- You change the perms for `hangman.py` with `chmod +x hangman.py` and then you can run `./hangman.py`.
- You can run `python3 hangman.py`
