# Purpose: to transfer the data to normalized data structure
# Normalized structure: (which exit in val of dict)
# {name, data(yyyy_mm_dd), category, type, expense, incomnse, borrow, lend, location, tab#, note}

from tony_def import *
from map_littlebox import *
from map_invoice import *
from map_excel import *
from map_manual import *
import re
import glob
import shutil



             
def gen_map_item_all():
    tony_func_proc_disp(msg=" Start to collect all map_*_item to .csv!")

    is_first_writeout = True

    # 1 
    tony_func_proc_disp(msg=" Start to gen littlebox to .csv!")
    file_in_path = "../dat/littlebox/*.csv" 
    file_in_all = glob.glob(file_in_path)
    for file_in in file_in_all:   
        logging.info("Processing %s" % file_in) 
        littlebox = map_item_littlebox()
        if (is_first_writeout):
            littlebox.do_all_map(file_in=file_in,fileout_override=True)
        else:
            littlebox.do_all_map(file_in=file_in,fileout_override=False)
            is_first_writeout = False
    tony_func_proc_disp(msg=" Done gen littlebox to .csv!")
    
    # 2
    tony_func_proc_disp(msg=" Start to gen invoice to .csv!")
    invoice = map_item_invoice()
    invoice.map_tab.add_map_src(dst="note",src="單價")
    invoice.map_tab.add_map_src(dst="note",src="個數")
    invoice.map_tab.add_map_src(dst="location",src="店家名稱")
    file_in_path = "../dat/invoice/*.csv" 
    file_in_all = glob.glob(file_in_path)
    for file_in in file_in_all:   
        logging.info("Processing %s" % file_in) 
        invoice.do_all_map(file_in=file_in,fileout_override=False)
    tony_func_proc_disp(msg=" Done gen invoice to .csv!")

    # 3
    file_in_path = "../dat/excel/*.xlsx" 
    file_in_all = glob.glob(file_in_path)
    for file_in in file_in_all:   
        logging.info("Processing %s" % file_in) 
        myexcel = map_item_excel()
        myexcel.wb = load_workbook(file_in)
        sheet_all = myexcel.wb.sheetnames
        myexcel.wb.close()
        
        for sheet in sheet_all:
            myexcel = map_item_excel()
            myexcel.wb = load_workbook(file_in)
            myexcel.sh_active_name = sheet 
            
            chk_pattern = r'.*My_account_inc.xlsx'
            myexcel.gen_rpt.chk_dayaccount_format_option  = []
            if ( re.match(chk_pattern,file_in,0) ):
                myexcel.gen_rpt.chk_dayaccount_format_option += ['IGNORE_CHK_INVALID_CONTENT']
        
            myexcel.do_all_map(file_in=file_in,fileout_override=False)
            myexcel.wb.close()
            tony_func_proc_disp(msg=" Done gen myexcel:%s:%s to .csv!" % (file_in,sheet))
    
    # 4
    tony_func_proc_disp(msg=" Start to gen manual to .csv!")
    manual = map_item_manual()
    file_in_path = "../dat/manual/*.csv" 
    file_in_all = glob.glob(file_in_path)
    for file_in in file_in_all:   
        logging.info("Processing %s" % file_in) 
        manual.do_all_map(file_in=file_in,fileout_override=False)
    tony_func_proc_disp(msg=" Done gen invoice to .csv!")

    
    #### for year in range(2014,2021,1): 
    ####     tony_func_proc_disp(msg=" Start to gen myexcel:%s to .csv!" % year)
    ####     myexcel = map_item_excel()
    ####     file_in_path = "../dat/My_account_old.xlsx"
    ####     myexcel.sh_active_name = str(year) 
    ####     myexcel.do_all_map(file_in=file_in_path,fileout_override=False)
    ####     del myexcel
    
    #### 4
    #### tony_func_proc_disp(msg=" Start to gen myexcel.inc to .csv!")
    #### myexcel = map_item_excel()
    #### myexcel.gen_rpt.chk_dayaccount_format_option += ['IGNORE_CHK_INVALID_CONTENT']
    #### file_in_path = "../dat/My_account_inc.xlsx"
    #### myexcel.sh_active_name = 'inc'
    #### myexcel.do_all_map(file_in=file_in_path,fileout_override=False)
    #### tony_func_proc_disp(msg=" Done gen myexcel.inc to .csv!")

def gen_map_item_all_backup():
    cur_date = time.strftime("%Y_%m_%d", time.localtime())
    src_file = TONY_ALLOUT_DIR+"mapped_item.all.csv"
    dst_file = "../dat/all_item_backup/mapped_item_" + cur_date + ".all.csv"
    shutil.copyfile(src=src_file, dst=dst_file)
    logging.info("backup file to %s" % dst_file)

if __name__ == "__main__":

    tony_func_proc_disp(msg=" Start to test map_item_all only!!")
    
    gen_map_item_all()
    gen_map_item_all_backup()
    
    tony_func_proc_disp(msg=" Done test map_item_all only!!")

