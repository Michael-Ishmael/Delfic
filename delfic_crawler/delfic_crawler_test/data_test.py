import unittest
from delfic.data.dbacccess import CompanyRepository

__author__ = 'scorpio'


class DbRepositoryTest(unittest.TestCase):

    def get_table_test(self):
        repo = CompanyRepository()
        companies = repo.get_companies()

        self.assertEqual(len(companies), 185)