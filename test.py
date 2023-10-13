from database import Database as DB

db = DB("test")

db.set_value("testäöü", "testäöü")
print(db.get_value("testäöü"))
print(db.get_keys())
