CREATE DATABASE IF NOT EXISTS routes;
use routes

CREATE TABLE IF NOT EXISTS airport (
ident NVARCHAR(10),
type NVARCHAR(50),
name NVARCHAR(200),
latitude FLOAT,
longitude FLOAT,
elevation_ft FLOAT,
continent NVARCHAR(10),
iso_country NVARCHAR(10),
iso_region NVARCHAR(10),
municipality NVARCHAR(100),
gps_code NVARCHAR(10),
iata_code NVARCHAR(10),
local_code NVARCHAR(10)
);

CREATE TABLE IF NOT EXISTS route_miles (
route_csv NVARCHAR(100),
segment_count INT,
direct_miles INT,
total_miles INT
);

GRANT SELECT ON airport TO 'web_user'@'localhost' IDENTIFIED BY 'SED_REPLACE_PASS';
GRANT SELECT ON route_miles TO 'web_user'@'localhost';


SELECT 'Completed!' AS 'Message:'