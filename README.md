# MMT Pygments Lexer

![Screenshot of highlighted MMT code](https://user-images.githubusercontent.com/1827709/59698193-7523c300-91ef-11e9-8c4b-80ec2d3e4a40.png)

# Usage

We don't have a Pip package currently, hence we recommend cloning this repository as a Git submodule:

```bash
git submodule add https://github.com/ComFreek/mmt-pygments-lexer.git mmt-pygments-lexer
```

## Usage in LaTeX

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

\begin{document}
	% Load from a file
	\inputminted{mmt-pygments-lexer.py:MMTLexer -x}{your-mmt-file.mmt}
	
	% Or inline
	\begin{minted}{mmt-pygments-lexer.py:MMTLexer -x}
theory MyTheory =
	c : type ❘ # abc ❙
❚
	\end{minted}
\end{document}
```

See the [minted manual](https://ctan.org/pkg/minted) on how to define shortcuts lest you have to type `mmt-pygments-lexer.py:MMTLexer -x` every time.
