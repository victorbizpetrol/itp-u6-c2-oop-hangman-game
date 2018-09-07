from .exceptions import *
import random

#test script:  py.test test_guess_word.py
class GuessAttempt(object):
    def __init__(self, guess_letter, miss=False, hit=False):
        self.character = guess_letter
        self.miss = miss
        self.hit = hit
        
        if self.hit == True and self.miss == True:
            raise InvalidGuessAttempt

        if len(self.character) > 1:
            raise InvalidGuessedLetterException
    
    def is_hit(self):
        return self.hit
    
    def is_miss(self):
        return self.miss


class GuessWord(object):
    def __init__(self, guess_word):
        self.answer = guess_word
        self.masked = ''

        if not self.answer:
            raise InvalidWordException

        for i in range(0, len(self.answer)):
            self.masked += '*'

    def perform_attempt(self, guess_letter):
        hit = None
        miss = None
        new_masked_word= ''

        for answer_index, answer_character in enumerate(self.answer):
            if answer_character.lower() == guess_letter.lower():
                new_masked_word += guess_letter.lower()
            else:
                new_masked_word += self.masked[answer_index]

        if self.masked == new_masked_word:
            hit = False
            miss = True
        else:
            hit = True
            miss = False

        self.masked = new_masked_word

        attempt = GuessAttempt(guess_letter, miss, hit)
        return attempt


class HangmanGame(object):
    
    WORD_LIST = ['rmotr', 'python', 'awesome']
    
    def __init__(self, word_list=None, number_of_guesses=5):
        if not word_list:
            word_list = self.WORD_LIST
            
        self.word_list = word_list
        self.remaining_misses = number_of_guesses
        self.previous_guesses = []
        select_word = self.select_random_word(word_list)
        self.word = GuessWord(select_word) #instance of GuessWord

    @classmethod
    def select_random_word(cls, word_list):
        try:
            guess_word = random.choice(word_list)
            return guess_word
        except Exception:
            raise InvalidListOfWordsException

    def guess(self, letter):
        if self.is_finished():
            raise GameFinishedException()
            
        self.previous_guesses.append(letter.lower())
        
        attempt = self.word.perform_attempt(letter)
        if attempt.is_miss():
            self.remaining_misses -= 1
            if self.remaining_misses < 1:
                raise GameLostException()
                
        if self.is_won():
            raise GameWonException()
            
        return attempt

    def is_finished(self):
        if self.is_won() or self.is_lost():
            return True
        return False
    
    def is_lost(self):
        if self.remaining_misses < 1:
            return True
        return False

    def is_won(self):
        if self.word.answer == self.word.masked:
            return True
        return False

        
#  py.test test_hangman_game.py -k test_game_already_lost_raises_game_finished


