# Chapter 15 research: wheels of the isolated environment (v1.0.2)

The executed claims of chapter 15 (data module sen0414_ch15_rdodi_data_v1_0_3.py) run in a virtual environment that 08-tooling/sen0414_ch15_isolated_env_v1_0_0.py builds itself, with no network, from committed wheels only. Python 3.14 on the machine's path is the only thing taken from the machine; no package of that interpreter is visible in the environment.

The environment holds the 14 wheels of ASSETS_PROVENANCE_v1_0_0.md (this folder, hashes there) and the 12 wheels below (folder env_wheels_v1_0_0), the packages that pip resolved on 2026-10-27 for ezsheets 2026.4.28 and google-api-python-client 2.201.0 once the 14 are fixed (`pip install` of the 14 committed wheels; `pip check` ends with No broken requirements found). Downloaded on 2026-10-27 from PyPI with pip (the proxy of the build machine).

| file | project page | licence | SHA-256 |
|---|---|---|---|
| certifi-2026.10.23-py3-none-any.whl | https://pypi.org/project/certifi/ | MPL-2.0 | e9b54de76e530bb6cf0ccd036787103acb58fd42ba930ea8bf948ddbaa2f61d1 |
| cffi-2.1.1-cp314-cp314-manylinux2014_x86_64.manylinux_2_17_x86_64.whl | https://pypi.org/project/cffi/ | MIT-0 | b0431303acaea1089ad4b3e9ce4e6518193def1118d4073ca848635ee4ea2e96 |
| charset_normalizer-3.5.2-py3-none-any.whl | https://pypi.org/project/charset-normalizer/ | MIT | b6b751274acb69d77b3323d6b7dbaa3c7fdfc1eb829b7eb61d262f32e1af9685 |
| cryptography-50.0.2-cp311-abi3-manylinux_2_34_x86_64.whl | https://pypi.org/project/cryptography/ | Apache-2.0 OR BSD-3-Clause | 9dab55f57c74c3cad24c323bacbbd04be4705ba6eb0d92e920b1fc4837ed5079 |
| idna-3.20-py3-none-any.whl | https://pypi.org/project/idna/ | BSD-3-Clause | ab7ae7122974553370f0bdb919e1a960b2cd1bc1ef0276416d896db81c14582c |
| opentelemetry_api-1.45.1-py3-none-any.whl | https://pypi.org/project/opentelemetry-api/ | Apache-2.0 | b31553efa588ae44bc306f863c785c5333a9ecc091248c6ee68b4b6c87fdedfb |
| protobuf-7.36.2-cp310-abi3-manylinux2014_x86_64.whl | https://pypi.org/project/protobuf/ | BSD-3-Clause | 89f23aa53c24553a2416fd4fd1ec06f74fa42b14b546d8883128813f775bbfd2 |
| pycparser-3.12-py3-none-any.whl | https://pypi.org/project/pycparser/ | BSD-3-Clause | a076f3f489b39b43ed13563a1dafe42447445bec2e294154ec5c57fcdda4c85e |
| pyparsing-3.3.3-py3-none-any.whl | https://pypi.org/project/pyparsing/ | MIT | ece8c00a69cf01b45d0b1dedabb469c90d8caf996d4fda40f147627a122849a4 |
| requests-2.34.2-py3-none-any.whl | https://pypi.org/project/requests/ | Apache-2.0 | 2a0d60c172f83ac6ab31e4554906c0f3b3588d37b5cb939b1c061f4907e278e0 |
| typing_extensions-4.16.0-py3-none-any.whl | https://pypi.org/project/typing-extensions/ | PSF-2.0 | 481caa481374e813c1b176ada14e97f1f67a4539ce9cfeb3f350d78d6370c2e8 |
| urllib3-2.8.0-py3-none-any.whl | https://pypi.org/project/urllib3/ | MIT | 0cf3cae568d36aa9576b28dfb35f11328f1cb974ca7647d9475ebb86c75ac6e3 |

Three of the twelve are built for a platform, not pure Python: cffi (CPython 3.14, manylinux x86_64), cryptography (abi3, manylinux_2_34 x86_64) and protobuf (abi3, manylinux2014 x86_64). google-auth 2.61.0 requires cryptography; the claims that sign in or build the authorization URL import it (measured: without it the claims that use the library fail with ModuleNotFoundError: No module named cryptography). The environment builder refuses to run on a machine that is not Linux x86_64 and says so; it does not fall back to the network.

The tool checks the SHA-256 of every wheel against the table in its own text before installing, and the installed package list against the pinned list after.
