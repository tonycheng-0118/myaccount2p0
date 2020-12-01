# Purpose: to transfer the data to normalized data structure
# Normalized structure: (which exit in val of dict)
# {name, data(yyyy_mm_dd), category, type, expense, incomnse, borrow, lend, location, tab#, note}

from tony_def import *
from map_tab import map_item_struction
import csv
import os
 


class map_item:

    def __init__(self):
        self.file_in  = None
        self.file_out = "./all_out/mapped_item.all.csv" 
        # the map item structure
        self.map_tab = map_item_struction()
        self.classify_ori    = [] 
        self.classify_mapped = [] # the content of mapped structure can be duplicated, and they will group together
    
    def chk_file(self,file_in):
        if not os.path.isfile(file_in):
            raise TypeError("No such file!!")
        # if not os.path.isfile(self.file_out):
            # raise TypeError("No such file!!")
        
        self.file_in = file_in 
        logging.info("Get the file_in: %s" % self.file_in)

    def __rpt_map_pair(self):
        tmp_list = [(self.classify_ori[x],self.classify_mapped[x]) for x in range(0,len(self.classify_ori))]
        logging.info("(Before, After): %s" % tmp_list)

    def do_classify_map(self):
        classify_map=[]
        for i in self.classify_ori:
            mapped = self.map_tab.find_item_struc_name(i.strip())
            logging.error("%s is not mapped" % (i.strip())) if mapped == "NA" else 0 
            classify_map.append(mapped)
        # report the unmapped member
        self.classify_mapped = classify_map
        self.map_tab.gen_classify_map_order(self.classify_mapped)
        self.__rpt_map_pair()
    
    def do_item_map(self,item):
        item_valid = self.do_item_map_gatekeeper(item)
        if (item_valid):
            self.do_item_map_preproc(item)
            item_mapped = self.map_tab.gen_item(self.classify_mapped,item)
            self.do_item_map_pstproc(item_mapped)
            logging.debug(item_mapped)
            return item_mapped
        else:
            logging.info("This item is invalid: %s" % item)
            return None
    
    def do_item_map_gatekeeper(self,item):
        """
        a call back to for all pre processing before do_item_map_preproc
        return: item_valid=True/False,
        purpose: to filter out the invalid item in raw data
        """
        return True
    
    def do_item_map_preproc(self,item):
        """
        a call back to for all pre processing before do_item_map
        purpose: 1. to translate the raw type to map_tab type 
        """
        pass
    
    def do_item_map_pstproc(self,item):
        """
        a call back to for all post processing before do_item_map
        purpose: 1. to assign value that raw don't provided
        """
        pass

    def do_all_map(self,file_in,fileout_override=False):
        tony_func_proc_disp(msg=" Start to map csv!")
        self.chk_file(file_in)
        self.do_write_header(create_file=fileout_override)
        with open(self.file_in,mode='r',encoding='UTF-8-sig') as fp:
            is_classify=True
            is_1st_item=True 
            for line in fp:
                if(is_classify):
                    is_classify=False
                    original = line.split(",")
                    original = [i.strip() for i in original]
                    self.classify_ori = original
                    self.do_classify_map()
                else:
                    item = line.split(",")
                    item = [i.strip() for i in item]
                    item_mapped = self.do_item_map(item)
                    if (item_mapped != None):
                        if (fileout_override and is_1st_item):
                            self.do_item_writeout(self.map_tab.item_struc_name)
                        self.do_item_writeout(item_mapped)
                        is_1st_item=False
                    else:
                        logging.info("This item is not written out")
                    # logging.debug(item)
    
    def do_item_writeout(self,item,create_file=False):
        """
        expect item is list
        """
        access = 'w' if (create_file) else 'a'
        with open(self.file_out, access, newline='') as csvfile:
            writer = csv.writer(csvfile, delimiter=',')
            # writer.writerow(self.map_tab.item_struc_name)
            writer.writerow(item)
    
    def do_write_header(self,create_file):
        access = 'w' if (create_file) else 'a'
        with open(self.file_out, access, newline='') as csvfile:
            writer = csv.writer(csvfile, delimiter=',')
            writer.writerow([self.map_tab.map_tab_cmt_prefix+'='*20])
            writer.writerow([self.map_tab.map_tab_cmt_prefix+self.file_in])
            writer.writerow([self.map_tab.map_tab_cmt_prefix+TONY_CURRENT_TIME])
            writer.writerow([self.map_tab.map_tab_cmt_prefix+'='*20])



        
             
if __name__ == "__main__":
    # for item in data_in:
    #     type = map_tab.find_item_struc_name(item)
    #     print ("item: %s, type: %s" % (item,type))
    # invoice = map_item()
    # invoice.map_tab.add_map_src(dst="note",src="單價")
    # invoice.map_tab.add_map_src(dst="note",src="個數")
    # invoice.map_tab.add_map_src(dst="note",src="店家名稱")
    # invoice.do_all_map()
    tony_func_proc_disp(msg=" For test only, do nothing!")
    pass
