import sys
import unittest
import itertools
import parser 

class MyCsvTest(unittest.TestCase):
    csv = parser.MyCsv("example.csv")
    csv2 = parser.MyCsv("example2.csv")
    csv_inference = parser.MyCsv("test_inference.csv")

    res_cells = [['John D', '120 any st.', '"Anytown, WW"', '08123', 'Andrew P', '114 Sansome st.',
                '"San Francisco, CA"', '94105', 'Morgan R', '905 Green st.', '"Chicago, IL"', '68100'],

                 ['"For whom the bells toll"', '0', '0', '"Bring me some shrubbery"', '2', '3',
                 '"Once upon \r\na time"', '5', '6', '"\'It\'s just a flesh wound."', '8', '9']
    ]
    res_types = [ ['String', 'String', 'String', 'Numeric'],
                  ['String', 'Numeric', 'Numeric'],
                  ['String', 'Numeric']
    ]
    res_nrows = [3,4]
    res_ncols = [4,3]
                
    def test_get_cell(self):
        cells = [self.csv.get_cell(i, j) for i, j in itertools.product(range(3), range(4))]
        cells2 = [self.csv2.get_cell(i, j) for i, j in itertools.product(range(4), range(3))]

        self.failUnless([cells, cells2] == self.res_cells)

    def test_n_rows(self):
        self.failUnless([self.csv.n_rows(), self.csv2.n_rows()] == self.res_nrows)

    def test_n_cols(self):
        self.failUnless([self.csv.n_cols(), self.csv2.n_cols()] == self.res_ncols)

    def test_infer_types(self):
        infer = self.csv.infer_types()
        infer2 = self.csv2.infer_types()
        infer_deep = self.csv_inference.infer_types() 

        self.failUnless([infer, infer2, infer_deep] == self.res_types)


def main():
    unittest.main()

if __name__ == '__main__':
    main()
