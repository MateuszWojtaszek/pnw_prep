# Start na Ubuntu — kolejność kroków

Stan na 2026-09-07. Wszystko poniżej wykonujesz **na Ubuntu**. Kroki są w kolejności
zależności — 2 jest tańszy teraz niż za tydzień, 3 naprawia szkodę, którą widać na żywo.
Po każdym kroku jest weryfikacja; jeśli nie przechodzi, nie idź dalej.

---

## 0. Pobierz zmiany

```bash
cd ~/Documents/pnw_prep && git pull
```

Powinny przyjechać: ten plik, poprawki liczb rozszerzeń w `VSCODE_studies_AI.md`
i poprawka warunku `alwaysUseUv` w sekcji 2.

---

## 1. Odblokowanie pracy

Dwie rzeczy, bez których projekt nie działa tak, jak go opisaliśmy.

```bash
sudo apt install -y latexmk

uv add --dev ruff basedpyright
```

**Dlaczego `uv add`, skoro w edytorze działa:** cały udokumentowany powód wyboru
basedpyrighta zamiast Pylance'a brzmiał „da się przypiąć jako dev-zależność i CI sprawdza
dokładnie to samo, co edytor". Dziś ani ruff, ani basedpyright nie są w grafie zależności —
działają wyłącznie binarki wożone przez rozszerzenia. To je domyka.

**Weryfikacja:**

```bash
uv run ruff check .          # oczekiwane: All checks passed!
uv run basedpyright --version
which latexmk
```

**Zacommituj** — to zmiana zależności projektu:

```bash
git add pyproject.toml uv.lock && git commit -m "dev deps: ruff, basedpyright" && git push
```

---

## 2. Zrównaj ścieżkę repo z Makiem

Na Macu repo leży w `~/Documents/projects/masters/pnw_prep`, na Ubuntu w `~/Documents/pnw_prep`.
Rozjazd kosztuje w dwóch miejscach: pamięć Claude Code jest kluczowana **ścieżką bezwzględną**
projektu, a `CLAUDE.md` wskazuje na `~/Documents/projects/masters/VSCODE_studies_AI.md`,
którego pod tą ścieżką nie ma.

> ⚠️ **Powiązanie folder→profil VS Code też jest kluczowane ścieżką.** Sam `mv` je zerwie
> i nowy folder otworzy się w profilu `Default`. Druga komenda przepina je z powrotem.

```bash
mkdir -p ~/Documents/projects/masters
mv ~/Documents/pnw_prep ~/Documents/projects/masters/pnw_prep
code --profile "studies_AI" ~/Documents/projects/masters/pnw_prep
```

**Weryfikacja:** otwórz nowe okno na tym folderze i sprawdź, czy pasek statusu pokazuje
profil `studies_AI`, a nie `Default`.

Stary wpis w `profileAssociations` będzie wskazywał martwą ścieżkę. Nieszkodliwe;
do sprzątnięcia przez `Profiles: Reset Workspace Profiles Associations` albo ręcznie
w `~/.config/Code/User/globalStorage/storage.json`.

---

## 3. Wyłącz Settings Sync

Sync ściąga profil `Default` z Maca i **na żywo nadpisuje linuksowe ścieżki macowymi** —
`cmake.environment` wraca do `/Users/mateuszwojtaszek/…darwin-arm64` po każdym starcie.
Profilu `studies_AI` w chmurze nie ma, więc sync nic tu nie wnosi, a szkodzi.

W VS Code: `Ctrl+Shift+P` → **`Settings Sync: Turn Off`**.
W oknie dialogowym **nie zaznaczaj** kasowania danych w chmurze — Mac ma z nich dalej korzystać.

> ⚠️ **`window.newWindowProfile` przyszło z Maca przez sync, nie zostało ustawione lokalnie.**
> Po wyłączeniu synchronizacji może zniknąć. Sprawdź i w razie czego wpisz ręcznie.

```bash
grep -n "newWindowProfile" ~/.config/Code/User/settings.json
```

Jeśli pusto — dodaj do `~/.config/Code/User/settings.json` (to plik profilu `Default`,
bo klucz ma scope `application`):

```jsonc
"window.newWindowProfile": "studies_AI"
```

**Sprzątnięcie po synchronizacji** — obejrzyj, co przyjechało z Maca, i usuń, co nie ma
sensu na Linuksie:

```bash
grep -n "mateuszwojtaszek\|homebrew\|parallels\|idf\." ~/.config/Code/User/settings.json
```

**Weryfikacja:** zrestartuj VS Code i powtórz `grep` — wpisy mają nie wracać.

---

## 4. Claude Code

```bash
mkdir -p ~/.claude
```

Utwórz `~/.claude/CLAUDE.md` z treścią z **Załącznika A** — to twoje globalne zasady
(zakaz gotowców, tło z C++, wymóg dawania opcji). Bez tego Claude na Ubuntu będzie
pisał kod za ciebie.

`~/.claude/settings.json` — dwa klucze:

```json
{ "model": "opus", "tui": "fullscreen" }
```

**Pamięć projektu (opcjonalnie).** Katalog pamięci nazywa się ścieżką projektu
z zamienionymi `/` na `-`. Policz go i utwórz:

```bash
cd ~/Documents/projects/masters/pnw_prep
python3 -c "import os; print(os.getcwd().replace('/','-'))"
mkdir -p ~/.claude/projects/$(python3 -c "import os; print(os.getcwd().replace('/','-'))")/memory
```

Zawartość (8 notatek + `MEMORY.md`) przenieś z Maca, jeśli chcesz, ale **traktuj pamięć
jak cache** — trwałe ustalenia i tak są w `CLAUDE.md` w repo, który jedzie z gitem.
Nie kopiuj `history.jsonl`, `sessions/`, `shell-snapshots/` ani transkryptów: to stan
lokalny maszyny, pełen macowych ścieżek.

---

## 5. Weryfikacja końcowa

Wszystko musi przejść:

```bash
cd ~/Documents/projects/masters/pnw_prep
uv run ruff check .                                   # All checks passed!
uv run basedpyright --version
which uv latexmk
nvidia-smi --query-gpu=name,driver_version --format=csv,noheader
code --profile "studies_AI" --list-extensions | wc -l  # 42
test -f ~/.claude/CLAUDE.md && echo "global CLAUDE.md ok"
git status --short                                     # czysto
```

---

## 6. Pierwsze zadanie: etap 1 z planu

Środowisko stoi, ale **projekt nadal nie ma torcha, Hydry ani MLflow** —
`dependencies = []` w `pyproject.toml`. To jest pierwsza rzecz z etapu 1.

Przy torchu pamiętaj: domyślne koło z PyPI nie wystarczy, bo 5080 to Blackwell (sm_120)
i potrzebny jest build `cu128+`. W `uv` robi się to przez zadeklarowanie osobnego indeksu
(`[[tool.uv.index]]`) i przypięcie do niego pakietu w `[tool.uv.sources]` — **nie** przez
`pip install` do venva obok `uv.lock`.

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
