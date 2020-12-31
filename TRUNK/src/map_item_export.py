# Purpose: to transfer the data to normalized data structure
# Normalized structure: (which exit in val of dict)
# {name, data(yyyy_mm_dd), category, type, expense, incomnse, borrow, lend, location, tab#, note}

from tony_def import *
from map_item import *
from map_andromoney import *
import pandas as pd
from shutil import copyfile
import re

class map_item_export():

    def __init__(self):
        self.file_in  = TONY_ALLOUT_DIR+"gen_rpt.db.csv"
        self.file_ref = "../dat/all_item_export/andromoney/"+"AndroMoney_example.csv" 
        self.file_out = "../dat/all_item_export/andromoney/"+"AndroMoney_export.csv" 
        self.classify_export = []
        self.df_db = None
    
    def chk_file(self):
        if not os.path.isfile(self.file_in):
            raise TypeError("No such file!!")
        if not os.path.isfile(self.file_ref):
            raise TypeError("No such file!!")
        if not os.path.isfile(self.file_out):
            with open(self.file_out, 'w', newline='', encoding='UTF-8-sig') as csvfile:
                logging.debug ("touch the file only")
    
    def do_export_classify_extract(self):
        with open(self.file_ref, mode='r', newline='', encoding='UTF-8-sig') as csvfile:
            i = 0
            for line in csvfile:
                # print (line)
                if (i==1):
                    tmp = line.split(",")
                    self.classify_export = [i.strip() for i in tmp]
                    # tmp = [i.strip() for i in tmp]
                    # self.classify_export = [i[1:-1] for i in tmp] # rid of dummy ""
                i += 1
            # print (self.classify_export)

    def do_item_map(self):
        '''
        from ["name","date","category","type","expense","income","source","status","location","tag","note"]
        to ['Id', '幣別', '金額', '分類', '子分類', '日期', '付款(轉出)', '收款(轉入)', '備註', 'Periodic', '專案', '商家(公司)', 'uid', '時間"']
        '''
        for i in range(self.df_db.shape[0]):


            df_item = map_item()
            item = [i for i in range(0,len(self.classify_export))]

            item[self.classify_export.index('Id')]          = self.df_db.index.values[i] 
            item[self.classify_export.index('幣別')]        = "TWD" 
            item[self.classify_export.index('金額')]        = self.df_db.iloc[i,df_item.map_tab.item_struc_name.index("expense")] 
            item[self.classify_export.index('分類')]        = self.df_db.iloc[i,df_item.map_tab.item_struc_name.index("category")] 
            item[self.classify_export.index('子分類')]      = self.df_db.iloc[i,df_item.map_tab.item_struc_name.index("type")] 
            item[self.classify_export.index('日期')]        = self.df_db.iloc[i,df_item.map_tab.item_struc_name.index("date")][0:4] + \
                                                              self.df_db.iloc[i,df_item.map_tab.item_struc_name.index("date")][5:7] + \
                                                              self.df_db.iloc[i,df_item.map_tab.item_struc_name.index("date")][8:10] 
            if (self.df_db.iloc[i,df_item.map_tab.item_struc_name.index("category")]==df_item.map_tab.item_category[df_item.map_tab.item_category.index("Income")]):
                item[self.classify_export.index('付款(轉出)')]  = ""
                item[self.classify_export.index('收款(轉入)')]  = "薪資戶"
            elif (self.df_db.iloc[i,df_item.map_tab.item_struc_name.index("category")]==df_item.map_tab.item_category[df_item.map_tab.item_category.index("Transfer")]):
                item[self.classify_export.index('付款(轉出)')]  = "現金"
                item[self.classify_export.index('收款(轉入)')]  = "薪資戶"
            else:
                item[self.classify_export.index('付款(轉出)')]  = "現金"
                item[self.classify_export.index('收款(轉入)')]  = ""
            # for note
            tmp_note0 = {}
            self.df_db.iloc[i,df_item.map_tab.item_struc_name.index("note")] = re.sub(','," ",self.df_db.iloc[i,df_item.map_tab.item_struc_name.index("note")])
            for j in df_item.map_tab.item_struc_name:
                # print (type(self.df_db.iloc[i,df_item.map_tab.item_struc_name.index(j)]))
                tmp_note0.update({j:self.df_db.iloc[i,df_item.map_tab.item_struc_name.index(j)]})
            tmp_note1 = str(tmp_note0) # can be recover by eval()
            tmp_note2 = re.sub(',',ANDROMONEY_EXPORT_COMMA_REPLACE,tmp_note1)
            item[self.classify_export.index('備註')]        = tmp_note2 # for andromoney reverse to myaccount usage
            item[self.classify_export.index('Periodic')]    = ""
            item[self.classify_export.index('專案')]        = "" # for differenciation from myaccount and andromoney
            item[self.classify_export.index('商家(公司)')]  = "" # self.df_db.iloc[i,df_item.map_tab.item_struc_name.index("location")]
            item[self.classify_export.index('uid')]         = "" 
            item[self.classify_export.index('時間')]        = TONY_CURRENT_TIME
            # print (str(item)) 
              
            if (self.df_db.iloc[i,df_item.map_tab.item_struc_name.index("status")] == ANDROMONEY_VALID_KEYWD):
                note = eval(self.df_db.iloc[i,df_item.map_tab.item_struc_name.index("note")])
                col2note = ["幣別","付款(轉出)","收款(轉入)","備註","Periodic","專案","商家(公司)","uid","時間"]
                for i in col2note:
                    item[self.classify_export.index(i)] = note[i]    
            
            self.do_item_writeout(item)
        
    def do_item_writeout(self,item,create_file=False):
        access = 'w' if (create_file) else 'a'
        with open(self.file_out, access, newline='', encoding='UTF-8-sig') as csvfile:
            writer = csv.writer(csvfile, delimiter=',')
            # writer.writerow(self.map_tab.item_struc_name)
            writer.writerow(item)

    def do_item_export(self):
        self.chk_file()
        self.do_export_classify_extract()
        self.df_db = pd.read_csv(self.file_in,index_col=False)
        copyfile(src=self.file_ref, dst=self.file_out)
        self.do_item_map()

             
if __name__ == "__main__":
    tony_func_proc_disp(msg=" Start to export!")
    item_export = map_item_export()
    item_export.do_item_export()
    tony_func_proc_disp(msg=" Done export!")
