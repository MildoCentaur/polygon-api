CREATE TABLE IF NOT EXISTS areas (
    name VARCHAR NOT NULL PRIMARY KEY,
    geom GEOMETRY(Polygon, 4326) NOT NULL,
    date TIMESTAMP NOT NULL,
    properties JSON NOT NULL
    );


INSERT INTO areas VALUES
  ('Polygon', ST_SetSRID(ST_GeomFromText('POLYGON((0 0, 1 0, 1 1, 0 1, 0 0))'),4326),to_timestamp('16-06-2020 15:36:38', 'dd-mm-yyyy hh24:mi:ss'), '{"property1":"value11","property4":"value4"}'),
  ('PolygonWithHole', ST_SetSRID(ST_GeomFromText('POLYGON((0 0, 10 0, 10 10, 0 10, 0 0),(1 1, 1 2, 2 2, 2 1, 1 1))'),4326), to_timestamp('16-07-2020 15:36:38', 'dd-mm-yyyy hh24:mi:ss'), '{"property2":"value21","property5":"value5"}'),
  ('testPolygon2', ST_SetSRID(ST_GeomFromText('POLYGON((0 4, 4 4, 7 2, 0 4))'),4326),to_timestamp('16-06-2020 15:36:38', 'dd-mm-yyyy hh24:mi:ss'), '{"property1":"value11","property4":"value4"}'),
  ('testPolygon3', ST_SetSRID(ST_GeomFromText('POLYGON((8 6, 6 9, 8 12, 12 11, 13 4, 10 3, 8 6))'),4326),to_timestamp('16-06-2020 15:36:38', 'dd-mm-yyyy hh24:mi:ss'), '{"property1":"value11","property4":"value4"}'),
  ('separated', ST_SetSRID(ST_GeomFromText('POLYGON((16 0, 20 4, 22 0, 16 0))'),4326),to_timestamp('16-06-2020 15:36:38', 'dd-mm-yyyy hh24:mi:ss'), '{"property1":"value11","property4":"value4"}');
