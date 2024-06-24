-- creates the required index on the names table
CREATE INDEX idx_name_first_score ON names (LEFT(name, 1), score);
