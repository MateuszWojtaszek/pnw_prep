# Profil VS Code: `studies_AI`

Ściąga do profilu utworzonego 2026-09-06. **31 rozszerzeń wybranych jawnie**; z zależnościami,
które VS Code dociąga sam (satelity Jupytera, `debugpy`, `remote-explorer`, `remote-ssh-edit`),
daje to **40 zainstalowanych**. Te dwie liczby łatwo pomylić — patrz tabela niżej.

Profil istnieje na dwóch maszynach. **ID profilu nadaje lokalna instalacja VS Code i jest różne
na każdej z nich** — poniżej oba.

| | macOS (M3 Pro) | **Ubuntu 24 / `black_mw` — maszyna robocza** |
|---|---|---|
| Katalog profilu | `~/Library/Application Support/Code/User/profiles/68e22d86/` | `~/.config/Code/User/profiles/407f9a50/` |
| Settings profilu | `.../68e22d86/settings.json` | `.../407f9a50/settings.json` |
| Backup poprzedniego stanu | `~/Library/Application Support/Code/User/_backup_20260906_193317/` | — (profil zakładany od zera) |
| Rozszerzeń **zainstalowanych** | 40 | 42 |
| w tym wybranych **jawnie** | 31 | 36 |

> Realna różnica między maszynami to **dwa zainstalowane rozszerzenia**, nie jedenaście —
> rozjazd w wierszu „jawnie" bierze się stąd, że na Ubuntu część satelitów instalowano
> ręcznie, a na Macu przyszły same. Jedno z dwóch to `swyddfa.esbonio` (na Macu świadomie
> pominięty, na Ubuntu wybrany). Żeby domknąć: `code --profile "studies_AI" --list-extensions`
> na obu maszynach i `diff`.

Profil na Ubuntu odtworzony 2026-09-07. Różnice względem Maca opisuje sekcja
[12. Ubuntu — czym się różni](#12-ubuntu--czym-się-różni). **VS Code jest tu ze snapa**
(`/snap/bin/code`, classic confinement), ale katalogi konfiguracji są zwykłe:
`~/.config/Code/User/` i wspólne `~/.vscode/extensions` (2,7 GB).

---

## Spis treści

1. [Zarządzanie profilem](#1-zarządzanie-profilem)
2. [Python: rdzeń i uv](#2-python-rdzeń-i-uv)
3. [Notebooki i ML](#3-notebooki-i-ml)
4. [Codzienna praca z kodem](#4-codzienna-praca-z-kodem)
5. [Zdalna praca](#5-zdalna-praca)
6. [Pisanie: LaTeX, Markdown, YAML](#6-pisanie-latex-markdown-yaml)
7. [Wygląd](#7-wygląd)
8. [Claude Code](#8-claude-code)
9. [Wygoda i czytelność](#9-wygoda-i-czytelność)
10. [Ściąga: co ustawić najpierw](#10-ściąga-co-ustawić-najpierw)
11. [Dokumentacja kodu: Sphinx](#11-dokumentacja-kodu-sphinx)
12. [Ubuntu — czym się różni](#12-ubuntu--czym-się-różni)

---

## 1. Zarządzanie profilem

Profile w VS Code **nie mają osobnych katalogów z rozszerzeniami**. Wszystko leży w jednym
`~/.vscode/extensions`, a profil trzyma tylko listę, które z nich są w nim aktywne.
Wniosek praktyczny: dopięcie do profilu rozszerzenia, które już masz gdzie indziej,
jest natychmiastowe i nic nie pobiera.

```bash
# co jest w profilu
code --profile "studies_AI" --list-extensions --show-versions

# dodaj / usuń
code --profile "studies_AI" --install-extension <publisher>.<name>
code --profile "studies_AI" --uninstall-extension <publisher>.<name>

# otwórz folder w tym profilu (zapisuje trwałe powiązanie folder→profil)
code --profile "studies_AI" ~/Documents/projects/masters/<projekt>

# aktualizacja wszystkich
code --profile "studies_AI" --update-extensions
```

**Jak działa „domyślność":** VS Code nie ma pojęcia „domyślnego profilu" — `Default` jest
wbudowany i nieusuwalny. To, co masz, to `window.newWindowProfile: "studies_AI"`
w settings profilu Default (klucz ma `scope: application`, więc mieszka tam i działa globalnie).
Efekt: **nowe okna i foldery bez zapisanego powiązania** startują w `studies_AI`.

**Uwaga na kolejność pierwszeństwa:** zapisane powiązanie folder→profil **wygrywa**
z `newWindowProfile`. Twoje stare projekty (`ml`, `pgm`, `rep_lern`, `sieci`, `pnw_prep`…)
mają powiązanie z `Default` i dalej będą się tam otwierać, dopóki nie przepniesz ich
komendą `code --profile "studies_AI" <folder>`.

W GUI: `Cmd+Shift+P` → `Profiles: Switch Profile` / `Profiles: Show Contents`.
Reset wszystkich powiązań: `Profiles: Reset Workspace Profiles Associations`.

---

## 2. Python: rdzeń i uv

### `ms-python.python` — baza
Bez tego nic nie działa. Sam w sobie robi mało: uruchamianie plików, wykrywanie interpretera,
integracja z terminalem. Cała moc siedzi w rozszerzeniach, które on koordynuje.

**Komendy:** `Python: Select Interpreter`, `Python: Run Python File in Terminal`.

---

### `ms-python.vscode-python-envs` — **to jest Twoja integracja z uv**
Najważniejsze rozszerzenie w tym zestawie, jeśli chodzi o Twój workflow.
GA od lutego 2026 po roku w preview. Zastępuje stary, rozjeżdżający się picker interpretera
jednym interfejsem nad venv / uv / conda / poetry / pyenv.

**Moc:** jeśli `uv` jest w PATH, rozszerzenie **automatycznie** używa go do tworzenia
środowisk i instalacji pakietów zamiast `python -m venv` + `pip`. Przy Twoim `pyproject.toml`
z `uv_build` jako build-backendem to jest dokładnie ten setup, o który chodzi.

**Jak używać:** w Explorerze pojawia się panel **Python Environments** — tworzysz env,
instalujesz i usuwasz pakiety klikając, bez schodzenia do terminala.
Komendy: `Python Envs: Create Environment`, `Python Envs: Manage Packages`.

**Ustawienia:**
```jsonc
"python-envs.alwaysUseUv": true,               // domyślnie true — uv zamiast venv+pip
"python.useEnvironmentsExtension": true,       // domyślnie FALSE — bez tego panelu nie ma
"python-envs.terminal.autoActivationType": "command"
// tryby: "shellStartup" (aktywacja w profilu shella, najszybsze),
//        "command" (domyślne, wysyła `activate` do terminala),
//        "off"
```

> ⚠️ **Klucz nazywa się `python.useEnvironmentsExtension`, nie `python.useEnvsExtension`.**
> Ta druga nazwa (wcześniej w tym dokumencie) nie istnieje w `ms-python.python` — sprawdzone
> w 2026.4.0, gdzie w `contributes.configuration` jest tylko pełna forma. Wpisana błędnie
> nie zgłasza się jako literówka, po prostu nic nie robi.
>
> Domyślna wartość to **`false`**, więc bez jawnego ustawienia panel Python Environments
> w ogóle się nie pojawi. Zmiana **wymaga przeładowania okna**.

**Jak dokładnie wchodzi tu uv — wbrew temu, co sugeruje nazwa ustawienia.**
Nie ma osobnego menedżera środowisk „uv". W `contributes` rozszerzenia są tylko
`ms-python.python:venv`, `:pip`, `:conda`, `:poetry`, `:pyenv`, `:pipenv`, `:system`,
a domyślne pozostają `defaultEnvManager = ms-python.python:venv` i
`defaultPackageManager = ms-python.python:pip`. **Tego nie zmieniaj** — uv nie jest osobną
pozycją na tej liście, tylko *podmienia się pod* menedżer `venv`. W kodzie rozszerzenia:

```js
shouldUseUv = async (e, t) => (… || getConfiguration("python-envs").get("alwaysUseUv", !0)) && isUvInstalled(e)
runUV = (…) => spawnProcess("uv", …)
```

Warunkiem **koniecznym** jest wyłącznie `isUvInstalled`, czyli **`uv` widoczne w PATH** —
`alwaysUseUv` stoi po prawej stronie `||`, więc wystarczy, że zadziała pierwszy człon
(wykropkowany wyżej). Ustawienie zostawiamy na `true` dla pewności. Jeśli uv nie ma w PATH,
rozszerzenie **cicho spada do `venv` + `pip`** — bez błędu, bez ostrzeżenia. To jest
dokładnie ten tryb awarii, którego nie zauważysz, dopóki nie sprawdzisz, czym powstało `.venv`.

Jeśli terminal Ci nie aktywuje env-a automatycznie — to jest ten ostatni klucz.
`shellStartup` bywa szybsze i mniej nachalne niż domyślne `command`.

---

### `charliermarsh.ruff` — linter + formatter
Jedno rozszerzenie za black + isort + flake8 + pyupgrade + część pylinta. Napisane w Ruscie,
więc lintuje projekt szybciej, niż flake8 startuje.

**Moc, której się nie docenia:** `ruff` robi też **autofix** i **sortowanie importów**.
Nie potrzebujesz do tego osobnych rozszerzeń.

**Ustawienia** (do dopisania, jeśli chcesz pełny automat na zapis):
```jsonc
"[python]": {
  "editor.defaultFormatter": "charliermarsh.ruff",
  "editor.formatOnSave": true,
  "editor.codeActionsOnSave": {
    "source.fixAll.ruff": "explicit",        // autofix lintów
    "source.organizeImports.ruff": "explicit" // sortowanie importów
  }
}
```

Konfiguracja reguł idzie do `pyproject.toml` projektu, **nie** do settings VS Code:
```toml
[tool.ruff]
line-length = 100
target-version = "py313"

[tool.ruff.lint]
select = ["E", "F", "I", "UP", "B", "SIM"]   # I = isort, UP = pyupgrade, B = bugbear
```
To dobre miejsce, żeby zacząć — dokładasz reguły, gdy zaczną Ci przeszkadzać braki.

---

### `detachhead.basedpyright` — type checker (zamiast Pylance)
Fork pyrighta, który dokłada surowsze reguły i **odtwarza w open source funkcje,
które Microsoft trzyma wyłącznie w Pylance** (inlay hints, semantic highlighting,
docstringi w podpowiedziach).

**Dlaczego to wybraliśmy zamiast Pylance:** basedpyright jest paczką na PyPI,
więc przypinasz go jako dev-zależność projektu i **CI sprawdza dokładnie to samo,
co widzisz w edytorze**. Pylance jest zamknięty i licencyjnie przywiązany do oficjalnych
buildów VS Code — nie odtworzysz go w pipeline.

> **Pylance został celowo usunięty z tego profilu.** Wchodzi jako zależność
> `ms-python.python`, ale dwa language servery dublują diagnostykę na tym samym pliku.
> Jeśli po aktualizacji Pythona wróci — usuń go ponownie:
> `code --profile "studies_AI" --uninstall-extension ms-python.vscode-pylance`

**Ustawienie, które już masz w profilu:**
```jsonc
"basedpyright.analysis.typeCheckingMode": "standard"
```
Tryby, od najluźniejszego: `off` → `basic` → `standard` → `strict` → `recommended`.

⚠️ **Domyślny tryb basedpyrighta to `recommended`** — bardzo agresywny, krzyczy m.in. na każde
`Any`. Przy numpy/torch, gdzie stuby są niepełne, zalejesz się błędami. Dlatego ustawiony
jest `standard`. Podnieś do `strict`, gdy poczujesz, że `standard` przepuszcza za dużo.

**W projekcie** (spójność z CI):
```bash
uv add --dev basedpyright
```
```toml
[tool.basedpyright]
typeCheckingMode = "standard"
venvPath = "."
venv = ".venv"
```

**Użyteczna moc:** inlay hints pokazują wywnioskowane typy zmiennych i zwracane —
świetne do czytania cudzego kodu na labkach:
```jsonc
"basedpyright.analysis.inlayHints.variableTypes": true,
"basedpyright.analysis.inlayHints.functionReturnTypes": true
```

---

### `ms-python.debugpy` — debugger
Breakpointy, watch, call stack, debug console (możesz w niej wykonywać dowolny kod
w kontekście zatrzymanego procesu).

**Moc, o której się zapomina:**
- **Conditional breakpoints** — prawy klik na breakpoint → warunek, np. `epoch > 50 and loss > 3`.
  Ratuje życie w pętlach treningowych.
- **Logpoints** — breakpoint, który nie zatrzymuje, tylko loguje wyrażenie. `print()` bez edycji kodu.
- **Debug notebooka** — działa też w komórkach Jupytera.

Masz już w profilu `"debug.allowBreakpointsEverywhere": true`, więc postawisz breakpoint
w dowolnym pliku, nie tylko rozpoznanym jako Python.

Konfiguracja idzie do `.vscode/launch.json` w projekcie.

---

## 3. Notebooki i ML

### `ms-toolsai.jupyter` (+ `-keymap`, `-renderers`, `-cell-tags`, `-slideshow`)
Notebooki natywnie w edytorze — z pełnym IntelliSense, refaktorem i debugerem,
czego Jupyter Lab w przeglądarce nie daje.

**Skróty (`-keymap` mapuje je na te z Jupytera):**

| Skrót | Co robi |
|---|---|
| `Shift+Enter` | wykonaj komórkę, przejdź niżej |
| `Ctrl+Enter` | wykonaj, zostań |
| `Esc` potem `A` / `B` | nowa komórka nad / pod |
| `Esc` potem `DD` | usuń komórkę |
| `Esc` potem `M` / `Y` | zamień na markdown / kod |
| `Esc` potem `Z` | cofnij usunięcie komórki |

**Moc:**
- **Variable Explorer** — przycisk „Variables" na pasku notebooka: podgląd wszystkich zmiennych.
  Kliknięcie w DataFrame otwiera go w Data Wrangler.
- **Interactive Window** — możesz pisać w **zwykłym `.py`**, oznaczać bloki `# %%`
  i wykonywać je jak komórki (`Shift+Enter`). Dostajesz workflow notebooka, a w gicie
  masz czysty plik `.py` bez JSON-owego bałaganu. **Do labek, które oddajesz — mocno polecane.**
- `-cell-tags` — tagi komórek (`parameters` dla papermill, `skip` dla nbconvert).

**Ustawienia (masz już w profilu):**
```jsonc
"notebook.output.scrolling": true,        // długi output nie rozpycha notebooka
"notebook.output.textLineLimit": 50,
"notebook.formatOnSave.enabled": true
```

---

### `ms-toolsai.datawrangler` — GUI do DataFrame'ów
Otwiera DataFrame albo CSV jako arkusz: rozkłady kolumn, braki, typy — od razu widoczne.

**Moc, przez którą to nie jest zabawka:** każda operacja wyklikana w GUI
(filtr, drop, fillna, one-hot, zmiana typu) **generuje kod pandas**, który wstawiasz
do notebooka. Czyli: eksplorujesz myszką, a wychodzisz z powtarzalnym kodem.

**Jak odpalić:** przy DataFrame w Variables → ikonka Data Wrangler.
Albo prawy klik na `.csv` → `Open in Data Wrangler`.

---

### `ms-toolsai.tensorboard`
TensorBoard w zakładce edytora zamiast w przeglądarce.
`Cmd+Shift+P` → `Python: Launch TensorBoard`, wskazujesz katalog z logami.

Jeśli używasz Weights & Biases zamiast TB — to rozszerzenie możesz spokojnie wyrzucić:
```bash
code --profile "studies_AI" --uninstall-extension ms-toolsai.tensorboard
```

---

### `mechatroner.rainbow-csv`
Każda kolumna CSV innym kolorem. Brzmi trywialnie, ale przy 30 kolumnach to różnica
między „widzę" a „liczę przecinki".

**Moc:** wbudowany **RBQL** — SQL-owe zapytania na pliku CSV bez ładowania go do pandas.
`Cmd+Shift+P` → `RBQL`, potem np.:
```sql
SELECT a.name, a.score WHERE a.score > 0.8 ORDER BY a.score DESC
```
Szybki sanity check na wynikach eksperymentu bez pisania skryptu.
Dodatkowo `Align CSV` — wyrównuje kolumny do czytania.

---

## 4. Codzienna praca z kodem

### `usernamehw.errorlens`
Wyświetla błąd/ostrzeżenie **inline przy linii**, zamiast chować go w panelu Problems.
Ze wszystkich rozszerzeń tutaj to zmienia rytm pracy najbardziej — przestajesz
najeżdżać myszką na podkreślenia.

W duecie z Ruff + basedpyright: błąd typu i lint widzisz w momencie pisania.

**Ustawienia — warto przyciszyć, bo domyślnie krzyczy:**
```jsonc
"errorLens.enabledDiagnosticLevels": ["error", "warning"],  // bez info/hint
"errorLens.excludeBySource": ["cSpell", "ltex"],            // spellcheck nie w kodzie
"errorLens.messageMaxChars": 120,
"errorLens.followCursor": "activeLine"   // pokazuj tylko przy aktywnej linii
```
`followCursor` to klucz, jeśli inline wszędzie Cię rozprasza.

---

### `tamasfe.even-better-toml`
Oparty o Taplo. Podświetlanie, walidacja TOML 1.0.0, składanie tablic i —
najważniejsze — **JSON Schema dla `pyproject.toml`**: autouzupełnianie kluczy
i błąd, gdy wpiszesz nieistniejący.

Przy uv/ruff/basedpyright cała Twoja konfiguracja siedzi w `pyproject.toml`, więc to
nie jest kosmetyka.

```jsonc
"evenBetterToml.formatter.alignEntries": true,
"[toml]": { "editor.defaultFormatter": "tamasfe.even-better-toml" }
```

---

### `njpwerner.autodocstring`
Wpisujesz `"""` pod sygnaturą → generuje szkielet docstringa z argumentami,
typami i sekcją returns.

```jsonc
"autoDocstring.docstringFormat": "google",   // albo "numpy" — standard w ML
"autoDocstring.startOnNewLine": false
```
Przy pracach naukowych `numpy` bywa oczekiwany — sprawdź, czego chce prowadzący.

---

### `eamodio.gitlens`
**Moc:** `git blame` inline na końcu każdej linii — kto, kiedy, w jakim commicie.
Przy pracach grupowych (`l0X-gr-Y-...`) natychmiast wiesz, kto co dopisał.

- **File History / Line History** — historia jednej linii przez commity
- **Interactive Rebase** — GUI zamiast `git rebase -i` (którego i tak nie odpalisz z tego terminala)
- Panel Commit Graph

Masz już w Default ustawienia `gitlens.ai.model` / `gitlens.ai.vscode.model` — ale te są
przypisane do profilu Default. Jeśli chcesz je tutaj, przekopiuj do settings profilu.

---

### `mhutchie.git-graph`
Lekki, robi jedną rzecz: czytelny graf gałęzi.
`Cmd+Shift+P` → `Git Graph: View Git Graph`. Z grafu klikasz checkout, merge, cherry-pick, rebase.
Nakłada się funkcjonalnie z GitLens — jak uznasz, że to duplikat, zostaw jeden.

---

## 5. Zdalna praca

### `ms-vscode-remote.remote-ssh` (+ `-edit`, `ms-vscode.remote-explorer`)
Masz w powiązaniach `ssh-remote+black_mw`, więc to Twoja ścieżka do maszyny z GPU.

**Jak to działa — i dlaczego to nie jest zwykłe SFTP:** VS Code instaluje na zdalnej
maszynie swój serwer. Language server, debugger, terminal i rozszerzenia **działają tam**,
lokalnie masz tylko UI. Czyli basedpyright analizuje kod na maszynie, gdzie stoi torch z CUDA.

**Konsekwencja, która zaskakuje:** rozszerzenia dzielą się na *UI* (motyw, ikony — lokalnie)
i *Workspace* (Python, Jupyter — zdalnie) i te drugie **musisz zainstalować osobno na hoście**.
VS Code sam o to zapyta przy pierwszym połączeniu.

`Cmd+Shift+P` → `Remote-SSH: Connect to Host`. Hosty czyta z `~/.ssh/config`.

```jsonc
"remote.SSH.remotePlatform": { "black_mw": "linux" },
"remote.SSH.connectTimeout": 30
```

### `ms-vscode-remote.remote-containers`
To samo, ale w kontenerze z `.devcontainer/devcontainer.json`.
Sensowne, gdy projekt musi się odtworzyć u prowadzącego 1:1.

---

## 6. Pisanie: LaTeX, Markdown, YAML

### `james-yu.latex-workshop`
Pod magisterkę. Kompilacja na zapis, podgląd PDF w drugiej kolumnie,
**SyncTeX** (`Cmd+klik` w PDF skacze do źródła i odwrotnie), podgląd wzorów po najechaniu,
autouzupełnianie `\cite{}` i `\ref{}` z `.bib`.

```jsonc
"latex-workshop.latex.autoBuild.run": "onFileChange",
"latex-workshop.view.pdf.viewer": "tab",
"latex-workshop.latex.recipe.default": "lastUsed",
"latex-workshop.message.badbox.show": false   // wycisza szum o hbox/vbox
```
Domyślny „recipe" to `latexmk` — jeśli piszesz po polsku, potrzebujesz `xelatex`/`lualatex`
i wtedy `latex-workshop.latex.recipes` trzeba nadpisać.

### `ltex-plus.vscode-ltex-plus`
Sprawdzanie **gramatyki** (LanguageTool) w LaTeX-u i Markdownie — rozumie składnię,
więc nie zgłasza `\textbf{}` jako błędu.

> Oryginalny `valentjn.vscode-ltex` został **zarchiwizowany w kwietniu 2026**.
> To jest utrzymywany następca — dlatego w profilu jest `ltex-plus`, nie stary `ltex`.

```jsonc
"ltex.language": "pl-PL",                       // albo "en-US" dla tekstów po angielsku
"ltex.additionalRules.motherTongue": "pl-PL",   // wyłapuje kalki z polskiego przy pisaniu po ang.
"ltex.checkFrequency": "save"
```
`motherTongue` to najbardziej niedoceniana opcja — przy pisaniu po angielsku
wskazuje konstrukcje kalkowane z polskiego.

Nieznane słowo → żarówka → `Add to dictionary`, ląduje w `ltex.dictionary`.

### `yzhang.markdown-all-in-one`
Skróty (`Cmd+B`, `Cmd+I`), automatyczne listy i checkboxy,
**auto-generowany spis treści** (`Markdown All in One: Create Table of Contents` —
aktualizuje się przy zapisie), formatowanie tabel, eksport do HTML.

### `bierner.markdown-mermaid`
Diagramy w podglądzie MD z bloku ```` ```mermaid ````. Architektura pipeline'u,
graf modelu, flowchart eksperymentu — w tym samym pliku co notatki.

### `tomoki1207.pdf` — podgląd PDF w edytorze (papiery, wyniki kompilacji)
### `redhat.vscode-yaml` — walidacja YAML po schemacie; konfigi eksperymentów (Hydra, W&B, CI)
```jsonc
"yaml.schemas": { "https://json.schemastore.org/github-workflow.json": ".github/workflows/*" }
```

---

## 7. Wygląd

- **`catppuccin.catppuccin-vsc`** — motyw. Profil ma ustawiony wariant **Macchiato**.
  Bez tego rozszerzenia klucz `workbench.colorTheme` w settings profilu nic nie robi.
- **`pkief.material-icon-theme`** — ikony plików/folderów; rozpoznaje `.ipynb`, `.toml`, `uv.lock`.

---

## 8. Claude Code

### `anthropic.claude-code`
Claude Code w panelu VS Code. Profil ma `"claudeCode.preferredLocation": "panel"`.

Integracja z edytorem daje: kontekst zaznaczenia, diffy w natywnym widoku VS Code,
świadomość otwartych plików i diagnostyki z language serverów (czyli Claude widzi
błędy basedpyrighta i Ruff, nie tylko sam kod).

---

## 9. Wygoda i czytelność

Warstwa QoL — nic z tego nie jest niezbędne, ale każde zdejmuje jakieś drobne tarcie.

### `aaron-bond.better-comments` + `Gruntfuggly.todo-tree` — para, nie dwa osobne
**Better Comments** koloruje komentarz zależnie od prefiksu:

| Prefiks | Znaczenie | Kolor |
|---|---|---|
| `# !` | alert / ostrzeżenie | czerwony |
| `# ?` | pytanie, wątpliwość | niebieski |
| `# TODO` | do zrobienia | pomarańczowy |
| `# *` | ważne / wyróżnione | zielony |
| `# //` | zakomentowany kod | przekreślony, szary |

**Todo Tree** zbiera te znaczniki z całego projektu do drzewka w sidebarze.
Osobno oba są w połowie bezużyteczne: pierwszy koloruje, ale nie pozwala znaleźć;
drugi znajduje, ale w kodzie nic nie widać. Razem to działa.

**Zsynchronizuj im znaczniki**, bo domyślnie każdy ma swoje:
```jsonc
"todo-tree.general.tags": ["TODO", "FIXME", "HACK", "BUG", "!", "?"],
"todo-tree.highlights.defaultHighlight": { "type": "text-and-comment" }
```
Własne tagi Better Comments dostroisz przez `better-comments.tags`
(tablica obiektów: `tag`, `color`, `backgroundColor`, `bold`, `strikethrough`).

W kodzie ML sprawdza się głównie na zapiski typu `# ! ten seed daje inne wyniki na CUDA`.

---

### `KevinRose.vsc-python-indent`
Naprawia jedną konkretną wadę VS Code: po otwarciu nawiasu łamie linię o 4 spacje zamiast
wyrównać do nawiasu. Przy wywołaniach z ośmioma kwargami (`torch`, `sklearn`) przestajesz
poprawiać wcięcia ręcznie. Zero konfiguracji, po prostu działa.

---

### `dnut.rewrap-revived`
`Alt+Q` — przelewa akapit, komentarz albo docstring do zadanej szerokości linii.

> Instalowaliśmy oryginalny `stkb.rewrap`, ale ma ostatnią aktualizację z **lutego 2022**
> i nie jest podpisany — VS Code odrzuca go z `Signature verification failed: NotSigned`.
> `dnut.rewrap-revived` to utrzymywany fork (aktualizowany 2026-05).

**Gdzie to naprawdę zarabia:** proza w LaTeX-u. Akapit magisterki w jednej długiej linii daje
w gicie diff „cała linia zmieniona" przy poprawce jednego słowa. Zawinięty do 100 znaków —
diff pokazuje realną zmianę.

```jsonc
"rewrap.wrappingColumn": 100,
"rewrap.autoWrap.enabled": false   // włącz, jeśli chcesz zawijanie w trakcie pisania
```

---

### `streetsidesoftware.code-spell-checker` (+ `-polish`)
Literówki w nazwach zmiennych, stringach i komentarzach.

**Nie dubluje LTeX+:** ten sprawdza **pisownię w kodzie**, LTeX+ **gramatykę prozy**
w LaTeX-u i Markdownie. Dlatego w [sekcji 4](#4-codzienna-praca-z-kodem) Error Lens ma
`"errorLens.excludeBySource": ["cSpell", "ltex"]` — inaczej literówki zalałyby Ci
inline'y przeznaczone na błędy typów.

```jsonc
"cSpell.language": "en,pl",
"cSpell.words": ["dataloader", "logits", "softmax", "pyplot", "numpy", "argmax"]
```
Nieznane słowo → żarówka → `Add to workspace dictionary` (ląduje w `.vscode/settings.json`
projektu, więc reszta grupy też z tego korzysta).

---

### `christian-kohler.path-intellisense`
Autouzupełnianie ścieżek wewnątrz stringów — `pd.read_csv("data/…")` podpowiada pliki.
Domyślnie pomija ścieżki względne wobec katalogu głównego:
```jsonc
"path-intellisense.showHiddenFiles": true,
"path-intellisense.absolutePathToWorkspace": true
```

---

### `alefragnani.Bookmarks`
`Cmd+Alt+K` postaw/zdejmij zakładkę, `Cmd+Alt+L` skok do następnej,
`Cmd+Alt+J` do poprzedniej. Panel Bookmarks w sidebarze.

Sens w 800-liniowym `train.py`, gdzie krążysz między definicją dataloadera, pętlą treningu
i ewaluacją. Zakładki żyją w obrębie sesji workspace, nie zaśmiecają repo.

---

### `emilast.LogFileHighlighter`
Koloruje `.log` wg poziomu (ERROR / WARN / INFO / DEBUG), timestampów, liczb i stringów.
Rozpoznaje pliki po rozszerzeniu; dla innych: `Change Language Mode` → `Log`.

```jsonc
"logFileHighlighter.customPatterns": [
  { "pattern": "loss=\\d+\\.\\d+", "foreground": "#89b4fa" },
  { "pattern": "\\bnan\\b|\\binf\\b", "foreground": "#f38ba8" }
]
```
Drugi wzorzec podświetla `nan`/`inf` w logu treningu na czerwono — wyłapiesz rozjechany
gradient, przewijając plik, zamiast czytać liczby.

---

### Świadomie pominięte

- **`oderwat.indent-rainbow`** — jest w każdej liście „best of", ale przy Ruff pilnującym
  formatowania i płytkim zagnieżdżeniu Pythona to głównie szum. Warto tylko do czytania
  cudzego, niesformatowanego kodu.
- **IntelliCode** — nakłada się z Claude Code i basedpyrightem.
- **Code Runner** — `ms-python.python` robi to samo, ale z poprawnym środowiskiem z uv.
- **`github.vscode-pull-request-github`**, **`ms-vsliveshare.vsliveshare`** — sensowne przy
  repozytoriach grupowych, do dobrania później:
  `code --profile "studies_AI" --install-extension ms-vsliveshare.vsliveshare`

---

## 10. Ściąga: co ustawić najpierw

Trzy rzeczy do dopisania w `~/Library/Application Support/Code/User/profiles/68e22d86/settings.json`,
gdy już poklikasz i zobaczysz, co Ci przeszkadza:

```jsonc
// 1. Ruff jako formatter + autofix na zapis
"[python]": {
  "editor.defaultFormatter": "charliermarsh.ruff",
  "editor.codeActionsOnSave": {
    "source.fixAll.ruff": "explicit",
    "source.organizeImports.ruff": "explicit"
  }
},

// 2. Error Lens przyciszony
"errorLens.enabledDiagnosticLevels": ["error", "warning"],
"errorLens.followCursor": "activeLine",

// 3. Języki: gramatyka prozy + pisownia w kodzie
"ltex.language": "pl-PL",
"cSpell.language": "en,pl",

// 4. Wspólne znaczniki dla Better Comments i Todo Tree
"todo-tree.general.tags": ["TODO", "FIXME", "HACK", "BUG", "!", "?"],

// 5. Szerokość zawijania dla Rewrap (Alt+Q)
"rewrap.wrappingColumn": 100
```

Reszta niech zostanie domyślna, dopóki nie zaboli — łatwiej dopisać jeden klucz,
niż debugować, który z trzydziestu psuje zachowanie.

---

## 11. Dokumentacja kodu: Sphinx

Skonfigurowane i zweryfikowane w `pnw_prep` 2026-09-06 (Sphinx 9.1.0, konwencja NumPy).
Ten sam układ przenosisz do każdego kolejnego projektu.

### Zmiana modelu myślenia po Doxygenie

To główne źródło nieporozumień przy przesiadce. W Doxygenie **komentarz jest deklaratywny** —
piszesz `@param n liczba iteracji`, bo C++ sam z siebie nie mówi generatorowi wystarczająco dużo.
W Pythonie te informacje **są w kodzie**:

| Doxygen | Python |
|---|---|
| `@param x` z typem | adnotacja typu w sygnaturze |
| `@return` z typem | `-> ReturnType` |
| `/** … */` **przed** deklaracją | **docstring** *wewnątrz* obiektu |
| `@brief` / `@details` | pierwsza linia docstringa / reszta |
| `Doxyfile` | `docs/conf.py` + `pyproject.toml` |

Konsekwencja praktyczna: **nie powtarzasz typów w docstringu**. Sphinx wyciąga je z adnotacji
(`autodoc_typehints = "description"`), a basedpyright je weryfikuje. W Doxygenie `@param int n`
mógł kłamać i nikt tego nie sprawdzał — tutaj rozjazd wywala się na type checkerze.

Druga różnica: docstring żyje w runtime jako `__doc__`. `help(obj)`, `obj?` w Jupyterze,
podpowiedzi w edytorze — wszystko czyta to samo źródło. To nie jest komentarz kasowany przy
kompilacji.

### Co jest zainstalowane

Grupa `docs` w `pyproject.toml` (PEP 735) — **nie** trafia do zależności produkcyjnych:

```toml
[dependency-groups]
docs = ["sphinx>=9.1.0", "furo>=2025.12.19", "myst-parser>=5.1.0",
        "sphinx-autobuild>=2025.8.25", "sphinx-autodoc-typehints>=3.13.5",
        "sphinx-copybutton>=0.5.2"]
```

| Rozszerzenie | Rola |
|---|---|
| `sphinx.ext.autodoc` | importuje pakiet, czyta docstringi i sygnatury |
| `sphinx.ext.autosummary` | tabele-skróty i strony per obiekt |
| `sphinx.ext.napoleon` | tłumaczy docstringi NumPy/Google na rST |
| `sphinx.ext.intersphinx` | linki do dokumentacji innych projektów |
| `sphinx.ext.viewcode` | link „source” przy każdym obiekcie |
| `myst_parser` | strony w Markdownie zamiast reStructuredText |
| `furo` | motyw (domyślny Sphinksa jest brzydki) |

Pierwsze pięć jest **wbudowane w Sphinksa** — nie instalujesz ich osobno, tylko włączasz
w `extensions` w `conf.py`.

### Struktura

```
docs/
  conf.py      # cała konfiguracja
  index.md     # strona główna + toctree
  api.md       # automodule -> referencja generowana z docstringów
  _build/      # wynik (w .gitignore)
```

### Codzienny workflow

```bash
# zbuduj
uv run --group docs sphinx-build -b html docs docs/_build/html

# otwórz
open docs/_build/html/index.html

# tryb "watch" — serwer z auto-reloadem (zainstalowany)
uv run --group docs sphinx-autobuild --watch src --open-browser docs docs/_build/html
```

`sphinx-autobuild` to odpowiednik `mkdocs serve`: trzyma serwer na `127.0.0.1:8000`,
przebudowuje przy każdej zmianie i przeładowuje stronę w przeglądarce przez websocket.

> ⚠️ **`--watch src` jest obowiązkowe, nie ozdobne.** W `--help` flaga opisana jest jako
> *„additional directories to watch"* — domyślnie autobuild pilnuje **wyłącznie katalogu
> źródłowego dokumentacji**, czyli `docs/`. A Ty edytujesz docstringi w `src/`.
> Bez tej flagi zmiana docstringa **nie wywoła przebudowy** i będziesz się zastanawiał,
> czemu strona się nie odświeża. Z flagą: zmierzone ~1 s od zapisu do przeładowania.

Przydatne flagi: `--port 8765` (gdy 8000 zajęte), `--open-browser`, `--no-initial`
(pomija pierwszy build), `--ignore '*.tmp'`.

**Traktuj ostrzeżenia jak błędy** (przydatne w CI):
```bash
uv run --group docs sphinx-build -b html -W --keep-going docs docs/_build/html
```

### Konwencja NumPy

To jest standard scientific Pythona — numpy, scipy, scikit-learn, pandas.
Ustaw `"autoDocstring.docstringFormat": "numpy"` w settings profilu, żeby
`njpwerner.autodocstring` generował od razu w tej konwencji.

```python
def train(model: nn.Module, epochs: int = 10) -> dict[str, float]:
    """Trenuje model i zwraca metryki walidacyjne.

    Dłuższy opis, jeśli potrzebny — trafia do sekcji "details" na stronie.

    Parameters
    ----------
    model
        Sieć do wytrenowania. Typu NIE powtarzaj — Sphinx bierze go z adnotacji.
    epochs
        Liczba epok.

    Returns
    -------
    dict[str, float]
        Metryki walidacyjne po ostatniej epoce.

    Raises
    ------
    ValueError
        Gdy ``epochs < 1``.

    Notes
    -----
    Wzory LaTeX-owe działają dzięki ``sphinx.ext.mathjax``:

    .. math:: \\mathcal{L} = -\\sum_i y_i \\log \\hat{y}_i

    Examples
    --------
    >>> train(model, epochs=3)
    {'acc': 0.91, 'loss': 0.23}
    """
```

Sekcje, których faktycznie używasz: `Parameters`, `Returns`, `Raises`, `Notes`,
`Examples`, `References`, `See Also`. `Examples` w formacie doctestu ma bonus —
`pytest --doctest-modules` wykona je jako testy.

### Ruff pilnuje docstringów

Odpowiednik `WARN_NO_PARAMDOC` z Doxygena, tylko lepszy: działa w edytorze przez Error Lens,
a nie dopiero przy generowaniu.

```toml
[tool.ruff.lint]
select = ["E", "F", "I", "UP", "B", "SIM", "D"]   # D = pydocstyle

[tool.ruff.lint.pydocstyle]
convention = "numpy"

[tool.ruff.lint.per-file-ignores]
"tests/*" = ["D"]          # w testach docstringi to narzut
"docs/conf.py" = ["D100"]
```

To jest najważniejsza część całego setupu. Generator postawisz w jedno popołudnie —
częścią, która się sypie, jest niespójność docstringów w miarę rośnięcia projektu.

### intersphinx — czego mkdocstrings nie dorównuje

W `conf.py` masz zmapowane python / numpy / pandas / sklearn / torch / matplotlib.
Efekt: `np.ndarray` albo `torch.Tensor` w docstringu staje się **klikalnym linkiem
do oficjalnej dokumentacji** tych bibliotek. Nic nie musisz robić poza wpisaniem typu.

Przy pierwszym buildzie Sphinx pobiera pliki `objects.inv` z każdej z tych domen —
dlatego pierwsze uruchomienie trwa dłużej i wymaga sieci.

### Rozbudowa, gdy projekt urośnie

| Potrzeba | Czym |
|---|---|
| Automatyczne strony dla **każdego** modułu | `autosummary` z `:recursive:` i szablonem w `_templates/` |
| Notebooki jako rozdziały dokumentacji | `uv add --group docs myst-nb` |
| **PDF** z tej samej treści | `sphinx-build -b latex` → `latexmk -pdf` (masz już TeX-a pod magisterkę) |
| Galeria przykładów ze skryptów | `sphinx-gallery` |
| Publikacja | GitHub Pages przez workflow albo Read the Docs |

### Rozszerzenie VS Code (opcjonalne)

`swyddfa.esbonio` (v2.1.0, aktualizowany 2026-06) — language server dla Sphinksa:
podgląd na żywo, autouzupełnianie dyrektyw i ról, skok do definicji w `toctree`.
Sensowne, jeśli będziesz dużo pisał w rST. Przy pisaniu stron w Markdownie (MyST)
zysk jest mniejszy — dlatego nie ma go domyślnie w profilu:

```bash
code --profile "studies_AI" --install-extension swyddfa.esbonio
```

---

## 12. Ubuntu — czym się różni

Odtworzenie profilu na `black_mw` 2026-09-07. Poniżej wyłącznie rzeczy, które **nie przeniosły
się 1:1** — reszta dokumentu obowiązuje bez zmian.

### Tworzenie profilu z CLI: pułapka

`code --profile "studies_AI" --install-extension …` **nie zadziała, dopóki profil nie istnieje** —
kończy się `Profile 'studies_AI' not found.`. Wbrew intuicji flaga `--profile` tworzy profil
**tylko przy otwieraniu folderu**, co pomoc CLI mówi wprost: *„Opens the provided folder or
workspace with the given profile… If the profile does not exist, a new empty one is created."*

Kolejność, która działa — pierwsza komenda przy okazji zapisuje powiązanie folder→profil:

```bash
code --profile "studies_AI" ~/Documents/pnw_prep     # tworzy profil + wiąże folder
code --profile "studies_AI" --install-extension ms-python.python
```

### Ścieżki

| macOS | Ubuntu |
|---|---|
| `~/Library/Application Support/Code/User/` | `~/.config/Code/User/` |
| `~/Library/Application Support/Code/User/profiles/68e22d86/` | `~/.config/Code/User/profiles/407f9a50/` |

`~/.vscode/extensions` jest w tym samym miejscu na obu systemach i jest **wspólne dla
wszystkich profili** — dopięcie rozszerzenia do profilu nic nie pobiera.

### Wersje: kanał stabilny vs pre-release

Zapytanie do Marketplace API (`flags=914`) zwraca też wersje **pre-release**, więc numery
z niego bywają wyraźnie wyższe niż to, co instaluje VS Code:

| Rozszerzenie | API (pre-release) | Zainstalowane (stabilne) |
|---|---|---|
| `ms-python.python` | 2026.7.2026082601 | 2026.4.0 |
| `eamodio.gitlens` | 2026.9.50513 | 19.1.0 |
| `ms-toolsai.jupyter` | 2026.6.2026071501 | 2025.9.1 |

To **nie jest** nieaktualna instalacja — `--update-extensions` odpowiada `No extension to update`.
Nie „naprawiaj" tego ręcznie.

### LaTeX: brakujący `latexmk`

Są `texlive-base`, `texlive-latex-extra`, `texlive-xetex` (czyli `xelatex` i `pdflatex` działają),
ale **nie ma `latexmk`**, a to jest domyślny recipe LaTeX Workshopa — kompilacja wywali się
przy pierwszym zapisie:

```bash
sudo apt install latexmk
```

### Remote-SSH stracił sens

Dokument zakładał `ssh-remote+black_mw` jako drogę do GPU. Na tej maszynie GPU jest **lokalne**
(RTX 5080, driver 580.178.04, CUDA 12.9 w PATH), a `~/.ssh/config` nie istnieje.
Rozszerzenia remote zostają w profilu na przyszłość, ale dziś nic nie obsługują.

### Środowisko: conda usunięta

`~/miniconda3` (31 GB, 10 środowisk) **usunięte** 2026-09-07 przy przesiadce na uv — conda
siedziała w PATH **przed** `~/.local/bin`, więc panel Python Environments podsuwałby jej
środowiska obok `.venv`. Bloki `conda initialize` wycięte z `~/.zshrc` i `~/.bashrc`.

Listy pakietów zachowane w `~/conda_backup_20260907/` (patrz README tamże). Uwaga przy
odtwarzaniu: **7 z 10 środowisk było uszkodzonych** — miały pakiety w `site-packages`, ale
żadnej binarki `python` w `bin/`, przez co `conda env export` zwracał dla nich pustkę,
a `conda run -n <env>` po cichu wykonywał się w `base`. Wiarygodne są pliki
`*.packages.txt` (czytane wprost z `dist-info`), nie `*.yml`.

### Settings Sync miesza między maszynami

Sync jest **włączony** i ściąga profil Default z Maca. Widać to gołym okiem: po starcie
VS Code `cmake.environment` w `~/.config/Code/User/settings.json` wraca do ścieżek
`/Users/mateuszwojtaszek/…darwin-arm64`, nadpisując linuksowe. W settings Default siedzą też
`parallels-desktop.*`, `/opt/homebrew/*` i `idf.*` z Maca.

Profilu `studies_AI` z Maca **w chmurze nie ma** (sync profili zawiera tylko „Agents"), więc
`407f9a50` jest lokalny i to on jest wypychany w górę. Skutek uboczny: `window.newWindowProfile:
"studies_AI"` przyszło z Maca samo, bez ustawiania.

Decyzja, czy zostawić sync włączony, jest otwarta — patrz `CLAUDE.md`.

---

## Awaryjnie

```bash
# co jest w profilu
code --profile "studies_AI" --list-extensions --show-versions

# Pylance wrócił jako zależność Pythona i dubluje basedpyrighta
code --profile "studies_AI" --uninstall-extension ms-python.vscode-pylance

# --- macOS: cofnięcie całego setupu profili (VS Code MUSI być zamknięty) ---
cp ~/Library/Application\ Support/Code/User/_backup_20260906_193317/settings.json \
   ~/Library/Application\ Support/Code/User/settings.json
cp ~/Library/Application\ Support/Code/User/_backup_20260906_193317/storage.json \
   ~/Library/Application\ Support/Code/User/globalStorage/storage.json

# --- Ubuntu: odpięcie profilu bez kasowania go ---
# w GUI: Profiles: Reset Workspace Profiles Associations
# ręcznie: usuń wpis 407f9a50 z profileAssociations w
#   ~/.config/Code/User/globalStorage/storage.json
```

---

## Źródła

- [Python Environments Extension GA — Microsoft for Python Developers Blog](https://devblogs.microsoft.com/python/python-in-visual-studio-code-february-2026-release/)
- [Python environments in VS Code — dokumentacja](https://code.visualstudio.com/docs/python/environments)
- [How to configure VS Code for a uv project — pydevtools](https://pydevtools.com/handbook/how-to/how-to-configure-vs-code-for-a-uv-project/)
- [basedpyright — GitHub](https://github.com/DetachHead/basedpyright)
- [LTeX+ — dokumentacja i ustawienia](https://ltex-plus.github.io/ltex-plus/settings.html)
- [Even Better TOML — Marketplace](https://marketplace.visualstudio.com/items?itemName=tamasfe.even-better-toml)
