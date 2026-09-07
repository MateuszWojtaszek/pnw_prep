# Start na Ubuntu — kolejność kroków

Stan na **2026-09-07, wieczór**. Setup jest **domknięty** — poniżej został jeden drobiazg
kosmetyczny i właściwa robota (etap 1). Plik zostaje w repo jako ślad tego, co i dlaczego
zostało zrobione, oraz jako instrukcja odtworzenia na kolejnej maszynie.

---

## Zrobione — zweryfikowane, nie powtarzaj

| Krok | Dowód |
|---|---|
| Repo pod ścieżką z Maca | `~/Documents/projects/masters/pnw_prep`, stary katalog nie istnieje |
| Powiązanie folder → profil `studies_AI` | `profileAssociations` → `407f9a50` dla nowej ścieżki |
| `latexmk` | `/usr/bin/latexmk` |
| `ruff` + `basedpyright` jako dev-zależności | grupa `dev` w `pyproject.toml`, commit `cdc7453` |
| **`.venv` odtworzony po przeniesieniu repo** | `rm -rf .venv && uv sync --all-groups`, patrz niżej |
| Settings Sync wyłączony | `sync.enable = false` w `state.vscdb` |
| `window.newWindowProfile` | `~/.config/Code/User/settings.json` |
| Macowe wpisy w `settings.json` profilu `Default` | 19 linii usuniętych, backup `settings.json.bak-20260907` |
| `~/.claude/CLAUDE.md` | globalne reguły z Załącznika A na miejscu |
| `~/.claude/settings.json` | `model: opus[1m]`, `tui: fullscreen`, `effortLevel`, `theme` |
| Katalog pamięci projektu | `~/.claude/projects/-home-black-mw-Documents-projects-masters-pnw-prep/memory` |
| Sterownik GPU | RTX 5080, 580.178.04 |
| 42 rozszerzenia w profilu | `code --profile studies_AI --list-extensions \| wc -l` |

### Pułapka, która kosztowała najwięcej: `.venv` nie przeżywa `mv`

Przeniesienie repo z `~/Documents/pnw_prep` zabrało ze sobą `.venv`, a launchery
w `.venv/bin/` mają **bezwzględny shebang**:

```
#!/home/black-mw/Documents/pnw_prep/.venv/bin/python3   ← katalog już nie istniał
```

39 martwych skryptów: `basedpyright` → `Failed to spawn (os error 2)`, `sphinx-build` →
`bad interpreter`. Plik istnieje, brakuje **interpretera z shebanga** — stąd mylący komunikat.

Dwie rzeczy, które to przepuściły:

- `ruff` to natywna binarka bez shebanga i działa mimo przeniesienia, więc `uv run ruff check .`
  przechodziło i cały krok wyglądał na zaliczony;
- `uv sync` tego **nie naprawia** — porównuje metadane pakietów, nie ścieżki w launcherach
  („Checked 48 packages", zero zmian).

Lekcja na przyszłość: **przenosisz repo → od razu `rm -rf .venv && uv sync --all-groups`.**
Venv jest w `.gitignore` i w całości odtwarzalny z `uv.lock`, więc kasowanie nic nie kosztuje.

### Co dokładnie wyleciało z `settings.json`

Rozszerzenia ESP-IDF i STM32 **są** zainstalowane na Ubuntu, więc macowe ścieżki były
aktywnie zepsute, nie tylko martwe:

- `idf.espIdfPath`, `idf.toolsPath`, `idf.pythonInstallPath` — `/Users/…`, `/opt/homebrew/…`
- `STM32VSCodeExtension.projectCreator.executablePath` (`/Applications/…app/Contents/MacOS`)
  i `.cubeCLT.path` (`/opt/ST/…`, na tej maszynie nie istnieje), wraz z blokiem
  `workbench.settings.applyToAllProfiles`, który już tylko na nie wskazywał
- cały `parallels-desktop.*` — rozszerzenia nie ma i na Linuksie być nie może
- `cmake.environment` / `cmake.configureArgs` / `cmake.additionalCompilerSearchDirs` —
  `darwin-arm64`, `/opt/homebrew/opt/llvm`

**Zostawione świadomie:** `idf.gitPath: "git"` (poprawne na Linuksie) oraz `idf.telemetry`,
`idf.showOnboardingOnInit`, `idf.enableStatusBar` — to preferencje zachowania, nie ścieżki;
kasowanie ich odblokowałoby telemetrię przy powrocie do ESP-IDF.

Ścieżki embedded odtworzysz lokalnie, kiedy faktycznie wrócisz do STM32 na tej maszynie.

---

## 1. Ostatni drobiazg — martwe wpisy po starej ścieżce

Nieszkodliwe, nic nie blokują.

```bash
# transkrypt sesji sprzed przeniesienia repo, pod starym kluczem ścieżki
mv ~/.claude/projects/-home-black-mw-Documents-pnw-prep/*.jsonl \
   ~/.claude/projects/-home-black-mw-Documents-projects-masters-pnw-prep/
rm -rf ~/.claude/projects/-home-black-mw-Documents-pnw-prep
```

Drugi wpis to `file:///home/black-mw/Documents/pnw_prep` w `profileAssociations`.
**Wymaga zamkniętego VS Code** — przy działającym edytorze plik jest nadpisywany stanem
z pamięci przy wyjściu, więc zewnętrzna edycja przepada:

```bash
# dopiero po zamknięciu VS Code
python3 - <<'EOF'
import json, pathlib
p = pathlib.Path.home()/'.config/Code/User/globalStorage/storage.json'
d = json.loads(p.read_text())
ws = d['profileAssociations']['workspaces']
ws.pop('file:///home/black-mw/Documents/pnw_prep', None)
p.write_text(json.dumps(d))
EOF
```

Alternatywa z palety: `Profiles: Reset Workspace Profiles Associations` — ale to czyści
**wszystkie** powiązania, więc trzeba potem na nowo otworzyć projekt w `studies_AI`.

---

## 2. Weryfikacja — stan bieżący, wszystko przechodzi

```bash
cd ~/Documents/projects/masters/pnw_prep
uv run ruff check .                                    # All checks passed!
uv run basedpyright                                    # 0 errors, 0 warnings, 0 notes
uv run sphinx-build --version                          # 9.1.0 — pokrywa grupę docs
which uv latexmk
nvidia-smi --query-gpu=name,driver_version --format=csv,noheader
code --profile "studies_AI" --list-extensions | wc -l  # 42
test -f ~/.claude/CLAUDE.md && echo "global CLAUDE.md ok"
git status --short                                     # czysto
```

---

## 3. Właściwa robota: etap 1 z planu

Środowisko stoi, ale **projekt nadal nie ma torcha, Hydry ani MLflow** —
`dependencies = []` w `pyproject.toml`.

Warunek wejścia, wciąż otwarty: **decyzja o datasecie.** PanNuke to propozycja czekająca
na potwierdzenie (punkt 4 „decyzji zamkniętych" w `CLAUDE.md`) — bez niej etap 1 nie ma
czego wczytać.

Przy torchu pamiętaj: domyślne koło z PyPI nie wystarczy, bo 5080 to Blackwell (sm_120)
i potrzebny jest build `cu128+`. W `uv` robi się to przez zadeklarowanie osobnego indeksu
(`[[tool.uv.index]]`) i przypięcie do niego pakietu w `[tool.uv.sources]` — **nie** przez
`pip install` do venva obok `uv.lock`.

Kryterium ukończenia etapu 1: widzisz obok siebie patch i jego maskę instancyjną,
a MLflow zalogował pusty przebieg.

---

## Załącznik A — treść `~/.claude/CLAUDE.md` (już zastosowana)

````markdown
# Instrukcje

## 1. Twoja Rola

Jesteś moim technicznym asystentem. Twój główny cel to **POMAGAĆ mi w rozwiązywaniu zadań,
a nie wykonywać je za mnie**. Masz mnie uczyć, naprowadzać i korygować moje błędy,
zmuszając mnie do samodzielnego myślenia i pisania kodu.

Dopasowujesz się do technologii, o której aktualnie rozmawiamy — Python, SQL, Docker, Git,
architektura systemów czy cokolwiek innego.

## 2. Mój Profil i Kontekst

- **Doświadczenie:** Programuję od dłuższego czasu w różnych technologiach. Rozumiem
  koncepcje programowania (pętle, struktury danych, OOP, wzorce projektowe), nie musisz
  mi tłumaczyć podstaw informatyki.
- **Główne braki:** Nie zawsze znam idiomatyczne sposoby rozwiązywania problemów w danej
  technologii, jej wbudowane narzędzia, biblioteki standardowe i najlepsze praktyki.
  To jest właśnie to, czego od Ciebie potrzebuję.

## 3. Główne Zasady Działania (CRITICAL)

- **ZAKAZ GOTOWCÓW:** Nigdy nie generuj gotowego rozwiązania mojego problemu (nie pisz
  za mnie pełnych funkcji, klas, zapytań, konfiguracji), chyba że wyraźnie o to poproszę
  używając komendy `zrób to za mnie`.
- **Naprowadzaj:** Jeśli moje podejście jest błędne od podstaw, poinformuj mnie i naprowadź.
- **Proponuj metody:** Często poruszam się w technologi której nie znam i nie znam np.
  metod w bibliotekach
- **Nie tłumacz oczywistości:** Nie wyjaśniaj mi, czym jest pętla, zmienna, klasa,
  interfejs itp. Skup się na tym, co specyficzne dla danej technologii.

## 4. Komendy Sterujące

| Komenda | Działanie |
|---|---|
| `zrób to za mnie` | Wyjątek od zakazu — generujesz pełne, gotowe rozwiązanie. |
````
