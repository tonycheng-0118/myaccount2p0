# Purpose: to transfer the data to normalized data structure
# Normalized structure: (which exit in val of dict)
# {name, data(yyyy_mm_dd), category, type, expense, incomnse, borrow, lend, location, tab#, note}

from tony_def import *
from map_item import *
import re

class map_item_littlebox(map_item):

    def __init__(self):
        super().__init__()
        self.map_tab.add_map_src(dst="name",src="註記")
        self.map_tab.add_map_src(dst="date",src="日期")
        self.map_tab.add_map_src(dst="type",src="分類")
        self.map_tab.add_map_src(dst="expense",src="支出")
        self.map_tab.add_map_src(dst="income",src="收入")
        self.map_tab.add_map_src(dst="location",src="定位")
        self.map_tab.add_map_src(dst="tag",src="標籤1")
        self.map_tab.add_map_src(dst="tag",src="標籤2")

    def do_item_map_gatekeeper(self,item):
        """
        a call back to for all pre processing before do_item_map_preproc
        return: item_valid=True/False,
        purpose: 1. to filter out the invalid item in raw data
        """
        chk = True
        
        # chk the date format
        chk_pattern = r'"0"' # no income in littlebox
        chk_src = item[self.classify_ori.index('收入')]
        if not ( re.match(chk_pattern,chk_src,0) ):
            logging.error("formate should be %s, and yours is %s" % (chk_pattern,chk_src))
            raise TypeError("Error")
            chk = False
        
        # # chk the expense format
        # chk_pattern = r'-?\d+'
        # chk_src = item[self.classify_ori.index('小計')]
        # if not ( re.match(chk_pattern,chk_src,0) ):
        #     logging.info("formate should be %s, and yours is %s" % (chk_pattern,chk_src))
        #     chk = False
        
        # # chk the other format
        # chk_pattern = r'-?\d+'
        # chk_src = item[self.classify_ori.index('個數')]
        # if not ( re.match(chk_pattern,chk_src,0) ):
        #     logging.info("formate should be %s, and yours is %s" % (chk_pattern,chk_src))
        #     chk = False
        
        # # chk the other format
        # chk_pattern = r'-?\d+'
        # chk_src = item[self.classify_ori.index('單價')]
        # if not ( re.match(chk_pattern,chk_src,0) ):
        #     logging.info("formate should be %s, and yours is %s" % (chk_pattern,chk_src))
        #     chk = False

        return chk
    
    def do_item_map_preproc(self,item):
        """
        a call back to for all pre processing before __do_item_map
        """
        # translate year of the "Republic Era" to AD
        date_yyyy =         item[self.classify_ori.index('日期')][0:4]
        date_mm   =         item[self.classify_ori.index('日期')][5:7]         
        date_dd   =         item[self.classify_ori.index('日期')][8:10]         
        item[self.classify_ori.index('日期')] = date_yyyy+"_"+date_mm+"_"+date_dd

        # rid of "" for string type
        for i in range(0,len(item)):
            if (i != self.classify_ori.index('日期')):
                item[i] = str(item[i][1:-1])

        # translate expense type from str to int
        item[self.classify_ori.index('支出')] = int(item[self.classify_ori.index('支出')])
        item[self.classify_ori.index('收入')] = int(item[self.classify_ori.index('收入')])

        # fill in empty name
        if (item[self.classify_ori.index('註記')] == ""):
            item[self.classify_ori.index('註記')] = "Unnamed"

        # extend tags
        if (len(item) != len(self.classify_ori)): # to extend the tags
            for i in range(len(item),len(self.classify_ori)):
                item.append("")
        # print(item)
    
    def do_item_map_pstproc(self,item):
        """
        a call back to for all post processing before __do_item_map
        """
        # assign a type to invoice's item,
        item[self.map_tab.item_struc_name.index("source")] = self.file_in 
        item[self.map_tab.item_struc_name.index("status")] = 'Valid' 

        

             
if __name__ == "__main__":
    tony_func_proc_disp(msg=" Start to gen littlebox to .csv!")
    littlebox = map_item_littlebox()
    file_in_path = "../dat/littlebox/小票盒_201109.csv" 
    # file_in_path = "../dat/littlebox/littlebox_example.csv" 
    littlebox.do_all_map(file_in=file_in_path,fileout_override=True)

    tony_func_proc_disp(msg=" Done gen littlebox to .csv!")