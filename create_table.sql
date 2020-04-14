CREATE TABLE coilgun_data (
    `id` int(10) NOT NULL AUTO_INCREMENT PRIMARY KEY,
    `area` float,
    `mass` float,
    `density` float,
    `constant` float,
    `velocity` float,
    `name` varchar(255) UNIQUE
);
