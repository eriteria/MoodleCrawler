import os, scrapy

class MoodleDownloaderSpider(scrapy.Spider):
    name = "moodledownloader"
    start_urls = ['https://moodle.covenantuniversity.edu.ng/login/index.php']
    
      
    def parse(self, response):
        print(f"filepath: {self.file_path}")
        return scrapy.http.FormRequest.from_response(
        response,
        formdata={'username':self.username, 'password':self.password},
        callback=self.after_login
     )


    def after_login(self, response):
        for course in response.css('a.aalink::attr(href)').getall(): #get all links
            yield scrapy.Request(url=course, callback=self.download_files)


    def download_file(self, response):
        courseCode = response.meta.get('courseCode')
        path = response.url.split('/')[-1].replace('%20', ' ')
        filepath = f"{self.file_path}/{courseCode}/{path}"
        if not os.path.exists(filepath):
            print(f'downloading {path}')
            with open(filepath, 'wb') as f:
                f.write(response.body)
        else:
            print(f'{path} already exists')


    def download_files(self, response):
        for link in response.css('a.aalink::attr(href)').getall():
            if 'resource' in link:
                courseCode = response.css('h1').extract()[0].split(':')[0].replace('<h1>', '')
            
                if not os.path.exists(self.file_path):
                    os.mkdir(self.file_path)  

                if not os.path.exists(f'{self.file_path}/{courseCode}'):
                    os.mkdir(f'{self.file_path}/{courseCode}')  

                yield scrapy.Request(url=link, callback=self.download_file, meta={'courseCode': courseCode})


        

        
                

            
                

        