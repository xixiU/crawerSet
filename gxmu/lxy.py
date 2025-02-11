from bs4 import BeautifulSoup
import time

def get_next_page_url(soup):
    """
    获取下一页的URL
    
    Args:
        soup: BeautifulSoup对象
    
    Returns:
        str: 下一页URL,如果没有下一页则返回None
    """
    # 查找带有class="Next"的a标签
    next_link = soup.find('a', class_='Next')
    
    if next_link:
        # 存在下一页,返回完整URL
        return next_link.get('href')
    
    # 不存在下一页,返回None
    return None

def process_pages(driver):
    """
    处理所有页面
    
    Args:
        driver: Selenium WebDriver对象
    """
    while True:
        # 处理当前页面
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        process_current_page(soup)
        
        # 检查是否有下一页
        next_url = get_next_page_url(soup)
        if not next_url:
            break
            
        # 跳转到下一页
        driver.get(next_url)
        time.sleep(2)  # 添加适当延迟,避免请求过快 