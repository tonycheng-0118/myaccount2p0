# Purpose: to transfer the data to normalized data structure
# Normalized structure: (which exit in val of dict)
# {name, data(yyyy_mm_dd), category, type, expense, incomnse, borrow, lend, location, tab#, note}

from tony_def import *
from map_littlebox import *
from map_invoice import *
from map_excel import *
from map_item_all import *
import re
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QMessageBox #導入PyQt相關模塊
from PyQt5.QtGui import QRegExpValidator
from PyQt5.QtCore import QRegExp 
import sys
from map_manual_ui import * #導入之前新生成的窗口模塊 

class MyWindow(QMainWindow, Ui_MainWindow): 
    
    def __init__(self, parent=None): 
        super(MyWindow, self).__init__(parent) 
        self.map_item = map_item()
        self.import_file_path = "../dat/manual/Untitled.csv"
        self.gen_rpt = gen_rpt_xlsx() # to reuse csv2df
        self.df = pd.DataFrame(columns=self.map_item.map_tab.item_struc_name)
        self.setupUi(self)
        
        # adjust the UI widget
        self.dateEdit_date.setDate(self.calendarWidget.selectedDate()) # get PyQt4.QtCore.QDate(2011, 11, 8)
        self.comboBox_type.addItems(self.map_item.map_tab.item_type)
        rx = QRegExp("-?\\d{1,}")
        validator = QRegExpValidator(rx, self)
        self.lineEdit_expense.setValidator(validator)

    def menubar_clicked(self,action):
        logging.debug (action.text()," @ menubar")
        
        if (action.text()=="New_File"):
            cur_date = time.strftime("%Y_%m_%d", time.localtime())
            dst_file = "../dat/manual/new_item_" + cur_date + ".csv"
            self.import_file_path, filetype = QFileDialog.getSaveFileName(self,"新檔案",dst_file,"(*csv);; (*.csv)") #最後兩個參數表示只允許顯示擇csv檔
            if (self.import_file_path != ""): 
                logging.info ("New: %s, %s" % (self.import_file_path, filetype) )
                # write out a template
                self.map_item.file_in  = "None"
                self.map_item.file_out = self.import_file_path
                # self.map_item.do_write_header(create_file=True) # create header @ .all.item
                self.map_item.do_item_writeout(item=self.map_item.map_tab.item_struc_name,create_file=True)

                # clean df 
                self.df = pd.DataFrame(columns=self.map_item.map_tab.item_struc_name)

                # clean ui
                self.textBrowser_file_path.clear()
                self.textBrowser_file_path.append("<font color=red> (UNSAVED!) </font> %s" % self.import_file_path)
                self.textBrowser_item_list.clear()
            else:
                logging.debug ("New File Fail: %s, %s" % (self.import_file_path, filetype) )
        
        elif (action.text()=="Open_File"):
            self.import_file_path, filetype = QFileDialog.getOpenFileName(self,"開啟檔案","../dat/manual/","(*csv);; (*.csv)") #最後兩個參數表示只允許顯示擇csv檔

            if (self.import_file_path is not ""): 
                logging.info ("OPEN: %s, %s" % (self.import_file_path, filetype) )
                
                # read csv
                self.df = self.gen_rpt.csv2df(csv_in=self.import_file_path)
                df_str = self.df.to_string() # so that df will display all of content
                
                # show ui content
                self.textBrowser_item_list.clear()
                self.textBrowser_item_list.append(df_str)
                self.textBrowser_file_path.clear()
                self.textBrowser_file_path.append("<font color=green> (SAVED!) </font> %s" % self.import_file_path)
            else:
                logging.info ("OPEN Fail: %s, %s" % (self.import_file_path, filetype) )
        
        elif (action.text()=="Save_File"):
            cur_date = time.strftime("%Y_%m_%d", time.localtime())
            dst_file = self.import_file_path
            # self.import_file_path, filetype = QFileDialog.getSaveFileName(self,"新檔案",dst_file,"(*csv);; (*.csv)") #最後兩個參數表示只允許顯示擇csv檔
            if (self.import_file_path != ""): 
                logging.info ("Save: %s" % self.import_file_path )
                
                # write out  
                self.map_item.file_in  = "None"
                self.map_item.file_out = self.import_file_path
                # self.map_item.do_write_header(create_file=True) # create a new file with the same file name, so that so item will not duplicated
                # self.map_item.do_write_header(create_file=True) # create header @ .all.item
                self.map_item.do_item_writeout(item=self.map_item.map_tab.item_struc_name,create_file=True) # create a new file with the same file name, so that so item will not duplicated

                for i in range(len(self.df.index)):
                    self.map_item.do_item_writeout(item=self.df.iloc[i,:],create_file=False)
                
                # ui clean
                self.textBrowser_file_path.clear()
                self.textBrowser_file_path.append(self.import_file_path)
                self.textBrowser_file_path.clear()
                self.textBrowser_file_path.append("<font color=green> (SAVED!) </font> %s" % self.import_file_path)
                
            else:
                logging.info ("Save File Fail: %s" % self.import_file_path )
        
        elif (action.text()=="Exit"):
            QtCore.QCoreApplication.quit()
            logging.info ("Exit QTPY")
        
        elif (action.text()=="README"):
            logging.info ("README")

            operate_text = """
a. To generate the personal excel report:
    a) Just click the blue button "Gen report" and wait for the precessing bar reaching 100%.

b. To create a *.csv
    1) File -> New_File -> Save (the dir is in ../dat/manual/*.csv and default name is date of today).
    2) It shows the file path in the top with a RED (UNSAVED!) ahead with it.
    3) File -> Save_File (save the file to the file path).
    4) It shows the file path in the top with a GREEN (SAVED!) ahead with it.
    5) Enter the "ITEM ENTITY", the calendar in the right middle panel shows the date of today, by using it can locate the date faster.
    6) CLick the "Add_Item" for add new item.
    7) CLick the "Load_Item" to load the item @ "item_index".
    8) CLick the "Modify_Item" to modify the item @ "item_index".
    9) CLick the "Del_Item" to delete the item @ "item_index".
    ** ALWAYS remember to Save_file anytime!!

c. To edit the existed *.csv
    1) File -> Open_File -> Open (the dir is in ../dat/manual/*.csv and choose one to open).
    2) Refer to b. for further action. 
    ** ALWAYS remember to Save_file anytime!!

d. To rename/delete the existed *.csv
    1) File -> Open_File -> right-clicked the file (the dir is in ../dat/manual/*.csv and choose one to open).
    2) Select Rename or Delete.
            """

            msg = QMessageBox()
            msg.setWindowModality(QtCore.Qt.ApplicationModal)
            msg.setStyleSheet("""
                QLabel{
                    width: 200 px;
                    height: 50px;
                    font-size: 12px;
                    white-space: nowrap;
                } 
                QPushButton{ 
                    width:100px; 
                    font-size: 12px; 
                }
                QTextBrowser {
                    background-color: white;
                    background-attachment: fixed;
                    width:1000 px; font-size: 12px;
                    white-space: nowrap;
                }
                QWidget {
                    border-width: 2px;
                    border-radius: 15px;
                    border-color: black;
                    padding: 4px;
                }
                """)
            msg.setIcon(QMessageBox.Information)
            msg.setText("Guild to generate person excel report.")
            msg.setInformativeText(operate_text)
            msg.setWindowTitle("Myaccount2.0 README")
            msg.setDetailedText(operate_text)
            msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
            retval = msg.exec_()
            logging.debug (retval)
        
        elif (action.text()=="Version"):
            logging.info ("Version")

            version_text = "v1.1"
            version_info = "INFO!"

            msg = QMessageBox()
            msg.setWindowModality(QtCore.Qt.ApplicationModal)
            msg.setStyleSheet("""
                QLabel{
                    width: 200 px;
                    height: 50px;
                    font-size: 12px;
                    white-space: nowrap;
                } 
                QPushButton{ 
                    width:100px; 
                    font-size: 12px; 
                }
                QTextBrowser {
                    background-color: white;
                    background-attachment: fixed;
                    width:1000 px; font-size: 12px;
                    white-space: nowrap;
                }
                QWidget {
                    border-width: 2px;
                    border-radius: 15px;
                    border-color: black;
                    padding: 4px;
                }
                """)
            msg.setIcon(QMessageBox.Information)
            msg.setText(version_text)
            msg.setWindowTitle("Myaccount2.0 Version")
            msg.setDetailedText(version_info)
            msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
            retval = msg.exec_()
            logging.debug (retval)
        
    def button_clicked_add_item(self):
        logging.info ("button_clicked_add_item")
        # get input from ui
        i_name      = self.textEdit_name.toPlainText()
        i_date      = self.dateEdit_date.date() # get PyQt4.QtCore.QDate(2011, 11, 8)
        i_type      = self.comboBox_type.currentText() 
        i_expense   = self.lineEdit_expense.text() 
        i_location  = self.textEdit_location.toPlainText() 
        i_tag       = self.textEdit_tag.toPlainText() 
        i_note      = self.textEdit_note.toPlainText() 
        
        # parse input
        j_name = i_name
        j_date = i_date.toPyDate().strftime('%Y_%m_%d') # get 2011_11_08
        j_type = i_type
        j_expense = int(i_expense) if (i_expense != "") else 0
        j_location = i_location
        j_tag = [i.strip() for i in i_tag.split("#")] # if ( (i_tag!='#TAG') and (i_tag!='')) else [] # cannot use is not
        j_tag = j_tag[1:] # not knowing why the 1st is "" 
        j_note = {"Note":i_note} # if ( (i_note!='Note') and (i_note!='') ) else {}

        # update to df 
        item = self.map_item.map_tab.gen_empty_item()
        item[self.map_item.map_tab.item_struc_name.index("name")] = j_name 
        item[self.map_item.map_tab.item_struc_name.index("date")] = j_date
        item[self.map_item.map_tab.item_struc_name.index("type")] = j_type
        item[self.map_item.map_tab.item_struc_name.index("expense")] = j_expense
        item[self.map_item.map_tab.item_struc_name.index("income")] = 0 # rsv so far 
        item[self.map_item.map_tab.item_struc_name.index("source")] = self.import_file_path
        item[self.map_item.map_tab.item_struc_name.index("status")] = "Valid"
        item[self.map_item.map_tab.item_struc_name.index("location")] = j_location
        item[self.map_item.map_tab.item_struc_name.index("tag")] = j_tag
        item[self.map_item.map_tab.item_struc_name.index("note")] = j_note
        logging.debug (item)

        if (len(self.df.index) != 0): 
            sub = pd.DataFrame([item],columns=self.map_item.map_tab.item_struc_name,index=[max(self.df.index.values)+1])
            self.df = self.df.append(sub)
        else:
            sub = pd.DataFrame([item],columns=self.map_item.map_tab.item_struc_name,index=[0])
            self.df = self.df.append(sub)
        logging.debug (self.df)

        # always refresh the textbrowser        
        df_str = self.df.to_string() # so that df will display all of content
        self.textBrowser_item_list.clear()
        self.textBrowser_item_list.append(df_str)
        self.textBrowser_file_path.clear()
        self.textBrowser_file_path.append("<font color=red> (UNSAVED!) </font> %s" % self.import_file_path)
        
        # update the item_index
        self.spinBox_item_index.setValue(max(self.df.index.values))

    def button_clicked_load_item(self):
        logging.debug ("button_clicked_load_item")
        idx = self.spinBox_item_index.value()
        logging.debug (idx) 
        if (idx in self.df.index.values):
            item = self.df.loc[idx,:]
            i_name = item[self.map_item.map_tab.item_struc_name.index("name")]
            i_date = item[self.map_item.map_tab.item_struc_name.index("date")]
            i_type = item[self.map_item.map_tab.item_struc_name.index("type")]
            i_expense = item[self.map_item.map_tab.item_struc_name.index("expense")]
            i_income = item[self.map_item.map_tab.item_struc_name.index("income")]
            i_source = item[self.map_item.map_tab.item_struc_name.index("source")]
            i_status = item[self.map_item.map_tab.item_struc_name.index("status")]
            i_location = item[self.map_item.map_tab.item_struc_name.index("location")]
            i_tag = item[self.map_item.map_tab.item_struc_name.index("tag")]
            i_note = item[self.map_item.map_tab.item_struc_name.index("note")]
            
            if (i_tag != []):
                i_tag = [ ('#'+str(i)) for i in i_tag ]
                i_tag = " ".join(i_tag)
            else:
                i_tag = "" 
            i_note = item[self.map_item.map_tab.item_struc_name.index("note")]
            i_note = i_note['Note'] if (i_note != {}) else ""
            
            self.textEdit_name.setText(i_name)
            self.dateEdit_date.setDate(QtCore.QDate.fromString(i_date, 'yyyy_MM_dd')) # get PyQt4.QtCore.QDate(2011, 11, 8)
            self.comboBox_type.setCurrentText(i_type) 
            self.lineEdit_expense.setText(str(i_expense)) 
            self.textEdit_location.setText(i_location) 
            self.textEdit_tag.setText(i_tag) 
            self.textEdit_note.setText(i_note)

    def button_clicked_modify_item(self):
        logging.debug ("button_clicked_modify_item")
        idx = self.spinBox_item_index.value()
        logging.debug (idx) 
        
        # get input from ui
        i_name      = self.textEdit_name.toPlainText()
        i_date      = self.dateEdit_date.date() # get PyQt4.QtCore.QDate(2011, 11, 8)
        i_type      = self.comboBox_type.currentText() 
        i_expense   = self.lineEdit_expense.text() 
        i_location  = self.textEdit_location.toPlainText() 
        i_tag       = self.textEdit_tag.toPlainText() 
        i_note      = self.textEdit_note.toPlainText() 
        
        # parse input
        j_name = i_name
        j_date = i_date.toPyDate().strftime('%Y_%m_%d') # get 2011_11_08
        j_type = i_type
        j_expense = int(i_expense) if (i_expense != "") else 0
        j_location = i_location
        j_tag = [i.strip() for i in i_tag.split("#")] #if ( (i_tag!='#TAG') and (i_tag!='')) else [] # cannot use is not
        j_tag = j_tag[1:] # not knowing why the 1st is "" 
        j_note = {"Note":i_note} #if ( (i_note!='Note') and (i_note!='') ) else {}

        # update to df 
        item = self.map_item.map_tab.gen_empty_item()
        item[self.map_item.map_tab.item_struc_name.index("name")] = j_name 
        item[self.map_item.map_tab.item_struc_name.index("date")] = j_date
        item[self.map_item.map_tab.item_struc_name.index("type")] = j_type
        item[self.map_item.map_tab.item_struc_name.index("expense")] = j_expense
        item[self.map_item.map_tab.item_struc_name.index("income")] = 0 # rsv so far 
        item[self.map_item.map_tab.item_struc_name.index("source")] = self.import_file_path
        item[self.map_item.map_tab.item_struc_name.index("status")] = "Valid"
        item[self.map_item.map_tab.item_struc_name.index("location")] = j_location
        item[self.map_item.map_tab.item_struc_name.index("tag")] = j_tag
        item[self.map_item.map_tab.item_struc_name.index("note")] = j_note
        logging.debug (item)

        # if (len(self.df.index) != 0): 
        #     sub = pd.DataFrame([item],columns=self.map_item.map_tab.item_struc_name,index=[max(self.df.index.values)+1])
        #     self.df = self.df.append(sub)
        # else:
        #     sub = pd.DataFrame([item],columns=self.map_item.map_tab.item_struc_name,index=[0])
        #     self.df = self.df.append(sub)
        if (idx in self.df.index.values):
            self.df.iloc[idx,:] = item
            logging.debug (self.df)

            # always refresh the textbrowser        
            df_str = self.df.to_string() # so that df will display all of content
            self.textBrowser_item_list.clear()
            self.textBrowser_item_list.append(df_str)
            self.textBrowser_file_path.clear()
            self.textBrowser_file_path.append("<font color=red> (UNSAVED!) </font> %s" % self.import_file_path)

    def button_clicked_del_item(self):
        logging.debug ("button_clicked_del_item")
        idx = self.spinBox_item_index.value()
        logging.debug (idx)
        is_confirm_del = False 
        
        # warning msg
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Warning)
        msg.setText("Confirm to delete item_index: %s ??" % idx)
        msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)

        ret = msg.exec()
        if (ret == QMessageBox.Ok):
            logging.debug ("Confirm to del")
            is_confirm_del = True
        else:
            logging.debug ("No action")
            is_confirm_del = False

        # save the del position
        if (idx in self.df.index.values):
            tmp = self.df.index.values.tolist() # self.df.index.values is a nd.array
            del_pos = tmp.index(idx)
        else:
            del_pos = None
        
        # del the item 
        if ( (is_confirm_del) and (idx in self.df.index.values) ):
            self.df.drop(index=idx,inplace=True)
            logging.debug (self.df)

            # always refresh the textbrowser        
            df_str = self.df.to_string() # so that df will display all of content
            self.textBrowser_item_list.clear()
            self.textBrowser_item_list.append(df_str)
            self.textBrowser_file_path.clear()
            self.textBrowser_file_path.append("<font color=red> (UNSAVED!) </font> %s" % self.import_file_path)
        
            # reload the next item after del
            if (len(self.df.index.values)):
                # update the item_index
                if (del_pos==len(self.df.index.values)): # del the rightest one
                    reload_idx = self.df.index.values[del_pos-1]
                else:
                    reload_idx = self.df.index.values[del_pos] # which will be the next item in deleted df
                self.spinBox_item_index.setValue(reload_idx)

                # reload the previous one based on the spinBox value
                self.button_clicked_load_item()
        
    
    def calendar_clicked_get_date(self):
        logging.debug ("calendar_clicked_get_date")
        self.dateEdit_date.setDate(self.calendarWidget.selectedDate()) # get PyQt4.QtCore.QDate(2011, 11, 8)
        i_date = self.calendarWidget.selectedDate()
        j_date = i_date.toPyDate().strftime('%Y_%m_%d') # get 2011_11_08
        logging.debug (i_date,j_date)
    
    def button_clicked_gen_rpt(self):
        logging.debug ("button_clicked_gen_rpt")
        
        self.progressBar_genrpt.setValue(0)

        # 0 clear gui 
        self.textBrowser_item_list.clear()
        self.textBrowser_file_path.clear()
        self.progressBar_genrpt.setValue(10)

        # 1 gen .all.csv
        gen_map_item_all()
        self.progressBar_genrpt.setValue(30)
    
        # 2 backup the result
        gen_map_item_all_backup()
        self.progressBar_genrpt.setValue(40)

        # 3 gen rpt
        rpt = gen_rpt_xlsx()
        rpt.chk_input_csv()
        rpt.gen_item_export()
        rpt.chk_gen_rpt_xlsx()
        rpt.gen_mapped_item_readable_xlsx()
        self.progressBar_genrpt.setValue(50)
        rpt.gen_mapped_item_diff_xlsx()
        self.progressBar_genrpt.setValue(60)
        rpt.gen_dayaccount_xlsx()
        self.progressBar_genrpt.setValue(90)
        rpt.gen_totalaccount_xlsx()
        self.progressBar_genrpt.setValue(100)

        # show error log
        self.do_grep_error_log()
        
        # Finish msg
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Warning)
        msg.setText("Gen_report Complete!!")
        msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        ret = msg.exec()

    def do_grep_error_log(self):
        file_log = "./"+TONY_LOG_NAME
        error_str = ""
        line_num = 0
        with open(file_log, 'r', newline='') as logfile:
            for line in logfile:
                chk_pattern = r"^\[ERROR\]"
                if ( re.match(chk_pattern,line,0) ):
                    # print (line)
                    error_str += str(line_num) + ":" + line
                line_num += 1
        
        if (error_str != ""):
            self.textBrowser_item_list.clear()
            self.textBrowser_item_list.append(error_str)


             
if __name__ == "__main__":
    # for item in data_in:
    #     type = map_tab.find_item_type(item)
    #     print ("item: %s, type: %s" % (item,type))

    tony_func_proc_disp(msg=" Start to gen manual to .csv!")
    # test = map_item_manual()
    # test.do_item_manual_qt()
    app = QApplication(sys.argv) 
    myWin = MyWindow() #創建對象 
    myWin.show() #顯示窗口 
    sys.exit(app.exec_()) # `的對象，啟動即可。

    tony_func_proc_disp(msg=" Done gen manual to .csv!")

# if __name__ == "__main__":
    
#     tony_func_proc_disp(msg=" The main entry of the my account 2.0!")

#     # 1 gen .all.csv
#     gen_map_item_all()
    
#     # 2 backup the result
#     gen_map_item_all_backup()

#     # 3 gen rpt
#     rpt = gen_rpt_xlsx()
#     rpt.chk_input_csv()
#     rpt.chk_gen_rpt_xlsx()
#     rpt.gen_mapped_item_readable_xlsx()
#     rpt.gen_mapped_item_diff_xlsx()
#     rpt.gen_dayaccount_xlsx()
#     # rpt.close_gen_rpt_xslx()
    
#     tony_func_proc_disp(msg=" All rpt done!")
