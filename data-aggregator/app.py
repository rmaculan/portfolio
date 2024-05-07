from bs4 import BeautifulSoup
import requests
import re
import time

# GET request code
def get_html(url, path):
    request = requests.get(url) # GET request   
    with open(path, "w", encoding="utf-8") as f:
        f.write(request.text)

get_html('https://en.wikipedia.org/wiki/List_of_old-growth_forests', './data/old_growth.html')
with open('data/old_growth.html', "r", encoding='utf-8') as f:
    html = f.read()
soup = BeautifulSoup(html, "html.parser")

# Get all tables
tables = soup.find_all('table', attrs={'class': 'wikitable sortable'})
print(len(tables))
print(tables[0], '\n')

data = {}

# find_previous_sibling("h2")
for t in tables:
    heading = t.find_previous_sibling("h2").text
    print(heading)
print()

for t in tables:
    heading = t.find_previous_sibling(['h2', 'h3']).text.replace('[edit]', '') # Clean up the [edit] tag from the label strings
    print(heading)
print()

# Add our tables to our dictionary
for t in tables:
    heading = t.find_previous_sibling(['h2', 'h3']).text.replace('[edit]', '')
    data[heading] = t  

table = data["Australia"]
first_row = table.tr 
for td in first_row:
    print(td.text, '\n')

columns = []
for td in first_row:
    if td.text.strip() != '': 
        columns.append(td.text.strip())
print(columns, '\n')

# back to our original intent here.
rows = table.find_all('tr')
print(rows[1], '\n')

# Collecting data from table rows
# get all the <td> of a single row.
example_row = rows[1]
table_cells = rows[1].find_all('td')
print(table_cells, '\n')

# ------------------------
# There are a few bits of formatting we can be (mostly) assured of here. We know that the <td> elements will always be in order of our 
# columns, such that columns[x] corresponds to table_cells[x]. See the Czech Republic row for an example of a breach in formatting
# that breaks this invariant! But 99% of the time, we should be good.
# Let's use this knowledge to try structuring data for a single row first.
row_data = {}
for i in range(len(table_cells)):
    row_data[columns[i]] = table_cells[i]
print(row_data["Country"])
print(row_data["Old-growth forest type"], '\n')
print(row_data['Old-growth forest type'].text.strip(), '\n') # We can also get just the text for our reference
# 05 - structuring a table
# Now that we can create an entry for a single row, we can
# start to make our full table data structure
australia_table = []
# Row numbers will be list indices. Each row will contain a dictionary with column names as keys.
# Let's first generalize our row data extraction into a function.
def extract_row_data(columns, row):
    row_data = {}
    table_cells = row.find_all('td')
    for i in range(len(table_cells)):
        row_data[columns[i]] = table_cells[i]
    return row_data
rows.pop(0) # Remove the first row with column names
for r in rows:
    australia_table.append(extract_row_data(columns, r))
print(australia_table[0], '\n')
# DATA CLEANING
# Now that we have a full table of data, we can take a look at cleaning up the data and performing
# some basic data integrity checks.
# Almost every substantial web scraping project will have to deal with this fundamental issue:
# data quality on the internet, even in a relatively well supervised environment like Wikipedia, is VERY low.
# While fixing formatting issues by hand as they come up can work for very small datasets,
# any attempt to generalize our scraping methods to a larger set of tables or even different articles
# can run into problems if we aren't proactive in anticpating, identifying, and correcting data integrity problems.
# First let's take a look at the table on Wikipedia, and note down some problems that we can see already that will have to be
# addressed.
# We'll start building up a function that takes in a row and performs our desired data cleaning operations.
# Takes in our row dictionary that we made previously.
def clean_row_data(row: dict):
    # print('ROW: ', row)
    for k in row.keys(): # Iterate through table columns
        val = row[k]
        # Empty cells. We should replace these with a consistent tag such as 'No data'.
        if re.match('\s', val.text): # We need to match all whitespace because some of these cells might have a variable number of space characters.
            row[k] = 'No data'
        # Dead or missing links. Links in red on Wikipedia pages are links to pages that do not exist.
        # We don't want to leave these links in so that we don't have to consider this case when 
        # programatically fetching linked pages later on.
        # How do we identify them? If we look at the HTML metadata of the dead links, they have '(page does not exist)' in the title field.
        links = val.find_all('a')
        
        for l in links:
            if l.get('title') is not None and '(page does not exist)' in l.get('title'): # Replace dead link <a> tags with their text.
                l.replace_with(l.text) # replace_with() is a bs4 function for editing the HTML tree within the BeautifulSoup object.
            # Remove citation links
            if 'cite' in l.get('href'):
                l.parent.decompose() # So we get the <sup> tag its inside of as well. decompose() destroys the tag.
        # Inconsistent text formatting.
        # Old-growth extent. Australia table has things like '2,000 square kilometres (770 sq mi)'. 
        # Contrast this to the other tables with things like '200 acres (81 ha)', '6 ha (15 acres)' and several others.
        # We'll need to get these all into a consistent unit and format!
        if k == 'Old-growth extent' and row[k] != 'No data':
            data = row[k].text.strip()
            # Annoying unicode characters that can break the RegEx!
            data = data.replace('\xa0', ' ') # From Quebec
            # A complex RegEx. We have to handle cases of numbers with commas and without
            data = re.search('\d+(?:,\d{3})*(?:\.\d*)? (?:hectares|square kilometres|ha|acres)', data).group()
            # Also decimal points!
            parent = row[k].parent
            row[k].decompose()
            new_tag = soup.new_tag('td')
            new_tag.string = data
            parent.append(new_tag)
            row[k] = new_tag
    return row
# print(clean_row_data(australia_table[6]))
# Check the full output
# for r in australia_table:
    # print(clean_row_data(r))
# Looks good. Let's save the results.
# for r in australia_table:
#     r = clean_row_data(r)
# print(australia_table)
# That was a lot!
# Now we can go back to our original data dictionary and add our new Australia table
# NOTE this must be commented out when doing the general method.
# data['Australia'] = australia_table
# print(data['Australia'])
# Okay, so we've proven that it works, but let's comment all this out for now, as we'll need to generalize 
# the method next.
# GENERALIZING THE METHOD! Another essential task in web scraping. 
# If we can do it to one table, we can do it to all of them!! (Even on other articles :))
def prepare_table_data(columns, table):
    table_data = []
    rows = table.find_all('tr')
    rows.pop(0) # Remove the first row with column names
    
    for r in rows:
        r = extract_row_data(columns, r)
        r = clean_row_data(r)
        table_data.append(r)
    # print('TABLE DATA: ', table_data)
    return table_data
# We also need to put them in dictionaries like we did with Australia!!
# And remove column names, etc. etc.
# Should add these to the function (they are written above)
def prepare_all_tables(columns, data):
    for k in data.keys():
        data[k] = prepare_table_data(columns, data[k])
    return data
# Let's check and make sure we won't run into any obvious formatting issues... hmm..
# Ah. Before we go ahead:
# Annoying one-off issue!
# Inconsistent table formatting. 
# See for instance the Czech Republic row.
data = prepare_all_tables(columns, data)
# print(data['Eurasia'])
print(len(data))
# Nice.
# USING OUR NEWLY COLLECTED DATA
# How can we access the data from our new data structure?
print(data['Australia'][3]['Old-growth extent'].text)
# We can access any piece of data from our tables now using this syntax.
# The table, followed by the row index, followed by the column name.
# BASIC ANALYTICS
# How many of the listed old-growth forests are in France?
eurasia = data['Eurasia']
france = [x for x in eurasia if 'France' in x['Country'].text] # Note that it's helpful to not look for an exact match, as there are often newlines, random unicode chars, etc.
print(len(france))
# How many of the listed old-growth forests in Australia are in Tasmania? (This will require the extra step of extracting Tasmania from the area info)
australia = data['Australia']
tasmania = [r for r in australia if 'Tasmania' in r['Area'].text]
print(len(tasmania))
def km_to_hectare(val):
    return val * 100
def hectare_to_km(val):
    return val/100
# Of those that have data, what is their total land area in hectares?
tasmania_area_data = [r for r in tasmania if r['Old-growth extent'] != 'No data']
print(len(tasmania_area_data))
total = 0
for r in tasmania_area_data:
    area = r['Old-growth extent'].text 
    # print(area) # We'll need to do some unit conversions!
    
    # Remove commas to parse as numeric
    area = area.replace(',', '')
    val = re.search('\d*', area).group()
    val = float(val)
    if 'square kilometres' in area:
        val = km_to_hectare(val)
    
    total += val
print('Total area for Tasmanian old growth with data: ', total, ' hectares, ', hectare_to_km(total), ' kilometres squared')
print()
# FOLLOWING LINKS TO OTHER PAGES
# We've done some basic analytics to test out our aggregated data. Web scraping, however, really shines when you can not only
# aggregate data from a single page, but from many pages.
# Saving pages
def get_links_for_one_row(data_row):
    # print(data_row)
    links = []
    # Need to exclude Old-growth forest type section
    keys = list(data_row.keys())
    keys.remove('Old-growth forest type') # We won't be using these 
    for k in keys:
        links += data_row[k].find_all('a')
    links = ['https://wikipedia.org' + a['href'] for a in links]
    return links
# test_links = get_links_for_one_row(data['United States'][1])
def collect_html_from_links(links: list, directory: str): #./html_docs/
    for l in links:
        # Create unique filename from URL
        filename = l.replace('https://wikipedia.org/wiki/', '')
        filename += '.html'
        response = requests.get(l)
        # RATE LIMIT
        time.sleep(0.5)
        with open(directory + filename, 'w', encoding='utf-8') as f:
            f.write(response.text)
            
# collect_html_from_links(test_links, './html_docs/')
# ADVANCED ANALYTICS INCORPORATING DATA FROM OTHER PAGES
# Query:
# Calculate the listed old growth forests in Bulgaria as a percentage of the entire
# area of Bulgaria.
# For this one we'll only need a single other article, since we already have the areas of the
# Bulgarian parks in our dataset. We will need to download the HTML for the article on Bulgaria to
# get the area of the whole country.
# Get ahold of the Bulgaria page link
bulgaria_rows = []
for row in data['Eurasia']:
    if row['Country'].text.strip() == 'Bulgaria':
        bulgaria_rows.append(row)
bulgaria_link = 'https://wikipedia.org' + bulgaria_rows[0]['Country'].a['href']
print('Bulgaria link: ', bulgaria_link)
# get_html(bulgaria_link, './html_docs/Bulgaria.html')
# Don't forget to comment out the code to pull down the links once you have them!
# Create soup for Bulgaria country article, parse infobox for area stat.
with open('data/Bulgaria.html', "r", encoding='utf-8') as f:
    bulgaria_html = f.read()
bulgaria_soup = BeautifulSoup(bulgaria_html, 'html.parser')
print(bulgaria_soup.title, '\n') # Test
def get_bulgaria_area(tag):
    return tag.name == 'td' and 'km' in tag.text and 'Total' in tag.parent.text
km_tags = [e.text for e in bulgaria_soup.find_all(get_bulgaria_area)]
print(km_tags)
area_tag = km_tags[0]
b_area = re.search('\d+(?:,\d{3})*(?:\.\d*)?', area_tag)
b_area = float(b_area.group().replace(',', '')) # Convert to Python numeric
print(b_area)
# This is in km2 though, and the rest of our data is in hectares. So let's convert it.
b_area = km_to_hectare(b_area)
print(b_area)
# Do final calculation.
# Add up the hectares of the Bulgaria forest data we already have.
# We'll need to do a bit of cleaning, though, to get the data into a numeric format.
forest_total = 0
for row in bulgaria_rows:
    f_data = row['Old-growth extent'].text
    f_data = re.search('\d+(?:,\d{3})*(?:\.\d*)?', f_data).group()
    f_data = f_data.replace(',', '')
    f_data = float(f_data)
    forest_total += f_data
print(forest_total)
# Final calculation
print('Percentage of Bulgarian land area accounted for by old-growth forest: ', round((forest_total / b_area) * 100, 5), '%')
# Of course, this is a calculation that would have been simple enough to do by hand with such a small dataset,
# but on larger, more complex datasets the advantage of doing it programatically becomes apparent.
# CHALLENGE analytics:
#
# How many different U.S. states have forests with some
# variety of oak tree?
us_table = data['United States']
states = set()
for r in us_table:
    f_type = r['Old-growth forest type']
    if f_type is not None and f_type != 'No data':
        if 'oak' in f_type.text.lower():
            states.add(r['Country'].text.strip())
print(states)
print(len(states))
