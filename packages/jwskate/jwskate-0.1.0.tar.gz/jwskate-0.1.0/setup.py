# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['jwskate',
 'jwskate.jwa',
 'jwskate.jwa.encryption',
 'jwskate.jwa.key_mgmt',
 'jwskate.jwa.signature',
 'jwskate.jwe',
 'jwskate.jwk',
 'jwskate.jws',
 'jwskate.jwt',
 'tests',
 'tests.test_jwk']

package_data = \
{'': ['*']}

install_requires = \
['binapy>=0.5', 'cryptography>=3.4']

setup_kwargs = {
    'name': 'jwskate',
    'version': '0.1.0',
    'description': 'A Pythonic implementation of Json Web Signature, Keys, Algorithms, Tokens and Encryption (RFC7514 to 7519), on top of the `cryptography` module.',
    'long_description': '# JwSkate\n\n\n<p align="center">\n<a href="https://pypi.python.org/pypi/jwskate">\n    <img src="https://img.shields.io/pypi/v/jwskate.svg"\n        alt = "Release Status">\n</a>\n\n<a href="https://github.com/guillp/jwskate/actions">\n    <img src="https://github.com/guillp/jwskate/actions/workflows/main.yml/badge.svg?branch=release" alt="CI Status">\n</a>\n\n<a href="https://jwskate.readthedocs.io/en/latest/?badge=latest">\n    <img src="https://readthedocs.org/projects/jwskate/badge/?version=latest" alt="Documentation Status">\n</a>\n\n</p>\n\n\nA Pythonic implementation of Json Web Signature, Keys, Algorithms, Tokens and Encryption (RFC7514 to 7519), and their\nextensions ECDH Signatures (RFC8037), and JWK Thumbprints (RFC7638).\n\n* Free software: MIT\n* Documentation: <https://guillp.github.io/jwskate/>\n\n\nA quick usage example, generating an RSA private key, signing some data, then validating that signature:\n\n```python\nfrom jwskate import Jwk\n\n# generate a RSA Jwk and sign a plaintext with it\nrsa_private_jwk = Jwk.generate_for_kty("RSA", key_size=2048, kid="my_key")\n\ndata = b"Signing is easy!"\nalg = "RS256"\nsignature = rsa_private_jwk.sign(data, alg)\n\n# extract the public key, and verify the signature with it\nrsa_public_jwk = rsa_private_jwk.public_jwk()\nassert rsa_public_jwk.verify(data, signature, alg)\n\n# let\'s see what a Jwk looks like:\nassert isinstance(rsa_private_jwk, dict)  # Jwk are dict\n\nprint(rsa_private_jwk)\n```\n\nThe result of this print JWK will look like this:\n```\n{ \'kty\': \'RSA\',\n  \'n\': \'...\',\n  \'e\': \'AQAB\',\n  \'d\': \'...\',\n  \'p\': \'...\',\n  \'q\': \'...\',\n  \'dp\': \'...\',\n  \'dq\': \'...\',\n  \'qi\': \'...\',\n  \'kid\': \'my_key\'\n}\n```\n\nNow let\'s sign a JWT containing arbitrary claims:\n\n```python\nfrom jwskate import Jwk, Jwt\n\nprivate_jwk = Jwk.generate_for_kty("EC", kid="my_key")\nclaims = {"sub": "some_sub", "claim1": "value1"}\nsign_alg = "ES256"\n\njwt = Jwt.sign(claims, private_jwk, sign_alg)\n# that\'s it! we have a signed JWT\nassert jwt.claims == claims  # claims can be accessed as a dict\nassert jwt.sub == "some_sub"  # or individual claims can be accessed as attributes\nassert jwt["claim1"] == "value1"  # or as dict items\nassert jwt.alg == sign_alg  # alg and kid headers are also accessible as attributes\nassert jwt.kid == private_jwk.kid\nassert jwt.verify_signature(private_jwk.public_jwk(), sign_alg)\n\nprint(jwt)\n```\nThis will output the full JWT compact representation. You can inspect it for example at <https://jwt.io>\n```\neyJhbGciOiJFUzI1NiIsImtpZCI6Im15a2V5In0.eyJzdWIiOiJzb21lX3N1YiIsImNsYWltMSI6InZhbHVlMSJ9.C1KcDyDT8qXwUqcWzPKkQD7f6xai-gCgaRFMdKPe80Vk7XeYNa8ovuLwvdXgGW4ZZ_lL73QIyncY7tHGXUthag\n```\n\nOr let\'s sign a JWT with the standardised lifetime, subject, audience and ID claims:\n```python\nfrom jwskate import Jwk, JwtSigner\n\nprivate_jwk = Jwk.generate_for_kty("EC")\nsigner = JwtSigner(issuer="https://myissuer.com", jwk=private_jwk, alg="ES256")\njwt = signer.sign(\n    subject="some_sub",\n    audience="some_aud",\n    extra_claims={"custom_claim1": "value1", "custom_claim2": "value2"},\n)\n\nprint(jwt.claims)\n```\nThe generated JWT claims will include the standardised claims:\n```\n{\'custom_claim1\': \'value1\',\n \'custom_claim2\': \'value2\',\n \'iss\': \'https://myissuer.com\',\n \'aud\': \'some_aud\',\n \'sub\': \'some_sub\',\n \'iat\': 1648823184,\n \'exp\': 1648823244,\n \'jti\': \'3b400e27-c111-4013-84e0-714acd76bf3a\'\n}\n```\n## Features\n\n* Simple, Clean, Pythonic interface\n* Convenience wrappers around `cryptography` for all algorithms described in JWA\n* Json Web Keys (JWK) loading and generation\n* Arbitrary data signature and verification using Json Web Keys\n* Json Web Signatures (JWS) signing and verification\n* Json Web Encryption (JWE) encryption and decryption\n* Json Web Tokens (JWT) signing, verification and validation\n* 100% type annotated\n* nearly 100% code coverage\n* Relies on [cryptography](https://cryptography.io) for all cryptographic operations\n* Relies on [BinaPy](https://guillp.github.io/binapy/) for binary data manipulations\n\n## Why a new lib ?\n\nThere are already multiple implementations of JOSE and Json Web Crypto related specifications in Python. However, I have\nbeen dissatisfied by all of them so far, so I decided to come up with my own module.\n\n- [PyJWT](https://pyjwt.readthedocs.io): lacks support for JWK, JWE, JWS, requires keys in PEM format.\n- [JWCrypto](https://jwcrypto.readthedocs.io/): very inconsistent and complex API.\n- [Python-JOSE](https://python-jose.readthedocs.io/): lacks easy support for JWT validation\n(checking the standard claims like iss, exp, etc.), lacks easy access to claims\n\n## Design\n### JWK are dicts\nJWK are specified as JSON objects, which are parsed as `dict` in Python. The `Jwk` class in `jwskate` is actually a\n`dict` subclass, so you can use it exactly like you would use a dict: you can access its members, dump it back as JSON, etc.\nThe same is true for Json Web tokens in JSON format.\n\n### JWA Wrappers\nWhile you can directly use `cryptography` to do the cryptographic operations that are described in [JWA](https://www.rfc-editor.org/info/rfc7518),\nits usage is not straightforward and gives you plenty of options to carefully select, leaving room for errors.\nTo work around this, `jwskate` comes with a set of wrappers that implement the exact JWA specification, with minimum\nrisk of mistakes.\n\n### Safe Signature Verification\nFor every signature verification method in `jwskate`, you have to provide the expected signature(s) algorithm(s).\nThat is to avoid a security flaw where your application accepts tokens with a weaker encryption scheme than what\nyour security policy mandates; or even worse, where it accepts unsigned tokens, or tokens that are symmetrically signed\nwith an improperly used public key, leaving your application exposed to exploitation by attackers.\n\nEach signature verification accepts 2 args `alg` and `algs`. If you always expect to verify tokens signed with a single\nsignature algorithm, pass that algorithm ID to alg. If you accept multiple algs (for example, any asymmetric alg that\nyou consider strong enough), you can instead pass an iterable of allowed algorithms with `algs`. The signature will be\nvalidated as long as it is signed with one of the provided algs.\n\nFor verification methods that accept a `Jwk` key, you don\'t have to provide an `alg` or `algs` if that Jwk has the\nappropriate `alg` member that define which algorithm is supposed to be used with that key.\n\n## Credits\n\nAll cryptographic operations are handled by [cryptography](https://cryptography.io).\n',
    'author': 'Guillaume Pujol',
    'author_email': 'guill.p.linux@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/guillp/jwskate',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
