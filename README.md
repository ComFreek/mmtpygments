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

**Collection of rendered codes:** [click here](https://comfreek.github.io/mmtpygments/mmtpygments/test/index.html)<br>
**Screenshot:** (click for live version)<br>
[![Screenshot of highlighted MMT code](https://user-images.githubusercontent.com/1827709/82438710-c7253680-9a99-11ea-97c9-8da8f715ac14.png)](https://comfreek.github.io/mmtpygments/mmtpygments/test/data/readme-showoff-example.mmt.html)

## Installation

- via Pip (easy)

    ```
    pip install Pygments mmtpygments
    ```

- via `pipenv` or other Python package managers superior to Pip:

    1. Run `pipenv install pygments mmtpygments` in your project directory, e.g. containing the LaTeX files in which you'd like to use this
	2. Remember to use `mmtpygments` from now on always in that virtual environment context: run your intended command within `pipenv shell`

	   For example, if you'd like to use this in LaTeX and use TeXStudio as an IDE, start TeXStudio from within that shell.
	   
    This way, you don't clutter your whole PC with the Pip packages *and* more importantly, you document the Pip package versions in the `Pipfile.lock` file generated in step (2.1).

## Usage

### CLI

```
pygmentize -f html -l mmt -O full,style=mmtdefault -o test.html test.mmt
```

This tells Pygments to use the HTML formatter (`-f`), the MMT lexer (`-l`) and to output a full HTML file using the `mmtdefault` style (`-O`) rendered of `test.mmt` into `test.html` (`-o`).


### LaTeX (with minted)

[minted](https://ctan.org/pkg/minted) is a LaTeX package rendering codes with Pygments as the backend.

```tex
% !TeX encoding = UTF-8
% !TEX TS-program = latexmk -xelatex -shell-escape -silent -latexoption="-synctex=1 -8bit" %
%
% ^^^ This is the build command. Install latexmk if you don't have it already.
%     You may choose an alternative LaTeX derivative, e.g. LuaLaTeX, but be warned that it must support Unicode!

\documentclass{article}

\usepackage{fontspec}

% Download GNU Unifont from http://unifoundry.com/unifont/index.html
% And save it, say, as "fonts/unifont-12.1.03.ttf"
\newfontfamily\unifont{unifont-12.1.03.ttf}[Path=./fonts/,NFSSFamily=unifont]

% Disable caching for debugging purposes (increases compilation times!)
\usepackage[cache=false]{minted}
\setminted{fontfamily=unifont,tabsize=2,breaklines=true}

\newminted[mmtcode]{mmt}{}
\newmintinline[mmtinline]{mmt}{}
\newmintedfile[mmtfile]{mmt}{}

\begin{document}
	% Variant 1: Code given in LaTeX, rendered in display mode
	\begin{mmtcode}
theory MyTheory = c : type ❘ # abc ❙❚
	\end{mmtcode}

	% Variant 2: Code given in LaTeX, rendered inline
	% You can use any delimiter you like, here we use /
	\mmtinline/theory MyTheory = c : type ❘ # abc ❙❚/

	% Variant 3: Code given externally in file, rendered in display mode
	% \mmtfile{your-mmt-file.mmt}
\end{document}
```

**LaTeX Beamer**: Use the `fragile` option for frames embedding codes: `\begin{frame}[fragile] ... \end{frame}`

See the [minted manual](https://ctan.org/pkg/minted) for more information on how to customize it.

#### Common Error: Rendered PDF shows tab characters of source

If you tab characters in the MMT source being highlighted and they are shown in the PDF rendered by XeLaTeX, you face a known bug of XeLaTeX ([\[1\]](https://tex.stackexchange.com/a/36872/38074), [\[2\]](https://tex.stackexchange.com/a/14776/38074)). It can be solved by passing `-8bit` to XeLaTeX.

![image](https://user-images.githubusercontent.com/1827709/59755955-23c81200-9289-11e9-92c5-1659b60d03d1.png)

## Development

1. Install [pipenv](https://github.com/pypa/pipenv), which provides a consistent Python, pip and package environment locked in the committed `Pipfile` and `Pipfile.lock` files.
2. `pipenv install`
3. `git submodule init`
4. `git submodule update`

### Testing

1. `cd mmtpygments/test`
2. `pipenv run python test.py ./` (returns non-zero exit code on failure)
3. Open `index.html` in a browser to see failures visually (red rectangles).

This [`test.py`](mmtpygments/test/test.py) runs the lexer on large MMT archives containing a lot of MMT surface syntax. It recursively searches for MMT files in `mmtpygments/test/data`, on which it then runs the provided lexer and Pygment's HtmlFormatter. The rendered versions are written next to the original `*.mmt` files with an `.html` extension. Furthermore, `index.html` and `amalgamation.html` are generated to link and display the results, respectively.

The Travis build automatically runs [`test.py`](mmtpygments/test/test.py) and deploys the results on the `gh-pages` branch, see <https://comfreek.github.io/mmtpygments/> and especially <https://comfreek.github.io/mmtpygments/mmtpygments/test/index.html>.

### Dev Workflow

For tinkering and testing the lexer, it is recommended to employ the same testing infrastructure as described above. Even though the Travis build fails on lexing error, [`test.py`](mmtpygments/test/test.py) actually doesn't -- it just returns a non-zero exit code. In fact, it even generates the HTML renderings with red rectangles around lexing errors. Hence, while tinkering with the lexer, just regularly run [`test.py`](mmtpygments/test/test.py) and look at the `index.html` locally in your browser to see any errors.

## Publishing

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

## For future maintainers: necessary changes in case of repository movement

In case you wish to host this repository or a fork thereof somewhere else, these are the places where you have to make changes:

  - `README.md`: Change all links referencing anything under `https://ComFreek.github.io/mmtpygments` to the URI where you deploy your things.
  - `.travis.yml`:
    - Change the base path with which `python test.py` is run to your hosting URI.
    - Change the secret value in under deploy/pypi to another PyPI token under which you are able to publish PyPI packages.
