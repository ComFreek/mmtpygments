[![Build Status](https://travis-ci.org/ComFreek/mmt-pygments-lexer.svg?branch=master)](https://travis-ci.org/ComFreek/mmt-pygments-lexer)
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/32b61ca59aba4a79ae4ab5582f210572)](https://app.codacy.com/app/ComFreek/mmt-pygments-lexer?utm_source=github.com&utm_medium=referral&utm_content=ComFreek/mmt-pygments-lexer&utm_campaign=Badge_Grade_Dashboard)
![GitHub License](https://img.shields.io/github/license/ComFreek/mmt-pygments-lexer.svg)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=flat-square)](http://makeapullrequest.com)
&nbsp;&nbsp; | [GitHub Repo](https://github.com/ComFreek/mmt-pygments-lexer) | [Collection of rendered codes](https://comfreek.github.io/mmt-pygments-lexer/test/index.html)

# MMT Pygments Lexer

Pygments lexer for [MMT Surface Syntax](https://uniformal.github.io/doc/language/) from the [MMT project](https://uniformal.github.io/).

**Collection of rendered codes:** [click here](https://comfreek.github.io/mmt-pygments-lexer/test/index.html)

![Screenshot of highlighted MMT code](https://user-images.githubusercontent.com/1827709/59698193-7523c300-91ef-11e9-8c4b-80ec2d3e4a40.png)

## Usage

We don't have a Pip package currently, hence we recommend cloning this repository as a Git submodule:

```bash
git submodule add https://github.com/ComFreek/mmt-pygments-lexer.git mmt-pygments-lexer
```

### Usage in LaTeX with minted

[minted](https://ctan.org/pkg/minted) is a LaTeX package rendering codes with Pygments lexer. As this is a Pygments lexer, we can let minted use it:

```tex
% You MUST USE XeLaTeX (or other LaTeX-derivatives which support Unicode)
\usepackage{fontspec}

% Download GNU Unifont from http://unifoundry.com/unifont/index.html
% And save it, say, as "fonts/unifont-12.1.02.ttf"
\newfontfamily\unifont{unifont-12.1.02.ttf}[Path=./fonts/,NFSSFamily=unifont]

% Disable caching for debugging purposes (increases compilation times!)
\usepackage[cache=false]{minted}
\setminted{
	fontfamily=unifont
}

% "./mmt-pygments-lexer" is this repository cloned on your drive
\newcommand{\mmtPygmentsLexerCommand}{./mmt-pygments-lexer/mmtpygments/mmt_lexer.py:MMTLexer -x}

\newminted[mmtcode]{\mmtPygmentsLexerCommand}{}
\newmintinline[mmtinline]{\mmtPygmentsLexerCommand}{}
\newmintedfile[mmtfile]{\mmtPygmentsLexerCommand}{}

\begin{document}
	% Variant 1: Code given in LaTeX, rendered in display mode
	\begin{mmtcode}
		theory MyTheory = c : type ❘ # abc ❙❚
	\end{mmtcode}

	% Variant 2: Code given in LaTeX, rendered inline
	% You can use any delimiter you like, here we use /
	\mmtinline/theory MyTheory = c : type ❘ # abc ❙❚/

	% Variant 3: Code given externally in file, rendered in display mode
	\mmtfile{your-mmt-file.mmt}
\end{document}
```

LaTeX Beamer: Use the `fragile` option for frames embedding codes: `\begin{frame}[fragile] ... \end{frame}`

See the [minted manual](https://ctan.org/pkg/minted) for more information on how to customize it.

#### Common Error: Rendered PDF shows tab characters of source

If you tab characters in the MMT source being highlighted and they are shown in the PDF rendered by XeLaTeX, you face a known bug of XeLaTeX ([\[1\]](https://tex.stackexchange.com/a/36872/38074), [\[2\]](https://tex.stackexchange.com/a/14776/38074)). It can be solved by passing `-8bit` to XeLaTeX.

![image](https://user-images.githubusercontent.com/1827709/59755955-23c81200-9289-11e9-92c5-1659b60d03d1.png)

## Testing

The lexer is heavily tested on large MMT archives containing a lot of MMT surface syntax. [`test/test.py`](./blob/master/test/test.py) is the main entry point of the test infrastructure. It recursively searches for MMT files in `test/data` and runs the lexer on them and formats them afterwards with Pygment's HtmlFormatter. The rendered versions are written next to the original `*.mmt` file with an `.html` extension. Furthermore, `index.html` and `amalgamation.html` are generated to link and display the results, respectively.

The Travis build automatically runs [`test/test.py`](./blob/master/test/test.py) and deploys the results on the `gh-pages` branch, see <https://comfreek.github.io/mmt-pygments-lexer/> and especially <https://comfreek.github.io/mmt-pygments-lexer/test/index.html>.

## Development

For tinkering and testing the lexer, it is recommended to employ the same testing infrastructure as described above. Even though the Travis build fails on lexing error, [`test/test.py`](./blob/master/test/test.py) actually doesn't -- it just returns a non-zero exit code. In fact, it even generates the HTML renderings with red rectangles around lexing errors. Hence, while tinkering with the lexer, just regularly run [`test/test.py`](./blob/master/test/test.py) and look at the `index.html` locally in your browser to see any errors.
