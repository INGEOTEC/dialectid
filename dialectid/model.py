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

from typing import Iterable
from dataclasses import dataclass
from collections import defaultdict
from random import shuffle
from os.path import isfile
import gzip
import json
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import Normalizer
from sklearn.utils.extmath import softmax
from encexp import EncExpT, TextModel
from encexp.download import download
from dialectid.utils import BASEURL


@dataclass
class DialectId(EncExpT):
    """DialectId"""
    token_max_filter: int=int(2**19)
    del_diac: bool=True
    with_intercept: bool=True
    probability: bool=False

    @property
    def seqTM(self):
        """SeqTM"""
        try:
            return self._seqTM
        except AttributeError:
            _ = TextModel(lang=self.lang,
                          del_diac=self.del_diac,
                          token_max_filter=self.token_max_filter)
            self.seqTM = _
        return self._seqTM

    @seqTM.setter
    def seqTM(self, value):
        self._seqTM = value

    def predict_proba(self, texts: list):
        """Predict proba"""
        assert self.probability
        X = self.transform(texts)
        norm = Normalizer()
        X = norm.transform(X)
        coef, intercept = self.proba_coefs
        res = X @ coef + intercept
        return softmax(res)

    def predict(self, texts: list):
        """predict"""
        if self.probability:
            X = self.predict_proba(texts)
        else:
            X = self.transform(texts)
        return self.names[X.argmax(axis=1)]

    def download(self, first: bool=True):
        """download"""
        return download(self.identifier, first=first,
                        base_url=BASEURL)
    
    @property
    def proba_coefs(self):
        """Probability coefs"""
        return self._proba_coefs

    @proba_coefs.setter
    def proba_coefs(self, value):
        self._proba_coefs = value

    def set_weights(self, data: Iterable):
        if not self.probability:
            return super().set_weights(data)
        data = list(data)
        super().set_weights([x for x in data if 'coef' in x])
        proba = [x for x in data if 'proba_coef' in x]
        if len(proba) == 0:
            return
        proba = proba[0]
        coef = np.frombuffer(bytearray.fromhex(proba['proba_coef']),
                             dtype=np.float32)
        inter = np.frombuffer(bytearray.fromhex(proba['proba_intercept']),
                              dtype=np.float32)
        coef.shape = (inter.shape[0], inter.shape[0])
        self.proba_coefs = (np.asanyarray(coef, dtype=self.precision),
                            np.asanyarray(inter, dtype=self.precision))
    
    def tailored(self, D: Iterable=None, filename: str=None,
                 tsv_filename: str=None, min_pos: int=32,
                 max_pos: int=int(2**15), n_jobs: int=-1,
                 self_supervised: bool=False, ds: object=None,
                 train: object=None, proba_instances: int=64):
        kwargs = dict(filename=filename, tsv_filename=tsv_filename,
                      min_pos=min_pos, max_pos=max_pos, n_jobs=n_jobs,
                      self_supervised=self_supervised, ds=ds, train=train)
        if not self.probability:
            return super().tailored(D=D, **kwargs)
        if filename is not None:
            filename = filename.split('.json.gz')[0]
        else:
            filename = self.identifier
        if isfile(f'{filename}.json.gz'):
            return super().tailored(D=D, **kwargs)
        data = defaultdict(list)
        for text in D:
            data[text['klass']].append(text)
        for value in data.values():
            shuffle(value)
        D = []
        for value in data.values():
            D.extend(value[proba_instances:])
        super().tailored(D=D, **kwargs)
        D = []
        for value in data.values():
            D.extend(value[:proba_instances])
        X = self.transform(D)
        norm = Normalizer()
        X = norm.transform(X)        
        y = [x['klass'] for x in D]
        lr = LogisticRegression().fit(X, y)
        self._lr = lr
        self.proba_coefs = (lr.coef_.T, lr.intercept_)
        with gzip.open(f'{filename}.json.gz', 'ab') as fpt:
            coef, intercept = self.proba_coefs
            data = dict(proba_coef=coef.astype(np.float32).tobytes().hex(),
                        proba_intercept=intercept.astype(np.float32).tobytes().hex())
            fpt.write(bytes(json.dumps(data) + '\n',
                      encoding='utf-8'))



# from dialectid.utils import BOW, load_dialectid, load_seqtm

# @dataclass
# class DialectId:
#     """DialectId"""
#     lang: str='es'
#     voc_size_exponent: int=15
#     subwords: bool=True

#     @property
#     def bow(self):
#         """BoW"""

#         try:
#             return self._bow
#         except AttributeError:
#             path = BOW[self.lang].split('.')
#             module = '.'.join(path[:-1])
#             text_repr = importlib.import_module(module)
#             kwargs = {}
#             if module != 'EvoMSA.text_repr':
#                 kwargs = dict(subwords=self.subwords)
#             _ = getattr(text_repr, path[-1])(lang=self.lang,
#                                              voc_size_exponent=self.voc_size_exponent,
#                                              **kwargs)
#             self._bow = _
#         return self._bow

#     @property
#     def weights(self):
#         """Weights"""
#         try:
#             return self._weights
#         except AttributeError:
#             self._weights = load_dialectid(self.lang,
#                                            self.voc_size_exponent,
#                                            self.subwords)
#         return self._weights
    
#     @property
#     def countries(self):
#         """Countries"""
#         try:
#             return self._countries
#         except AttributeError:
#             _ = [x.labels[-1] for x in self.weights]
#             self._countries = np.array(_)
#         return self._countries

#     def decision_function(self, D: List[Union[dict, list, str]]) -> np.ndarray:
#         """Decision function"""
#         if isinstance(D, str):
#             D = [D]
#         X = self.bow.transform(D)
#         hy = [w.decision_function(X) for w in self.weights]
#         return np.array(hy).T

#     def predict(self, D: List[Union[dict, list, str]]) -> np.ndarray:
#         """Prediction"""

#         hy = self.decision_function(D)
#         return self.countries[hy.argmax(axis=1)]


# @dataclass
# class DenseBoW:
#     """DenseBoW"""

#     lang: str='es'
#     voc_size_exponent: int=13
#     precision: int=32

#     def estimator(self, **kwargs):
#         """Estimator"""

#         from sklearn.svm import LinearSVC
#         return LinearSVC(class_weight='balanced')

#     @property
#     def bow(self):
#         """BoW"""

#         try:
#             return self._bow
#         except AttributeError:
#             from dialectid.text_repr import SeqTM
#             self._bow = SeqTM(language=self.lang,
#                               voc_size_exponent=self.voc_size_exponent)
#         return self._bow

#     @property
#     def weights(self):
#         """Weights"""
#         try:
#             return self._weights
#         except AttributeError:
#             iterator = load_seqtm(self.lang,
#                                   self.voc_size_exponent,
#                                   self.precision)
#             precision = getattr(np, f'float{self.precision}')            
#             weights = []
#             names = []
#             for data in iterator:
#                 _ = np.frombuffer(bytes.fromhex(data['coef']), dtype=precision)
#                 weights.append(_)
#                 names.append(data['labels'][-1])
#             self._weights = np.vstack(weights)
#             self._names = np.array(names)
#         return self._weights

#     @property
#     def names(self):
#         """Vector space components"""

#         return self._names    

#     def encode(self, text):
#         """Encode utterace into a matrix"""

#         token2id = self.bow.token2id
#         seq = []
#         for token in self.bow.tokenize(text):
#             try:
#                 seq.append(token2id[token])
#             except KeyError:
#                 continue
#         W = self.weights
#         if len(seq) == 0:
#             dtype = getattr(np, f'float{self.precision}') 
#             return np.ones((W.shape[0], 1), dtype=dtype)
#         return np.vstack([W[:, x] for x in seq]).T
