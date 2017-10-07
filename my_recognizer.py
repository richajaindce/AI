import warnings
from asl_data import SinglesData


def recognize(models: dict, test_set: SinglesData):
    """ Recognize test word sequences from word models set

   :param models: dict of trained models
       {'SOMEWORD': GaussianHMM model object, 'SOMEOTHERWORD': GaussianHMM model object, ...}
   :param test_set: SinglesData object
   :return: (list, list)  as probabilities, guesses
       both lists are ordered by the test set word_id
       probabilities is a list of dictionaries where each key a word and value is Log Liklihood
           [{SOMEWORD': LogLvalue, 'SOMEOTHERWORD' LogLvalue, ... },
            {SOMEWORD': LogLvalue, 'SOMEOTHERWORD' LogLvalue, ... },
            ]
       guesses is a list of the best guess words ordered by the test set word_id
           ['WORDGUESS0', 'WORDGUESS1', 'WORDGUESS2',...]
   """
    warnings.filterwarnings("ignore", category=DeprecationWarning)
    probabilities = []
    guesses = []
    for index in range(0, len(test_set.get_all_Xlengths())):
        best_score = float("-inf")
        best_match = None
        X, lengths = test_set.get_all_Xlengths()[index]
        probabilities_dict = {}
        for word, model in models.items(): 
            try:
                logL = model.score(X, lengths)
            except:
                logL = float("-inf")
            probabilities_dict[word] = logL
            if logL > best_score:
                best_match, best_score = word, logL
        guesses.append(best_match)
        probabilities.append(probabilities_dict)
    return probabilities, guesses
