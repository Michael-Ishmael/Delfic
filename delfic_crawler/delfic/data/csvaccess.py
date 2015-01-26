import csv
from delfic.entities.company import Company

__author__ = 'scorpio'


class CsvLoader:
    def __init__(self):
        self.fieldOrdinals = []
        self.setup_field_ordinals()

    def load_company_file(self, path):
        with open(path) as csv_file:
            self.read_company_file(csv_file)

    def read_company_file(self, csv_file):
        csv.register_dialect('norm', delimiter=',', quoting=csv.QUOTE_MINIMAL)
        csv_file.seek(0)
        reader = csv.reader(csv_file, 'norm')
        reader.next()
        reader.next()
        companies = []
        for rowDef in reader:
            cur_comp = CompanyCsvLine()
            set = True
            try:
                i = 0
                for val in rowDef:
                    val_stp = val.strip()
                    if val_stp != "NULL":
                        if i > 13:
                            setattr(cur_comp, self.fieldOrdinals[13], val_stp)
                        else:
                            setattr(cur_comp, self.fieldOrdinals[i], val_stp)
                    i += 1
            except Exception as ex1:
                print(ex1.message)
                set = False
            if set:
                try:
                    new_comp = Company(cur_comp.reg_no, cur_comp.name, cur_comp.turnover, cur_comp.post_code)
                    companies.append(new_comp)
                except Exception as ex:
                    print(ex.message)
                    pass
        return companies

    def setup_field_ordinals(self):
        self.fieldOrdinals = [
            "reg_no",
            "name",
            "turnover",
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
            "post_code"
        ]


class CompanyCsvLine:
    def __init__(self):
        self.post_code = None
        self.turnover = None
        self.name = None
        self.reg_no = None