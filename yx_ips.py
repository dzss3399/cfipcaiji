import os
import requests
from bs4 import BeautifulSoup
import re


# 定义请求头
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

# 定义五个网址
urls = [
    "https://cf.090227.xyz/",
    "https://stock.hostmonit.com/CloudFlareYes",
    "https://ip.164746.xyz/",
    "https://monitor.gacjie.cn/page/cloudflare/ipv4.html",
    "https://345673.xyz/",
    "https://www.wetest.vip/page/cloudflare/address_v4.html",
    "https://www.wetest.vip/page/cloudflare/address_v6.html"
]

# 解析延迟数据的正则表达式
latency_pattern = re.compile(r'(\d+(\.\d+)?)\s*(ms|毫秒)?')

# 提取表格数据的函数
def extract_table_data(url):
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            return soup
        else:
            print(f"Failed to fetch data from {url}. Status code: {response.status_code}")
    except requests.RequestException as e:
        print(f"Request failed for {url}: {e}")
    return None

# 处理每个网址的数据
def process_site_data(url):
    soup = extract_table_data(url)
    if not soup:
        return []

    data = []
    if "cf.090227.xyz" in url:
        rows = soup.find_all('tr')
        for row in rows:
            columns = row.find_all('td')
            if len(columns) >= 3:
                line_name = columns[0].text.strip()
                ip_address = columns[1].text.strip()
                latency_text = columns[2].text.strip()
                latency_match = latency_pattern.match(latency_text)
                if latency_match:
                    latency_value = latency_match.group(1)
                    latency_unit = 'ms'
                    data.append(f"{ip_address}#{line_name}-{latency_value}{latency_unit}")

    elif "stock.hostmonit.com" in url:
        rows = soup.find_all('tr', class_=re.compile(r'el-table__row'))
        for row in rows:
            columns = row.find_all('td')
            if len(columns) >= 3:
                line_name = columns[0].text.strip()
                ip_address = columns[1].text.strip()
                latency_text = columns[2].text.strip()
                latency_match = latency_pattern.match(latency_text)
                print(latency_text)
                if latency_match:
                    latency_value = latency_match.group(1)
                    latency_unit = 'ms'
                    data.append(f"{ip_address}#{line_name}-{latency_value}{latency_unit}")

    elif "ip.164746.xyz" in url:
        rows = soup.find_all('tr')
        for row in rows:
            columns = row.find_all('td')
            if len(columns) >= 5:
                ip_address = columns[0].text.strip()
                latency_text = columns[4].text.strip()
                latency_match = latency_pattern.match(latency_text)
                if latency_match:
                    latency_value = latency_match.group(1)
                    latency_unit = 'ms'
                    data.append(f"{ip_address}#-{latency_value}{latency_unit}")

    elif "monitor.gacjie.cn" in url:
        rows = soup.find_all('tr')
        for row in rows:
            tds = row.find_all('td')
            if len(tds) >= 5:
                line_name = tds[0].text.strip()
                ip_address = tds[1].text.strip()
                latency_text = tds[4].text.strip()
                latency_match = latency_pattern.match(latency_text)
                if latency_match:
                    latency_value = latency_match.group(1)
                    latency_unit = 'ms'
                    data.append(f"{ip_address}#{line_name}-{latency_value}{latency_unit}")


    elif "https://www.wetest.vip/page/cloudflare/address_v4.html" in url:
        rows = soup.find_all('tr')
        for row in rows:
            tds = row.find_all('td')
            if len(tds) >= 5:
                line_name = tds[0].text.strip()
                ip_address = tds[1].text.strip()
                print(line_name)
                latency_text = tds[4].text.strip()
                latency_match = latency_pattern.match(latency_text)
                if latency_match:
                    latency_value = latency_match.group(1)
                    print(latency_match)
                    latency_unit = 'ms'
                    data.append(f"{ip_address}#{line_name}-{latency_value}{latency_unit}")
                    print(data)
                    
    elif "https://www.wetest.vip/page/cloudflare/address_v6.html" in url:
        rows = soup.find_all('tr')
        for row in rows:
            tds = row.find_all('td')
            if len(tds) >= 5:
                line_name = tds[0].text.strip()
                ip_address = tds[1].text.strip()
                print(line_name)
                latency_text = tds[4].text.strip()
                latency_match = latency_pattern.match(latency_text)
                if latency_match:
                    latency_value = latency_match.group(1)
                    print(latency_match)
                    latency_unit = 'ms'
                    data.append(f"[{ip_address}]#{line_name}-{latency_value}{latency_unit}")
                    print(data)
                    
    elif "345673.xyz" in url:
        rows = soup.find_all('tr', class_=re.compile(r'line-cm|line-ct|line-cu'))
        for row in rows:
            tds = row.find_all('td')
            if len(tds) >= 4:
                line_name = tds[0].text.strip()
                ip_address = tds[1].text.strip()
                latency_text = tds[3].text.strip()
                latency_match = latency_pattern.match(latency_text)
                if latency_match:
                    latency_value = latency_match.group(1)
                    latency_unit = 'ms'
                    data.append(f"{ip_address}#{line_name}-{latency_value}{latency_unit}")

    return data

# 主函数，处理所有网站的数据
def main():
    all_data = []
    for url in urls:
        site_data = process_site_data(url)
        all_data.extend(site_data)

    # 去除重复的IP地址行
    unique_data = list(set(all_data))

    # 过滤延迟数据低于100ms的行
    filtered_data = [line for line in unique_data if float(line.split('-')[-1].replace('ms', '')) < 150]

    # 检查ip.txt文件是否存在,如果存在则删除它
    if os.path.exists('yx_ips.txt'):
        os.remove('yx_ips.txt')
        
    # 写入到yx_ips.txt文件
    with open('yx_ips.txt', 'w', encoding='utf-8') as f:
        for line in filtered_data:
            f.write(line + '\n')

    print('IP地址已保存到yx_ips.txt文件中。')

if __name__ == "__main__":
    main()
