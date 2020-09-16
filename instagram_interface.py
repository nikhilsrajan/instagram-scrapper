from selenium import webdriver

class InstagramInterface(object):
    def __init__(self, chromedrive_executable_path):
        self.driver = webdriver.Chrome(executable_path=chromedrive_executable_path)
        self.resize_options = [
            (400, 563),
            (1080, 720),
        ]
        self.resize_index = 0

    def resize_window(self, width, height):
        self.driver.set_window_size(width, height)

    def resize_window_by_preset(self):
        if self.resize_index == len(self.resize_options):
            raise Exception('Ran out of resize options. Must rest resize index.')
        dim = self.resize_options[self.resize_index]
        self.resize_window(dim[0], dim[1])
        self.resize_index += 1

    def reset_resize_index(self):
        self.resize_index = 0

    def close(self):
        self.driver.close()

    def quit(self):
        self.driver.quit()

    def go_to(self, url):
        status = True
        try:
            self.driver.get(url)
        except:
            status = False
        return status

    def login(self, username, password):
        status = True
        try:
            username_textbox = self.driver.find_element_by_xpath('/html/body/div[1]/section/main/article/div[2]/div[1]/div/form/div/div[1]/div/label/input')
            password_textbox = self.driver.find_element_by_xpath('/html/body/div[1]/section/main/article/div[2]/div[1]/div/form/div/div[2]/div/label/input')
            login_button = self.driver.find_element_by_xpath('/html/body/div[1]/section/main/article/div[2]/div[1]/div/form/div/div[3]/button')
            username_textbox.send_keys(username)
            password_textbox.send_keys(password)
            login_button.click()
        except:
            status = False
        return status

    def post_login(self):
        status = True
        try:
            not_now_button = self.driver.find_element_by_xpath('/html/body/div[1]/section/main/div/div/div/div/button')
            not_now_button.click()
        except:
            status = False
        return status

    def get_header_info(self, filepath=None):
        header_info = {
            'username' : self.get_username(),
            'posts' : self.get_posts_count(),
            'followers' : self.get_followers_count(),
            'following' : self.get_following_count(),
            'given name' : self.get_given_name(),
            'bio' : self.get_bio(),
            'website' : self.get_website()
        }
        if filepath is not None:
            with open(filepath, 'w+') as fout:
                for k, v in header_info.items():
                    fout.write(f'{k}: ')
                    if k in ['bio']:
                        for c in v:
                            try:
                                fout.write(c)
                            except:
                                fout.write('[?]')
                    else:
                        fout.write(f'{v}')
                    fout.write('\n')
        return header_info        
    
    def load_header_info(self, filepath):
        header_info = {}
        with open(filepath, 'r') as fin:
            for line in fin:
                line = line.replace('\n', '')
                splits = line.split(': ')
                if splits[0] in ['posts', 'followers', 'following']:
                    header_info[splits[0]] = int(splits[1])
                else:
                    header_info[splits[0]] = splits[1]
        return header_info

    def check_if_at_private_account_page(self):
        try:
            at_private_account_page = str(self.driver.find_element_by_xpath('/html/body/div[1]/section/main/div/div/article/div/div/h2').get_attribute('innerHTML')) == 'This Account is Private'
        except:
            at_private_account_page = False
        return at_private_account_page

    def get_username(self):
        return str(self.driver.find_element_by_xpath('/html/body/div[1]/section/main/div/header/section/div[1]/h2').get_attribute('innerHTML'))

    def get_posts_count(self):
        return int(self.driver.find_element_by_xpath('/html/body/div[1]/section/main/div/header/section/ul/li[1]/span/span').get_attribute('innerHTML').replace(',', ''))

    def get_followers_count(self):
        return int(self.driver.find_element_by_xpath('/html/body/div[1]/section/main/div/header/section/ul/li[2]/a/span').get_attribute('title').replace(',', ''))

    def get_following_count(self):
        return int(self.driver.find_element_by_xpath('/html/body/div[1]/section/main/div/header/section/ul/li[3]/a/span').get_attribute('innerHTML').replace(',', ''))
    
    def get_given_name(self):
        return str(self.driver.find_element_by_xpath('/html/body/div[1]/section/main/div/header/section/div[2]/h1').get_attribute('innerHTML'))

    def get_bio(self):
        bio = ''
        try:
            bio = str(self.driver.find_element_by_xpath('/html/body/div[1]/section/main/div/header/section/div[2]/span').get_attribute('innerHTML'))
        except:
            print('Warning: bio element not found.')
        return bio
    
    def get_website(self):
        website = ''
        try:
            website = str(self.driver.find_element_by_xpath('/html/body/div[1]/section/main/div/header/section/div[2]/a').get_attribute('innerHTML'))
        except:
            print('Warning: website element not found.')
        return website

    def go_to_account(self, username):
        return self.go_to(f'https://www.instagram.com/{username}')

    def get_available_posts_links(self):
        posts_links = []
        contents_element = self.driver.find_element_by_xpath('/html/body/div[1]/section/main/div/div[3]/article/div[1]/div')
        elements_tag_name_a = contents_element.find_elements_by_tag_name('a')
        for a_element in elements_tag_name_a:
            posts_links.append(a_element.get_attribute('href'))
        return posts_links
    
    def get_pageYOffset(self):
        return int(self.driver.execute_script('return window.pageYOffset'))

    def scroll_down(self, by):
        self.driver.execute_script(f'window.scrollTo(0, {self.get_pageYOffset() + by})')

    def get_first_comment(self):
        return str(self.driver.find_element_by_xpath('/html/body/div[1]/section/main/div/div[1]/article/div[3]/div[1]/ul/div/li/div/div/div[2]/span').get_attribute('innerHTML'))
    
    def get_datetime_string(self):
        return str(self.driver.find_element_by_xpath('/html/body/div[1]/section/main/div/div[1]/article/div[3]/div[2]/a/time').get_attribute('datetime'))