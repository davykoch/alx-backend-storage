-- Create table users with id, email, name and country columns
CREATE TABLE IF NOT EXISTS users (
	id INTEGER NOT NULL AUTO_INCREMENT,
	email VARCHAR(255) NOT NULL UNIQUE,
	name VARCHR(255),
	country ENUM('US', 'CO', 'TN') NOT NULL DEFAULT 'US',
	PRIMARY KEY(id)
);

