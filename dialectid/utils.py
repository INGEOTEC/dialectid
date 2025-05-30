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


BASEURL = 'https://github.com/INGEOTEC/dialectid/releases/download/data'

COUNTRIES = {'es':['mx', 'cl', 'es', # Mexico (MX), Chile (CL), Spain (ES)
                   'ar', 'co', 'pe', # Argentina (AR), Colombia (CO), Peru (PE)
                   've', 'do', 'py', # Venezuela (VE), Dominican Republic (DO), Paraguay (PY)
                   'ec', 'uy', 'cr', # Ecuador (EC), Uruguay (UY), Costa Rica (CR)
                   'sv', 'pa', 'gt', # El Salvador (SV), Panama (PA), Guatemala (GT)
                   'hn', 'ni', 'bo', # Honduras (HN), Nicaragua (NI), Bolivia (BO)
                   'cu', 'gq', 'pr'  # Cuba (CU), Equatorial Guinea, Puerto Rico (PR)
             ],
             'en':['ai', 'ag', 'au', # Anguilla, Antigua and Barbuda, Australia
                   'bs', 'bb', 'bz', # Bahamas, Barbados, Belize
                   'bm', 'vg', 'cm', # Bermuda, British Virgin Islands, Cameroon
                   'ca', 'ky', 'ck', # Canada, Cayman Islands, Cook Islands
                   'dm', 'sz', 'fk', # Dominica, Eswatini, Falkland Islands
                   'fj', 'gm', 'gh', # Fiji, Gambia, Ghana
                   'gi', 'gd', 'gu', # Gibraltar, Grenada, Guam
                   'gg', 'gy', 'in', # Guernsey, Guyana, India
                   'ie', 'im', 'jm', # Ireland, Isle of Man, Jamaica
                   'ke', 'ls', 'lr', # Kenya, Lesotho, Liberia
                   'mw', 'mt', 'mu', # Malawi, Malta, Mauritius
                   'fm', 'na', 'nz', # Micronesia, Namibia, New Zealand
                   'ng', 'mp', 'pk', # Nigeria, Northern Mariana Islands, Pakistan
                   'pw', 'pg', 'ph', # Palau, Papua New Guinea, Philippines
                   'rw', 'sh', 'kn', # Rwanda, Saint Helena, Ascension, and Tristan da Cunha, Saint Kitts and Nevis
                   'lc', 'vc', 'sl', # Saint Lucia, Saint  Vincent and the Grenadines, Sierra Leone
                   'sg', 'sx', 'sb', # Singapore, Sint Maarten, Solomon Islands
                   'za', 'sd', 'to', # South Africa, Sudan, Tonga
                   'tt', 'tc', 'ug', # Trinidad y Tobago, Turks and Caicos Islands, Uganda
                   'gb', 'us', 'vu', # United Kingdom, United States, Vanuatu
                   'vi', 'zm', 'zw',  # Virgin Islands (US), Zambia, Zimbabwe
                   'pr'              # Puerto Rico (PR)
             ],
             'ar':['dz', 'bh', 'td', # Algeria, Bahrain, Chad
                   'dj', 'eg', 'iq', # Djibouti, Egypt, Iraq
                   'jo', 'kw', 'lb', # Jordan, Kuwait, Lebanon,
                   'ly', 'mr', 'ma', # Libya, Mauritania, Morocco
                   'om', 'qa', 'sa', # Oman, Qatar, Saudi Arabia
                   'so', 'sd', 'sy', # Somalia, Sudan, Syria
                   'tn', 'ae', 'ye' # Tunisia, United Arab Emirates, Yemen
             ],
             'ca':['es'], # Spain
             'de':['at', 'de', 'ch'], # Austria, Germany, Switzerland
             'fr':['be', 'bj', 'bf', # Belgium, Benin, Burkina Faso
                   'cm', 'ca', 'cf', # Cameroon, Canada, Central African Republic
                   'td', 'km', 'cd', # Chad, Comoros, Congo (Republic)
                   'cg', 'ci', 'dj', # Congo, Cote d'lvoire, Djibouti
                   'fr', 'pf', 'ga', # France, French Polynesia, Gabon
                   'gn', 'ht', 'lu', # Guinea, Haiti, Luxembourg
                   'ml', 'mc', 'nc', # Mali, Monaco, New Caledonia
                   'ne', 'rw', 'sn', # Niger, Rwanda, Senegal
                   'ch', 'tg' # Switzerland, Togo
             ],
             'hi':['in'], # India
             'in':['id'], # Indonesia
             'it':['it'], # Italy
             'ja':['jp'], # Japan
             'ko':['kr'], # Korea
             'nl':['be', 'nl'], # Belgium, Netherlands
             'pl':['pl'], # Poland
             'pt':['ao', 'br', 'cv', # Angola, Brazil, Cabo Verde
                   'mz', 'pt' # Mozambique, Portugal 
             ],
             'ru':['by', 'kz', 'kg', # Belarus, Kazakhstan, Kyrgyzstan
                   'ru' # Russian
             ],
             'tl':['ph'], # Philippines
             'tr':['cy', 'tr'], # Cyprus, Turkey
             'zh':['cn', 'sg', 'hk', # China, Singapore, Hong Kong
                   'tw' # Taiwan
             ]
            }