import urllib2
from lxml.html import parse

def game_search(search):
    '''Scrapes gamefaqs search page to get search results. Returns list of
    results.
    Each element is a dictionary with the following keys:
     * title - Name of the game
     * platform - Distribution platform of the game (PS1, XBOX, WII, etc)
     * url - URL to GameFAQs FAQ page
    '''
    # Turn spaces into plus signs (needed to construct valid search url
    search.replace(' ', '+')

    # Construct url from search string
    url = 'http://www.gamefaqs.com/search/index.html?game=' + search

    # Create document tree
    doc = parse(url)

    # Make all links absolute
    doc.getroot().make_links_absolute()

    # Results list
    results = []

    # Get all tables rows
    for row in doc.findall('//tr'):
        children = row.getchildren()
        
        # Extract platform name
        # If the platform field is blank that means that it is the same
        # platform as the previous entry.
        # Only update the platform variable when there is a real string
        # there.
        platform_text = row[0].text_content().strip().encode('utf-8')
        if platform_text != '':
            platform = platform_text

        # Extract game title
        title = row[1].text_content().strip().encode('utf-8')

        # Extract URL to FAQs page
        # Some games have no FAQs page, in which case row[2] will have
        # no children.
        # So that's why we catch the IndexError and move to the next
        # search result.
        try:
            url = row[2].getchildren()[0].get('href')
        except IndexError:
            continue

        # Add row to results list
        results.append({'title':title, 'platform':platform, 'url':url})

    return results

def faqs(faq_url):
    '''Scrapes FAQs page for a game and returns list of results.
    Each element is a dictionary with the following keys:
     * title - Guide title
     * url - URL to the guide
     * date - Date of last modification
     * author - Author of guide
     * version - Version of guide
     * size - File size of the guide
    '''
    # Create document tree
    doc = parse(faq_url)

    # Make all links absolute
    doc.getroot().make_links_absolute()

    # Results list
    results = []

    # Get all tables rows
    for row in doc.findall('//tr'):
        # Get link element from first field
        link_element = row[0].find('a')

        # Skip over this row if it doesn't have 5 fields
        # For example, Gamespot game guides get thrown in the table sometimes
        # and only have 2 fields, SO FUCK THAT SHIT.
        if len(row) != 5:
            continue

        # Extract title, FAQ link, date, author, version, file size
        title = link_element.text_content()
        url = link_element.get('href')
        date = row[1].text_content()
        author = row[2].text_content()
        version = row[3].text_content()
        size = row[4].text_content()

        # Add fields to list
        results.append({'title':title, 'url':url, 'date':date, 'author':author,
            'version':version, 'size':size})

    return results

def plaintext_faq_url(faq_url):
    # URL points directly to text file so we have no work to do.
    import fnmatch
    if fnmatch.fnmatch(faq_url, '*.txt'):
        return faq_url

    # Create document tree
    doc = parse(faq_url)

    # Make all links absolute
    doc.getroot().make_links_absolute()

    # Extract link to plain text FAQ url
    for link in doc.findall('//a'):
        if link.text_content() == 'View/Download Original File':
            return link.get('href')
    
    # If we got here that means that something bad happened, such as a change
    # in the webpage format and the scraper needs to be updated.
    raise Exception("Cannot retrieve text file URL from " + faq_url)

