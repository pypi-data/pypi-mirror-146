from setuptools import setup

name = "types-stdlib-list"
description = "Typing stubs for stdlib-list"
long_description = '''
## Typing stubs for stdlib-list

This is a PEP 561 type stub package for the `stdlib-list` package.
It can be used by type-checking tools like mypy, PyCharm, pytype etc. to check code
that uses `stdlib-list`. The source for this package can be found at
https://github.com/python/typeshed/tree/master/stubs/stdlib-list. All fixes for
types and metadata should be contributed there.

See https://github.com/python/typeshed/blob/master/README.md for more details.
This package was generated from typeshed commit `354787f6e0037f7b8d37d11eb851b8f4e0931a42`.
'''.lstrip()

setup(name=name,
      version="0.8.0",
      description=description,
      long_description=long_description,
      long_description_content_type="text/markdown",
      url="https://github.com/python/typeshed",
      project_urls={
          "GitHub": "https://github.com/python/typeshed",
          "Changes": "https://github.com/typeshed-internal/stub_uploader/blob/main/data/changelogs/stdlib-list.md",
          "Issue tracker": "https://github.com/python/typeshed/issues",
          "Chat": "https://gitter.im/python/typing",
      },
      install_requires=[],
      packages=['stdlib_list-stubs'],
      package_data={'stdlib_list-stubs': ['__init__.pyi', 'base.pyi', 'METADATA.toml']},
      license="Apache-2.0 license",
      classifiers=[
          "License :: OSI Approved :: Apache Software License",
          "Typing :: Stubs Only",
      ]
)
