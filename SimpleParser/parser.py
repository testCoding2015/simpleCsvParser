import re

class MyCsv(object):
    def __init__(self, path):
        """
        Simple csv parser that provides 
        access to every cell, number of rows,
        number of columns, type inference
        """
        self. list_all_fields = []
        self.csv_file = path

        csv_file = open(path, 'r')
        self.all_file_in_str = csv_file.read()

        rgx = re.compile(r'''
            \s*                # illimted number of spaces
            (                  # begin group
              [^,"]+?          # serie of non-comma non-quote characters
              |                # or
              "(?:             # A double-quote followed by a string of characters...
                  [^"]         # That non-quotes 
               )*              # ...repeated any number of times.
              "                # Followed by a closing double-quote.
            )                  # End group.
            \s*                # Allow arbitrary space before the comma.
            (?:,|\r\n)         # Followed by a comma or a newline.
            ''', re.VERBOSE)
        self.list_all_fields = rgx.findall(self.all_file_in_str) 

    def n_cols(self):   
        """
        computes how many columns we get based on list_all_fields
        which is a flattened list of all cells
        """
        nb_commas = 0
        idx_char = 0
        nb_quotes = 0

        while idx_char <= (len(self.all_file_in_str)-1):
            if self.all_file_in_str[idx_char] == '"':
                nb_quotes += 1

            if nb_quotes%2 == 0: #we are not inside a wrapper
                if self.all_file_in_str[idx_char] == ',':
                    nb_commas += 1

                elif self.all_file_in_str[idx_char] == '\r':
                    break;
            idx_char += 1
        return nb_commas +1 

    def n_rows(self):
        return len(self.list_all_fields) / self.n_cols()

    def get_cell(self, row, col): 
        """
        * access and individual cell of the csv
        given the 2 cordinantes (row,col)
        * known n_cols() we can easily acess the cell 
        """
        if not(0 <= row < self.n_rows() and  0 <= col < self.n_cols()):
            raise ValueError('incorrect cell index')
        return self.list_all_fields[row*self.n_cols()+col] 

    def infer_types(self): 
        """
        We assume that the possible number formats are: 
        xxx yyy.zz   (for example 123 145.12) 
        xxx,yyy.zz   (for example 123,145.12) 
        xxxyyy.zz    (for example 123145.12)  
        xxx          (for example 123 ) 
        """   
        types = ["Numeric"]*self.n_cols()
        
        for idx_col in range(self.n_cols()):
            maybe_numeric = True
            idx_line = 0

            while maybe_numeric and  idx_line <= (self.n_rows()-1):
                cell = self.get_cell(idx_line, idx_col)

                try:
                    _ = float(cell.replace(" ", "").replace("\"", ""))   
                except ValueError:
                    try:        
                        _ = float(cell.replace(",", "").replace("\"", ""))  
                    except ValueError:        
                        types[idx_col] = 'String'
                        maybe_numeric = False
                
                idx_line += 1
                
        return types   


