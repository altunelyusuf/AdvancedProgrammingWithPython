# Chapter 17 research: wheels of the isolated environment (v1.0.2)

The executed claims of chapter 17 (data module sen0414_ch17_rdodi_data_v1_0_3.py) run in a virtual environment that 08-tooling/sen0414_ch17_isolated_env_v1_0_0.py builds itself, with no network, from committed wheels only. Python 3.14 on the machine's path is the only thing taken from the machine; no package of that interpreter is visible in the environment.

The environment holds the two wheels already in this folder, pypdf-6.20.1-py3-none-any.whl and python_docx-1.2.0-py3-none-any.whl (committed 2026-10-12), and the eight wheels of the folder env_wheels_v1_0_0 below: pdfminer.six 20260107, Pillow 12.3.0, cryptography 50.0.2 and lxml 6.1.3, the packages the data module v1_0_2 names, and the four packages they need (cffi, pycparser, charset-normalizer, typing-extensions). Resolved with `pip install` of these wheels with no network and `pip check` (No broken requirements found). The first three were downloaded on 2026-10-29 from PyPI with pip (the proxy of the build machine); cffi, charset-normalizer, cryptography, pycparser and typing-extensions are the byte-identical files committed for chapter 15 (same SHA-256).

| file | project page | licence | SHA-256 |
|---|---|---|---|
| pypdf-6.20.1-py3-none-any.whl (this folder) | https://pypi.org/project/pypdf/ | BSD-3-Clause | aa5a55ddcffdc5e5ab291d5decb23f6383f4e56f8e3263dc39af41fff03885ad |
| python_docx-1.2.0-py3-none-any.whl (this folder) | https://pypi.org/project/python-docx/ | MIT | 3fd478f3250fbbbfd3b94fe1e985955737c145627498896a8a6bf81f4baf66c7 |
| env_wheels_v1_0_0/pdfminer_six-20260107-py3-none-any.whl | https://pypi.org/project/pdfminer.six/ | MIT | 366585ba97e80dffa8f00cebe303d2f381884d8637af4ce422f1df3ef38111a9 |
| env_wheels_v1_0_0/pillow-12.3.0-cp314-cp314-manylinux_2_27_x86_64.manylinux_2_28_x86_64.whl | https://pypi.org/project/pillow/ | MIT-CMU | 251bf95b67017e27b13d82f5b326234ca62d70f9cf4c2b9032de2358a3b12c7b |
| env_wheels_v1_0_0/lxml-6.1.3-cp314-cp314-manylinux_2_26_x86_64.manylinux_2_28_x86_64.whl | https://pypi.org/project/lxml/ | BSD-3-Clause | a7eb78ba28b187e1e9203a55c60fcf70df2d22cb205fe6d51b9383d6097419f0 |
| env_wheels_v1_0_0/cryptography-50.0.2-cp311-abi3-manylinux_2_34_x86_64.whl | https://pypi.org/project/cryptography/ | Apache-2.0 OR BSD-3-Clause | 9dab55f57c74c3cad24c323bacbbd04be4705ba6eb0d92e920b1fc4837ed5079 |
| env_wheels_v1_0_0/cffi-2.1.1-cp314-cp314-manylinux2014_x86_64.manylinux_2_17_x86_64.whl | https://pypi.org/project/cffi/ | MIT-0 | b0431303acaea1089ad4b3e9ce4e6518193def1118d4073ca848635ee4ea2e96 |
| env_wheels_v1_0_0/pycparser-3.12-py3-none-any.whl | https://pypi.org/project/pycparser/ | BSD-3-Clause | a076f3f489b39b43ed13563a1dafe42447445bec2e294154ec5c57fcdda4c85e |
| env_wheels_v1_0_0/charset_normalizer-3.5.2-py3-none-any.whl | https://pypi.org/project/charset-normalizer/ | MIT | b6b751274acb69d77b3323d6b7dbaa3c7fdfc1eb829b7eb61d262f32e1af9685 |
| env_wheels_v1_0_0/typing_extensions-4.16.0-py3-none-any.whl | https://pypi.org/project/typing-extensions/ | PSF-2.0 | 481caa481374e813c1b176ada14e97f1f67a4539ce9cfeb3f350d78d6370c2e8 |

Four wheels are built for a platform, not pure Python: cffi (CPython 3.14, manylinux x86_64), cryptography (abi3, manylinux_2_34 x86_64), lxml (CPython 3.14, manylinux x86_64) and Pillow (CPython 3.14, manylinux x86_64). The environment builder refuses to run on a machine that is not Linux x86_64 and says so; it does not fall back to the network. So the claims of the chapter reproduce on Linux x86_64 with CPython 3.14 only.

The tool checks the SHA-256 of every wheel against the table in its own text before installing, and the installed package list against the pinned list after.
