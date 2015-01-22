from delfic.entities.company import Company

__author__ = 'scorpio'

import MySQLdb as mDB
import sys


class DbRepository:
    def __init__(self):
        self.con = None

    def get_table(self, table_query):

        try:
            con = mDB.connect('localhost', 'root', '', 'delfic')
            cur = con.cursor(mDB.cursors.DictCursor)
            cur.execute(table_query)

            return cur

        except mDB.Error, e:

            print "Error %d: %s" % (e.args[0], e.args[1])

        finally:

            if con:
                con.close()

    def execute_non_query(self, update_query, params, hold_con=False):
        try:
            if not self.con:
                self.con = mDB.connect('localhost', 'root', '', 'delfic')

            cur = self.con.cursor()
            cur.execute(update_query, params)

            affected = cur.rowcount
            return affected

        except mDB.Error, e:

            print "Error %d: %s" % (e.args[0], e.args[1])

        finally:

            if self.con:
                if not hold_con:
                    self.con.close()

    def dispose(self):
        if self.con:
            self.con.close()


class CompanyRepository(DbRepository):

    def get_company_query(self, top_filter=-1, name_filter='', reg_filter='', turnover_filter=-1, last_id = -1):
        return "SELECT  * FROM company_seed"

    def get_companies(self, count=-1):
        query = self.get_company_query()
        company_cur = self.get_table(query)
        companies = []
        for i in range(company_cur.rowcount):
            row = company_cur.fetchone()
            company = Company(row['registered_number'], row['name'], row['turnover'], row['post_code'])
            companies.append(company)
        return companies

    def get_update_website_query(self):
        return "UPDATE company_seed SET website_url = %s WHERE registered_number = %s"


    def save_company_websites(self, companies):
        for company in companies:
            if company.website_url:
                query = self.get_update_website_query()
                self.execute_non_query(query, (company.website_url, company.reg_no), True)
        self.dispose()


