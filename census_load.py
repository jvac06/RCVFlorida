import sqlite3
import pandas
import numpy
import censusdata
import re
import os

# Connect to DB
conn = sqlite3.connect('RCV.sqlite')
cur = conn.cursor()

sql_script = './queries/create_tb.sql'
queryfile = open(sql_script).read()
cur.executescript(queryfile)

# # Gather State Data
# states = censusdata.geographies(censusdata.censusgeo([('state', '*')]),'acs5', 2018, key=os.environ.get('KEY'))
# for state in states:
#     fips = states[state].params()[0][1]
#     try:
#         cur.execute('INSERT OR IGNORE INTO states (name, fips) VALUES (?,?)', (state, fips))
#         conn.commit()
#     except EOFError:
#         print('Error inserting state:', state, fips)
#         break

# # Gather County
# state = 'Florida'
# cur.execute('SELECT * FROM states WHERE name = ? LIMIT 1', (state,))
# ID, fips, name = cur.fetchone()
# counties = censusdata.geographies(censusdata.censusgeo([('state', fips),('county', '*')]), 'acs5', 2018, key=os.environ.get('KEY'))
# for county in counties:
#     fips = counties[county].params()[1][1]
#     name = re.findall(r'([A-Za-z.\s]+)\sCounty',county)[0]
#     try:
#         cur.execute('INSERT OR IGNORE INTO counties (name, fips, state_id) VALUES (?,?,?)', (name, fips, ID))
#         conn.commit()
#     except EOFError:
#         print('Error inserting county:', county, fips)
#         break

# # Gather Subdiv
# cur.execute('SELECT counties.id, counties.fips, states.fips FROM counties INNER JOIN states ON states.id = state_id')
# counties = cur.fetchall()
# for county in counties:
#     subdivisions = censusdata.geographies(censusdata.censusgeo([('state', county[2]), ('county', county[1]), ('county subdivision', '*')]), 'acs5', 2018, key=os.environ.get('KEY'))
#     for division in subdivisions:
#         fips = subdivisions[division].params()[2][1]
#         name = re.findall(r'([A-Za-z.\s\-]+)\s..[D],', division)[0]
#         try:
#             cur.execute('INSERT OR IGNORE INTO subdivisions (name, fips, county_id) VALUES (?,?,?)', (name, fips, county[0]))
#             conn.commit()
#         except EOFError:
#             print('Error inserting subdivision:', name, fips)
#             break

# Gather Places & Populations
cur.execute('''SELECT subdivisions.id, subdivisions.fips, counties.fips, states.fips FROM subdivisions INNER JOIN counties ON counties.id = county_id 
                INNER JOIN states ON states.id = state_id''')
subdivisions = cur.fetchall()
for division in subdivisions:
    places = censusdata.geographies(censusdata.censusgeo([('state',division[3]), ('county', division[2]), ('county subdivision', division[1]), ('place/remainder (or part)', '*')]), 'acs5', 2018, key=os.environ.get('KEY'))
    for place in places:
        fips = places[place].params()[3][1]
        name = place.split(',')[0]
        incorp = 1 if ('city' or 'town' or 'village') in name else 0
        geo_code = censusdata.censusgeo([('state',division[3]), ('county', division[2]), ('county subdivision', division[1]), ('place/remainder (or part)', fips)])
        voters = int(censusdata.download('acs5', 2018, geo_code,[('B01001_'+str(x).zfill(3)+'E') for x in list(range(4,50)) if x not in [4,5,6,26,27,28,29,30]],key=os.environ.get('KEY')).sum(axis=1)[0])
        try:
            cur.execute('INSERT OR IGNORE INTO places (name, fips, subdiv_id, incorp, voters) VALUES (?,?,?,?,?)', (name, fips, division[0], incorp, voters))
            conn.commit()
        except EOFError:
            print('Error inserting places:', name, fips)
            break

