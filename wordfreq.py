from itertools import groupby
from operator import itemgetter

import click
import nltk

import sys


IGNORED_TAGS = {
    ',',                        # Punctuation
    '.',                        # Sentence terminators
    '(', ')',                   # Parentheses
    '``', "''",                 # Quotation marks
    'IN',                       # Prespositions or conjunctions
    'DT',                       # Determiners
    'CC',                       # Conjunctions
    'WP',                       # 'Wh' pronouns
    'WDT',                      # 'Wh' determiners
    'WRB',                      # 'Wh' adverbs
    'PRP',                      # Personal pronouns
    'PRP$',                     # Possessive pronouns
    'MD',                       # Modal auxiliaries
    'CD',                       # Cardinal numbers
    'TO',                       # Preposition or infinitive marker
    'RP',                       # Particles
    'POS',                      # Genitive markers
}

IGNORED_WORDS = {
    'be',
    '–',                        # En-dash
}

KNOWN_TYPES = {
    # Nouns
    'NNS': 'n', 'NNP': 'n', 'NNPS': 'n', 'NN': 'n',

    # Verbs
    'VB': 'v', 'VBD': 'v', 'VBG': 'v', 'VBN': 'v', 'VBP': 'v', 'VBZ': 'v',

    # Adjectives
    'JJ': 'a', 'JJR': 'a', 'JJS': 'a',

    # Adverbs
    'RB': 'r', 'RBR': 'r', 'RBS': 'r',
}


@click.command()
@click.option('--maxwords', type=int, default=5)
@click.argument('infile', type=click.File('r'))
def wordfreq(infile, maxwords):
    lemmatizer = nltk.WordNetLemmatizer()
    tokens = nltk.pos_tag(nltk.word_tokenize(infile.read()))
    new_tags = set()
    count = dict()

    for word, tag in tokens:
        if tag in IGNORED_TAGS:
            continue
        if tag in KNOWN_TYPES:
            word = lemmatizer.lemmatize(word.lower(), KNOWN_TYPES[tag])
            if word in IGNORED_WORDS:
                continue
            count[word] = count.get(word, 0) + 1
        elif tag not in new_tags:
            print(f"Unknown tag discovered: {tag}")
            nltk.help.upenn_tagset(tag)
            new_tags.add(tag)

    total = sum(count.values())
    print(f"{total} significant words found, {len(count)} unique")

    output = sorted(count.items(), key=itemgetter(1), reverse=True)
    output = groupby(output, key=itemgetter(1))
    for num, words in output:
        words = list(w for w, _ in words)
        displwords = ', '.join(words[:maxwords])
        extrawords = max(len(words) - maxwords, 0)
        percentage = num / total * 100
        if extrawords == 0:
            print(f"{percentage:5.1f}% - {num: 3} - {displwords}")
        else:
            print(f"{percentage:5.1f}% - {num: 3} - {displwords} and {extrawords} others")


if __name__ == '__main__':
    wordfreq()
