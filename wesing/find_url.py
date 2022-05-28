import re


def find_urls(content):
    matches = re.findall(r'https://[\w\d?=&_/.%]+', content)
    return list(sorted(matches))
