[minted](https://ctan.org/pkg/minted) is a LaTeX package rendering codes with Pygments as the backend.

1. `pipenv install pygments mmtpygments` (recommended way; [install pipenv](https://pipenv.pypa.io/en/latest/install/#installing-pipenv) if you haven't already)

   Alternative way: if you don't have the package manager `pipenv` which operates on folders, you can instead also do `pip install --user pygments mmtpygments`.
   However, this will clutter your user-wide Python package directory and lead to non-reproducible papers as the versions of the packages are not persisted within the paper folder.

2. In your terminal, run
   - `pipenv shell`
   - and then your IDE, e.g. on Windows with PowerShell as terminal `& "C:\Program Files (x86)\texstudio\texstudio.exe" "main.tex"`


3. write LaTeX

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

4. Before sending LaTeX sources to outsiders (e.g. editors or publishers):

 - compile once successfully using `\usepackage[finalizecache=true,frozencache=false]{minted}`
 - modify source to `\usepackage[finalizecache=false,frozencache=true]{minted}`
 - send files (incl. cache files) to outsider

**LaTeX Beamer**: Use the `fragile` option for frames embedding codes: `\begin{frame}[fragile] ... \end{frame}`

See the [minted manual](https://ctan.org/pkg/minted) for more information on how to customize it.