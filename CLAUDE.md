# pnw_prep — projekt rozgrzewkowy przed magisterką

Pętla **active learning** do segmentacji instancyjnej jąder komórkowych, na prostym
modelu i małym zbiorze. Cztery tygodnie od **2026-09-06**.

**Celem nie jest wynik ani infrastruktura, tylko zdjęcie ryzyka metodycznego** przed
właściwą magisterką (Fuzzy IT2 Active Learning dla segmentacji jąder). Jeśli jakaś
propozycja poprawia produkt, a nie zmniejsza ryzyka metodycznego — jest poza zakresem.

Pełny opis z rysunkami, planem i literaturą:
https://claude.ai/code/artifact/970c01fc-4968-435d-a7c9-38718e19762c

---

## Jak ze mną pracować

**Nie pisz za mnie kodu.** Naprowadzaj, proponuj metody i biblioteki, koryguj błędne
podejście — ale rozwiązanie mam napisać sam. Wyjątek wyłącznie na komendę
`zrób to za mnie`.

Przychodzę z C++/embedded (STM32, ESP-IDF, CMake, Doxygen). Koncepcji programowania
nie tłumacz. Tłumacz to, co specyficzne dla Pythona i ekosystemu ML — idiomy, wbudowane
narzędzia, konwencje, pułapki bibliotek. Analogie do C++ trafiają celnie.

Gdy jest wybór: **daj zweryfikowane opcje z wyraźną opinią** („to bym brał, tego nie i
dlaczego"), sekcję „świadomie pomijam", i **poczekaj na moją decyzję**. Nie instaluj ani
nie konfiguruj hurtem. Weryfikuj wersje i ID paczek przed poleceniem — kilka razy
uratowało to przed porzuconą zależnością.

> Globalne instrukcje są w `~/.claude/CLAUDE.md` — przeniesione na Ubuntu 2026-09-07.
> Ta sekcja jest ich zawężeniem do tego projektu i wygrywa tam, gdzie się różnią.

---

## Środowisko

Ubuntu 24, RTX 5080 (host `black_mw`). Menedżerem środowiska jest **`uv`** — nie pip,
nie conda. `pyproject.toml` i `uv.lock` są w repo i one, a nie ten plik, są źródłem prawdy
o zależnościach.

### Odtworzenie po `git clone`

```bash
uv sync --all-groups     # venv + zależności dokładnie z uv.lock
uv run ruff check .
uv run basedpyright
uv run sphinx-autobuild --watch src docs docs/_build   # --watch src jest konieczne
```

`uv sync` sam tworzy `.venv` i sam pobiera CPythona w wersji z `.python-version` — nie
instaluj Pythona ręcznie i nie aktywuj venva do uruchamiania komend, od tego jest `uv run`.

### Co jest ustalone w `pyproject.toml`

- `requires-python = ">=3.13"`, `.python-version` = `3.13`
- build backend: `uv_build` (nie hatchling, nie setuptools)
- ruff: `line-length = 100`, `target-version = "py313"`,
  reguły `E, F, I, UP, B, SIM, D`, docstringi w konwencji **numpy**
  (`D` jest włączone — odpowiednik `WARN_NO_PARAMDOC` z Doxygena, tylko widoczne w edytorze;
  wyłączone dla `tests/`)
- grupa `docs`: sphinx, furo, myst-parser, sphinx-autobuild, autodoc-typehints, copybutton

### Czego jeszcze NIE ma

`dependencies = []` — **torch, Hydra i MLflow nie są jeszcze dodane.** To pierwsza rzecz
w etapie 1. Przy dokładaniu torcha pamiętaj, że domyślne koło z PyPI nie wystarczy:
5080 to Blackwell (sm_120) i potrzebny jest build `cu128+`. W `uv` robi się to przez
zadeklarowanie osobnego indeksu (`[[tool.uv.index]]`) i przypięcie do niego pakietu
w `[tool.uv.sources]` — nie przez `pip install` do venva obok `uv.lock`.

### Edytor

Profil VS Code `studies_AI` (31 rozszerzeń jawnych / 40 zainstalowanych, ustawienia,
setup Sphinksa) jest opisany
w **`VSCODE_studies_AI.md` w katalogu głównym repo** — kopia przywieziona po to, żeby
środowisko dało się odtworzyć jednym `git clone`.

Oryginał żyje w `~/Documents/projects/masters/VSCODE_studies_AI.md` (obsługuje wszystkie
przedmioty, nie tylko ten projekt), a wersja do czytania jest tutaj:
https://claude.ai/code/artifact/c7ca13d5-d776-4ed5-8df2-4677412a13c2
**Przy zmianie profilu trzeba zaktualizować wszystkie trzy.**

Dokument opisuje macOS — ścieżki profilu są w nim postaci
`~/Library/Application Support/Code/User/profiles/<id>/`. Na Ubuntu ten sam katalog to
`~/.config/Code/User/profiles/<id>/`, a identyfikator profilu będzie inny, bo nadaje go
lokalna instalacja VS Code. Reszta (lista rozszerzeń, `settings.json`, `window.newWindowProfile`)
przenosi się bez zmian.

Pułapki stamtąd, które łatwo powtórzyć na nowej maszynie:

- **Pylance wraca sam** jako zależność `ms-python.python`. Type checkerem jest
  `detachhead.basedpyright`; dwa language servery dublują diagnostykę.
- Klucz to `basedpyright.analysis.typeCheckingMode` (`standard`), **nie**
  `python.analysis.typeCheckingMode` — ten drugi to Pylance i jest ignorowany.
  Domyślny tryb `recommended` zalewa błędami przy numpy/torch.
- `valentjn.vscode-ltex` jest zarchiwizowany — następca to `ltex-plus.vscode-ltex-plus`.
- `stkb.rewrap` jest niepodpisany i VS Code go odrzuca — fork `dnut.rewrap-revived`.

**Bez Dockera i bez DVC.** To świadoma decyzja zakresowa, nie zaległość.

---

## Decyzje zamknięte — nie otwieraj ich bez powodu

1. **Wyrocznią jest GT**, nie Cellpose-SAM. Etykiety są fizycznie na dysku, ale protokół
   udaje, że ich nie ma, i odsłania wyłącznie te patche, o które poprosiła pętla.
   Wyrocznia doskonała, żeby nie mylić błędu selekcji z błędem wyroczni.
2. **Cellpose-SAM = baseline**, uruchamiany wyłącznie w inferencji, nigdy trenowany.
   Odpowiada na pytanie „ile mały uczeń nadrabia względem dużego generalisty".
3. **Ubuntu, nie Mac.** Decyzja z 2026-09-07; wcześniejszy plan na M3 Pro / MPS odrzucony.
4. **Dataset: PanNuke** — propozycja, czeka na moje potwierdzenie. Gotowe patche 256×256,
   pula w tysiącach, foldy z pudełka. Alternatywy (MoNuSeg, CoNSeP) wymagają tilingu.

---

## Kontrakty i konwencje

- `Selector.score(pool) -> [N] float` — **ten sam interfejs co w projekcie docelowym**,
  żeby kod przeniósł się 1:1. Każda strategia to implementacja tego kontraktu.
- Uczeń jest **trenowany od zera w każdej iteracji**, nie dotrenowywany. Dotrenowywanie
  mierzy coś innego, niż się wydaje.
- Uczeń musi być mały: jedna pętla to N pełnych treningów × liczba seedów.
  **Jeden trening powyżej ~10 minut = zmniejsz model, zanim ruszysz dalej.**
- Metryki instancyjne: **PQ i AJI**, nie sam Dice. Dice nagradza trafienie w piksele,
  więc dwa zlepione jądra wyglądają na sukces.

## Twarde zasady eksperymentu

- **Ewaluacja wyłącznie przeciwko prawdziwemu GT na zbiorze testowym.** Wyrocznia dotyka
  tylko puli treningowej. Pomieszanie tego to najczęstszy sposób, w jaki taki eksperyment
  cicho traci sens.
- Zbiór testowy nie może przeciekać do treningu **ani do doboru hiperparametrów**.
- Każdy wykres AL potrzebuje trzech rzeczy, inaczej nic nie znaczy: **losowej selekcji
  jako baseline**, **sufitu z treningu na pełnej puli** i **pasma rozrzutu między seedami**.
- Pięć seedów na strategię, **ten sam zestaw seedów** dla każdej, ten sam budżet strojenia.
- Nakładające się pasma znaczą „bez różnicy", nie „nasza jest lepsza".

---

## Cztery ryzyka, dla których ten projekt istnieje

1. **Agregacja komórka → patch** — score per komórka, anotacja per patch. Średnia,
   maksimum, kwantyl? W projekcie docelowym to właśnie tu wchodzi Fuzzy IT2.
2. **Uczciwy protokół porównawczy** — wystarczy, że jedna strategia dostanie więcej
   uwagi przy strojeniu, i wykres kłamie.
3. **Wariancja krzywych AL** — rozrzut między seedami bywa większy niż różnica między
   strategiami. Jeden przebieg to anegdota.
4. **Metryki instancyjne** — patrz wyżej: sklejone jądra.

---

## Etapy

Kolejność jest wiążąca — każdy etap potrzebuje liczby albo interfejsu z poprzedniego.
Aktualny stan odhaczenia trzymam w artifacie (link na górze), nie tutaj.

1. **Fundament** (dni 1–3) — środowisko, dataset wczytany, widoczny patch z maską.
2. **Sufit** (dni 4–8) — trening na pełnej puli, 3 seedy. Liczba, do której dąży każda krzywa.
3. **Szkielet pętli** (dni 9–14) — kontrakt selektora, `RandomSelector`, pełna pętla.
   Test regresyjny: krzywa losowa przy 100% budżetu = sufit z etapu 2.
4. **Strategie** (dni 15–21) — niepewność per piksel, agregacja do patcha (min. 2 warianty),
   MC dropout **albo** ensemble, core-set przeciw duplikatom.
5. **Protokół** (dni 22–26) — 5 seedów, pasma, jeden skrypt odtwarzający wykresy z MLflow.
6. **Domknięcie** (dni 27–30) — Cellpose-SAM jako baseline, raport, lista kodu do
   przeniesienia 1:1 i do przepisania.

---

## Czego nie proponować na tym etapie

VAAL i adversarial AL · implementację HoVer-Net · WSI, tiling, sliding window, MIL ·
AL dla detekcji obiektów · Docker i DVC · Cellpose-SAM w roli wyroczni (to etap 2 badań) ·
bitowej powtarzalności — protokół opiera się na wielu seedach i przedziałach, nie na
determinizmie.
