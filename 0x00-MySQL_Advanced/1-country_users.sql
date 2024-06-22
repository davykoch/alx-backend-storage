-- Create table users with id, email, name and country columns
CREATE TABLE IF NOT EXISTS users (
	id INTEGER NOT NULL AUTO_INCREMENT,
	email VARCHAR(255) NOT NULL UNIQUE,
	name VARCHR(255),
	country VARCHAR(2) NOT NULL DEFAULT 'US' CHECK (counrty IN('US', 'CO', 'TN')),
	PRIMARY KEY(id)
);

