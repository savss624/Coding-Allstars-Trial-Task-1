# Coding Allstars Trial Task 1

The task was to copy [ClassCentral](https://www.classcentral.com/) pages up to a depth of one level and translate their content to Hindi. You can check out the translated live website at [this link](http://ec2-3-1-200-236.ap-southeast-1.compute.amazonaws.com/web/translated_html/index.html).

### Scraping the pages

To scrape the pages, I used [HTTrack](https://www.httrack.com/) Website Copier and customized its settings by selecting the following options:

- Maximum link scanning depth - 2
- Structure type - HTML in web/html, images/other in web/xxx, where xxx is file extension

### Translating the pages

I wrote a python script to extract data from HTML files using [BeautifulSoup](https://beautiful-soup-4.readthedocs.io/en/latest/) and translate the content of each tag using [Amazon Translate](https://aws.amazon.com/translate/).

- Script - [translate.py](./translate.py)
- Original HTML directory - [Link](./web/html/)
- Translated HTML directory - [Link](./web/translated_html/)

### Testing the script

If you want to test the script, you'll need to install the following Python packages:

- bs4==0.0.1
- boto3==1.26.69
- python-dotenv==0.21.1

Once you have installed the packages, you can run the script. It may take a few seconds as there is already a [translations.json](./translations.json) file containing all the translations that have been made, and the script will use this file. The [translations.json](./translations.json) file contains 25,388 translations.

To test the API calls, you'll need to create a new file called .env in the same directory as the script and copy the contents of [.env.sample](./.env.sample) into it. You'll also need to delete the [translations.json](./translations.json) file, or the script will simply use the existing translations.

### Deployment

I used an Amazon EC2 instance to deploy the website.
