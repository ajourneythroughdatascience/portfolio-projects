# -*- coding: utf-8 -*-
"""
Created on Thu Mar  2 19:29:01 2023

@author: Pablo Aguirre

GitHub: https://github.com/pabloagn
Website: https://pabloagn.com
Contact: https://pabloagn.com/contact

Part of Portfolio Project: sentiment-analysis-in-python
"""

class StringFormatting:
    '''
    Mixin class:
        - Pad string
        - Insert log into application textlog
    '''
    def padStr(self, measure_title, value_title):
        '''
        Format a string to be inserted into log.
        '''
        measure_title += ' '
        self.padded_str = measure_title + '.'*(self.dot_sep - len(measure_title))
        self.padded_str = ('%s %s' % ( self.padded_str, value_title))

        return self.padded_str

    def insertLog(self, *args, clear=False):
        '''
        Insert a log into textlog.
        Perform all required activities associated:
            - Enable text log.
            - If clear==True, clear the log before. Else, keep.
            - Insert all kwargs into text log.
            - Disable text log.
            - Update idle tasks.
        '''
        if clear==True:
            self.textlog.configure(state="normal")
            self.textlog.delete("0.0", "end")
            for textlog in args:
                self.textlog.insert(self.print_position, textlog)
            self.textlog.configure(state="disabled")
            self.update_idletasks()

        elif clear==False:
            self.textlog.configure(state="normal")
            for textlog in args:
                self.textlog.insert(self.print_position, textlog)
            self.textlog.configure(state="disabled")
            self.update_idletasks()

        return None

# Call main function
if __name__ == '__main__':
    main()