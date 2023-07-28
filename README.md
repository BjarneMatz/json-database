# JSON-Datenbank
In dieser Repository liegt ein Skript, welches eine oder mehrere JSON-Dateien als Datenbank für Python nutzbar macht. Es ist in vielen meiner anderen Projekte vertreten.

## Aufbau als Klasse
Das Skript ist als Python Klasse konzipiert und kann demnach mit `from database import Database as DB` importiert werden. Jede benötigte Datenbank wird dann im Skript ein eigenes Objekt, wie z.B. `meine_datenbank = DB("meine_datenbank)`. Danach können die nachfolgenden method-calls verwendet werden, um mit der Datenbank zu interagieren. Zum Beispiel `meine_datenbank.set("Schlüssel", "Wert)`. 

Die Datenbank speichert sämtliche Aufrufe in Form von Logs in einer Log-Datei. Der Pfad für die Log- und Datenbank-Dateien kann über die Konstanten im Skript abgeändert werden. Standardmäßig sind diese für die Datenbanken als `DB_ROOT_PATH = "databases/"` und für die Logs als `LOG_ROOT_PATH = "database-logs/"` definiert.

## Method-Calls
Das Skript beherrscht die Standardfunktionen einer Datenbank, darunter:

### Holen
- `get_value(key: str)`
- `get_keys()`
- `get_raw()` Gibt die vollständige Datenbank als Rohdatensatz zurück.

### Setzen
- `set_value(key: str, value: Any)`
- `set_raw(data: dict)` Setzt die gesamte Datenbank auf den gegebenen Rohdatensatz.

### Löschen
- `delete_key(key: str)`
- `delete_all()` Löscht die gesamte Datenbank - Die Datei bleibt erhalten.
- `delete_db_file()`

### Überprüfen
- `does_key_exist(key: str)`

### Suchen
In das Skript ist eine einfache Suchfunktion für Werte eingebaut. Da diese einfach linear die Datei von oben nach unten absucht, kann die Suche bei größeren Datensätzen sehr viel Zeit beanspruchen. Es empfiehlt sich daher, ein externes Modul für die Suche zu verwenden.
- `search_value(value: Any)` Gibt den ersten vorkommenden Schlüssel zurück.
- `search_values(value: Any)` Sucht alle vorkommen in der Datenbank.
