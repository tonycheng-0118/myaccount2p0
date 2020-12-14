# Purpose: to map the every type of the input *.csv to the normalize structure
# Normalized structure: (which exit in val of dict)
# {name, data(yyyy_mm_dd), category, type, expense, incomnse, source, status, location, tab#, note}i
# expense is the amount of the NTD; income, borrow, and lend are reserved for future usage 
from tony_def import *
import re
import os
import csv

class map_item_struction: 
    # initial global variable
    map_dict = {}
    item_struc_name = ["name","date","category","type","expense","income","source","status","location","tag","note"]
    item_struc_type = [i for i in range(0,len(item_struc_name))]
    item_type = ("Breakfast","Lunch","Dinner","Food_Material","Supplyment","Other_Food","Rental","Electicity","Motor_Fuel","Motor_Maintenance","Car_Fuel","Car_Maintenance","Transpotation","Parking","Easy_Card","Fitness_Fee","Sport_Equipment","Fitness_Supply","Daily_Needs","Enhancement","Book","Hair_Cut","Communication","Gift","Furniture","Medical","Cloth_Shoe","Red_Envelope","Entertainmant","Other","Salary","Bonus","Health_Examination","Reserved_Budget","Insurance","Marriage_Fund","House_Down_Payment","House_Installment","Car_Down_Payment","Car_Installment","Trave_Fund","Pension","Children_Fund","Dream_Fund","Tax","Investment","Lend","Borrow")
    map_tab_cmt_prefix = '//##'
        
    def __init__(self):
        # initialize mapping pair
        self.classify_map_order = []
        self.map_dict["name"]       = ["name","消費品項","註記"]
        self.map_dict["date"]       = ["date","消費日期","日期"]
        self.map_dict["category"]   = ["category"]
        self.map_dict["type"]       = ["type","分類"]
        self.map_dict["expense"]    = ["expense","小計","支出"]
        self.map_dict["income"]     = ["income","收入"]
        self.map_dict["source"]     = ["source"]
        self.map_dict["status"]     = ["status"]
        self.map_dict["location"]   = ["location","定位"]
        self.map_dict["tag"]        = ["tag","標籤1","標籤2"]
        self.map_dict["note"]       = ["note"]
        self.chk_map_dict_uniq()

        # for customized type feature  
        self.type_file_in  = "../exe/customized_type.csv"
        if not os.path.isfile(self.type_file_in):
            with open(self.type_file_in, 'w', newline='', encoding='UTF-8-sig') as csvfile:
                writer = csv.writer(csvfile, delimiter=',')
                writer.writerow(self.item_type)
                logging.debug ("create a default type_file")
        else:
            with open(self.type_file_in,mode='r',encoding='UTF-8-sig') as csvfile:
                for line in csvfile:
                    customized_type = line.split(",")
                    self.item_type = [i.strip() for i in customized_type]
                logging.debug ("update self.item_type")

    def gen_empty_item(self):
        empty_item = [i for i in range(0,len(self.item_struc_type))]
        empty_item[self.item_struc_name.index("name")]      = ""
        empty_item[self.item_struc_name.index("date")]      = ""
        empty_item[self.item_struc_name.index("category")]  = ""
        empty_item[self.item_struc_name.index("type")]      = ""
        empty_item[self.item_struc_name.index("expense")]   = 0
        empty_item[self.item_struc_name.index("income")]    = 0  
        empty_item[self.item_struc_name.index("source")]    = ""  
        empty_item[self.item_struc_name.index("status")]    = ""  
        empty_item[self.item_struc_name.index("location")]  = ""
        empty_item[self.item_struc_name.index("tag")]       = []
        empty_item[self.item_struc_name.index("note")]      = {}
        return empty_item
    
    def gen_classify_map_order(self,classify):
        # make sure the classify can map to item_struc_name
        self.__chk_classify_content(classify)
        
        for i in classify:
            self.classify_map_order.append((classify.index(i),self.item_struc_name.index(i)))
            # aaaa = []
            # aaaa.append((classify.index(i),self.item_struc_name.index(i)))
            # print ((classify.index(i),self.item_struc_name.index(i)))
            # print (self.classify_map_order)
            # print (aaaa) 
            logging.debug("classify_map_order, (ori,map) is %s" % self.classify_map_order)

    def gen_item(self,classify,value):
        """
        classify: indicate how to map the value into item_struct_name
        value: the content put into item_struct_name
        """
        # the size of the classify and value should be the same
        if (len(value) != len(classify)):
            logging.error("the len of value is not legal: yours is %s, expecte is %s" % (len(value),len(classify)) )
        
        # make sure the classify can map to item_struc_name
        self.__chk_classify_content(classify)

        # assign content
        item = self.gen_empty_item()
        classify_copy = classify.copy() # so that the classify content can modify locally
        for i in classify:
            # print("HAHA",i)
            # print("GAGA",value[classify_copy.index(i)])
            # print("DDDD",value)
            if (i == "note"):
                # print ("in note")
                item[self.item_struc_name.index(i)].update(value[classify_copy.index(i)])
                # print (item[self.item_struc_name.index(i)])
                # print (value[classify.index(i)])
                classify_copy[classify_copy.index(i)] = "retired" # so that the next one can be found by index
            elif (i == "tag"):
                if (type(value[classify_copy.index(i)]) == list):
                    item[self.item_struc_name.index(i)] += value[classify_copy.index(i)]
                else:
                    item[self.item_struc_name.index(i)].append(value[classify_copy.index(i)])
                classify_copy[classify_copy.index(i)] = "retired" # so that the next one can be found by index
            else:
                item[self.item_struc_name.index(i)]  = value[classify_copy.index(i)]
        
        # make sure the content of the item is legal
        self.__chk_mapped_item_content(classify,item)

        return item
    
    def __chk_classify_content(self,classify):
        # the classify should map to the item_struc_name's content
        for i in classify:
            if (i not in self.item_struc_name):
                logging.error("%s is not legal classify" % (i))
    
    def __chk_mapped_item_content(self,classify,item):
        ref_item = self.gen_empty_item()
        
        # chk the size of the content
        if (len(item) != len(ref_item)):
            logging.error("the len of item is not legal: yours is %s, expecte is %s" % (len(item),len(ref_item)) )

        # chk the type of the content
        for i in range(0,len(item)):
            if (type(item[i]) != type(ref_item[i])):
                logging.error("in %s, the type of %s is no legal: yours is %s, expecte is %s" % (self.item_struc_name[i],item[i],type(item[i]),type(ref_item[i])) )

        # chk the format of the content
        chk_pattern = r'\d{4}_\d{2}_\d{2}'
        if not ( re.match(chk_pattern,item[self.item_struc_name.index('date')],0) ):
            logging.error("date formate should be yyyy_mm_dd, and yours is %s" % item[self.item_struc_name.index('date')])
        
        #chk the content existence
        if not (item[self.item_struc_name.index('type')] in self.item_type):
            # it may be Ok for invoice, because the type is assigned at pstproc stage 
            logging.info("no such type. yours is %s" % item[self.item_struc_name.index('type')])

    
    def print_map(self):
        logging.info(self.map_dict)

    def find_item_struc_name(self,type="NA"):
        match = "NA"
        for k,v in self.map_dict.items():
            try:
                match = v.index(type)
                logging.info("Type: %s is found, and mapped to: %s" % (type,k))
                return k 
            except (ValueError):
                # logging.debug("Type: %s is NOT found" % (type)
                pass
        return "NA"

    def add_map_src(self,dst="NA",src="NA"):
        """
        dst: Normalized structure, src: original classify
        """
        self.map_dict[dst].append(src)
        self.chk_map_dict_uniq()

    def chk_map_dict_uniq(self):
        """
        to check the uniquence of classify before map
        """
        a_list = []
        for v in self.map_dict.values():
            a_list+=v # using append will not merge the list content
        duplicate_list = [ i for i in a_list if (a_list.count(i)>1)] # find out the dupplicated member
        duplicate_list = set(duplicate_list) # unique the duplicated one
        # logging.debug(a_list)
        logging.error("Those classify is dulicated!! %s" % str(duplicate_list)) if len(duplicate_list)>0 else 0

    def chk_item_type(self,item_type):
        """
        chk the existence of the item type
        """
        return self.item_type[self.item_type.index(item_type)]
    
    def get_item_type(self,item_type):
        """
        get the item type
        """
        self.chk_item_type(item_type) 
        return item_type 
    
    def chg_mapped_item_type(self,src_item):
        """
        change every item's type back to expected one   
        """
        ref_item = self.gen_empty_item()
        
        # chk the size of the item   
        if (len(src_item) != len(ref_item)):
            raise TypeError("the len of item is not legal: yours is %s, expecte is %s" % (len(item),len(ref_item)) )

        # chg the type of the content
        for i in range(0,len(src_item)):
            if (type(src_item[i]) != type(ref_item[i])):
                # print (src_item[i])
                if (type(ref_item[i]) == int ):
                    # print (i, " ", type(src_item[i]), " ", src_item)
                    src_item[i] = int(src_item[i])
                elif (type(ref_item[i]) == str ):
                    src_item[i] = str(src_item[i])
                elif (type(ref_item[i]) == list ):
                    if(src_item[i] =="[]"):
                        src_item[i] = []
                    else:
                        src_item[i] = list(src_item[i])
                elif (type(ref_item[i]) == dict ):
                    src_item[i] = eval(src_item[i])
                else:
                    raise ("No other is supported here")

        
if __name__ == "__main__":
    # test
    A = map_item_struction()
    print(A.find_item_struc_name("消費日期"))
    print(A.find_item_struc_name("消費品項AAAA"))
    A.add_map_src(dst="date",src="註記")
    A.chk_map_dict_uniq()
    t0 = list(enumerate(A.item_struc_name))
    print (t0[0][0])
    print (t0[0][1])
    print (type(t0[0]))
    t_classify = ["name","date"]
    t_value = ["HAHA","202010230706"]
    t_item = A.gen_item(t_classify,t_value)
    print (t_item)
