class Venue:
    def __init__(self, id):
        self.id = id

    def concerts(self):
        conn = psycopg2.connect("dbname=your_database user=your_user password=your_password")
        cur = conn.cursor()
        cur.execute("""
        SELECT id, band_id, date
        FROM concerts
        WHERE venue_id = %s;
        """, (self.id,))
        results = cur.fetchall()
        cur.close()
        conn.close()
        return results

    def bands(self):
        conn = psycopg2.connect("dbname=your_database user=your_user password=your_password")
        cur = conn.cursor()
        cur.execute("""
        SELECT bands.id, bands.name, bands.hometown
        FROM bands
        JOIN concerts ON bands.id = concerts.band_id
        WHERE concerts.venue_id = %s;
        """, (self.id,))
        results = cur.fetchall()
        cur.close()
        conn.close()
        return results

    def concert_on(self, date):
        conn = psycopg2.connect("dbname=your_database user=your_user password=your_password")
        cur = conn.cursor()
        cur.execute("""
        SELECT id, band_id
        FROM concerts
        WHERE venue_id = %s AND date = %s
        LIMIT 1;
        """, (self.id, date))
        result = cur.fetchone()
        cur.close()
        conn.close()
        return result

    def most_frequent_band(self):
        conn = psycopg2.connect("dbname=your_database user=your_user password=your_password")
        cur = conn.cursor()
        cur.execute("""
        SELECT bands.name
        FROM bands
        JOIN concerts ON bands.id = concerts.band_id
        WHERE concerts.venue_id = %s
        GROUP BY bands.name
        ORDER BY COUNT(concerts.id) DESC
        LIMIT 1;
        """, (self.id,))
        result = cur.fetchone()
        cur.close()
        conn.close()
        return result[0]
