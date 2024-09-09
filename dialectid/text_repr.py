# MIT License

# Copyright (c) 2024 Eric Sadit Tellez Avila, Daniela Alejandra Moctezuma Ochoa, Luis Guillermo Ruiz Velazquez, Mario Graff Guerrero

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from collections import OrderedDict
from os.path import join, dirname
from EvoMSA import BoW as EvoMSABoW
from b4msa.textmodel import TextModel
from microtc.weighting import TFIDF
from microtc import emoticons
from microtc.utils import tweet_iterator
from dialectid.utils import load_bow
import numpy as np


class BoW(EvoMSABoW):
    """BoW
    
    >>> from dialectid import BoW
    >>> bow = BoW(lang='es')
    >>> bow.transform(['Buenos dias', 'Disfruta dialectid'])
    """

    def __init__(self, pretrain: bool=True,
                 v1: bool=False,
                 estimator_kwargs: dict=None,
                 loc: str=None,
                 subwords: bool=False,
                 **kwargs):
        assert pretrain
        assert not v1
        self._bow = None
        if subwords:
            assert loc is None
            loc = 'qgrams'
        self.loc = loc
        self.subwords = subwords
        if estimator_kwargs is None:
            estimator_kwargs = {'dual': True, 'class_weight': 'balanced'}
        super().__init__(pretrain=pretrain,
                         estimator_kwargs=estimator_kwargs,
                         v1=v1, **kwargs)

    @property
    def loc(self):
        """Location/Country"""
        return self._loc

    @loc.setter
    def loc(self, value):
        self._loc = value

    @property
    def subwords(self):
        """Whether to use subwords"""
        return self._subwords

    @subwords.setter
    def subwords(self, value):
        self._subwords = value

    @property
    def bow(self):
        """BoW"""

        if self._bow is not None:
            return self._bow
        data = load_bow(lang=self.lang,
                        d=self.voc_size_exponent,
                        func=self.voc_selection,
                        loc=self.loc)
        params = data['params']
        counter = data['counter']
        params.update(self.b4msa_kwargs)
        bow = TextModel(**params)
        tfidf = TFIDF()
        tfidf.N = counter.update_calls
        tfidf.word2id, tfidf.wordWeight = tfidf.counter2weight(counter)
        bow.model = tfidf
        self._bow = bow
        return bow


class SeqTM(TextModel):
    """TextModel where the utterance is segmented in a sequence."""

    def __init__(self, language='es',
                 voc_size_exponent: int=17,
                 voc_selection: str='most_common',
                 loc: str=None, subwords: bool=True,
                 sequence: bool=True, lang=None, **kwargs):
        assert lang is None
        if sequence and subwords:
            loc = 'seq'
        elif subwords:
            assert loc is None
            loc = 'qgrams'
        self._map = {}
        data = load_bow(lang=language,
                        d=voc_size_exponent,
                        func=voc_selection,
                        loc=loc)
        params = data['params']
        counter = data['counter']
        params.update(kwargs)
        super().__init__(**params)
        self.language = language
        self.voc_size_exponent = voc_size_exponent
        self.voc_selection = voc_selection
        self.loc = loc
        self.subwords = subwords
        self.sequence = sequence
        self.__vocabulary(counter)

    def __vocabulary(self, counter):
        """Vocabulary"""

        tfidf = TFIDF()
        tfidf.N = counter.update_calls
        tfidf.word2id, tfidf.wordWeight = tfidf.counter2weight(counter)
        self.model = tfidf
        tokens = self.tokens
        for value in tfidf.word2id:
            key = value
            if value[:2] == 'q:':
                key = value[2:]
                if key in self._map:
                    continue
                self._map[key] = value
            else:
                key = f'~{key}~'
                self._map[key] = value
            tokens[key] = value
        _ = join(dirname(__file__), 'data', 'emojis.json.gz')
        emojis = next(tweet_iterator(_))
        for k, v in emojis.items():
            self._map[k] = v
            tokens[k] = v
            for x in [f'~{k}~', f'~{k}', f'{k}~']:
                self._map[x] = v
                tokens[x] = v

    @property
    def language(self):
        """Language of the pre-trained text representations"""

        return self._language

    @language.setter
    def language(self, value):
        self._language = value

    @property
    def voc_selection(self):
        """Method used to select the vocabulary"""

        return self._voc_selection

    @voc_selection.setter
    def voc_selection(self, value):
        self._voc_selection = value

    @property
    def voc_size_exponent(self):
        """Vocabulary size :math:`2^v`; where :math:`v` is :py:attr:`voc_size_exponent` """

        return self._voc_size_exponent

    @voc_size_exponent.setter
    def voc_size_exponent(self, value):
        self._voc_size_exponent = value

    @property
    def loc(self):
        """Location/Country"""

        return self._loc

    @loc.setter
    def loc(self, value):
        self._loc = value

    @property
    def subwords(self):
        """Whether to use subwords"""

        return self._subwords

    @subwords.setter
    def subwords(self, value):
        self._subwords = value

    @property
    def sequence(self):
        """Vocabulary compute on sequence text-transformation"""

        return self._sequence
    
    @sequence.setter
    def sequence(self, value):
        self._sequence = value

    @property
    def names(self):
        """Vector space components"""

        try:
            return self._names
        except AttributeError:
            _names = [None] * len(self.id2token)
            for k, v in self.id2token.items():
                _names[k] = v
            self._names = np.array(_names)
            return self._names
        
    @property
    def weights(self):
        """Vector space weights"""

        try:
            return self._weights
        except AttributeError:
            w = [None] * len(self.token_weight)
            for k, v in self.token_weight.items():
                w[k] = v
            self._weights = np.array(w)
            return self._weights

    @property
    def tokens(self):
        """Tokens"""

        try:
            return self._tokens
        except AttributeError:
            self._tokens = OrderedDict()
        return self._tokens

    @property
    def data_structure(self):
        """Datastructure"""

        try:
            return self._data_structure
        except AttributeError:
            _ = emoticons.create_data_structure
            self._data_structure = _(self.tokens)
        return self._data_structure

    def compute_tokens(self, text):
        """
        Labels in a text

        :param text:
        :type text: str
        :returns: The labels in the text
        :rtype: set
        """

        get = self._map.get
        lst = self.find_token(text)
        _ = [text[a:b] for a, b in lst]
        return [[get(x, x) for x in _]]

    def find_token(self, text):
        """Obtain the position of each label in the text

        :param text: text
        :type text: str
        :return: list of pairs, init and end of the word
        :rtype: list
        """

        blocks = []
        init = i = end = 0
        head = self.data_structure
        current = head
        text_length = len(text)
        while i < text_length:
            char = text[i]
            try:
                current = current[char]
                i += 1
                if "__end__" in current:
                    end = i
            except KeyError:
                current = head
                if end > init:
                    blocks.append([init, end])
                    if (end - init) >= 2 and text[end - 1] == '~':
                        init = i = end = end - 1
                    else:
                        init = i = end
                elif i > init:
                    if (i - init) >= 2 and text[i - 1] == '~':
                        init = end = i = i - 1
                    else:
                        init = end = i
                else:
                    init += 1
                    i = end = init
        if end > init:
            blocks.append([init, end])
        return blocks
