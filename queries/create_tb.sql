-- State
CREATE TABLE IF NOT EXISTS states(
    id INTEGER PRIMARY KEY,
    fips TEXT NOT NULL,
    name TEXT UNIQUE NOT NULL
);
CREATE UNIQUE INDEX IF NOT EXISTS idx_states_fips ON states(fips);

-- County
CREATE TABLE IF NOT EXISTS counties(
    id INTEGER PRIMARY KEY,
    state_id INTEGER NOT NULL, 
    fips TEXT NOT NULL,
    name TEXT UNIQUE NOT NULL,
    FOREIGN KEY(state_id) REFERENCES states(id)
);
CREATE UNIQUE INDEX IF NOT EXISTS idx_counties_fips ON counties(fips);

-- Cencus County Divisions (CCD)s
CREATE TABLE IF NOT EXISTS subdivisions(
    id INTEGER PRIMARY KEY,
    county_id INTEGER NOT NULL,
    fips TEXT NOT NULL,
    name TEXT UNIQUE NOT NULL,
    FOREIGN KEY(county_id) REFERENCES counties(id)
);
CREATE UNIQUE INDEX IF NOT EXISTS idx_subdivisions_fips ON subdivisions(fips);

-- Census Designated Places (CDP)s
CREATE TABLE IF NOT EXISTS places(
    id INTEGER PRIMARY KEY,
    subdiv_id INTEGER NOT NULL,
    fips TEXT NOT NULL,
    name TEXT NOT NULL,
    incorp INTEGER NOT NULL,
    voters INTEGER NOT NULL,
    FOREIGN KEY(subdiv_id) REFERENCES subdivisions(id)
);
CREATE UNIQUE INDEX IF NOT EXISTS idx_places_fips ON places(fips);