#!/usr/bin/env python
"""
This is a hangman game that uses the random-word-api.herokuapp.com API to get a random word. 
Then uses multiple threads to get the definition from the word.

Author: Cédric Skwar
E-mail: cdrc+hangman@skwar.me
"""
# TODO: make that while the threads get the definition, you can still enter a guess
from multiprocessing.dummy import Pool as ThreadPool
# pretty print
from pprint import pprint

from sys import exit

import requests
import yaml

import random_word_file


class Hangman:

    def __init__(self):
        # make a running boolean that starts as 1
        self.running = 1
        self.cycle = 0
        # self.word = self._random_word_fn()
        self.word = random_word_file.random_word_fn()
        # self.word = "fubar"
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

        self.underscores = []
        for i in range(len(self.word)):
            self.underscores.append(self._get_replacement_char(self.word[i]))

        # ask the user to input a letter and append it to the guessed letters list
        self.guess = ''
        self.wrong_letters = []

        # load yaml file
        with open("hangman.yml", "r") as stream:
            try:
                self.cfg = yaml.safe_load(stream)
            except yaml.YAMLError as exc:
                print("Error in yaml file:" + exc)

        self.pool = ThreadPool(4)

        # hangman.definitions = hangman._get_definitions(hangman.word)
        self.definitions = self._get_definitions(self.word)

    def _get_definition_from_lingua_api(self, word):
        url = "https://lingua-robot.p.rapidapi.com/language/v1/entries/en/" + word
        headers = {
            'x-rapidapi-host': self.cfg["apis"]["linguarobot"]["host"],
            'x-rapidapi-key': self.cfg["apis"]["linguarobot"]["apikey"]
        }
        response = requests.request("GET", url, headers=headers)
        if response.json()['entries']:
            definition = response.json(
            )["entries"][0]["lexemes"][0]["senses"][0]["definition"]
        else:
            definition = False
        return definition

    def _get_definition_from_words_api(self, word):
        url = "https://wordsapiv1.p.rapidapi.com/words/" + word + "/definitions"
        headers = {
            'x-rapidapi-host': self.cfg["apis"]["wordsapi"]["host"],
            'x-rapidapi-key': self.cfg["apis"]["wordsapi"]["apikey"]
        }
        response = requests.request("GET", url, headers=headers)

        if 'success' in response.json():
            definition = False
        else:
            if response.json()["definitions"]:
                definition = response.json()["definitions"][0]["definition"]
            else:
                definition = False

        # if response.json()['success']:
        #     definition = response.json()["definitions"][0]["definition"]
        # else:
        #     definition = False

        return definition

    def _get_definition_from_dictionary_api(self, word):
        url = "https://dictionaryapi.dev/api/v2/entries/en/" + word
        response = requests.get(url)
        if response.status_code == requests.codes.ok:
            definition = response.json(
            )[0]["meanings"][0]["definitions"][0]["definition"]
        else:
            definition = False
        return definition

    def _get_definition_from_one_api(self, func):
        defintion = func(self.word)
        return defintion

    def _get_definitions(self, word):
        funcs = [self._get_definition_from_words_api,
                 self._get_definition_from_lingua_api,
                 self._get_definition_from_dictionary_api]

        defis = self.pool.map(self._get_definition_from_one_api, funcs)

    def _get_replacement_char(self, c):
        if c.isalpha():
            return '_'
        else:
            return c

    def ask_letter(self):
        # ask the user to input a letter and convert the input to lowercase and to the first letter
        self.guess = input("Guess a letter: ").lower()[0]

    def check_letter(self):
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
                for i in range(len(self.letters)):
                    # if the letter is in the word
                    if self.guess == self.letters[i]:
                        # replace the underscore with the letter
                        self.underscores[i] = self.guess
            # if the letter is not in the word
            else:
                # print Sorry the" letter "is not in the word."
                print("Sorry the letter " + self.guess + " is not in the word.")
                # add one to the cycle
                self.cycle += 1
                # add the letter to the wrong letters list
                self.wrong_letters.append(self.guess)

    def check_win(self):
        # if "_" not in self.underscores print "you win" and ask if user wants to play again
        if "_" not in self.underscores:
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
            pprint(self.definitions)

            # exit the program
            self.play_again()
        else:
            # print goodbye
            print("goodbye")
            # set the running boolean to 0
            self.running = 0
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
            print(" |        /|\   ")
            print(" |              ")
            print(" |              ")
            print("_|___           ")
        # if the cycle is 5
        elif self.cycle == 5:
            #
            print("  _________     ")
            print(" |         |    ")
            print(" |         O    ")
            print(" |        /|\   ")
            print(" |        /     ")
            print(" |              ")
            print("_|___           ")
        # if the cycle is 6
        elif self.cycle == 6:
            #
            print("  _________     ")
            print(" |         |    ")
            print(" |         O    ")
            print(" |        /|\   ")
            print(" |        / \   ")
            print(" |              ")
            print("_|___           ")
        # print "you lose" and ask if the user wants to play again
        else:
            # print "You lost" and the word
            print("You lost.\n The word was: " + self.word)
            self.play_again()


if __name__ == '__main__':
    # call the Hangman class
    hangman = Hangman()
    hangman.definitions = hangman._get_definitions(hangman.word)

    # while the running boolean is true
    while hangman.running:
        hangman.draw_hangman()
        print("The word is: " + "".join(hangman.underscores) +
              " (Length: " + str(len(hangman.word)) + ")")
        print("Remaining letters: " + hangman.unguessed_letters)
        hangman.ask_letter()
        hangman.check_letter()
        hangman.check_win()
