CREATE TABLE IF NOT EXISTS areas (
    name VARCHAR NOT NULL PRIMARY KEY,
    geom GEOMETRY NOT NULL,
    date TIMESTAMP NOT NULL,
    properties JSON NOT NULL
    );


INSERT INTO areas VALUES
  ('Point', 'POINT(0 0)',to_timestamp('16-04-2020 15:36:38', 'dd-mm-yyyy hh24:mi:ss'), '{"property1":"value1","property2":"value2"}'),
  ('Polygon', 'POLYGON((0 0, 1 0, 1 1, 0 1, 0 0))',to_timestamp('16-06-2020 15:36:38', 'dd-mm-yyyy hh24:mi:ss'), '{"property1":"value11","property4":"value4"}'),
  ('PolygonWithHole', 'POLYGON((0 0, 10 0, 10 10, 0 10, 0 0),(1 1, 1 2, 2 2, 2 1, 1 1))', to_timestamp('16-07-2020 15:36:38', 'dd-mm-yyyy hh24:mi:ss'), '{"property2":"value21","property5":"value5"}'),
  ('testPolygon2', 'POLYGON((0 4, 4 4, 7 2, 0 4))',to_timestamp('16-06-2020 15:36:38', 'dd-mm-yyyy hh24:mi:ss'), '{"property1":"value11","property4":"value4"}'),
  ('testPolygon3', 'POLYGON((8 6, 6 9, 8 12, 12 11, 13 4, 10 3, 8 6))',to_timestamp('16-06-2020 15:36:38', 'dd-mm-yyyy hh24:mi:ss'), '{"property1":"value11","property4":"value4"}'),
  ('separated', 'POLYGON((16 0, 20 4, 22 0, 16 0))',to_timestamp('16-06-2020 15:36:38', 'dd-mm-yyyy hh24:mi:ss'), '{"property1":"value11","property4":"value4"}');
