import requests
from bs4 import BeautifulSoup

urls = ['http://www.funi.com/loupan/region_55_0_0_0_{}'.format(str(i)) for i in range(1,20,1))]
def get_title_name(url):
    web_data = requests.get(url)
    soup = BeautifulSoup(web_data.text,'lxml')
    title_list = soup.select('dt.clearfix > h2 > a')
    addr_list = soup.select('i.address')
    for addr,name in zip(addr_list,title_list):
        data = {
            'name': name.get('title'),
            'addrs': addr.get('title')
        }
        print(data)

url = 'http://www.funi.com/loupan/region_55_0_0_0_2'
for single_url in urls:
   get_title_name(single_url)

   get_session = requests.session()
   get_session.headers = headers
   get_result = get_session.get(url).text
   # print(get_result)
   need_row = re.compile(r'<input  (.*)>')
   need_reuslt = need_row.findall(get_result)
   # need = re.split(r'[ =]',need_reuslt)[4]

   itvdetection14.jsinf.net

  '''url = "http://jslyj.jiasule.com/yjsghdf/domain_manage/site/list/?keywords=cnhzz.com&search_type=domain&group_id=&source=&user_group=&site_belong="
   web_data = requests.get(url, headers=headers)
   soup = BeautifulSoup(web_data.text, 'lxml')
   print(soup)
   title_list = soup.select('table.font12.table_box.table-bordered.table')
   print(title_list)
'''