import numpy as np
import pickle as pkl
import os

application_path = os.path.dirname(__file__)

english_word_counts,charcter_counts = pkl.load(open(os.path.join(application_path, "model.pkl"),"rb"))

#encoding
ENCODING = {char:val for char,val in zip(["a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q",
                                          "r","s","t","u","v","w","x","y","z"],range(26))}

DECODING = {val:key for key,val in ENCODING.items()}

def encoder(string):
    """
    one-hot encode string
    :param string: str, string to encode
    :return: arr, numpy array of encoded string
    """
    string = string.lower()
    return tuple([ENCODING[x] for x in string])

def decoder(word):
    string = ""
    for x in word:
        string += DECODING[x]
    return string

def checkCharacters(word,charcounts):
    for char,count in charcounts.items():
        if count > 0:
            if char not in word:#len([x for x in word if x == char]) < count:
                return False
    return True

def filterWords(pos,chars,exclude,words):
    tmp = list(words)
    for p,v in pos.items():
        tmp = [x for x in tmp if x[p] == v]

    tmp = [x for x in tmp if not any(e in x for e in exclude)]
    tmp = [x for x in tmp if checkCharacters(x,chars)]

    return tmp

def parseInput(result,guess,pos,chars,exclude):
    for x in range(len(result)):
        if float(result[x]) > 1.5:
            pos[x] = guess[x]
            chars[guess[x]] += 1
        elif float(result[x]) > .5:
            chars[guess[x]] += 1
        else:
            exclude.append(guess[x])
    exclude = list(set(exclude))

    return pos,chars,exclude



def getMostLikelyWord(words,scoringModel):
    words.sort(key=lambda x: scoringModel[x],reverse=True)
    return words[0]

def getMostLikelyWordByCharacter(words,scoringModel):
    words.sort(key=lambda x: np.sum([scoringModel[y] for y in x]),reverse=True)
    return words[0]

def scoreGuess(guess,word):
    result = []
    for g,w in zip(guess,word):
        if g == w:
            result.append(2)
        elif g in word:
            result.append(1)
        else:
            result.append(0)
    return result

def wordler(words,characterScores,wordScores,word):
    word = encoder(word)
    guess = getMostLikelyWordByCharacter(words,characterScores)

    pos = {}
    chars = {char:0 for char in ENCODING.values()}
    exclude = []

    guessCount = 0
    won = False
    history = []
    guesses = []
    while not won and guessCount < 6:
        guesses.append(guess)
        result = scoreGuess(guess,word)
        history.append(result)
        guessCount += 1
        pos,chars,exclude = parseInput(result,guess,pos,chars,exclude)
        words = filterWords(pos,chars,exclude,words)

        if len(pos) == 5:
            won = True
        else:
            words = [x for x in words if decoder(x) != decoder(guess)]
            if len(words) > 0:
                guess = getMostLikelyWord(words,wordScores)
            else:
                break

    return won, [decoder(x) for x in guesses],history
