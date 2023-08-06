#!/usr/bin/env python3


import nltk
try:
    from nltk.corpus import wordnet as wn
    from nltk import sent_tokenize, word_tokenize
except ImportError:
    nltk.download("wordnet")
    nltk.download("punkt")  # tokenizer
    nltk.download('averaged_perceptron_tagger')
    from nltk.corpus import wordnet as wn
    from nltk import sent_tokenize, word_tokenize



convert = {"j": "a",
           "n": "n",
           "r": "r",
           "v": "v"
}



def vagueify(text):
    """
    Create a vague version of a sentence?
    """
    # make list of words
    sents = sent_tokenize(text)
    out = []
    for sent in sents:
        words = word_tokenize(sent)
        for word_tag in nltk.pos_tag(words):
            out.append(word_tag)
    result = []
    # iterate over the pos tagged words
    for word, tag in out:
        # get the wordnet letter for lemmatising
        letter = tag.lower()[0]
        wntag = convert.get(letter)
        # do lemmatisation
        lemma = wn.morphy(word, wntag)
        # get this word's synsets if possible
        forms = wn.synsets(word, pos=wntag)
        if forms:
            # get hypernyms
            hyps = forms[0].hypernyms()
            if hyps:
                # try to do correct capisalisation!
                title_case = word.istitle()
                # get the text of the hypernym and turn underscore into space
                word = hyps[-1].lemma_names('eng')[0].replace("_", " ")
                if title_case:
                    word = word.title()
                # attempt pluralisation and 3rd-person-singular
                if tag.endswith("S"):
                    word += "s"
        result.append(word)
    return " ".join(result)


if __name__ == "__main__":

    import argparse
    parser = argparse.ArgumentParser(description="Make text vague")
    parser.add_argument("-i", "--input", type=str, required=True, help="Input file path")
    parser.add_argument("-o", "--output", type=str, help="Output file path")
    args = parser.parse_args()

    with open(args.input, "r") as fo:
        data = fo.read()

    print(f"Original:\n\n{data}")

    result = vagueify(data)

    print(f"\n\nVague:\n\n{result}\n\n")

    outfile = args.output
    if not outfile:
        outfile = "results.txt"
    with open(outfile, "a") as fo:
        fo.write(result + "\n")

