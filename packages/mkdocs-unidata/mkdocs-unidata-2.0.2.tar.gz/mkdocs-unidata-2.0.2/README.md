[![Travis][travis-image]][travis-link]
[![Codacy][codacy-image]][codacy-link]
[![PyPI][pypi-image]][pypi-link]


  [travis-image]: https://travis-ci.org/mjames-upc/mkdocs-unidata.svg?branch=master
  [travis-link]: https://travis-ci.org/mjames-upc/mkdocs-unidata
  [codacy-image]: https://api.codacy.com/project/badge/Grade/1e6e1042cc0d43c98dc42847ef3b428a
  [codacy-link]: https://www.codacy.com/app/mjames/mkdocs-unidata?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=mjames/mkdocs-unidata&amp;utm_campaign=Badge_Grade
  [pypi-image]: https://img.shields.io/pypi/v/mkdocs-unidata.svg
  [pypi-link]: https://pypi.python.org/pypi/mkdocs-unidata

# Custom Material Theme for MkDocs

A custom Material Design theme for [MkDocs][1].

[![Material for MkDocs](docs/images/material.png)][2]

  [1]: http://www.mkdocs.org
  [2]: http://mjames-upc.github.io/mkdocs-unidata/

## Quick start

Install the latest version of Material with `pip`:

``` sh
pip install mkdocs-unidata
```

Append the following line to your project's `mkdocs.yml`:

``` yaml
theme: 'unidata'
```

``` sh
conda env create -f environment.yml
source activate mkdocs-unidata
```

``` sh
mkdocs serve
```

## What to expect

* Responsive design and fluid layout for all kinds of screens and devices,
  designed to serve your project documentation in a user-friendly way with
  optimal readability.

* Easily customizable primary and accent color, fonts, favicon and logo;
  straight forward localization through theme extension; integrated with Google
  Analytics, Disqus and GitHub.

* Well-designed search interface accessible through hotkeys (<kbd>F</kbd> or
  <kbd>S</kbd>), intelligent grouping of search results, search term
  highlighting and lazy loading.

For detailed installation instructions and a demo, visit
http://mjames-upc.github.io/mkdocs-unidata/

## License

**MIT License**

Copyright (c) 2016-2017 Martin Donath

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to
deal in the Software without restriction, including without limitation the
rights to use, copy, modify, merge, publish, distribute, sublicense, and/or
sell copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NON-INFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS
IN THE SOFTWARE.
