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

from dialectid import utils


def test_countries():
    """Test countries"""

    es = utils.COUNTRIES['es']
    assert 'es' in es and 'mx' in es
    en = utils.COUNTRIES['en']
    assert 'us' in en and 'zw' in en
    ar = utils.COUNTRIES['ar']
    assert 'ye' in ar and 'so' in ar
    de = utils.COUNTRIES['de']
    assert 'de' in de and 'ch' in de
    for lang in ['ca', 'hi', 'in',
                 'it', 'ja', 'ko',
                 'pl', 'tl']:
        assert lang in utils.COUNTRIES
        _ = utils.COUNTRIES[lang]
        assert len(_) == 1
    pt = utils.COUNTRIES['pt']
    assert 'br' in pt and 'pt' in pt
    ru = utils.COUNTRIES['ru']
    assert 'ru' in ru and 'kz' in ru
    tr = utils.COUNTRIES['tr']
    assert 'cy' in tr
    zh = utils.COUNTRIES['zh']
    assert 'cn' in zh and 'tw' in zh
    for k, v in utils.COUNTRIES.items():
        assert len(k) == 2
        for i in v:
            assert len(i) == 2

def test_load_bow():
    """Test load_bow"""

    from microtc.utils import Counter

    c = utils.load_bow()
    assert isinstance(c['counter'], Counter)
    c2 = utils.load_bow(loc='mx')
    assert c['counter'].most_common(n=1)[0][1] != c2['counter'].most_common(n=1)[0][1]


def test_BOW():
    """Test BOW"""
    import importlib

    BOW = utils.BOW
    for lang in ['ar', 'de', 'en',
                 'es', 'fr', 'nl',
                 'pt', 'ru', 'tr', 'zh']:
        assert lang in BOW
        path = BOW[lang].split('.')
        module = '.'.join(path[:-1])
        text_repr = importlib.import_module(module)
        instance = getattr(text_repr, path[-1])


def test_load_dialectid():
    """Test dialectid"""

    from EvoMSA.utils import Linear
    from dialectid.utils import COUNTRIES
    models = utils.load_dialectid('es', 15)
    assert len(models) == 20
    assert isinstance(models[0], Linear)
    for model, cntry in zip(models, COUNTRIES['es']):
        assert model.labels[-1] == cntry


