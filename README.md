[![PyPI](https://img.shields.io/pypi/v/mmtpygments)](https://pypi.org/project/mmtpygments/) [![Build Status](https://travis-ci.org/ComFreek/mmtpygments.svg?branch=master)](https://travis-ci.org/ComFreek/mmtpygments)
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/32b61ca59aba4a79ae4ab5582f210572)](https://app.codacy.com/app/ComFreek/mmtpygments?utm_source=github.com&utm_medium=referral&utm_content=ComFreek/mmtpygments&utm_campaign=Badge_Grade_Dashboard)
![GitHub License](https://img.shields.io/github/license/ComFreek/mmtpygments.svg)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=flat-square)](http://makeapullrequest.com)
&nbsp;&nbsp; | [GitHub Repo](https://github.com/ComFreek/mmtpygments) | [Collection of rendered codes](https://comfreek.github.io/mmtpygments/mmtpygments/test/index.html)

# mmtpygments: Pygments plugin for MMT surface syntax

To support syntax highlighting of the [MMT Surface Syntax](https://uniformal.github.io/doc/language/) from the [MMT project](https://uniformal.github.io/) this package is a Pygments plugin including

- a Pygments lexer (`mmt`)
- a recommended Pygments style for it (`mmtdefault`)
- and experimentally a Pygments lexer for MMT relational data (`mmtrel`).

**Tested on 15k lines of code.** [see collection](https://comfreek.github.io/mmtpygments/mmtpygments/test/index.html)<br>

<p align="center">
	<a href="https://comfreek.github.io/mmtpygments/mmtpygments/test/data/readme-showoff-example.mmt.html">
		<img src="https://user-images.githubusercontent.com/1827709/82438710-c7253680-9a99-11ea-97c9-8da8f715ac14.png" alt="Screenshot of highlighted MMT code"/>
	</a><br>
	(click to see live version)
</p>


## Highlighting MMT code in LaTeX Documents

See readme in [./examples/latex](./examples/latex).

## Highlighting from Command Line (for devs)

1. `pipenv install pygments mmtpygments` in your project directory
2. `pipenv run pygmentize -f html -l mmt -O full,style=mmtdefault -o test.html test.mmt`

   This tells Pygments to use the HTML formatter (`-f`), the MMT lexer (`-l`) and to output a full HTML file using the `mmtdefault` style (`-O`) rendered of `test.mmt` into `test.html` (`-o`).

<hr>

## Development

1. Install [pipenv](https://github.com/pypa/pipenv), which provides a consistent Python, pip and package environment locked in the committed `Pipfile` and `Pipfile.lock` files.
2. `pipenv install`
3. `git submodule init`
4. `git submodule update`

## Exports to CodeMirror & Rouge Lexers

- `cd mmtpygments && pipenv run python ./mmt_lexer.py convert codemirror ../exports/codemirror/mode/mmt/mmt.js`
- `cd mmtpygments && pipenv run python ./mmt_lexer.py convert rouge ../exports/rouge/lib/rouge/lexers/mmt.rb`

### Testing

1. `cd mmtpygments/test`
2. `pipenv run python test.py ./` (returns non-zero exit code on failure)
3. Open `index.html` in a browser to see failures visually (red rectangles).

This [`test.py`](mmtpygments/test/test.py) runs the lexer on large MMT archives containing a lot of MMT surface syntax. It recursively searches for MMT files in `mmtpygments/test/data`, on which it then runs the provided lexer and Pygment's HtmlFormatter. The rendered versions are written next to the original `*.mmt` files with an `.html` extension. Furthermore, `index.html` and `amalgamation.html` are generated to link and display the results, respectively.

The Travis build automatically runs [`test.py`](mmtpygments/test/test.py) and deploys the results on the `gh-pages` branch, see <https://comfreek.github.io/mmtpygments/> and especially <https://comfreek.github.io/mmtpygments/mmtpygments/test/index.html>.

### Dev Workflow

For tinkering and testing the lexer, it is recommended to employ the same testing infrastructure as described above. Even though the Travis build fails on lexing error, [`test.py`](mmtpygments/test/test.py) actually doesn't -- it just returns a non-zero exit code. In fact, it even generates the HTML renderings with red rectangles around lexing errors. Hence, while tinkering with the lexer, just regularly run [`test.py`](mmtpygments/test/test.py) and look at the `index.html` locally in your browser to see any errors.

### Publishing

Publishing is done automatically via [.travis.yml](./.travis.yml) upon tagged commits on the master branch. For that do

1. Locally commit all your changes.
2. Create a new version tag: `git tag -a vx.y.z -m "Version x.y.z, see CHANGELOG.md"` (the tag name needs to start with `v` and a digit for Travis CI to pick it up, see [`.travis.yml`](./.travis.yml))
3. Push the commit and the tag: `git push && git push --tags`

**Not recommended:** If you really have to publish a version manually for whatever reason, do the following:

```bash
# Packaging
$ pipenv run python setup.py sdist bdist_wheel

# Checking if packages are okay (PyPi server will do the same)
$ pipenv run twine check dist/*

# Upload to Test PyPi repository
$ pipenv run twine upload --repository-url https://test.pypi.org/legacy/ dist/*

# Upload to real PyPi repository
$ pipenv run twine upload dist/*
```

### For future maintainers: necessary changes in case of repository movement

In case you wish to host this repository or a fork thereof somewhere else, these are the places where you have to make changes:

  - `README.md`: Change all links referencing anything under `https://ComFreek.github.io/mmtpygments` to the URI where you deploy your things.
  - `.travis.yml`:
    - Change the base path with which `python test.py` is run to your hosting URI.
    - Change the secret value in under deploy/pypi to another PyPI token under which you are able to publish PyPI packages.
