import psycopg2

class Concert:
    def __init__(self, id):
        self.id = id

    def band(self):
        conn = psycopg2.connect("dbname=concert user=fonte password=QWERTY")
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
        if result:
            return result
        else:
            return "Band not found for this concert."

    def venue(self):
        conn = psycopg2.connect("dbname=concert user=fonte password=QWERTY")
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
        if result:
            return result
        else:
            return "Venue not found for this concert."

    def hometown_show(self):
        conn = psycopg2.connect("dbname=concert user=fonte password=QWERTY")
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
        if result:
            return result[0]
        else:
            return "Concert data not available."

    def introduction(self):
        conn = psycopg2.connect("dbname=concert user=fonte password=QWERTY")
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
        if result:
            return result[0]
        else:
            return "Introduction data not available."

class Band:
    def __init__(self, id):
        self.id = id

    def concerts(self):
        conn = psycopg2.connect("dbname=concert user=fonte password=QWERTY")
        cur = conn.cursor()
        cur.execute("""
        SELECT id, venue_id, date
        FROM concerts
        WHERE band_id = %s;
        """, (self.id,))
        results = cur.fetchall()
        cur.close()
        conn.close()
        return results if results else "No concerts found for this band."

    def venues(self):
        conn = psycopg2.connect("dbname=concert user=fonte password=QWERTY")
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
        return results if results else "No venues found for this band."

    def play_in_venue(self, venue_title, date):
        conn = psycopg2.connect("dbname=concert user=fonte password=QWERTY")
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
        concerts = self.concerts()
        if isinstance(concerts, str):
            return concerts
        for concert in concerts:
            c = Concert(concert[0])
            intros.append(c.introduction())
        return intros

    def most_performances(self):
        conn = psycopg2.connect("dbname=concert user=fonte password=QWERTY")
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
        return result[0] if result else "No performances found."

class Venue:
    def __init__(self, id):
        self.id = id

    def concerts(self):
        conn = psycopg2.connect("dbname=concert user=fonte password=QWERTY")
        cur = conn.cursor()
        cur.execute("""
        SELECT id, band_id, date
        FROM concerts
        WHERE venue_id = %s;
        """, (self.id,))
        results = cur.fetchall()
        cur.close()
        conn.close()
        return results if results else "No concerts found for this venue."

    def bands(self):
        conn = psycopg2.connect("dbname=concert user=fonte password=QWERTY")
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
        return results if results else "No bands found for this venue."

    def concert_on(self, date):
        conn = psycopg2.connect("dbname=concert user=fonte password=QWERTY")
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
        return result if result else "No concert found on this date."

    def most_frequent_band(self):
        conn = psycopg2.connect("dbname=concert user=fonte password=QWERTY")
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
        return result[0] if result else "No frequent band found."

def main():
    # Replace with appropriate IDs for testing
    band_id = 1
    venue_id = 1
    concert_id = 1
    
    band = Band(band_id)
    venue = Venue(venue_id)
    concert = Concert(concert_id)

    # Test Concert methods
    print("Band for Concert:", concert.band())
    print("Venue for Concert:", concert.venue())
    print("Hometown Show:", concert.hometown_show())
    print("Introduction:", concert.introduction())

    # Test Band methods
    print("Band's Concerts:", band.concerts())
    print("Band's Venues:", band.venues())
    band.play_in_venue("Venue B", "2024-09-30")
    print("All Introductions:", band.all_introductions())
    print("Most Performances:", band.most_performances())

    # Test Venue methods
    print("Venue's Concerts:", venue.concerts())
    print("Venue's Bands:", venue.bands())
    print("Concert on Date:", venue.concert_on("2024-09-18"))
    print("Most Frequent Band:", venue.most_frequent_band())

if __name__ == "__main__":
    main()
