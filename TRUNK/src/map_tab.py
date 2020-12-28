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
    item_struc_name = ["name","date","category","type","expense","income","source","status","location","tag","note"]
    item_struc_type = [i for i in range(0,len(item_struc_name))]
    #item_category = ("Food","Rental","Transpotation","Sport","Enhancement","Entertainment","Other","Sporadic","Income","Transfer","Financial_Goal")
    item_category = ("3C","Education","Enhancement","Entertainment","Fashion","Financial_Goal","Food","Home_Fee","Income",\
                     "Medical","Motor","Other","Social","Sport","Transfer","Transportation","e-Invoice")
    item_type = ("Breakfast","Lunch","Dinner","Food_Material","Supplyment","Other_Food","Rental","Electricity",\
                 "Motor_Fuel","Motor_Maintenance","Car_Fuel","Car_Maintenance","Transportation","Parking",\
                 "Easy_Card","Fitness_Fee","Sport_Equipment","Fitness_Supply","Daily_Needs","Enhancement","Book","Hair_Cut",\
                 "Communication","Gift","Furniture","Medical","Cloth_Shoe","Red_Envelope","Entertainment",\
                 "Other","Salary","Bonus","Health_Examination","Reserved_Budget","Insurance","Marriage_Fund","House_Down_Payment",\
                 "House_Installment","Car_Down_Payment","Car_Installment","Trave_Fund","Pension","Children_Fund","Dream_Fund","Tax",\
                 "Investment","Lend","Borrow","Refund",'Electricity_Bill', 'Bus', 'Part-Time', 'Transfer', 'Party', 'Backpack', 'Fruit', \
                 'Plane', 'HSR', 'Stationery', 'Other_Income', 'Jeans', 'Exhibition', 'Hiking', 'Water_Fee', 'KTV', 'Accessories', \
                 'Jacket', 'Bar_Code', 'Toy', 'Donation', 'Pet', 'ETC', 'Social_Fee', 'Gas_Fee', 'MRT', 'Cable-TV', 'Fine_Ticket', \
                 'Taxi', 'Movie', 'T-shirt', 'Shoes', 'Computer_Misc', 'Education_misc', 'Shopping', 'Trip', 'House_Admin_Fee', \
                 'Allowance', 'Appliance', 'Snack', 'Computer_Device', 'Mackup', 'Internet_Fee', 'Tuition')
    item_type2category = {}
    map_tab_cmt_prefix = '//##'
        
    def __init__(self):
        # initialize mapping pair
        self.classify_map_order = []
        self.map_dict = {}
        self.map_dict["name"]       = ["name"]
        self.map_dict["date"]       = ["date"]
        self.map_dict["category"]   = ["category"]
        self.map_dict["type"]       = ["type"]
        self.map_dict["expense"]    = ["expense"]
        self.map_dict["income"]     = ["income"]
        self.map_dict["source"]     = ["source"]
        self.map_dict["status"]     = ["status"]
        self.map_dict["location"]   = ["location"]
        self.map_dict["tag"]        = ["tag"]
        self.map_dict["note"]       = ["note"]
        self.chk_map_dict_uniq()

        # for type2category

        self.item_type2category["Communication"]                =    "3C"                                                
        self.item_type2category["Computer_Device"]              =    "3C"                                                
        self.item_type2category["Computer_Misc"]                =    "3C"                                                
        self.item_type2category["Stationery"]                   =    "Education"
        self.item_type2category["Tuition"]                      =    "Education"
        self.item_type2category["Book"]                         =    "Enhancement"
        self.item_type2category["Enhancement"]                  =    "Enhancement"
        self.item_type2category["Entertainment"]                =    "Entertainment"
        self.item_type2category["Exhibition"]                   =    "Entertainment"
        self.item_type2category["Hiking"]                       =    "Entertainment"
        self.item_type2category["Education_misc"]               =    "Education"
        self.item_type2category["KTV"]                          =    "Entertainment"
        self.item_type2category["Movie"]                        =    "Entertainment"
        self.item_type2category["Party"]                        =    "Entertainment"
        self.item_type2category["Shopping"]                     =    "Entertainment"
        self.item_type2category["Toy"]                          =    "Entertainment"
        self.item_type2category["Trip"]                         =    "Entertainment"
        self.item_type2category["Accessories"]                  =    "Fashion"
        self.item_type2category["Backpack"]                     =    "Fashion"
        self.item_type2category["Hair_Cut"]                     =    "Fashion"
        self.item_type2category["Jacket"]                       =    "Fashion"
        self.item_type2category["Jeans"]                        =    "Fashion"
        self.item_type2category["Mackup"]                       =    "Fashion"
        self.item_type2category["Shoes"]                        =    "Fashion"
        self.item_type2category["T-shirt"]                      =    "Fashion"
        self.item_type2category["Cloth_Shoe"]                   =    "Fashion"
        self.item_type2category["Breakfast"]                    =    "Food"
        self.item_type2category["Dinner"]                       =    "Food"
        self.item_type2category["Food_Material"]                =    "Food"
        self.item_type2category["Fruit"]                        =    "Food"
        self.item_type2category["Lunch"]                        =    "Food"
        self.item_type2category["Other_Food"]                   =    "Food"
        self.item_type2category["Snack"]                        =    "Food"
        self.item_type2category["Supplyment"]                   =    "Food"
        self.item_type2category["Appliance"]                    =    "Home_Fee"
        self.item_type2category["Cable-TV"]                     =    "Home_Fee"
        self.item_type2category["Electricity"]                  =    "Home_Fee"
        self.item_type2category["Electricity_Bill"]             =    "Home_Fee"
        self.item_type2category["Furniture"]                    =    "Home_Fee"
        self.item_type2category["Gas_Fee"]                      =    "Home_Fee"
        self.item_type2category["House_Admin_Fee"]              =    "Home_Fee"
        self.item_type2category["Internet_Fee"]                 =    "Home_Fee"
        self.item_type2category["Rental"]                       =    "Home_Fee"
        self.item_type2category["Water_Fee"]                    =    "Home_Fee"
        self.item_type2category["Medical"]                      =    "Medical"
        self.item_type2category["Car_Fuel"]                     =    "Motor"
        self.item_type2category["Car_Maintenance"]              =    "Motor"
        self.item_type2category["ETC"]                          =    "Motor"
        self.item_type2category["Fine_Ticket"]                  =    "Motor"
        self.item_type2category["Motor_Maintenance"]            =    "Motor"
        self.item_type2category["Motor_Fuel"]                   =    "Motor"
        self.item_type2category["Parking"]                      =    "Motor"
        self.item_type2category["Donation"]                     =    "Other"
        self.item_type2category["Other"]                        =    "Other"
        self.item_type2category["Pet"]                          =    "Other"
        self.item_type2category["Gift"]                         =    "Social"
        self.item_type2category["Red_Envelope"]                 =    "Social"
        self.item_type2category["Social_Fee"]                   =    "Social"
        self.item_type2category["Fitness_Fee"]                  =    "Sport"
        self.item_type2category["Fitness_Supply"]               =    "Sport"
        self.item_type2category["Sport_Equipment"]              =    "Sport"
        self.item_type2category["Bus"]                          =    "Transportation"
        self.item_type2category["Easy_Card"]                    =    "Transportation"
        self.item_type2category["HSR"]                          =    "Transportation"
        self.item_type2category["MRT"]                          =    "Transportation"
        self.item_type2category["Plane"]                        =    "Transportation"
        self.item_type2category["Taxi"]                         =    "Transportation"
        self.item_type2category["Transportation"]               =    "Transportation"
        self.item_type2category["Bar_Code"]                     =    "e-Invoice"
        self.item_type2category["Daily_Needs"]                  =    "Home_Fee"
        self.item_type2category["Salary"]                       =    "Income"
        self.item_type2category["Part-Time"]                    =    "Income"
        self.item_type2category["Allowance"]                    =    "Income"
        self.item_type2category["Other_Income"]                 =    "Income"
        self.item_type2category["Bonus"]                        =    "Income"
        self.item_type2category["Car_Down_Payment"]             =    "Financial_Goal"
        self.item_type2category["Insurance"]                    =    "Financial_Goal"
        self.item_type2category["Investment"]                   =    "Financial_Goal"
        self.item_type2category["Lend"]                         =    "Financial_Goal"
        self.item_type2category["Marriage_Fund"]                =    "Financial_Goal"
        self.item_type2category["Tax"]                          =    "Financial_Goal"
        self.item_type2category["Trave_Fund"]                   =    "Financial_Goal"
        self.item_type2category["Transfer"]                     =    "Transfer"
        self.item_type2category["Refund"]                       =    "Transfer"
        self.item_type2category["Health_Examination"]           =    "Financial_Goal"
        self.item_type2category["Borrow"]                       =    "Financial_Goal"
        self.item_type2category["Dream_Fund"]                   =    "Financial_Goal"
        self.item_type2category["House_Down_Payment"]           =    "Financial_Goal"
        self.item_type2category["Reserved_Budget"]              =    "Financial_Goal"
        self.item_type2category["Children_Fund"]                =    "Financial_Goal"
        self.item_type2category["House_Installment"]            =    "Financial_Goal"
        self.item_type2category["Car_Installment"]              =    "Financial_Goal"
        self.item_type2category["Pension"]                      =    "Financial_Goal"

        # for customized type feature  
        type_file_in  = "../exe/customized_type.csv"
        if not os.path.isfile(type_file_in):
            with open(type_file_in, 'w', newline='', encoding='UTF-8-sig') as csvfile:
                writer = csv.writer(csvfile, delimiter=',')
                writer.writerow(self.item_type)
                logging.debug ("create a default type_file")
        else:
            with open(type_file_in,mode='r',encoding='UTF-8-sig') as csvfile:
                for line in csvfile:
                    customized_type = line.split(",")
                    self.item_type = [i.strip() for i in customized_type]
                logging.debug ("update self.item_type")
        
        # for customized category feature  
        category_file_in  = "../exe/customized_category.csv"
        if not os.path.isfile(category_file_in):
            with open(category_file_in, 'w', newline='', encoding='UTF-8-sig') as csvfile:
                writer = csv.writer(csvfile, delimiter=',')
                writer.writerow(self.item_category)
                logging.debug ("create a default category_file")
        else:
            with open(category_file_in,mode='r',encoding='UTF-8-sig') as csvfile:
                for line in csvfile:
                    customized_category = line.split(",")
                    self.item_category = [i.strip() for i in customized_category]
                logging.debug ("update self.item_category")

        # for type2category 
        type2category_file_in  = "../exe/customized_type2type2category.csv"
        str_tmp = []
        for k,v in self.item_type2category.items():
            str_tmp += ['{key}:{value}'.format(key=k,value=v)]
        if not os.path.isfile(type2category_file_in):
            with open(type2category_file_in, 'w', newline='', encoding='UTF-8-sig') as csvfile:
                writer = csv.writer(csvfile, delimiter=',')
                writer.writerow(str_tmp)
                logging.debug ("create a default type2category_file")
        else:
            with open(type2category_file_in,mode='r',encoding='UTF-8-sig') as csvfile:
                self.item_type2category = {} 
                for line in csvfile:
                    tmp = line.split(",")
                    customized_type2category = [i.strip() for i in tmp]
                    for i in customized_type2category:
                        j = i.split(":")
                        self.item_type2category.update({j[0]:j[1]})
                logging.debug ("update self.item_type2category")
        if (set(self.item_type2category.keys()) != set(self.item_type)): # all type have to map to a existed category
            A = set(self.item_type2category.keys())
            B = set(self.item_type)
            logging.error("Not all item_type is assigned to category!")
            logging.error("type2category - item_type: %s" % A.difference(B))
            logging.error("item_type - type2category: %s" % B.difference(A))
            raise TypeError("Error, please check log!")
        if (set(self.item_type2category.values()) != set(self.item_category)):
            A = set(self.item_type2category.values())
            B = set(self.item_category)
            logging.info("Not all item_category is assigned to category!")
            logging.info("type2category - item_type: %s" % A.difference(B))
            logging.info("item_type - type2category: %s" % B.difference(A))
        for k,v in self.item_type2category.items(): # to chk the exist of type and category pair
            if ( (k in self.item_type) and (v in self.item_category) ):
                pass
            else:
                logging.error("customized_type: %s and customized_category: %s is not available" % (k,v))
                raise TypeError("Error, please check log!")
        pass

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
                # print (value[classify_copy.index(i)])
                # print (type(value[classify_copy.index(i)]))
                # print (self.item_struc_name.index(i))
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

    def add_map_src(self,dst="NA",src="NA",chk_uniq=True):
        """
        dst: Normalized structure, src: original classify
        """
        self.map_dict[dst].append(src)
        self.chk_map_dict_uniq(chk_uniq)

    def chk_map_dict_uniq(self,chk_uniq=True):
        """
        to check the uniquence of classify before map
        """
        if (chk_uniq):
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
