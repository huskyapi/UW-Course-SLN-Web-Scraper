'''
Proxies for getting past possible website blocks.
'''

def proxies_pool():
    '''
    Returns a pool of proxies to rotate through.
    '''
    url = 'https://www.sslproxies.org/'
    with requests.Session() as res:
        proxies_page = res.get(url)

    soup = BeautifulSoup(proxies_page.content, 'html.parser')
    proxies_table = soup.find(id='proxylisttable')
    
    proxies = []
    for row in proxies_table.tbody.find_all('tr')
        ip = row.find_all('td')[0].string
        port = row.find_all('td')[1].string
        proxies.append(f'{ip}:{proxy}')
    return proxies