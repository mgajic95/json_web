import sqlite3, hashlib, time

conn = sqlite3.connect('banka.db') #koktovanje ka data base banka
c = conn.cursor()

#kreiranje tabele klijenata sa njihovim podacima
c.execute('''
    CREATE TABLE IF NOT EXISTS klijenti (
    id INTEGER PRIMARY KEY,
    ime_prezime TEXT,
    broj_racuna TEXT,
    sifra TEXT,
    token TEXT
    )
''')
# spisak klijenata sa brojem racuna i siframa
klijenti = [
    ("Marko Markovic", "123456", "123456", ""),
    ("Ana Ana", "987654", "987654", ""),
    ("Djura Djuric", "012345", "012345", "")
]

# unos podataka
c.executemany('INSERT INTO klijenti(ime_prezime, broj_racuna, sifra, token) VALUES (?, ?, ?, ?)', klijenti)
conn.commit()

def generate_token():
    timestamp = int(time.time())  # trenutni vremenski pecat
    return hashlib.sha256(str(timestamp).encode()).hexdigest()

def pristup_korisnika():  # definisanje broja racuna i sifre i promtovanja
    broj_racuna = input("Unesite broj racuna: ")
    sifra = input("Unesite sifru: ")

    c.execute("SELECT id, token FROM klijenti WHERE broj_racuna = ? AND sifra = ?", (broj_racuna, sifra))
    korisnik = c.fetchone()

    if korisnik:
        token = generate_token()
        korisnik_id = korisnik[0]

        c.execute('UPDATE klijenti SET token = ? WHERE id = ?', (token, korisnik_id))
        conn.commit()

        print("Uspesan pristup, token:", token)
    else:
        print("Podaci koje ste uneli nisu vazeci.")

    conn.close()
#pozivanje funkcije
pristup_korisnika()
