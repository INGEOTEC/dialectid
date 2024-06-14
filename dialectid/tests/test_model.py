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


def test_DialectId():
    """Test DialectId"""

    from dialectid.model import DialectId
    from dialectid import BoW

    dialectid = DialectId(voc_size_exponent=15)
    assert dialectid.lang == 'es' and dialectid.voc_size_exponent == 15
    assert isinstance(dialectid.bow, BoW)


def test_DialectId_df():
    """Test DialectId"""

    from dialectid.model import DialectId

    dialectid = DialectId(voc_size_exponent=15)
    hy = dialectid.decision_function('comiendo tacos')
    assert hy.shape == (1, 20)
    assert hy.argmax(axis=1)[0] == 0


def test_countries():
    """Test countries"""

    from dialectid.model import DialectId

    dialectid = DialectId(voc_size_exponent=15)
    assert len(dialectid.countries) == 20
    assert dialectid.countries[0] == 'mx'


def test_predict():
    """Test predict"""

    from dialectid.model import DialectId

    dialectid = DialectId(voc_size_exponent=15)
    countries = dialectid.predict('comiendo tacos')
    assert countries[0] == 'mx'
    countries = dialectid.predict(['comiendo tacos',
                                   'tomando vino'])
    assert countries.shape == (2, )

