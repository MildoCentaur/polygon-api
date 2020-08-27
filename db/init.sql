CREATE TABLE IF NOT EXISTS areas (
    name VARCHAR NOT NULL PRIMARY KEY,
    area GEOMETRY NOT NULL,
    date TIMESTAMP NOT NULL,
    properties JSON NOT NULL
    );


INSERT INTO areas VALUES
  ('Point', 'POINT(0 0)',to_timestamp('16-04-2020 15:36:38', 'dd-mm-yyyy hh24:mi:ss'), '{ "property1":"value1","property2":"value2"}'),
  ('Linestring', 'LINESTRING(0 0, 1 1, 2 1, 2 2)',to_timestamp('16-05-2020 15:36:38', 'dd-mm-yyyy hh24:mi:ss'), '{ "property1":"value1","property2":"value2"}'),
  ('Polygon', 'POLYGON((0 0, 1 0, 1 1, 0 1, 0 0))',to_timestamp('16-06-2020 15:36:38', 'dd-mm-yyyy hh24:mi:ss'), '{ "property1":"value11","property4":"value4"}'),
  ('PolygonWithHole', 'POLYGON((0 0, 10 0, 10 10, 0 10, 0 0),(1 1, 1 2, 2 2, 2 1, 1 1))', to_timestamp('16-07-2020 15:36:38', 'dd-mm-yyyy hh24:mi:ss'), '{ "property2":"value21","property5":"value5"}'),
  ('Collection', 'GEOMETRYCOLLECTION(POINT(2 0),POLYGON((0 0, 1 0, 1 1, 0 1, 0 0)))', to_timestamp('16-08-2020 15:36:38', 'dd-mm-yyyy hh24:mi:ss'), '{ "property3":"value31","property6":"value6"}');
