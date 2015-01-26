from delfic.entities.company import Company

__author__ = 'scorpio'

import MySQLdb as mDB
import sys


class DbRepository:
    def __init__(self):
        self.con = None

    def get_table(self, table_query, last_id):

        try:
            con = mDB.connect('localhost', 'root', '', 'delfic')
            cur = con.cursor(mDB.cursors.DictCursor)
            cur.execute(table_query, (last_id, ))

            return cur

        except mDB.Error, e:

            print "Error %d: %s" % (e.args[0], e.args[1])

        finally:

            if con:

                con.close()

    def execute_non_query(self, update_query, params, hold_con=False):
        try:
            if not self.con or self.con.open == 0:
                self.con = mDB.connect('localhost', 'root', '', 'delfic')

            cur = self.con.cursor()
            cur.execute(update_query, params)

            affected = cur.rowcount

            self.con.commit()
            return affected

        except Exception as ex:

            print ex.message

        finally:

            if self.con:
                if not hold_con:
                    try:
                        self.con.close()
                    except:
                        pass

    def dispose(self):
        if self.con and not self.con.open == 0:
            try:
                self.con.close()
            except:
                pass


class CompanyRepository(DbRepository):

    def get_company_query(self):
        return "SELECT  * FROM company_seed WHERE company_seed_id > %s"

    def get_companies(self, last_id=0):
        query = self.get_company_query()
        company_cur = self.get_table(query, last_id)
        companies = []
        for i in range(company_cur.rowcount):
            row = company_cur.fetchone()
            company = Company(row['registered_number'], row['name'], row['turnover'], row['post_code'])
            companies.append(company)
        return companies

    def get_update_website_query(self):
        return "UPDATE company_seed SET website_url = %s WHERE registered_number = %s"

    def get_insert_new_company_query(self):
        return "INSERT INTO company_seed (company_seed_id, registered_number, name, turnover, post_code) " \
               "VALUES (%s, %s, %s, %s, %s)"


    def save_company_websites(self, companies):
        for company in companies:
            if company.website_url:
                query = self.get_update_website_query()
                self.execute_non_query(query, (company.website_url, company.reg_no), True)
        self.dispose()


