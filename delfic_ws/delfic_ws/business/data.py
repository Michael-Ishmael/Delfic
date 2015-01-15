import sys
from CompanyCrawler.models import Company

__author__ = 'funhead'

import csv


class CsvLoader:
    def __init__(self):
        self.fieldOrdinals = []
        self.setup_field_ordinals()

    def handle_uploaded_file(self, csvFile):
        csv.register_dialect('norm', delimiter=',', quoting=csv.QUOTE_MINIMAL)
        csvFile.seek(0)
        reader = csv.reader(csvFile, 'norm')
        reader.next()
        # companies = []
        for rowDef in reader:
            i = 0
            cur_comp = Company()
            set = True
            try:
                for val in rowDef:
                    val_stp = val.strip()
                    if val_stp != "NULL":
                        setattr(cur_comp, self.fieldOrdinals[i], val_stp)
                    i += 1
            except:
                set = False
            if set:
                try:
                    cur_comp.save()
                except Exception as ex:
                    sys.stdout.write(ex.message)
                    pass
                    # companies.append(cur_comp)
                    #return companies

    def setup_field_ordinals(self):
        self.fieldOrdinals = [
            "RegisteredNumber",
            "Name",
            "Turnover",
            "Profit",
            "Employees",
            "SIC",
            "AddressLine1",
            "AddressLine2",
            "AddressLine3",
            "AddressLine4",
            "AddressLine5",
            "Town",
            "County",
            "Postcode"
        ]