import scrapy


class GradleSpider(scrapy.Spider):
    name = "gradle"
    # start_urls = [
    #     "file:///home/molefe/Software/Developer/AttributeChangeProject/app/build/reports/tests/testDebugUnitTest/classes/com.example.attributechangeproject.ExampleUnitTest.html",
    #     'file:///home/molefe/Software/Developer/AttributeChangeProject/app/build/reports/androidTests/connected/com.example.attributechangeproject.ExampleInstrumentedTest.html'
    # ]
    # Argument = path/to/project
    # abs_path="/home/molefe/Software/Developer/AttributeChangeProject"

    # Run
    # scrapy crawl gradle -a abs="/home/molefe/Software/Developer/AttributeChangeProject"
    def __init__(self, abs=None, *args, **kwargs):
        super(GradleSpider, self).__init__(*args, **kwargs)
        self.abs_path = abs
        self.file="file://"
        self.package= "com.example"
        self.example_unit_test = "ExampleUnitTest.html"
        self.example_instrument_test = "ExampleInstrumentedTest.html"
        self.project_name=self.abs_path.split("/")[-1]
        # unit_path = "/home/molefe/Software/Developer/AttributeChangeProject/app/build/reports/tests/testDebugUnitTest/classes/com.example.attributechangeproject.ExampleUnitTest.html"
        # instrument_path =  "/home/molefe/Software/Developer/AttributeChangeProject/app/build/reports/androidTests/connected/com.example.attributechangeproject.ExampleInstrumentedTest.html"
        self.unit_path = "app/build/reports/tests/testDebugUnitTest/classes"
        self.instrument_path =  "app/build/reports/androidTests/connected"

        self.full_package_name = self.package + "." + self.project_name.lower()

        self.full_unit_path = self.abs_path + "/" + self.unit_path + "/" + self.full_package_name + "." + self.example_unit_test
        self.full_instrument_path = self.abs_path + "/" + self.instrument_path + "/" + self.full_package_name + "." + self.example_instrument_test
        print("FULL UNIT PATH")
        print(self.full_unit_path)
        print("FULL INSTRUMENT PATH")
        print(self.full_instrument_path)
        # print(abs_path)
        self.start_urls = [
            self.file + self.full_unit_path,
            self.file + self.full_instrument_path

        ]


    # Fix The Classification
    def fetch_gradle_results(self,title,response):
        test_dir = {}
        test_status = {}
        test_type = {}
        type = self.select_type(title)
        if type == self.example_unit_test:
            test_dir,test_status = self.fetch_unit_test(response)[0],self.fetch_unit_test(response)[1]
            test_type["unit"] = test_dir
        elif type == self.example_instrument_test:
            test_dir,test_status = self.fetch_instrumented_test(response)[0],self.fetch_instrumented_test(response)[1]
            test_type["instrument"] = test_dir
        test_type['status'] = test_status
        return test_type

    # These would be the general grades and status
    def fetch_status(self, results, status):
        result_status = {}
        for state, result in zip(status, results):
            result_status[state] = result
        return result_status


    # Fetch The Test Title
    # Check Whether A Test Is Instrumented Or Unit
    def select_type(self,title):
      space = title.split(" ")
      package = space[-1]
      package_split = package.split(".")
      type = package_split[-1]
      return type + ".html"


    #If type is instrmented then fetch instrument tests
    def instrument(self,tests):
        test_dir = {}
        test_dir = {tests[i]:tests[i+1] for i in range(0,len(tests),2)}
        return test_dir

    # If type is unit then fetch unit tests
    def unit(self,tests):
        test_dir = {}
        #test_dir = {tests[i]:tests[i-1] for i in range(0,len(tests),3)}
        for test in range(len(tests)):
            if (test + 2) <= len(tests) -1:
                if tests[test+2] == 'failed' or tests[test+2] == 'passed':
                        test_dir[tests[test]] = tests[test+2]
        return test_dir

    def fetch_instrumented_test(self,response):
        status = response.css('div.infoBox div.counter::text').getall()
        percent = response.css('div.percent::text').get()
        status_names = ["grade", "tests", "failures", "time"]
        status.insert(0, percent)

        instrument_status = self.fetch_status(status,status_names)
        # test_dir = self.instrument()
        tests = response.css('div#tab0 tr td::text').getall()
        test_dir = self.instrument(tests)
        return (test_dir,instrument_status)



    def fetch_unit_test(self,response):
        status_names = ["grade","tests","failures","ignored","time"]
        grade = response.css("div.percent::text").getall()[0]
        # "50"

        status = response.css("div.counter::text").getall()
        status.insert(0,grade)
        # Fetches Tests In One List
        tests = response.css("div#tab1 tr td::text").getall()
        """
        ['addition_isCorrect',
         '0.002s',
         'failed',
         'subtraction_isCorrect',
         '0.001s',
         'passed']
        """
        # ['2', '1', '0', '0.003s']
        unit_status = self.fetch_status(status,status_names)
        test_dir = self.unit(tests)
        return (test_dir,unit_status)


    def parse(self, response):
        self.generate_html(response)
        title = response.css("h1::text").get()
        test_type = self.fetch_gradle_results(title,response)
        yield test_type

    def generate_html(self,response):
        package_name = response.url.split("/")[-1]
        test = package_name.split('.')[-2]
        filename = 'gradle-%s.html' % test
        with open(filename,'wb') as f:
            f.write(response.body)
