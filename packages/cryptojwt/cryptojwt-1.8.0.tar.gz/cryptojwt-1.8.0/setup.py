# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['cryptojwt',
 'cryptojwt.jwe',
 'cryptojwt.jwk',
 'cryptojwt.jws',
 'cryptojwt.serialize',
 'cryptojwt.tools']

package_data = \
{'': ['*']}

install_requires = \
['cryptography>=3.4.6', 'requests>=2.25.1,<3.0.0']

entry_points = \
{'console_scripts': ['jwkconv = cryptojwt.tools.keyconv:main',
                     'jwkgen = cryptojwt.tools.keygen:main',
                     'jwtpeek = cryptojwt.tools.jwtpeek:main']}

setup_kwargs = {
    'name': 'cryptojwt',
    'version': '1.8.0',
    'description': 'Python implementation of JWT, JWE, JWS and JWK',
    'long_description': '# cryptojwt\n\n![License](https://img.shields.io/badge/license-Apache%202-blue.svg)\n![Python version](https://img.shields.io/badge/python-3.6%20%7C%203.7%7C%203.8%20%7C%203.9%20%7C%203.10-blue.svg)\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n\nAn implementation of the JSON cryptographic specs JWS, JWE, JWK, and JWA [RFC 7515-7518] and JSON Web Token (JWT) [RFC 7519]\n\nPlease read the [Official Documentation](https://cryptojwt.readthedocs.io/en/latest/) for getting usage examples and further informations.\n',
    'author': 'Roland Hedberg',
    'author_email': 'roland@catalogix.se',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/IdentityPython/JWTConnect-Python-CryptoJWT',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6.2,<4.0.0',
}


setup(**setup_kwargs)
