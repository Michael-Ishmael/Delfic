__author__ = 'scorpio'


class Company():

    def __init__(self, reg_no, name, turnover, post_code):
        self.post_code = post_code
        self.turnover = turnover
        self.name = name
        self.reg_no = reg_no
        self.website_url = None
