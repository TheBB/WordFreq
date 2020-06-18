# MIT License
#
# Copyright (c) 2020 Eivind Fonn
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.


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
    ':',                        # Colon or ellipsis
    '#',                        # ?
    'EX',                       # Existential 'there'
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
    'SYM',                      # Symbols
    'PDT',                      # Pre-determiner
}

IGNORED_WORDS = {
    '–',                        # En-dash
    "’", "‘",                   # Single quotation marks
    '“', '”',                   # Double quotation marks
    '+', '/', '>',
    's', "'s", "n't",
    "½",

    'be', 'i', 'do', 'have', 'not', 'so', 'more', 'also', 'make',
    'thing', 'get', 'something', 'day', 'really', 'way', 'well',
    'see', 'find', 'very', 'take', 'want', 'e.g', 'always', 'as',
    'start', 'bit', 'already', 'put', 'lot', 'then', 'most', 'come',
    'stay', 'everyday', 'hi', 'just', 'sloth', 'my', 'often',
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

    # Foreign words
    'FW': 'n',
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
            while word[0] in ("'", '-'):
                word = word[1:]
            if word in IGNORED_WORDS or len(word) < 2:
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
        total_percentage = num * len(words) / total * 100
        if extrawords == 0:
            print(f"{percentage:5.2f}% - {total_percentage:5.2f}% - {num: 4} - {displwords}")
        else:
            print(f"{percentage:5.2f}% - {total_percentage:5.2f}% - {num: 4} - {displwords} and {extrawords} others")


if __name__ == '__main__':
    wordfreq()
