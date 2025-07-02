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
from numpy.testing import assert_almost_equal
from sklearn.preprocessing import Normalizer
from microtc.utils import tweet_iterator
from dialectid.model import DialectId
from encexp.utils import load_dataset
import os


def test_DialectId_identifier():
    """Test DialectId identifier"""
    dialectid = DialectId(lang='es')
    assert dialectid.identifier == 'DialectId_c69aaba0f1b0783f273f85de6f599132'
    dialectid = DialectId(lang='es', distance=True)
    assert dialectid.identifier == 'DialectId_c69aaba0f1b0783f273f85de6f599132'


def test_DialectId_predict():
    """Test DialectId predict"""
    X, y = load_dataset(['mx', 'ar', 'es'], return_X_y=True)
    D = [dict(text=text, klass=klass) for text, klass in zip(X, y)]
    enc = DialectId(lang='es', pretrained=False)
    enc.tailored(D, tsv_filename='tailored.tsv',
                 min_pos=32,
                 filename='tailored_intercept.json.gz',
                 self_supervised=False)
    hy = enc.predict(['comiendo unos tacos'])
    assert hy[0] in ('mx', 'ar', 'es')
    os.unlink('tailored_intercept.json.gz')
    os.unlink('tailored.tsv')


def test_DialectId_predict_2cl():
    """Test DialectId predict"""
    X, y = load_dataset(['mx', 'ar'], return_X_y=True)
    D = [dict(text=text, klass=klass) for text, klass in zip(X, y)]
    enc = DialectId(lang='es', pretrained=False)
    enc.tailored(D, tsv_filename='tailored.tsv',
                 min_pos=32,
                 filename='tailored_intercept.json.gz',
                 self_supervised=False)
    X = enc.transform(['comiendo unos tacos'])
    assert X.shape[1] == 1
    hy = enc.predict(['comiendo unos tacos'])
    assert hy[0] in ('mx', 'ar')
    os.unlink('tailored_intercept.json.gz')
    os.unlink('tailored.tsv')    


def test_DialectId_download():
    """Test DialectId download"""
    dialectid = DialectId(lang='es', token_max_filter=2**17)
    dialectid.weights
    assert len(dialectid.names) == 21


def test_DialectId_probability():
    """Test DialectId predict"""
    X, y = load_dataset(['mx', 'ar', 'es'], return_X_y=True)
    D = [dict(text=text, klass=klass) for text, klass in zip(X, y)]
    enc = DialectId(lang='es',
                    pretrained=False,
                    probability=True)
    enc.tailored(D,
                 tsv_filename='tailored.tsv',
                 min_pos=32,
                 filename='tailored_intercept2.json.gz',
                 self_supervised=False)
    X = enc.transform(['comiendo unos tacos', 'pibe'])
    hy = enc.predict_proba(['comiendo unos tacos', 'pibe'])
    _ = enc._lr.predict_proba(X)
    assert_almost_equal(_, hy)
    enc2 = DialectId(lang='es',
                    pretrained=False,
                    probability=True)
    enc2.set_weights(tweet_iterator('tailored_intercept2.json.gz'))
    assert_almost_equal(enc._lr[1].coef_.T, enc2.proba_coefs[0])
    assert_almost_equal(enc._lr[1].intercept_, enc2.proba_coefs[1])
    hy2 = enc2.predict_proba(['comiendo unos tacos', 'pibe'])
    assert_almost_equal(hy, hy2)
    os.unlink('tailored_intercept2.json.gz')
    os.unlink('tailored.tsv')


def test_DialectId_probability_2cl():
    """Test DialectId predict"""
    X, y = load_dataset(['mx', 'ar'], return_X_y=True)
    D = [dict(text=text, klass=klass) for text, klass in zip(X, y)]
    enc = DialectId(lang='es',
                    pretrained=False,
                    probability=True)
    enc.tailored(D,
                 tsv_filename='tailored.tsv',
                 min_pos=32,
                 filename='tailored_intercept2.json.gz',
                 self_supervised=False)
    X = enc.transform(['comiendo unos tacos', 'pibe'])
    hy = enc.predict_proba(['comiendo unos tacos', 'pibe'])
    _ = enc._lr.predict_proba(X)
    assert_almost_equal(_, hy)    
    assert_almost_equal(hy[0].sum(), 1)
    enc2 = DialectId(lang='es',
                    pretrained=False,
                    probability=True)
    enc2.set_weights(tweet_iterator('tailored_intercept2.json.gz'))
    assert_almost_equal(enc._lr[1].coef_[0], enc2.proba_coefs[0])
    assert_almost_equal(enc._lr[1].intercept_, enc2.proba_coefs[1])
    hy2 = enc2.predict_proba(['comiendo unos tacos', 'pibe'])
    assert_almost_equal(hy, hy2)
    os.unlink('tailored_intercept2.json.gz')
    os.unlink('tailored.tsv')


def test_DialectId_model():
    """Test DialectID"""

    dial = DialectId(lang='es')
    assert len(dial.countries) == 21
    dial.predict(['comiendo unos tacos'])
