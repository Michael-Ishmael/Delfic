from delfic.crawler.sitelocator import WebsiteLocator
from delfic.data.dbacccess import CompanyRepository

__author__ = 'scorpio'


repo = CompanyRepository()
companies = repo.get_companies(3323)

missedCompanies = []
foundCompanies = []

for i in range(0, len(companies)):
    company = companies[i]
    if i == 0:
        locator = WebsiteLocator(company.name, company.reg_no, company.post_code, False)
    else:
        locator.reload(company.name, company.reg_no, company.post_code)
    url = locator.find_website()
    if url:
        company.website_url = url
        foundCompanies.append(company)
    else:
        missedCompanies.append(company)
    print(i)
    if i > 0 and i % 10 == 0:
        repo.save_company_websites(foundCompanies)
        foundCompanies = []

print("{0}% websites found".format(len(missedCompanies) / float(len(foundCompanies))))




