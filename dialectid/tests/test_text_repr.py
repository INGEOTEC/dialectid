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


from dialectid.text_repr import BoW
import numpy as np


def test_bow():
    """Test BoW"""
    from b4msa.textmodel import TextModel

    bow = BoW(lang='es', voc_size_exponent=13)
    assert isinstance(bow.bow, TextModel)
    X = bow.transform(['Buenos dias'])
    bow2 = BoW(lang='es', loc='mx', voc_size_exponent=13)
    X2 = bow2.transform(['Buenos dias'])
    assert (X - X2).sum() != 0


def test_subwords():
    """Test subwords"""

    bow = BoW(lang='es', voc_size_exponent=13,
              subwords=True)
    bow.transform(['Hola'])
    