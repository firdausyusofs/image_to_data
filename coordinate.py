import psycopg2
from mercator import Location, Mercator
import datetime

class Coordinate():
    conn = None
    cur = None
    top_left: Location = None
    bottom_right: Location = None
    index = None
    area_id = None
    conditions = ["green", "orange", "red", "maroon"]

    def __init__(self, top_left: Location, bottom_right: Location, index: int):
        self.conn = psycopg2.connect(
            host="localhost",
            database="roads",
            user="techfirdausyusof",
            password=""
        )
        self.cur = self.conn.cursor()
        self.top_left = top_left
        self.bottom_right = bottom_right
        self.index = index

        self.create_area()

    def create_area(self):
        self.cur.execute(f"SELECT id FROM areas WHERE index = {self.index}")
        row = self.cur.fetchone()
        if row is not None:
            self.area_id = row[0]
            return

        sql = f'''
            INSERT INTO
                areas(geometry, index)
            VALUES (
                ST_MakePolygon(
                    ST_MakeLine(
                        ARRAY[
                            ST_SetSRID(
                                ST_MakePoint({self.top_left.longitude}, {self.top_left.latitude}),
                                4326
                            ),
                            ST_SetSRID(
                                ST_MakePoint({self.bottom_right.longitude}, {self.top_left.latitude}),
                                4326
                            ),
                            ST_SetSRID(
                                ST_MakePoint({self.bottom_right.longitude}, {self.bottom_right.latitude}),
                                4326
                            ),
                            ST_SetSRID(
                                ST_MakePoint({self.top_left.longitude}, {self.bottom_right.latitude}),
                                4326
                            ),
                            ST_SetSRID(
                                ST_MakePoint({self.top_left.longitude}, {self.top_left.latitude}),
                                4326
                            )
                        ]
                    )
                ),
                {self.index}
            )
            RETURNING id;
        '''

        self.cur.execute(sql)
        self.area_id = self.cur.fetchone()[0]
        self.conn.commit()

    def insert_to_db(self, coordinates: list[Location], key: int, day_id: int, time_id: int):
        for i, v in enumerate(coordinates):
            code = f'''
                INSERT INTO
                    traffics(coordinate, condition, area_id, day_id, time_id)
                VALUES (
                    ST_SetSRID(
                        ST_MakePoint({v.longitude}, {v.latitude}),
                        4326
                    ),
                    '{self.conditions[key]}',
                    {self.area_id},
                    {day_id},
                    {time_id}
                );
            '''

            self.cur.execute(code)
            self.conn.commit()

    def __del__(self):
        self.cur.close()
        self.conn.close()
