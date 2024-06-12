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

from EvoMSA import BoW as EvoMSABoW
from EvoMSA.utils import b4msa_params
from b4msa.textmodel import TextModel
from microtc.weighting import TFIDF
from dialectid.utils import load_bow


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
                 **kwargs):
        assert pretrain
        assert not v1
        self._bow = None
        self.loc = loc
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
    def bow(self):
        """BoW"""

        if self._bow is not None:
            return self._bow
        data = load_bow(lang=self.lang,
                        d=self.voc_size_exponent,
                        func=self.voc_selection,
                        loc=self._loc)
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