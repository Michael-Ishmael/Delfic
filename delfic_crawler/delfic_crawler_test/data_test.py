import unittest
from delfic.data.csvaccess import CsvLoader
from delfic.data.dbacccess import CompanyRepository

__author__ = 'scorpio'


class DbRepositoryTest(unittest.TestCase):

    def get_table_test(self):
        repo = CompanyRepository()
        companies = repo.get_companies()

        self.assertEqual(len(companies), 185)


class CsvLoaderTest(unittest.TestCase):

    def load_company_file_test(self):
        loader = CsvLoader()
        loader.load_company_file("/Users/scorpio/Dev/Work/Delfic/data/comps.csv")
