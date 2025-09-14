import os
class FileManager:
    """
    Třída FileManager poskytuje funkčnost pro získání názvů souborů z adresáře
    bez jejich přípon.
    """

    @staticmethod
    def file_names(path):
        """
        Získá názvy všech souborů (bez přípon) v určeném adresáři.

        Argumenty:
            path (str): Cesta k adresáři, ze kterého mají být načteny názvy souborů.

        Vrací:
            list: Seznam názvů souborů (řetězce) bez jejich přípon.

        Vyvolá:
            FileNotFoundError: Pokud zadaný adresář neexistuje.
            Exception: Pokud dojde k jakékoliv jiné neočekávané chybě při načítání souborů.
        """
        try:
            # Získá všechny soubory v zadaném adresáři a odstraní jejich přípony
            names = [os.path.splitext(file)[0] for file in os.listdir(path) if os.path.isfile(os.path.join(path, file))]
        except FileNotFoundError:
            print(f"Chyba: Adresář '{path}' nebyl nalezen.")
            names = []
        except Exception as e:
            print(f"Došlo k neočekávané chybě: {e}")
            names = []

        return names
