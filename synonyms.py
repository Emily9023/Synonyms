'''Semantic Similarity: starter code

Author: Michael Guerzhoy. Last modified: Nov. 14, 2016.
'''

import math


def norm(vec):
    '''Return the norm of a vector stored as a dictionary,
    as described in the handout for Project 3.
    '''

    sum_of_squares = 0.0
    for x in vec:
        sum_of_squares += vec[x] * vec[x]

    return math.sqrt(sum_of_squares)


def cosine_similarity(vec1, vec2):
    '''This function returns the cosine similarity between the sparse vectors vec1 and vec2, stored as dictionaries.
    For example,
    cosine_similarity({"a": 1, "b": 2, "c": 3}, {"b": 4, "c": 5, "d": 6})
    should return approximately 0.70 (as a float).'''

    sum = 0
    vkeys = list(vec1.keys())
    wkeys = list(vec2.keys())
    vvalues = list(vec1.values())
    wvalues = list(vec2.values())

    for j in range(len(vkeys)):
        if vkeys[j] in wkeys:
            sum += vvalues[j]*wvalues[wkeys.index(vkeys[j])]

    u_sumsquared = 0
    w_sumsquared = 0

    for i in range(len(vvalues)):
        u_sumsquared += vvalues[i]**2

    for k in range(len(wvalues)):
        w_sumsquared += wvalues[k]**2

    sim = (sum)/math.sqrt(u_sumsquared*w_sumsquared)

    return sim

def build_semantic_descriptors(sentences):
    '''This function takes in a list sentences which contains lists of strings (words) representing sentences, and
    returns a dictionary d such that for every word w that appears in at least one of the sentences, d[w] is itself
    a dictionary which represents the semantic descriptor of w (note: the variable names here are arbitrary).'''
    words = []
    dict_semantic = {}
    dict_words = {}

    for i in range(len(sentences)):
        dict_words = {}


        for word in sentences[i]:

            if not word in dict_words.keys():
                dict_words[word] = 1


        for word in dict_words:

            if not word in dict_semantic:
                temp_list = dict_words.copy()

                temp_list.pop(word, None)



                dict_semantic[word] = temp_list

            else:
                temp_list = dict_words.copy()
                temp_list.pop(word, None)


                for word2 in temp_list:

                    temp = dict_semantic[word]


                    if not word2 in temp.keys():
                        temp[word2] = 1
                    else:
                        temp[word2] += 1


    return dict_semantic



def build_semantic_descriptors_from_files(filenames):
    '''This function takes a list of filenames of strings, which contains the names of files (the first one can
    be opened using open(filenames[0], "r", encoding="latin1")), and returns the a dictionary of the
    semantic descriptors of all the words in the files filenames, with the files treated as a single text.
    You should assume that the following punctuation always separates sentences: ".", "!", "?", and that
    is the only punctuation that separates sentences. You should also assume that that is the only punctuation
    that separates sentences. Assume that only the following punctuation is present in the texts:
    [",", "-", "--", ":", ";"]'''
    sentences = ""
    for file in filenames:
        f = open(file, "r")
        sentences += f.read()

    sentences = sentences.lower()
    lines = sentences.replace("!", ".").replace("?", ".").replace("\n", ".").replace(". ", ".").split(".")

    while "" in lines:
        lines.remove("")


    list_sentences = []

    for line in lines:
        add = line.replace(",", " ").replace("-", " ").replace("--", " ").replace(":", " ").replace(";", " ").split(" ")

        while "" in add:
            add.remove("")

        if add != "":
            list_sentences.append(add)

    return build_semantic_descriptors(list_sentences)

def most_similar_word(word, choices, semantic_descriptors, similarity_fn):
    '''This function takes in a string word, a list of strings choices, and a dictionary semantic_descriptors
    which is built according to the requirements for build_semantic_descriptors, and returns the element
    of choices which has the largest semantic similarity to word, with the semantic similarity computed using
    the data in semantic_descriptors and the similarity function similarity_fn. The similarity function is
    a function which takes in two sparse vectors stored as dictionaries and returns a float. An example of such
    a function is cosine_similarity. If the semantic similarity between two words cannot be computed, it is
    considered to be −1. In case of a tie between several elements in choices, the one with the smallest index
    in choices should be returned (e.g., if there is a tie between choices[5] and choices[7], choices[5] is
    returned).'''
    max_similarity = -1
    similarity_list = []

    keys = list(semantic_descriptors.keys())

    if word not in keys:
        return choices[0]

    if word in choices:
        return word

    for j in range(len(choices)):
        if choices[j] not in keys:
            similarity = -1
            similarity_list.append(similarity)
            continue

        similarity = similarity_fn(semantic_descriptors[word], semantic_descriptors[choices[j]])
        similarity_list.append(similarity)
        max_similarity = max(max_similarity, similarity)

    i = similarity_list.index(max_similarity)
    if i != -1:
        return choices[i]
    else:
        return choices[0]

def run_similarity_test(filename, semantic_descriptors, similarity_fn):
    '''This function takes in a string filename which is the name of a file in the same format as test.txt, and
    returns the percentage (i.e., float between 0.0 and 100.0) of questions on which most_similar_word()
    guesses the answer correctly using the semantic descriptors stored in semantic_descriptors, using the
    similarity function similarity_fn.
    The format of test.txt is as follows. On each line, we are given a word (all-lowercase), the correct
    answer, and the choices. For example, the line:'''
    correct_answers = 0
    f = open(filename)
    lines = f.readlines()
    for i in range(len(lines)):
        words = lines[i].split(" ")
        word = words[0]
        choices = []
        for j in range(2, len(words)):
            choices.append(words[j].strip())
        correct_answer = words[1]

        if most_similar_word(word, choices, semantic_descriptors, similarity_fn) == correct_answer:
            correct_answers += 1

    return (correct_answers/len(lines))*100


if __name__ == "__main__":

    build_semantic_descriptors_from_files(["War_and_Peace.txt"])

