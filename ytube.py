from selenium import webdriver; from selenium.webdriver.common.keys import Keys
import time; import re; import db_model; from bs4 import BeautifulSoup
from ytube_utils import vid_date_convert, cmt_date_convert, count_convert, text_trim, addslashes, term_dict

if __name__ == "__main__":
    import ytube
    keyword = input('검색 키워드: ')
    term = input('검색 기간(시, 일, 주, 달, 연): ')
    max_vid_num = int(input('수집할 영상 수: '))
    max_comment_num = int(input('영상당 수집할 최대 댓글 수: '))

    start = time.time()
    cr = ytube.ytube_execution()
    vid_data, vid_comment_data= cr.ytube_getdata(keyword, term, max_vid_num, max_comment_num)
    print('수집한 영상 수:', len(vid_data), '수집한 댓글 수:', len(vid_comment_data), '\nInserting data to DB...')
    cr.ytube_to_db(vid_data, vid_comment_data, keyword)
    elapsed= time.time() - start; mnt, sec = divmod(elapsed, 60)
    print('Finished!', '\nElapsed time: {}m {}s'.format(int(mnt), int(sec)))
        
class ytube_execution():
    def __init__(self):
        self.db_model = db_model.DB_model()
    def ytube_getdata(self, keyword, term, max_vid_num, max_comment_num): 
        chromedriver_path= r'/home/warrior01/chromedriver'
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_experimental_option('prefs', {'intl.accept_languages': 'ko'})
        driver = webdriver.Chrome(executable_path=chromedriver_path, options=chrome_options)
        driver.maximize_window(); driver.implicitly_wait(10)
        init_url = "https://www.youtube.com/results?search_query="+keyword+'&sp=EgII{}%253D%253D'.format(term_dict[term])
        driver.get(init_url)
        driver.find_elements_by_css_selector("div[class='style-scope ytd-topbar-menu-button-renderer']")[1].click()
        driver.find_elements_by_css_selector("yt-icon[class='style-scope ytd-compact-link-renderer']")[0].click()
        driver.find_elements_by_css_selector("ytd-compact-link-renderer[class='style-scope yt-multi-page-menu-section-renderer']")[90].click()

        old_height = driver.execute_script("return document.documentElement.scrollHeight")
        while True:
            time.sleep(1.5)
            driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);")
            url_elements= driver.find_elements_by_css_selector("a[class='yt-simple-endpoint style-scope ytd-video-renderer']")
            vid_urls= [i.get_attribute('href') for i in url_elements]
            new_height= driver.execute_script("return document.documentElement.scrollHeight")
            if len(vid_urls) >= max_vid_num or new_height == old_height: break
            old_height= new_height
    
        vid_data= []
        vid_comment_data= []
        vid_numtoget= len(vid_urls) if len(vid_urls) < max_vid_num else max_vid_num
        for idx, url in enumerate(vid_urls[:vid_numtoget]):
        
            driver.get(url); time.sleep(1.5)
            comment_shown_num= len(driver.find_elements_by_xpath("//a[@id='author-text']//span"))
            old_height = driver.execute_script("return document.documentElement.scrollHeight")
            while True:
                driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);")
                time.sleep(1.5)
                new_height = driver.execute_script("return document.documentElement.scrollHeight")
                if comment_shown_num >= max_comment_num or new_height == old_height: break
                old_height= new_height
                comment_shown_num= len(driver.find_elements_by_xpath("//a[@id='author-text']//span"))

            vid_id= url.split('/')[3][8:]

            html_source = driver.page_source
            soup = BeautifulSoup(html_source, 'lxml')
            overlay_text = soup.find("div", {"class": "ytp-button ytp-paid-content-overlay-text"}).text
            vid_title = text_trim(driver.find_elements_by_css_selector("yt-formatted-string[class='style-scope ytd-video-primary-info-renderer']")[0].text)
            if '광고' in overlay_text:
                vid_title= '[유료광고영상]' + vid_title


            # vid_title= text_trim(driver.find_elements_by_css_selector("yt-formatted-string[class='style-scope ytd-video-primary-info-renderer']")[0].text)
            vid_creator= addslashes(driver.find_element_by_xpath("//yt-formatted-string[@id='text']//a[@class='yt-simple-endpoint style-scope yt-formatted-string']").text)
            vid_date= vid_date_convert(driver.find_elements_by_css_selector("yt-formatted-string[class='style-scope ytd-video-primary-info-renderer']")[1].text)
            vid_view_count= int(re.sub('[^0-9]', '', driver.find_element_by_css_selector("span[class='view-count style-scope ytd-video-view-count-renderer']").text))
            vid_total_comment_count= int(re.sub('[^0-9]', '', driver.find_elements_by_css_selector("yt-formatted-string[class='count-text style-scope ytd-comments-header-renderer']")[0].text[3:-1]))
            vid_creator_follower_count= count_convert(driver.find_element_by_xpath("//yt-formatted-string[@id='owner-sub-count']").text[4:-1])
            vid_description= text_trim(driver.find_element_by_css_selector("yt-formatted-string[class='content style-scope ytd-video-secondary-info-renderer']").text)
            vid_like_count= count_convert(driver.find_elements_by_css_selector("yt-formatted-string[class='style-scope ytd-toggle-button-renderer style-text']")[0].text)
            vid_dislike_count= count_convert(driver.find_elements_by_css_selector("yt-formatted-string[class='style-scope ytd-toggle-button-renderer style-text']")[1].text)

            vid_info= {'vid_id': vid_id,
                       'vid_title': vid_title,
                       'vid_creator': vid_creator,
                       'vid_date': vid_date,
                       'vid_view_count': vid_view_count,
                       'vid_creator_follower_count': vid_creator_follower_count,
                       'vid_description': vid_description,
                       'vid_like_count': vid_like_count,
                       'vid_dislike_count': vid_dislike_count,
                       'vid_total_comment_count': vid_total_comment_count
                       }
            vid_data.append(vid_info)
            
            comment_user= [addslashes(vid_creator) if i.text == ''  else addslashes(i.text) for i in driver.find_elements_by_xpath("//a[@id='author-text']//span")]
            comment_content= [text_trim(i.text) for i in driver.find_elements_by_xpath("//yt-formatted-string[@id='content-text']")]
            comment_when= [cmt_date_convert(i.text) for i in driver.find_elements_by_xpath("//yt-formatted-string[@class='published-time-text above-comment style-scope ytd-comment-renderer']//a")]
            comment_like_count= [int(0) if i.text=='' else count_convert(i.text) for i in driver.find_elements_by_xpath("//span[@id='vote-count-middle']")]
        
            comment_numtoget= comment_shown_num if comment_shown_num < max_comment_num else max_comment_num
            print('Scraping', '{}/{}'.format(idx+1, vid_numtoget), url, '({})'.format(comment_numtoget), '...')
            for i in range(comment_shown_num)[:comment_numtoget]:
                vid_comment_info= {'vid_id': vid_id,
                                   'vid_title': vid_title,
                                   'comment_user': comment_user[i],
                                   'comment_when': comment_when[i],
                                   'comment_like_count': comment_like_count[i],
                                   'comment_content': comment_content[i]
                                   }
                vid_comment_data.append(vid_comment_info)

        driver.quit()
        return vid_data, vid_comment_data

    def ytube_to_db(self, vid_data, vid_comment_data, keyword):
        for idx, i in enumerate(vid_data):
            try:
                vid_data_db= {'unique_id': i['vid_id'],
                          'keyword': keyword,
                          'title': i['vid_title'],
                          'user_id': 0,
                          'user_name': i['vid_creator'],
                          'posting_date': i['vid_date'],
                          'view_count': i['vid_view_count'],
                          'like_count': i['vid_like_count'],
                          'dislike_count': i['vid_dislike_count'],
                          'contents': i['vid_description'],
                          'user_follow': 0,
                          'user_follower': i['vid_creator_follower_count'],
                          'user_medias': 0,
                          'comment_count': i['vid_total_comment_count'],
                          'additional_data': []
                          }         
                #  {'data_key': 'comment_num', 'data_value': i['vid_total_comment_count']} 
                vid_isnew = self.db_model.set_data_body(1, vid_data_db)
                self.db_model.set_data_body_info(1, vid_isnew['is_new'], vid_data_db)
            except:
                print('Error occured at {} in video info data.'.format(idx+1))

        for idx, j in enumerate(vid_comment_data):
            try:
                vid_comment_data_db = {"unique_id": j['vid_id'],
                                   "keyword": keyword,
                                   "comment_id": j['vid_title'],
                                   "user_name": j['comment_user'],
                                   "comment_date": (j['comment_when']),
                                   "comment": addslashes(j['comment_content']),
                                   "comment_like": int(j['comment_like_count'])
                                   }
                self.db_model.set_data_comment(1, vid_comment_data_db, vid_isnew['is_new'], vid_isnew['last_time_update'])
            except:
                print('Error occured at {} in video comment data.'.format(idx+1))

        row_id = self.db_model.set_daily_log(keyword, 1)
        self.db_model.set_daily_log('', '', row_id)