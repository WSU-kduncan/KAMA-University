import mariadb
import sys



try:
    conn = mariadb.connect(
        user="root",
        password="password",
        host="localhost",
        port=3306,
        database="kama"
)
    print("Connected!")

except mariadb.Error as e:
    print(f"Error connecting to MariaDB: {e}")
    sys.exit(1)




cur = conn.cursor()

try:
    cur.execute(
        "INSERT INTO Program (program_id, program_name, degree_type) VALUES (?, ?, ?)",
        (1, "Computer Science", "Major")
    )
    conn.commit()  # <-- IMPORTANT to save the change
    print("Row inserted successfully!")

except mariadb.Error as e:
    print(f"Error: {e}")

conn.close()   