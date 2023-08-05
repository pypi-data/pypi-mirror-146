# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['hpke']

package_data = \
{'': ['*']}

install_requires = \
['cryptography>=3.4.7,<4.0.0']

setup_kwargs = {
    'name': 'hpke',
    'version': '0.1.1',
    'description': 'HPKE implementation',
    'long_description': '# hpke.py\n\n![CI status](https://github.com/ctz/hpke-py/actions/workflows/ci.yaml/badge.svg)\n\nThis is an implementation of [RFC9180](https://datatracker.ietf.org/doc/rfc9180/) in python3, using\n[cryptography.io](https://cryptography.io) for the underlying cryptography.\n\n## Features\n\n - Modes\n   - [x] mode_base\n   - [ ] mode_psk\n   - [ ] mode_auth\n   - [ ] mode_auth_psk\n - AEADs\n   - [x] AES-128-GCM\n   - [x] AES-256-GCM\n   - [ ] ChaCha20Poly1305\n   - [x] Export only\n - KEMs\n   - [x] DHKEM(P-256, HKDF-SHA256)\n   - [ ] DHKEM(P-384, HKDF-SHA384)\n   - [x] DHKEM(P-521, HKDF-SHA512)\n   - [ ] DHKEM(X25519, HKDF-SHA256)\n   - [ ] DHKEM(X448, HKDF-SHA512)\n - KDFs\n   - [x] HKDF-SHA256\n   - [x] HKDF-SHA384\n   - [x] HKDF-SHA512\n\n## Author\nJoseph Birr-Pixton <jpixton@gmail.com>\n\n## License\nhpke.py is licensed under the Apache License, Version 2.0. See\n[LICENSE](LICENSE) for the full license text.\n',
    'author': 'Joseph Birr-Pixton',
    'author_email': 'jpixton@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/ctz/hpke-py',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
