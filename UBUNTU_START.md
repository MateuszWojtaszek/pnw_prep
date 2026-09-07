# Start na Ubuntu — kolejność kroków

Stan na **2026-09-07, po weryfikacji na maszynie**. Pierwsza wersja tego pliku zakładała
maszynę świeżo po `git clone`; część kroków jest już wykonana, a jeden z nich (przeniesienie
repo) zostawił po sobie szkodę, której ówczesna weryfikacja nie wyłapała.

Kroki są w kolejności zależności. Po każdym jest weryfikacja; jeśli nie przechodzi, nie idź dalej.

---

## Zrobione — zweryfikowane, nie powtarzaj

| Krok | Stan | Dowód |
|---|---|---|
| Repo pod ścieżką z Maca | ✅ | `~/Documents/projects/masters/pnw_prep`, stary katalog nie istnieje |
| Powiązanie folder → profil `studies_AI` | ✅ | `profileAssociations` → `407f9a50` dla nowej ścieżki |
| `latexmk` | ✅ | `/usr/bin/latexmk` |
| `ruff` + `basedpyright` jako dev-zależności | ✅ | grupa `dev` w `pyproject.toml`, commit `cdc7453` wypchnięty |
| Settings Sync wyłączony | ✅ | `sync.enable = false` w `state.vscdb` |
| `window.newWindowProfile` | ✅ | linia 34 w `~/.config/Code/User/settings.json` |
| `~/.claude/settings.json` | ✅ | `model: opus[1m]`, `tui: fullscreen` + `effortLevel`, `theme` |
| Katalog pamięci projektu | ✅ | `~/.claude/projects/-home-black-mw-Documents-projects-masters-pnw-prep/memory` (pusty) |
| Sterownik GPU | ✅ | RTX 5080, 580.178.04 |
| 42 rozszerzenia w profilu | ✅ | `code --profile studies_AI --list-extensions \| wc -l` |

---

## 1. Napraw `.venv` po przeniesieniu repo — **blokujące**

`mv` z poprzedniej wersji kroku 2 przeniósł też `.venv`. Launchery w `.venv/bin/` mają
**bezwzględny shebang** wskazujący na starą ścieżkę, więc dziś 39 z nich jest martwych:

```
#!/home/black-mw/Documents/pnw_prep/.venv/bin/python3   ← katalog już nie istnieje
```

Objaw: `uv run basedpyright --version` → `Failed to spawn: basedpyright (os error 2)`,
`sphinx-build` → `bad interpreter`. Plik **istnieje**, brakuje interpretera z shebanga —
stąd mylący komunikat.

**Dlaczego poprzednia weryfikacja tego nie złapała:** `ruff` to natywna binarka bez shebanga
i działa mimo przeniesienia. `uv run ruff check .` przechodziło, więc krok 1 wyglądał na zaliczony,
a `uv run basedpyright --version` uruchomiłeś dopiero po `mv`. `uv sync` tego nie naprawia —
porównuje metadane pakietów, nie ścieżki w launcherach („Checked 48 packages", zero zmian).

```bash
cd ~/Documents/projects/masters/pnw_prep
rm -rf .venv
uv sync --all-groups
```

Venv jest w całości odtwarzalny z `uv.lock` i jest w `.gitignore` — kasowanie go nic nie kosztuje.
Na przyszłość: przenosisz repo → od razu odtwarzasz venva, nie migrujesz go.

**Weryfikacja — wszystkie trzy muszą przejść:**

```bash
uv run ruff check .            # All checks passed!
uv run basedpyright --version  # numer wersji, nie "Failed to spawn"
uv run sphinx-build --version  # sprawdza grupę docs, też była zepsuta
```

---

## 2. Globalne `~/.claude/CLAUDE.md`

Jedyny brakujący plik konfiguracyjny. `~/.claude/settings.json` już jest, ale reguł
(zakaz gotowców, tło z C++, wymóg dawania opcji) nadal nie ma — do tego czasu obowiązuje
sekcja „Jak ze mną pracować" z repo, która jest ich zawężoną kopią.

Utwórz `~/.claude/CLAUDE.md` z treścią z **Załącznika A**.

**Weryfikacja:**

```bash
test -f ~/.claude/CLAUDE.md && echo "global CLAUDE.md ok"
```

Po utworzeniu można skrócić notkę w `CLAUDE.md` w repo („Globalne instrukcje leżą na Macu…") —
przestaje być prawdziwa.

---

## 3. Sprzątanie po Macu — kosmetyka, nie blokuje

Sync jest wyłączony, więc te wpisy już nie wracają, ale przyjechały wcześniej i zostały
w `~/.config/Code/User/settings.json` (profil `Default`). Wszystkie wskazują na ścieżki,
których na Linuksie nie ma:

```bash
grep -n "mateuszwojtaszek\|homebrew\|parallels\|idf\." ~/.config/Code/User/settings.json
```

Dziś to 16 linii w trzech grupach:

- `idf.*` (ESP-IDF) — ścieżki `/Users/mateuszwojtaszek/esp/…`, `/opt/homebrew/opt/python@3.13`
- `parallels-desktop.*` — Parallels na Linuksie nie istnieje, cała sekcja do usunięcia
- `cmake.environment` / `cmake.configureArgs` / `cmake.additionalCompilerSearchDirs` —
  wskazują na `…-darwin-arm64` i `/opt/homebrew/opt/llvm`

Usuń, co nie ma sensu na Linuksie. Wpisy embedded odtworzysz lokalnymi ścieżkami, kiedy
faktycznie będziesz wracał do STM32 na tej maszynie — nie rób tego teraz.

Dwa martwe wpisy do sprzątnięcia przy okazji (oba nieszkodliwe):

- `profileAssociations` ma wciąż `file:///home/black-mw/Documents/pnw_prep` → `407f9a50`.
  `Profiles: Reset Workspace Profiles Associations` albo ręcznie w
  `~/.config/Code/User/globalStorage/storage.json`.
- `~/.claude/projects/-home-black-mw-Documents-pnw-prep/` — pamięć kluczowana starą ścieżką.
  Nowy katalog już istnieje i jest pusty, więc przenosić nie ma czego; stary możesz skasować.

**Weryfikacja:** zrestartuj VS Code i powtórz `grep` — wpisy mają nie wracać.

---

## 4. Weryfikacja końcowa

Wszystko musi przejść:

```bash
cd ~/Documents/projects/masters/pnw_prep
uv run ruff check .                                    # All checks passed!
uv run basedpyright --version
uv run sphinx-build --version
which uv latexmk
nvidia-smi --query-gpu=name,driver_version --format=csv,noheader
code --profile "studies_AI" --list-extensions | wc -l  # 42
test -f ~/.claude/CLAUDE.md && echo "global CLAUDE.md ok"
git status --short                                     # czysto
```

---

## 5. Pierwsze zadanie: etap 1 z planu

Środowisko stoi, ale **projekt nadal nie ma torcha, Hydry ani MLflow** —
`dependencies = []` w `pyproject.toml`. To jest pierwsza rzecz z etapu 1.

Przy torchu pamiętaj: domyślne koło z PyPI nie wystarczy, bo 5080 to Blackwell (sm_120)
i potrzebny jest build `cu128+`. W `uv` robi się to przez zadeklarowanie osobnego indeksu
(`[[tool.uv.index]]`) i przypięcie do niego pakietu w `[tool.uv.sources]` — **nie** przez
`pip install` do venva obok `uv.lock`.

Otwartą decyzją zakresową pozostaje dataset: **PanNuke** to propozycja czekająca na twoje
potwierdzenie (punkt 4 „decyzji zamkniętych" w `CLAUDE.md`) — bez niej etap 1 nie ma czego wczytać.

Kryterium ukończenia etapu 1: widzisz obok siebie patch i jego maskę instancyjną,
a MLflow zalogował pusty przebieg.

---

## Załącznik A — treść `~/.claude/CLAUDE.md`

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
