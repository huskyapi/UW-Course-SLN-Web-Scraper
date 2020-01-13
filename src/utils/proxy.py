'''
Proxies for getting past possible website blocks.
'''



def random_header():
    accept = {"Firefox": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                        "Safari, Chrome": "application/xml,application/xhtml+xml,text/html;q=0.9, text/plain;q=0.8,image/png,*/*;q=0.5"}
    ua = UserAgent()
    if random.random() > 0.5:
        random_user_agent = ua.firefox
        valid_accept = accept['Firefox']
    else:
        random_user_agent = ua.chrome
        valid_accept = accept['Safari, Chrome']        
    
    headers = {"User-Agent": random_user_agent, "Accept": valid_accept}
    return headers

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