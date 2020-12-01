# Purpose: to transfer the data to normalized data structure
# Normalized structure: (which exit in val of dict)
# {name, data(yyyy_mm_dd), category, type, expense, incomnse, borrow, lend, location, tab#, note}

from tony_def import *
from map_item import *
import re

class map_item_invoice(map_item):

    def __init__(self):
        super().__init__()

    def do_item_map_gatekeeper(self,item):
        """
        a call back to for all pre processing before do_item_map_preproc
        return: item_valid=True/False,
        purpose: 1. to filter out the invalid item in raw data
        """
        chk = True
        
        # chk the date format
        chk_pattern = r'\d{3}\d{2}\d{2}'
        chk_src = item[self.classify_ori.index('消費日期')]
        if not ( re.match(chk_pattern,chk_src,0) ):
            logging.info("formate should be %s, and yours is %s" % (chk_pattern,chk_src))
            chk = False
        
        # chk the expense format
        chk_pattern = r'-?\d+'
        chk_src = item[self.classify_ori.index('小計')]
        if not ( re.match(chk_pattern,chk_src,0) ):
            logging.info("formate should be %s, and yours is %s" % (chk_pattern,chk_src))
            chk = False
        
        # chk the other format
        chk_pattern = r'-?\d+'
        chk_src = item[self.classify_ori.index('個數')]
        if not ( re.match(chk_pattern,chk_src,0) ):
            logging.info("formate should be %s, and yours is %s" % (chk_pattern,chk_src))
            chk = False
        
        # chk the other format
        chk_pattern = r'-?\d+'
        chk_src = item[self.classify_ori.index('單價')]
        if not ( re.match(chk_pattern,chk_src,0) ):
            logging.info("formate should be %s, and yours is %s" % (chk_pattern,chk_src))
            chk = False

        return chk
    
    def do_item_map_preproc(self,item):
        """
        a call back to for all pre processing before __do_item_map
        """
        # translate year of the "Republic Era" to AD
        date_yyyy = str(int(item[self.classify_ori.index('消費日期')][0:3]) + 1911)
        date_mm   =         item[self.classify_ori.index('消費日期')][3:5]         
        date_dd   =         item[self.classify_ori.index('消費日期')][5:7]         
        item[self.classify_ori.index('消費日期')] = date_yyyy+"_"+date_mm+"_"+date_dd

        # translate expense type from str to int
        item[self.classify_ori.index('小計')] = int(item[self.classify_ori.index('小計')])

        # traslate note to dict
        item[self.classify_ori.index('單價')] = {"單價":item[self.classify_ori.index('單價')]}
        item[self.classify_ori.index('個數')] = {"個數":item[self.classify_ori.index('個數')]}
        item[self.classify_ori.index('店家名稱')] = str(item[self.classify_ori.index('店家名稱')])
        # print(item)
    
    def do_item_map_pstproc(self,item):
        """
        a call back to for all post processing before __do_item_map
        """
        # assign a type to invoice's item,
        item[self.map_tab.item_struc_name.index("type")] = self.map_tab.get_item_type('Other_Food') # TODO, create a re to map the type from name
        item[self.map_tab.item_struc_name.index("source")] = self.file_in 
        item[self.map_tab.item_struc_name.index("status")] = 'Valid' 

        

             
if __name__ == "__main__":
    # for item in data_in:
    #     type = map_tab.find_item_type(item)
    #     print ("item: %s, type: %s" % (item,type))
    tony_func_proc_disp(msg=" Start to gen invoice to .csv!")
    invoice = map_item_invoice()
    invoice.map_tab.add_map_src(dst="note",src="單價")
    invoice.map_tab.add_map_src(dst="note",src="個數")
    invoice.map_tab.add_map_src(dst="location",src="店家名稱")
    file_in_path = "../dat/invoice/invoice_detail_export_10908.csv"
    invoice.do_all_map(file_in=file_in_path,fileout_override=True)
    # for year in range(108,110,1):
    #     for month in range(1,13,1):
    #         i = year*100+month
    #         if ( (10812<=i) and (i<=10911) ):
    #             path = "../dat/invoice_detail_export_"
    #             file_in_path = path + str(i) + ".csv"
    #             invoice.do_all_map(file_in=file_in_path,fileout_override=(i==10812))
    #         else:
    #             pass

    tony_func_proc_disp(msg=" Done gen invoice to .csv!")