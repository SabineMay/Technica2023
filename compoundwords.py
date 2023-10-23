#from translate import Translator
import string
#assuming that it recieves a list of tuples, first index word, second index is pos

def test():
    list = [("first", "noun"), ("second", "noun"), ("third", "noun")]
    print("here")

    compound_words(list)


def compound_words(list_of_tuples):
    previous = ("firstword", "First")
    AllowedPOS = [("adj","noun"), ("noun","noun")] #add in sequence of what typical compound words are NEED TO CAHNGE TO ABBREV
    for word_pos_pair in list_of_tuples:
        print("here")
        if previous == ("firstword", "First"):
            previous = word_pos_pair
        else:
            currTuplePos = (previous[1], word_pos_pair[1])
            if currTuplePos in AllowedPOS:
                possiblecompoundword = previous[1].append(word_pos_pair[0])
                print(possiblecompoundword)
                #check translate to see if it comes back the same
            previous = word_pos_pair
