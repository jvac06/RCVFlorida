# %%
import censusdata
import pandas as pd
import sqlite3
import ssl
import re
pd.set_option('display.expand_frame_repr', False)
pd.set_option('display.precision', 2)

# %%
# Aggregate Population by Age
censusdata.printtable(censusdata.censustable('acs5', 2018, 'B01001'))

# %%
# Geographies by state>place
censusdata.geographies(censusdata.censusgeo([('state','12'),('place', '*')]), 'acs5', 2018)

# %%
# By County
censusdata.geographies(censusdata.censusgeo([('state','12'),('county', '*')]), 'acs5', 2018)

# %% 
# By County Subdivision
censusdata.geographies(censusdata.censusgeo([('state','12'), ('county', '057'), ('county subdivision', '*')]), 'acs5', 2018)

# %%
# By State>County>County Subdivision>Place or Remainder
censusdata.geographies(censusdata.censusgeo([('state','12'), ('county', '057'), ('county subdivision', '93367'), ('place/remainder (or part)', '*')]), 'acs5', 2018)


# %%
# Example drawing data on voting ages(18+) for Hillsborough County/Tampa CCD: 
tampa = censusdata.download('acs5', 2018, censusdata.censusgeo([('state','12'), ('county', '057'), ('county subdivision', '93367'), ('place/remainder (or part)', '*')]),[('B01001_'+str(x).zfill(3)+'E') for x in list(range(4,50)) if x not in [4,5,6,26,27,28,29,30]])

# %%
# # Simplified example
# censusdata.download('acs5', 2018, censusdata.censusgeo([('state','12'), ('county', '057'), ('county subdivision', '93367'), ('place/remainder (or part)', '*')]),['B01001_007E'])

# # %%
# # Example from documentation: works with three tuples for parameters
# censusdata.download('acs5', 2015,
#                         censusdata.censusgeo([('state','12'), ('county', '057'), ('county subdivision', '*')]),
#                         ['B23025_003E', 'B23025_005E', 'B15003_001E', 'B15003_002E', 'B15003_003E',
#                         'B15003_004E', 'B15003_005E', 'B15003_006E', 'B15003_007E', 'B15003_008E',
#                         'B15003_009E', 'B15003_010E', 'B15003_011E', 'B15003_012E', 'B15003_013E',
#                         'B15003_014E', 'B15003_015E', 'B15003_016E'])

# %% [markdown]
# # Next Steps
#1. Small sample with this library API is not working:
# - Submit issue to creator
# - Explore other API, see if it can drill down to city level: https://pypi.org/project/census/
#2. Create table with all Geolocations for Florida at the Place or Remainder level
#3. Create Script for DB storage

# %% [markdown]
# Exploring dataframe access

# %%
# checking how to add rows
tampa['voters'] = tampa.sum(axis=1)
tampa.head(2)

# %%
# # checking how to access state, county, subdivision, places values
counties = censusdata.geographies(censusdata.censusgeo([('state','12'),('county', '*')]), 'acs5', 2018)
subdivisions = censusdata.geographies(censusdata.censusgeo([('state','12'), ('county', '057'), ('county subdivision', '*')]), 'acs5', 2018)
places = censusdata.geographies(censusdata.censusgeo([('state','12'), ('county', '057'), ('county subdivision', '93367'), ('place/remainder (or part)', '*')]), 'acs5', 2018)
states = censusdata.geographies(censusdata.censusgeo([('state', '*')]),'acs5', 2018)
# %% 
for state in states:
    print(state)
    print(states[state].params()[0][1])

# %%
for county in counties:
    print(re.findall(r'([A-Za-z.\s]+)\sCounty',county)[0])
    print(counties[county].params()[1][1])

# %%
for division in subdivisions:
    # print(division)
    print(re.findall(r'([A-Za-z.\s]+)\s..[D],', division)[0])
    print(subdivisions[division].params()[2][1])

# %%
for place in places:
    print(place)
    # print(re.findall())
    print(places[place].params())
    print(places[place].params()[3][1])

# %%
