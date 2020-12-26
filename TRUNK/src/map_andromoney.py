# Purpose: to transfer the data to normalized data structure
# Normalized structure: (which exit in val of dict)
# {name, data(yyyy_mm_dd), category, type, expense, incomnse, borrow, lend, location, tab#, note}

from numpy.core.numeric import NaN
from tony_def import *
from map_item import *
import pandas as pd
import re

class map_item_andromoney(map_item):

    def __init__(self):
        super().__init__()
        self.map_tab.add_map_src(dst="name",src="Id")
        self.map_tab.add_map_src(dst="note",src="幣別")
        self.map_tab.add_map_src(dst="date",src="日期")
        self.map_tab.add_map_src(dst="category",src="分類")
        self.map_tab.add_map_src(dst="type",src="子分類")
        self.map_tab.add_map_src(dst="expense",src="金額")
        self.map_tab.add_map_src(dst="income",src="金額") # will be distinguish via type
        self.map_tab.add_map_src(dst="note",src="付款(轉出)")
        self.map_tab.add_map_src(dst="note",src="收款(轉入)")
        self.map_tab.add_map_src(dst="note",src="備註")
        self.map_tab.add_map_src(dst="note",src="Periodic")
        self.map_tab.add_map_src(dst="note",src="專案")
        self.map_tab.add_map_src(dst="note",src="商家(公司)")
        self.map_tab.add_map_src(dst="note",src="uid")
        self.map_tab.add_map_src(dst="note",src="時間")
        self.map_tab.add_map_src(dst="note",src="status")


    def do_item_map_preparse(self,file_in,file_out):
        """
        a call back to for all pre paraing before do_item_map_gatekeeper 
        return: file 
        purpose: 1. to normalize the /r case 
        """

        pass

    
    def do_item_map_gatekeeper(self,item):
        """
        a call back to for all pre processing before do_item_map_preproc
        return: item_valid=True/False,
        purpose: 1. to filter out the invalid item in raw data
        """
        # to differentiate andromoney and other
        chk_pattern = r'{pattern}'.format(pattern = ANDROMONEY_EXPORT_COMMA_REPLACE)
        chk_src = str(item[self.classify_ori.index('備註')])
        logging.info (re.findall(chk_pattern,chk_src,0))
        found_myaccount_note_pattern = ( len(re.findall(chk_pattern,chk_src,0)) == (len(self.map_tab.item_struc_name)-1) ) 
        if (found_myaccount_note_pattern): # the note of non primitive andromoney will not have such pattern 
            chk = False
        else:
            logging.info("Found andromoney primitive format item")
            if ( item[self.classify_ori.index('分類')] == ANDROMONEY_RSV_CATEGORY ): # a rsv item in andromoney
                logging.info("Found andromoney primitive rsv category")
                chk = False
            else:
                chk = True
        
        # weird part, due to some utf8 translate error from andromoney, some note can be totally disapeared and leave status=14
        if (type(item[self.classify_ori.index('status')])==float): # sometimes andromoney have nothing in status
            if ((found_myaccount_note_pattern==0) and item[self.classify_ori.index('status')]==14.0): # I thonk this is how andromoney differentiate non primitive key word
                logging.info ("GOTTA from andromoney, for non primitive item and utf8 encode error!")
                chk = False

        return chk
    
    def do_item_map_preproc(self,item):
        """
        a call back to for all pre processing before __do_item_map
        """
        # translate year of the "Republic Era" to AD
        # print (self.classify_ori.index('日期'))
        # print (type(item[self.classify_ori.index('日期')]))
        tmp = str(item.iloc[self.classify_ori.index('日期')])
        date_yyyy = tmp[0:4]
        date_mm   = tmp[4:6]         
        date_dd   = tmp[6:8]         
        # item.iloc[self.classify_ori.index('日期')] = date_yyyy+"_"+date_mm+"_"+date_dd # may have potential call by share hazard
        item.iat[self.classify_ori.index('日期')] = date_yyyy+"_"+date_mm+"_"+date_dd # recommend way
        
        # traslate note to dict
        col2note = ["幣別","付款(轉出)","收款(轉入)","備註","Periodic","專案","商家(公司)","uid","時間"]
        for i in col2note:
            # print (item[self.classify_ori.index(i)])
            tmp0 = str(item.iloc[self.classify_ori.index(i)])
            tmp1 = tmp0.strip()
            tmp2 = re.sub('\r\n'," ",tmp1) # to remove newline case
            # item.iloc[self.classify_ori.index(i)] = str({i:tmp2})
            item.iat[self.classify_ori.index(i)] = {i:tmp2}
            pass

        # # rid of "" for string type
        # for i in range(0,len(item)):
        #     if (i != self.classify_ori.index('日期')):
        #         item[i] = str(item[i][1:-1])

        # # translate expense type from str to int
        # item[self.classify_ori.index('支出')] = int(item[self.classify_ori.index('支出')])
        # item[self.classify_ori.index('收入')] = int(item[self.classify_ori.index('收入')])

        # # fill in empty name
        # if (item[self.classify_ori.index('註記')] == ""):
        #     item[self.classify_ori.index('註記')] = "Unnamed"

        # # extend tags
        # if (len(item) != len(self.classify_ori)): # to extend the tags
        #     for i in range(len(item),len(self.classify_ori)):
        #         item.append("")
        # # print(item)
    
    def do_item_map_pstproc(self,item):
        """
        a call back to for all post processing before __do_item_map
        """
        # assign a type to invoice's item,
        item[self.map_tab.item_struc_name.index("source")] = self.file_in 
        item[self.map_tab.item_struc_name.index("status")] = ANDROMONEY_VALID_KEYWD

    # rewrite via pd 
    def do_all_map(self,file_in,fileout_override=False,pre_parse=False):
        tony_func_proc_disp(msg=" Start to map csv!")
        self.chk_file(file_in)
        self.do_write_header(create_file=fileout_override)
        
        df = pd.DataFrame() # raw data from csv
        df = pd.read_csv(file_in,index_col=False, header=1)
        df.fillna("",inplace=True)
        # print (df)


        self.classify_ori = [i for i in df.columns]
        self.do_classify_map()
        is_1st_item=True 
        for i in range(df.shape[0]):
            item_mapped = self.do_item_map(df.iloc[i,:]) # please aware of pass by share
            if (item_mapped != None):
                if (fileout_override and is_1st_item):
                    self.do_item_writeout(self.map_tab.item_struc_name)
                self.do_item_writeout(item_mapped)
                is_1st_item=False
            else:
                logging.info("This item is not written out")

        # with open(file_proc,mode='r',encoding='UTF-8-sig') as fp:
        #     is_classify=True
        #     is_1st_item=True 
        #     for line in fp:
        #         if(is_classify):
        #             is_classify=False
        #             original = line.split(",")
        #             original = [i.strip() for i in original]
        #             self.classify_ori = original
        #             self.do_classify_map()
        #         else:
        #             item = line.split(",")
        #             item = [i.strip() for i in item]
        #             item_mapped = self.do_item_map(item)
        #             if (item_mapped != None):
        #                 if (fileout_override and is_1st_item):
        #                     self.do_item_writeout(self.map_tab.item_struc_name)
        #                 self.do_item_writeout(item_mapped)
        #                 is_1st_item=False
        #             else:
        #                 logging.info("This item is not written out")
        #             # logging.debug(item)
        

             
if __name__ == "__main__":
    tony_func_proc_disp(msg=" Start to gen andromoney to .csv!")
    andromoney = map_item_andromoney()
    file_in_path = "../dat/andromoney/AndroMoney_test_example.csv" 
    andromoney.do_all_map(file_in=file_in_path,fileout_override=True)

    tony_func_proc_disp(msg=" Done gen andromoney to .csv!")
