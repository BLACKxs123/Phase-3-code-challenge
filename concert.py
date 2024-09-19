import psycopg2

class Concert:
    def __init__(self, id):
        self.id = id

    def band(self):
        conn = psycopg2.connect("dbname=your_database user=your_user password=your_password")
        cur = conn.cursor()
        cur.execute("""
        SELECT bands.name, bands.hometown
        FROM bands
        JOIN concerts ON bands.id = concerts.band_id
        WHERE concerts.id = %s;
        """, (self.id,))
        result = cur.fetchone()
        cur.close()
        conn.close()
        return result

    def venue(self):
        conn = psycopg2.connect("dbname=your_database user=your_user password=your_password")
        cur = conn.cursor()
        cur.execute("""
        SELECT venues.title, venues.city
        FROM venues
        JOIN concerts ON venues.id = concerts.venue_id
        WHERE concerts.id = %s;
        """, (self.id,))
        result = cur.fetchone()
        cur.close()
        conn.close()
        return result

    def hometown_show(self):
        conn = psycopg2.connect("dbname=your_database user=your_user password=your_password")
        cur = conn.cursor()
        cur.execute("""
        SELECT (bands.hometown = venues.city) AS hometown_show
        FROM bands
        JOIN concerts ON bands.id = concerts.band_id
        JOIN venues ON venues.id = concerts.venue_id
        WHERE concerts.id = %s;
        """, (self.id,))
        result = cur.fetchone()
        cur.close()
        conn.close()
        return result[0]

    def introduction(self):
        conn = psycopg2.connect("dbname=your_database user=your_user password=your_password")
        cur = conn.cursor()
        cur.execute("""
        SELECT CONCAT('Hello ', venues.city, '!!!!! We are ', bands.name, ' and we\'re from ', bands.hometown) AS introduction
        FROM bands
        JOIN concerts ON bands.id = concerts.band_id
        JOIN venues ON venues.id = concerts.venue_id
        WHERE concerts.id = %s;
        """, (self.id,))
        result = cur.fetchone()
        cur.close()
        conn.close()
        return result[0]
