import urllib2
from lxml.html import parse

def game_search(search):
	'''Scrapes gamefaqs search page to get search results.
	Returns list of results.
	Each element is  a tuple with the following fields: (platform, game title, link to faqs page)
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
		# If the platform field is blank that means that it is the same platform as the previous entry
		# Only update the platform variable when there is a real string there
		platform_text = row[0].text_content().strip().encode('utf-8')
		if platform_text != '':
			platform = platform_text

		# Extract game name 
		game_name = row[1].text_content().strip().encode('utf-8')

		# Extract link to FAQs page
		# Some games have no FAQs page, in which case row[3] will have no children
		# So that's why we catch the IndexError and move to the next search result
		try:
			faqs_link = row[3].getchildren()[0].get('href')
		except IndexError:
			continue

		# Add row to results list
		results.append((platform, game_name, faqs_link))

	return results

def faqs(faq_url):
	'''Scrapes FAQs page for a game.
	Returns list of results.
	Each element is  a tuple with the following fields: (platform, game title, link to faqs page)
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

		# Extract title, FAQ link, date, author, version, file size
		title = link_element.text_content()
		link = link_element.get('href')
		date = row[1].text_content()
		author = row[2].text_content()
		version = row[3].text_content()
		size = row[4].text_content()

		# Add fields to list
		results.append((title, date, author, version, size, link))

	return results

def plaintext_faq(faq_url):
	# Create document tree
	doc = parse(faq_url)

	# Make all links absolute
	doc.getroot().make_links_absolute()

	# Extract link to plain text FAQ url
	for link in doc.findall('//a'):
		if link.text_content() == 'View/Download Original File':
			return link.get('href')
	
	return 'something went wrong'

