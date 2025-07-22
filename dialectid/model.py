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
from os.path import isfile, dirname, join
import gzip
import json
import numpy as np
from scipy.special import expit
from sklearn.svm import LinearSVC
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import Normalizer
from sklearn.model_selection import StratifiedKFold
from sklearn.pipeline import make_pipeline
from sklearn.utils.extmath import softmax
from encexp import EncExpT, TextModel
from encexp.download import download
from dialectid.utils import BASEURL
MODELS = join(dirname(__file__), 'models')


class BoW(TextModel):
    def download(self, first: bool=True):
        """download"""
        return download(self.identifier, first=first,
                        base_url=BASEURL,
                        outputdir=MODELS)


@dataclass
class DialectId(EncExpT):
    """DialectId"""
    token_max_filter: int=int(2**19)
    del_diac: bool=True
    with_intercept: bool=True
    probability: bool=False
    uniform_distribution: bool=True

    def identifier_filter(self, key, value):
        """Test default parameters"""
        if key == 'probability':
            return True
        return super().identifier_filter(key, value)

    @property
    def seqTM(self):
        """SeqTM"""
        try:
            return self._seqTM
        except AttributeError:
            _ = BoW(lang=self.lang,
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
        if res.ndim == 1:
            expit(res, out=res)
            return np.c_[1 - res, res]
        return softmax(res)
    
    def decision_function(self, texts: list):
        """Decision function"""
        X = self.transform(texts)
        if X.shape[1] == 1:
            X = np.c_[-X[:, 0], X[:, 0]]
        return X

    def predict(self, texts: list):
        """predict"""
        if self.probability:
            X = self.predict_proba(texts)
        else:
            X = self.decision_function(texts)
        return self.names[X.argmax(axis=1)]

    def download(self, first: bool=True):
        """download"""
        return download(self.identifier, first=first,
                        base_url=BASEURL,
                        outputdir=MODELS)

    @property
    def proba_coefs(self):
        """Probability coefs"""
        return self._proba_coefs

    @proba_coefs.setter
    def proba_coefs(self, value):
        self._proba_coefs = value

    @property
    def countries(self):
        """Countries"""
        try:
            return self.names
        except AttributeError:
            self.weights
        return self.names

    def set_weights(self, data: Iterable):
        # if not self.probability:
        #     return super().set_weights(data)
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
        if inter.shape[0] > 1:
            coef.shape = (inter.shape[0], inter.shape[0])
        self.proba_coefs = (np.asanyarray(coef, dtype=self.precision),
                            np.asanyarray(inter, dtype=self.precision))

    def tailored(self, D: Iterable=None, filename: str=None,
                 tsv_filename: str=None, min_pos: int=32,
                 max_pos: int=int(2**21), n_jobs: int=-1,
                 self_supervised: bool=False, ds: object=None,
                 train: object=None, Dprob: list=None):
        kwargs = dict(filename=filename, tsv_filename=tsv_filename,
                      min_pos=min_pos, max_pos=max_pos, n_jobs=n_jobs,
                      self_supervised=self_supervised, ds=ds, train=train)
        if filename is not None:
            filename = filename.split('.json.gz')[0]
        else:
            filename = self.identifier
        if isfile(f'{filename}.json.gz'):
            return super().tailored(D=D, **kwargs)
        super().tailored(D=D, **kwargs)
        _, nrows = self.weights.shape
        if Dprob is None:
            Dprob = D
        X = self.seqTM.transform(Dprob)
        df = np.empty((X.shape[0], nrows))        
        y = np.array([x['klass'] for x in Dprob])
        for tr, vs in StratifiedKFold(n_splits=3).split(X, y):
            m = LinearSVC(class_weight='balanced').fit(X[tr], y[tr])
            _ = m.decision_function(X[vs])
            if _.ndim == 1:
                _ = np.c_[_]
            df[vs] = _
        model = make_pipeline(Normalizer(),
                              LogisticRegression(class_weight='balanced')).fit(df, y)
        lr = model[1]
        self._lr = model
        if lr.coef_.shape[0] == 1:
            self.proba_coefs = (lr.coef_[0], lr.intercept_)
        else:
            self.proba_coefs = (lr.coef_.T, lr.intercept_)

        with gzip.open(f'{filename}.json.gz', 'ab') as fpt:
            coef, intercept = self.proba_coefs
            data = dict(proba_coef=coef.astype(np.float32).tobytes().hex(),
                        proba_intercept=intercept.astype(np.float32).tobytes().hex())
            fpt.write(bytes(json.dumps(data) + '\n',
                      encoding='utf-8'))
