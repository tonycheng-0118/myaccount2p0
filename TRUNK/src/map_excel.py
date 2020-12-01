# Purpose: to transfer the data to normalized data structure
# Normalized structure: (which exit in val of dict)
# {name, data(yyyy_mm_dd), category, type, expense, incomnse, borrow, lend, location, tab#, note}

from tony_def import *
from map_item import *
from gen_rpt_xlsx import *
import re
import numexpr

class map_item_excel(map_item):

    
    def __init__(self):
        super().__init__()
        self.wb = None
        self.sh_active_name = None
        self.date_range = ()
        self.gen_rpt = gen_rpt_xlsx() # to reuse the chk*foramt

    def do_item_map_gatekeeper(self,item):
        """
        a call back to for all pre processing before do_item_map_preproc
        return: item_valid=True/False,
        purpose: 1. to filter out the invalid item in raw data
        """
        chk = True
        
        return chk
    
    def do_item_map_preproc(self,item):
        """
        a call back to for all pre processing before __do_item_map
        """
        pass
    
    def do_item_map_pstproc(self,item):
        """
        a call back to for all post processing before __do_item_map
        """
        # assign a type to invoice's item,
        item[self.map_tab.item_struc_name.index("name")] = 'Unnamed' 
        item[self.map_tab.item_struc_name.index("source")] = self.file_in+":"+self.sh_active_name
        item[self.map_tab.item_struc_name.index("status")] = 'Valid' 
    
    def chk_file(self,file_in):

        super().chk_file(file_in)

        # amke sure the wb is existed 
        try:
            self.wb = load_workbook(self.file_in)
        except:
            logging.error("%s is not existed!!!" % self.file_in)
        
        # make sure the sheet is there and unify the format
        sheet_name = self.sh_active_name 
        if (sheet_name not in self.wb.sheetnames):
            logging.error(" %s is not existed" % sheet_name)
            raise TypeError(" %s is not existed" % sheet_name)
        sheet_active = self.wb[sheet_name]
        self.gen_rpt.chk_dayaccount_format(sheet_active)


    def do_all_map(self,file_in,fileout_override=False):
        tony_func_proc_disp(msg=" Start to map csv!")
        self.chk_file(file_in)
        self.classify_ori = ['date','type','expense','note'] # pure excel can only provide these information
        
        # always write out header first
        self.do_write_header(create_file=fileout_override)
        
        # write out classify if the first all.item
        is_1st_item=True 
        if (fileout_override and is_1st_item):
            self.do_item_writeout(self.map_tab.item_struc_name)
            is_1st_item=False

        # map the ori to mapped 
        self.do_classify_map()

        # write out to csv 
        sheet_active = self.wb[self.sh_active_name]
        # tmp_list = self.gen_rpt.dayaccount_date_position.copy() # due to reverse is an in place operation, copy for manipulate
        # tmp_date = next(i for i in tmp_list if i is not 'None')  # formate is yyyy_mm_dd
        # start_date = tmp_date[0:4]+tmp_date[5:7]+tmp_date[8:10] # format is yyyymmdd
        # tmp_list.reverse()
        # tmp_date = next(i for i in tmp_list if i is not 'None')  # formate is yyyy_mm_dd
        # end_date = tmp_date[0:4]+tmp_date[5:7]+tmp_date[8:10] # format is yyyymmdd
        # tmp_date = pd.date_range(start_date,end_date)
        # tmp_date = tmp_date.format(formatter=lambda x: x.strftime('%Y_%m_%d'))

        mydate_vld = [i for i in self.gen_rpt.dayaccount_date_position if i is not 'None']
        for mydate in mydate_vld:    
            logging.debug(mydate)
            row = self.gen_rpt.locate_dayaccount_date(self.wb[self.sh_active_name],mydate)
            col_valid = [] # to collect of (pos,type) the non empty cell
            for i in range(0,len(self.gen_rpt.dayaccount_type_position)):
                col = int(self.gen_rpt.dayaccount_type_start_position[1:]) + i # start_position always start @ A col 
                pos = row + str(col) 
                cell = sheet_active[pos]
                col_valid.append((pos,self.gen_rpt.dayaccount_type_position[i])) if cell.value != None else None

            for cell_pos in col_valid: 
                cell = sheet_active[cell_pos[0]]
                mytype = cell_pos[1]
                myexpense = cell.value
                mynote = {"CMT":cell.comment.text.strip()} if (cell.comment) else ""
                line = [mydate,mytype,myexpense,mynote]
                logging.info(line)
                # item = [i.strip() for i in line]
                item_mapped = self.do_item_map(line)
                if (item_mapped != None):
                    self.do_item_writeout(item_mapped)
                    is_1st_item=False
                else:
                    logging.info("This item is not written out")

             
if __name__ == "__main__":
    tony_func_proc_disp(msg=" Start to gen myexcel to .csv!")
    
    # myexcel = map_item_excel()
    # file_in_path = "../dat/My_account_old.xlsx"
    # myexcel.sh_active_name = "2020" 
    
    # to verify the env stability
    # myexcel = map_item_excel()
    # file_in_path = "./all_out.202011131943.bu/gen_rpt.xlsx"
    # myexcel.sh_active_name = "dayaccount" 
    # myexcel.do_all_map(file_in=file_in_path,fileout_override=True)
    
    # to test inc.xlsx
    myexcel = map_item_excel()
    myexcel.gen_rpt.chk_dayaccount_format_option += ['IGNORE_CHK_INVALID_CONTENT']
    file_in_path = "../dat/excel/My_account_old.xlsx"
    myexcel.sh_active_name = "2016" 
    myexcel.do_all_map(file_in=file_in_path,fileout_override=True)
    
    tony_func_proc_disp(msg=" Done gen myexcel to .csv!")