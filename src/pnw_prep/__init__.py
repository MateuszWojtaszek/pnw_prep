"""Projekt naukowo-wdrożeniowy — pakiet główny."""

def main() -> None:
    """Punkt wejścia CLI zadeklarowany w ``[project.scripts]``.

    Wypisuje komunikat powitalny na standardowe wyjście. Docstring jest
    w konwencji NumPy — tak samo dokumentujesz każdą kolejną funkcję.

    Returns
    -------
    None
        Funkcja nie zwraca wartości.

    Examples
    --------
    >>> main()
    Hello from pnw-prep!
    """
    print("Hello from pnw-prep!")
