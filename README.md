Python code for scraping FT.com articles based on company search results

From the command line, once you're at the parent FT/ folder, you can create a new .json file using the company name you wish to search with the following:

scrapy crawl FT -o company_name.json -t json

Where "company_name" is the name of the file you wish to create based on the company you'll be searching on FT
