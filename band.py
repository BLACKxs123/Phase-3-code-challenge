class Band:
    def __init__(self, id):
        self.id = id

    def concerts(self):
        conn = psycopg2.connect("dbname=your_database user=your_user password=your_password")
        cur = conn.cursor()
        cur.execute("""
        SELECT id, venue_id, date
        FROM concerts
        WHERE band_id = %s;
        """, (self.id,))
        results = cur.fetchall()
        cur.close()
        conn.close()
        return results

    def venues(self):
        conn = psycopg2.connect("dbname=your_database user=your_user password=your_password")
        cur = conn.cursor()
        cur.execute("""
        SELECT venues.id, venues.title, venues.city
        FROM venues
        JOIN concerts ON venues.id = concerts.venue_id
        WHERE concerts.band_id = %s;
        """, (self.id,))
        results = cur.fetchall()
        cur.close()
        conn.close()
        return results

    def play_in_venue(self, venue_title, date):
        conn = psycopg2.connect("dbname=your_database user=your_user password=your_password")
        cur = conn.cursor()
        cur.execute("""
        INSERT INTO concerts (band_id, venue_id, date)
        SELECT %s, id, %s FROM venues WHERE title = %s;
        """, (self.id, date, venue_title))
        conn.commit()
        cur.close()
        conn.close()

    def all_introductions(self):
        intros = []
        for concert in self.concerts():
            c = Concert(concert[0])
            intros.append(c.introduction())
        return intros

    def most_performances(self):
        conn = psycopg2.connect("dbname=your_database user=your_user password=your_password")
        cur = conn.cursor()
        cur.execute("""
        SELECT bands.name
        FROM bands
        JOIN concerts ON bands.id = concerts.band_id
        GROUP BY bands.name
        ORDER BY COUNT(concerts.id) DESC
        LIMIT 1;
        """)
        result = cur.fetchone()
        cur.close()
        conn.close()
        return result[0]
