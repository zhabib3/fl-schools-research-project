import re
from bs4 import BeautifulSoup


def main():
	with open('test-html.html') as html_f:
		soup = BeautifulSoup(html_f, 'lxml')
		for element in soup.find_all('a', text=re.compile(
            r"staff|faculty|directory|employee", re.IGNORECASE)):
			try:
				print(element['href'])
			except KeyError:
				print('Error: href attribute not found')


if __name__ == "__main__":
    main()
