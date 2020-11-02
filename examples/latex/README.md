# Highlighting MMT Code in LaTeX Documents using `mmtpygments`

[`mmtpygments`](./../../) is a source code highlighter for the Pygments framework, which is written in Python.
The LaTeX package [minted](https://ctan.org/pkg/minted) allows us to use any Pygments highlighter to typeset highlighted code in LaTeX documents.
Crucially, this means that while typesetting you are *dependent* on a Python and pygments installation. However, there is an easy way to submit a standalone (i.e. independent) version to outsiders (e.g. editors, publishers).

The tutorial below will walk you through installation, typesetting a simple document, and preparing an (imaginary) submission-ready LaTeX document.

1. Clone this repository/the containing folder of this readme to follow along.

2. Install [Python](https://www.python.org/) and [pipenv](https://pipenv.pypa.io/en/latest/install/#installing-pipenv) if you haven't already. (The second is not strictly required, you can also use mere `pip`; see next point.)
3. `pipenv install pygments mmtpygments`

   Alternative way using pip: `pip install --user pygments mmtpygments`. If pip warns you about something not on PATH, be sure to add it to your PATH and to restart your TeX IDE if you have already opened one. 
   However, using a *real* package manager like pipenv is the better option. It will (a) not clutter your user-wide installation of Python packages and (b) manifest the actual installed dependencies in a `Pipfile.lock` file, which makes installations & typesetting (say, of papers) reproducible in the future.

4. In case you chose pipenv, open a terminal and type `pipenv shell`.
5. Open `main.tex` using your favorite IDE. If you chose pipenv, you need to open it from the "pipenv shell" you just initiated, e.g. on Windows with PowerShell as terminal `& "C:\Program Files (x86)\texstudio\texstudio.exe" "main.tex"`.

   For quick reference, here's how you will be including MMT code in your documents:

   ```tex
   \begin{mmtcode}
   theory MyTheory =
   	ℕ : type ❙
   	succ : ℕ ⟶ℕ ❘ # S 1❙
   ❚
   \end{mmtcode}
   
   
   \mmtfile{test.mmt}
   
   \mmtinline/theory MyTheory = c : type ❘ # abc ❙❚/
   ```

6. Compile and run the just opened `main.tex`.

   Ideally your IDE picks up the `TS-program` TeX magic comment at the beginning of the file. If not, you have to manually configure your IDE to run the command specified in that comment.

   Three things are crucial in that command line:

     - `-xelatex`: usage of XeLaTeX (or LuaLaTeX) is required for MMT codes' Unicode characters to work.
     - `-shell-escape`: needed for the minted package to invoke Pygments. In the next point, we see how we can get rid of this.
     - `-8bit`: needed to typeset tabs within verbatim environments correctly. Not needed if you only typeset from external files.

       Otherwise, tabs will typeset in the weird way below. This is a known bug of XeLaTeX, see [here](https://tex.stackexchange.com/a/36872/38074) and [here](https://tex.stackexchange.com/a/14776/38074).

       ![Weird typeset tabs as `^^I`](https://user-images.githubusercontent.com/1827709/59755955-23c81200-9289-11e9-92c5-1659b60d03d1.png)

7. To get rid of the dependence on `-shell-escape`, a Python, and a Pygments installation, do:

   - Compile once uing the `finalizecache=true,frozencache=false` options, e.g.: `\usepackage[finalizecache=true,frozencache=false]{minted}`.
   - Modify again to `finalizecache=false,frozencache=true`, e.g.: `\usepackage[finalizecache=false,frozencache=true]{minted}`. If desired, you can compile now again to see if it's working.
   - Submit all files, incl. cache files, to the editor/publisher/outsider.

See the [minted manual](https://ctan.org/pkg/minted) for more information on how to customize typesetting of code blocks.

## LaTeX Beamer: need fragile option

With Beamer, you need to use the `fragile` option for frames that embed codes: `\begin{frame}[fragile] ... \end{frame}`.

See `slides.tex` for an example.
