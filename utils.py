import psycopg2
import datetime


class Utils():

    @staticmethod
    def get_or_create_day(day: str) -> int:
        conn = psycopg2.connect(
            host="localhost",
            database="roads",
            user="techfirdausyusof",
            password=""
        )

        cur = conn.cursor()

        # Check if day exists
        cur.execute(f"SELECT id FROM days WHERE name = '{day}'")
        row = cur.fetchone()

        if row is not None:
            cur.close()
            conn.close()
            return row[0]

        # if day's not exists, create new
        cur.execute(f"INSERT INTO days(name) VALUES('{day}') RETURNING id;")
        day_id = cur.fetchone()[0]
        conn.commit()

        cur.close()
        conn.close()

        return day_id

    @staticmethod
    def get_or_create_time(time: str) -> int:
        conn = psycopg2.connect(
            host="localhost",
            database="roads",
            user="techfirdausyusof",
            password=""
        )

        cur = conn.cursor()

        hour, minute = tuple(int(i) for i in time.split("_"))

        time = datetime.time(hour, minute, 0)

        cur.execute(f"SELECT id FROM times WHERE time = '{time}'")
        row = cur.fetchone()

        if row is not None:
            cur.close()
            conn.close()
            return row[0]

        cur.execute(f"INSERT INTO times(time) VALUES('{time}') RETURNING id;")
        time_id = cur.fetchone()[0]
        conn.commit()

        cur.close()
        conn.close()

        return time_id
