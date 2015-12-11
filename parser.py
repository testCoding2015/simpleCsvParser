
import re

class MyCsv:

    def __init__(self, csv_file):
        self. list_all_fields = []

        f = open(csv_file,'r')
        self.all_file_in_str = f.read()

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
        
        self.list_all_fields = rgx.findall(self.all_file_in_str)  # gives a flat list of all the fields for all the columns and all the lines
            
    def n_cols(self):   # this method is also necessary for get_cell since list_all_fields is a flat list
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

    def get_cell(self,x,y): 
        if not(0<=x<self.n_rows() and  0<=y<self.n_cols()) :
            raise ValueError('incorrect cell index')

        return self.list_all_fields[x*self.n_cols() + y]   
        
    def infer_types(self): 
        """
        We assume that the possible number formats are: 

        xxx yyy.zz   (for exemple 123 145.12) 
        xxx,yyy.zz   (for exemple 123,145.12) 
        xxxyyy.zz    (for exemple 123145.12)  
        xxx          (for exemple 123 ) 

        """   
        types = ["Numeric"]*self.n_cols()
        
        for idx_col in range(0,self.n_cols()):
            maybe_numeric = True
            idx_line = 0

            while ( maybe_numeric and  idx_line <= (self.n_rows()-1) ):
                cell = self.get_cell(idx_line, idx_col)
                
                try:
                    cell_num = float(cell.replace(" ","").replace("\"",""))   # will converts 123 145.12 to the float 12314512/100
                except ValueError:
                    try:        
                        cell_num = float(cell.replace(",","").replace("\"",""))  # will converts 123,124.12 to the float 12314512/100
                    except ValueError:        
                        types[idx_col] = 'String'
                        maybe_numeric = False
                
                idx_line += 1
                
        return types   


