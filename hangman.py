#!/usr/bin/env python
"""
We use the random-word-api.herokuapp.com to get a random word.
Then uses async methods to get the definition from the word.

Author: Cédric Skwar
E-mail: cdrc+hangman@skwar.me
"""
# from sys import exit
import asyncio
import aiohttp
import yaml
# import the random word from the helper file
import random_word_file


class Hangman:
    """
    This class is the hangman game.

    :return: None
    """

    def __init__(self):
        """:return: None"""
        # make a running boolean that starts as 1
        self.session = None
        self.running = True
        self.cycle = 0
        # self.word = self._random_word_fn()
        self.word = random_word_file.random_word_fn()
        self.word = "word"
        print("word:", self.word)
        # add the word to the list of words
        self.word_list = [self.word]
        # printtype self.word
        # make a list of letters in the word
        self.letters = list(self.word)
        # make a list of letters that have been guessed
        self.guessed_letters = []
        # make a list of letters that have not been guessed
        self.unguessed_letters = "abcdefghijklmnopqrstuvwxyz"
        # replace only the letters that are in the alphabet with "_"

        self.underscore = []
        for i in range(len(self.word)):
            self.underscore.append(self._get_replacement_char(self.letters[i]))

        # Define the self .guess variable
        self.guess = ''

        # load yaml file
        with open("hangman.yml", "r") as stream:
            try:
                self.cfg = yaml.safe_load(stream)
            except yaml.YAMLError as exc:
                print("Error in yaml file:" + exc)

        self.loop = asyncio.get_event_loop()

        self.definitions = []

    async def _get_request(self, method, url, headers):
        """:return: status_code, json"""
        async with self.session.request(method, url, headers=headers) as response:
            # return await (response.status_code, response.json())
            json = await response.json()
            status = response.status
            return status, json

    async def _get_def_lingua_api(self, word):
        url = "https://lingua-robot.p.rapidapi.com/language/v1/entries/en/" + word
        headers = {
            'x-rapidapi-host': self.cfg["apis"]["linguarobot"]["host"],
            'x-rapidapi-key': self.cfg["apis"]["linguarobot"]["apikey"]
        }
        status_code, json = await self._get_request(method="GET", url=url, headers=headers)

        if json['entries']:
            definition = json["entries"][0]["lexemes"][0]["senses"][0]["definition"]
        else:
            definition = False
        return definition

    async def _get_definition_from_words_api(self, word):
        url = "https://wordsapiv1.p.rapidapi.com/words/" + word + "/definitions"
        headers = {
            'x-rapidapi-host': self.cfg["apis"]["wordsapi"]["host"],
            'x-rapidapi-key': self.cfg["apis"]["wordsapi"]["apikey"]
        }
        status_code, json = await self._get_request(method="GET", url=url, headers=headers)

        if 'success' not in json and json["definitions"]:
            return json["definitions"][0]["definition"]
        return None

    @staticmethod
    def _get_replacement_char(c):
        if c.isalpha():
            return '_'
        else:
            return c

    def ask_letter(self):
        # ask the user to input a letter and convert the input to lowercase and to the first letter
        # check if the input is "" or " "
        # if it is, ask the user to input a letter again
        # if it is not, append the letter to the self.guess
        while True:
            self.guess = input("Guess a letter: ").lower()
            if self.guess in ['', ' ']:
                print("You must guess a letter!")
            else:
                break

    def check_letter(self):
        # In this function, we check if the letter is in the word
        self.guess = self.guess[0]
        # remove the guessed letter in unguessed letters
        self.unguessed_letters = self.unguessed_letters.replace(
            self.guess, " ")
        # check if the letter was already guessed
        if self.guess in self.guessed_letters:
            print("You already guessed that letter")
            # if the letter was not guessed
        else:
            # add the letter to the guessed letters list
            self.guessed_letters.append(self.guess)
            # if the letter is in the word
            if self.guess in self.letters:
                # print a message saying the letter is in the word
                print("The letter is in the word")
                # for each letter in the word
                # for i in range(len(self.letters)):
                for i, n in enumerate(self.letters):
                    # if the letter is in the word
                    if self.guess == self.letters[i]:
                        # replace the underscore with the letter
                        self.underscore[i] = self.guess
            elif self.guess == "\\":
                print("\\ is not allowed")
            elif self.guess == "^":
                print("^ is not allowed")
            elif self.guess in ["F1", "F2", "F3", "F4", "F5",
                                "F6", "F7", "F8", "F9", "F10", "F11", "F12"]:
                print("F1-F12 is not allowed")
            else:
                # print Sorry the " letter "is not in the word."
                print("Sorry the letter " + self.guess + " is not in the word.")
                # add one to the cycle
                self.cycle += 1

    def check_win(self):
        # if "_" not in self.underscores print "you win" and ask if user wants to play again
        if "_" not in self.underscore:
            print("you win")
            self.play_again()

    def play_again(self):
        # ask if the user wants to play again
        play_again = input("Play again? (y/n/d): ")
        # cut the input to lowercase and to the first letter
        play_again = play_again.lower()[0]
        # if the user wants to play again
        if play_again == "y":
            # reset the game
            self.__init__()
        # if the user does not want to play again
        elif play_again == "d":
            # print the definition of the word
            print("The word was: " + self.word)
            # print the definition of the word
            print("Linguarobot definition: " + self.definitions[0])
            print("WordsAPI definition: " + self.definitions[1])
            # ask again
            self.play_again()
        else:
            # Print a nice goodbye message
            print("Goodbye and have a nice day!")
            # set the running boolean to False
            self.running = False
            # exit the game
            exit()

        # if the cycle is greater than the length of the word

    # draw the hangman
    def draw_hangman(self):
        # if the cycle is 0
        if self.cycle == 0:
            #
            print("  _________     ")
            print(" |         |    ")
            print(" |              ")
            print(" |              ")
            print(" |              ")
            print(" |              ")
            print("_|___           ")
        # if the cycle is 1
        elif self.cycle == 1:
            #
            print("  _________     ")
            print(" |         |    ")
            print(" |         O    ")
            print(" |              ")
            print(" |              ")
            print(" |              ")
            print("_|___           ")
        # if the cycle is 2
        elif self.cycle == 2:
            #
            print("  _________     ")
            print(" |         |    ")
            print(" |         O    ")
            print(" |         |    ")
            print(" |              ")
            print(" |              ")
            print("_|___           ")
        # if the cycle is 3
        elif self.cycle == 3:
            #
            print("  _________     ")
            print(" |         |    ")
            print(" |         O    ")
            print(" |        /|    ")
            print(" |              ")
            print(" |              ")
            print("_|___           ")
        # if the cycle is 4
        elif self.cycle == 4:
            #
            print("  _________     ")
            print(" |         |    ")
            print(" |         O    ")
            print(" |        /|\\   ")
            print(" |              ")
            print(" |              ")
            print("_|___           ")
        # if the cycle is 5
        elif self.cycle == 5:
            #
            print("  _________     ")
            print(" |         |    ")
            print(" |         O    ")
            print(" |        /|\\   ")
            print(" |        /     ")
            print(" |              ")
            print("_|___           ")
        # if the cycle is 6
        elif self.cycle == 6:
            #
            print("  _________     ")
            print(" |         |    ")
            print(" |         O    ")
            print(" |        /|\\   ")
            print(" |        / \\   ")
            print(" |              ")
            print("_|___           ")
        # print "you lose" and ask if the user wants to play again
        else:
            # print "You lost" and the word
            print("You lost.\n The word was: " + self.word)
            self.play_again()

    async def play(self):
        self.session = aiohttp.ClientSession(loop=self.loop)

        lingua_api_returned = await self._get_def_lingua_api(self.word)
        # print("lingua_api_returned: " + str(lingua_api_returned))

        words_api_returned = await self._get_definition_from_words_api(self.word)
        # print("words_api_returned: " + str(words_api_returned))

        self.definitions = [lingua_api_returned, words_api_returned]

        await self.session.close()

        while self.running:
            self.draw_hangman()
            print("The word is: " + "".join(self.underscore) +
                  " (Length: " + str(len(self.word)) + ")")
            print("Remaining letters: " + self.unguessed_letters)
            self.ask_letter()
            self.check_letter()
            self.check_win()


if __name__ == '__main__':
    # call the Hangman class
    hangman = Hangman()
    # call the play method
    hangman.loop.run_until_complete(hangman.play())
