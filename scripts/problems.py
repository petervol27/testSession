import sqlite3

ENGINE = {"id": 1, "name": "engine", "price": 2000, "represent": "Engine Problems"}
BREAKS = {"id": 2, "name": "breaks", "price": 1000, "represent": "Break Problems"}
TREATMENT_5K = {
    "id": 3,
    "name": "treatment_5k",
    "price": 500,
    "represent": "5K Treatment",
}
TREATMENT_10K = {
    "id": 4,
    "name": "treatment_10k",
    "price": 1000,
    "represent": "10K Treatment",
}
FILTERS_OIL = {
    "id": 5,
    "name": "filters_oil",
    "price": 250,
    "represent": "Filters and Oil",
}
GEARS = {"id": 6, "name": "gears", "price": 1000, "represent": "Gears Problems"}

problems = [ENGINE, BREAKS, TREATMENT_5K, TREATMENT_10K, FILTERS_OIL, GEARS]

con = sqlite3.connect("data.db")
cur = con.cursor()
for problem in problems:
    cur.execute(
        """INSERT INTO problems(id,name,price,represent) VALUES(?,?,?,?)
          """,
        (problem["id"], problem["name"], problem["price"], problem["represent"]),
    )
con.commit()
con.close()
