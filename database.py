import json
import os
import time
from typing import Any, Union

__author__ = "Bjarne Matz"
__version__ = "0.1.0"

# Der (relative) Pfad zum Ordner, in dem die Datenbanken und Logs gespeichert werden.
DB_ROOT_PATH = "databases/"
LOG_ROOT_PATH = "database-logs/"


class Database:
    def __init__(self, database_name: str) -> None:
        """Initialisiert die Datenbank mit dem übergebenen Namen.
        
        Args:
            database_name (str): Der Name der Datenbank.
        """
        # Überprüfen, ob die Ordner existieren und sie ggf. erstellen.
        self.generate_folders()

        # Klassenvariablen initialisieren.
        self.database = database_name
        self.database_path = f"{DB_ROOT_PATH}{self.database}.json"

        # Überprüfen, ob die Datenbank Datei bereits existiert und funktioniert.
        try:
            self._read()
            self.log_action("Datenbankdatei gefunden und funktioniert.")
        except FileNotFoundError:
            self.log_action(
                f"Die Datenbankdatei wurde nicht gefunden. Erstelle neue Datenbankdatei...")
            self._write({})
        except json.decoder.JSONDecodeError as e:
            self.log_action(
                f"Die Datenbankdatei ist beschädigt. Manuelle Reparatur erforderlich. JSON Fehler: {e}")
            raise Exception(
                f"Die Datenbankdatei für '{self.database}' ist beschädigt. Manuelle Reparatur erforderlich. Die Fehler-Ausgabe wurde in der Log-Datei gespeichert.")

    def _read(self) -> dict:
        """Liest die Datenbank aus der Datei aus und gibt sie als Dictionary zurück.
        
        Returns:
            dict: Die Datenbank als Dictionary.
        """
        self.log_action("Lese aus Datenbank...")
        with open(self.database_path, "r") as file:
            return json.load(file)

    def _write(self, data: dict) -> None:
        """Speichert den gegebenen Datensatz in der Datenbankdatei ab.

        Args:
            data (dict): Der Datensatz, der gespeichert werden soll.
        """
        with open(self.database_path, "w") as file:
            self.log_action("Schreibe in Datenbank...")
            json.dump(data, file, indent=4)

    def get_value(self, key: str) -> Any:
        """Gibt den Wert des gegebenen Schlüssels zurück.
        
        Args:
            key (str): Der Schlüssel, dessen Wert zurückgegeben werden soll.
        Returns:
            Any: Der Wert des Schlüssels.
        """
        data = self._read()
        self.log_action(f"Hole Wert von Schlüssel '{key}'...")
        try:
            value = data[key]
            return value
        except KeyError:
            return None
       

    def get_keys(self) -> list:
        """Gibt alle Schlüssel der Datenbank zurück.
        
        Returns:
            list: Alle Schlüssel der Datenbank.
        """
        data = self._read()
        self.log_action("Hole alle Schlüssel...")
        keys = list(data.keys())
        return keys

    def get_raw(self) -> dict:
        """Gibt die gesamte Datenbank als Dictionary zurück.
        
        Returns:
            dict: Die gesamte Datenbank als Dictionary.
        """
        data = self._read()
        self.log_action("Hole Rohdaten...")
        return data

    def set_value(self, key: str, value: Any) -> None:
        """Setzt den Wert des gegebenen Schlüssels.
        
        Args:
            key (str): Der Schlüssel, dessen Wert gesetzt werden soll.
            value (Any): Der Wert, der beim Schlüssel gesetzt werden soll.
        """
        data = self._read()
        self.log_action(f"Setze Wert von Schlüssel '{key}' auf '{value}'...")
        data[key] = value
        self._write(data)

    def set_raw(self, data: dict) -> None:
        """Setzt die gesamte Datenbank auf den gegebenen Datensatz.
        
        Args:
            data (dict): Der Datensatz, der gespeichert werden soll.
        """
        self.log_action("Schreibe Rohdaten...")
        self._write(data)

    def delete_key(self, key: str) -> None:
        """Löscht das gegebene Schlüssel-Wert-Paar.
        
        Args:
            key (str): Der Schlüssel, der gelöscht werden soll.
        """
        data = self._read()
        self.log_action(f"Lösche Schlüssel '{key}' mit Wert '{data[key]}'...")
        del data[key]
        self._write(data)

    def delete_all(self) -> None:
        """Löscht die gesamte Datenbank."""
        self.log_action("Lösche Datenbank...")
        self._write({})

    def delete_db_file(self) -> None:
        """Löscht die Datenbankdatei."""
        self.log_action("Lösche Datenbankdatei...")
        os.remove(self.database_path)

    def does_key_exist(self, key: str) -> bool:
        """Prüft, ob der gegebene Schlüssel existiert.
        
        Args:
            key (str): Der Schlüssel, der überprüft werden soll.
        Returns:
            bool: True, falls der Schlüssel existiert, sonst False.
        """
        data = self._read()
        self.log_action(f"Prüfe, ob Schlüssel '{key}' existiert...")
        return key in data

    def search_value(self, value: Any) -> Union[Any, None]:
        """Durchsucht die Datenbank nach dem gegebenen Wert und gibt den ersten gefundenen Schlüssel zurück.
        Vorsicht: Die Suche kann sehr lange dauern, wenn die Datenbank sehr groß ist.
        
        Args:
            value (Any): Der Wert, nach dem gesucht werden soll.
        Returns:
            Union[Any, None]: Der erste gefundene Schlüssel oder None, falls keiner gefunden wurde.
        """
        data = self._read()
        self.log_action(f"Einfachsuche nach Wert '{value}'...")
        for key in data:
            if data[key] == value:
                return key
        return None

    def search_values(self, value: Any) -> list:
        """Durchsucht die Datenbank nach dem gegebenen Wert und gibt alle Schlüssel zurück, falls einer gefunden wurde.
        Vorsicht: Die Suche kann sehr lange dauern, wenn die Datenbank sehr groß ist.
        
        Args:
            value (Any): Der Wert, nach dem gesucht werden soll.
        Returns:
            list: Die Liste mit allen gefundenen Schlüsseln.
        """
        data = self._read()
        self.log_action(f"Mehrfachsuche nach Wert '{value}'...")
        keys = []
        for key in data:
            if data[key] == value:
                keys.append(key)
        return keys

    def log_action(self, message: str) -> None:
        """Speichert die gegebene Nachricht in der Log-Datei der Datenbank ab.

        Args:
            message (str): Die Nachricht, die gespeichert werden soll.
        """
        with open(f"{LOG_ROOT_PATH}{self.database}.log", "a", encoding="UTF-8") as file:
            file.write(
                f"[{time.asctime(time.localtime(time.time()))}] {message}\n")

    def generate_folders(self) -> None:
        """Generiert die benötigten Ordner für Datenbank und Logs, falls sie noch nicht existieren."""
        try:
            os.mkdir(LOG_ROOT_PATH)
        except FileExistsError:
            pass
        try:
            os.mkdir(DB_ROOT_PATH)
        except FileExistsError:
            pass


if __name__ == "__main__":
    # Teste Datenbank Funktionen
    db = Database("test")
    db.set_value("test", "test")
    db.set_value("test2", "test2")
    db.set_value("test3", "test3")
    print(db.get_value("test"))
    print(db.get_keys())
    print(db.does_key_exist("test3"))
    db.delete_key("test3")
    print(db.does_key_exist("test3"))
    db.delete_all()
    print(db.get_keys())
    db.delete_db_file()
