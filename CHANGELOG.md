# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.4.0] - 2020-05-20
### Changed
- Improved documentation on installation and usage in readme.

### Fixed
- Remove failing `import` statement in `setup.py` preventing installation via Pip.

## [0.3.1], [0.3.2], [0.3.3], [0.3.4], [0.3.5], [0.3.6] - 2020-05-20

Just version bumps to retrigger faulty Travis CI configurations to auto-deploy to PyPI.

## [0.3.0] - 2020-05-20
### Added
- MMT Lexer: Support for `meta` annotations in lexer, see [the rendered `meta-annotations.mmt`](https://comfreek.github.io/mmtpygments/mmtpygments/test/data/meta-annotations.mmt.html) for an example.
- MMT Lexer: More inspection/lexing of notations to be able to highlight pecifiers for argument positions, implicit arguments and so on as well.

### Changed
- MMT Lexer: Output more meaningful token types when lexing. For the end user, this might mean that Pygments will render MMT code in slightly different color.

### Security
- Updated all Python (PyPI) dependencies


## [0.2.0] - 2019-09-09

### Added
- First release, no detailled information available anymore.