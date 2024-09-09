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
# https://www.cia.gov/the-world-factbook/about/archives/2021/field/languages/

from typing import Union, List
from dataclasses import dataclass
import importlib
import numpy as np
from dialectid.utils import BOW, load_dialectid, load_seqtm

@dataclass
class DialectId:
    """DialectId"""
    lang: str='es'
    voc_size_exponent: int=15
    subwords: bool=True

    @property
    def bow(self):
        """BoW"""

        try:
            return self._bow
        except AttributeError:
            path = BOW[self.lang].split('.')
            module = '.'.join(path[:-1])
            text_repr = importlib.import_module(module)
            kwargs = {}
            if module != 'EvoMSA.text_repr':
                kwargs = dict(subwords=self.subwords)
            _ = getattr(text_repr, path[-1])(lang=self.lang,
                                             voc_size_exponent=self.voc_size_exponent,
                                             **kwargs)
            self._bow = _
        return self._bow

    @property
    def weights(self):
        """Weights"""
        try:
            return self._weights
        except AttributeError:
            self._weights = load_dialectid(self.lang,
                                           self.voc_size_exponent,
                                           self.subwords)
        return self._weights
    
    @property
    def countries(self):
        """Countries"""
        try:
            return self._countries
        except AttributeError:
            _ = [x.labels[-1] for x in self.weights]
            self._countries = np.array(_)
        return self._countries

    def decision_function(self, D: List[Union[dict, list, str]]) -> np.ndarray:
        """Decision function"""
        if isinstance(D, str):
            D = [D]
        X = self.bow.transform(D)
        hy = [w.decision_function(X) for w in self.weights]
        return np.array(hy).T

    def predict(self, D: List[Union[dict, list, str]]) -> np.ndarray:
        """Prediction"""

        hy = self.decision_function(D)
        return self.countries[hy.argmax(axis=1)]


@dataclass
class DenseBoW:
    """DenseBoW"""

    lang: str='es'
    voc_size_exponent: int=13
    precision: int=32

    def estimator(self, **kwargs):
        """Estimator"""

        from sklearn.svm import LinearSVC
        return LinearSVC(class_weight='balanced')

    @property
    def bow(self):
        """BoW"""

        try:
            return self._bow
        except AttributeError:
            from dialectid.text_repr import SeqTM
            self._bow = SeqTM(language=self.lang,
                              voc_size_exponent=self.voc_size_exponent)
        return self._bow

    @property
    def weights(self):
        """Weights"""
        try:
            return self._weights
        except AttributeError:
            iterator = load_seqtm(self.lang,
                                  self.voc_size_exponent,
                                  self.precision)
            precision = getattr(np, f'float{self.precision}')            
            weights = []
            names = []
            for data in iterator:
                _ = np.frombuffer(bytes.fromhex(data['coef']), dtype=precision)
                weights.append(_)
                names.append(data['labels'][-1])
            self._weights = np.vstack(weights)
            self._names = np.array(names)
        return self._weights

    @property
    def names(self):
        """Vector space components"""

        return self._names    

    def encode(self, text):
        """Encode utterace into a matrix"""

        token2id = self.bow.token2id
        seq = []
        for token in self.bow.tokenize(text):
            try:
                seq.append(token2id[token])
            except KeyError:
                continue
        W = self.weights
        return np.vstack([W[:, x] for x in seq]).T
