# Purpose: to transfer the data to normalized data structure
# Normalized structure: (which exit in val of dict)
# {name, data(yyyy_mm_dd), category, type, expense, incomnse, borrow, lend, location, tab#, note}

from tony_def import *
from map_item import *
import re

class map_item_manual(map_item):

    def __init__(self):
        super().__init__()

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

        # because manual item utilizes the format of df, which is little after write out to csv
        item[self.classify_ori.index('tag')] = eval(item[self.classify_ori.index('tag')]) #[ i for i in item[self.classify_ori.index('tag')] ] # to pure list
        item[self.classify_ori.index('note')] =  eval(item[self.classify_ori.index('note')]) #{"Note":item[self.classify_ori.index('note')]['Note']} # to pure dict 

        pass
    
    def do_item_map_pstproc(self,item):
        """
        a call back to for all post processing before __do_item_map
        """
        pass
    
    # def do_item_manual(self):

    #     gen_rpt = gen_rpt_xlsx() # to reuse the chk*foramt
    #     df = pd.DataFrame()

    #     # inner def
    #     def open_import_file ():
    #         # import_file_path = filedialog.asksaveasfilename(defaultextension='.csv')
    #         import_file_path = filedialog.askopenfilename(initialdir = "../dat/manual/",title = "Select file",filetypes = (("item files","*.csv"),("all files","*.*")))
    #         df = gen_rpt.csv2df(csv_in=import_file_path)
    #         df_str = df.to_string() # so that df will display all of content
    #         text.configure(state='normal')
    #         text.delete("1.0","end") # clear all of content
    #         text.insert('insert', df_str)
    #         text.configure(state='disabled') # make teh text is RO
    #         pass

    #     def do_job():
    #         print ("HAHA")
    #         pass

    #     # initial windows
    #     window = tk.Tk()
    #     window.title('Myaccount2.0 manual mode')
    #     window.geometry('800x600')  # 這裡的乘是小x
    #     # canvas = tk.Canvas(window, width=400, height=135, bg='green')

    #     # Frame
    #     # height_frame = tk.Frame(window)
    #     # height_frame.pack(side=tk.TOP)

    #     # menubar
    #     menubar = tk.Menu(window)
    #     filemenu = tk.Menu(menubar,tearoff=0)
    #     menubar.add_cascade(label='File', menu=filemenu)
    #     filemenu.add_command(label='New', command=do_job)
    #     filemenu.add_command(label='Open', command=open_import_file)
    #     filemenu.add_command(label='Save', command=do_job)
    #     filemenu.add_separator()    # 新增一條分隔線
    #     filemenu.add_command(label='Exit', command=window.quit) # 用tkinter裡面自帶的quit()函式



    #     # for usage infomation
    #     label_info = tk.Label(window, text='User name:', font=('Arial', 14))
    #     label_info.grid(row=0, column=2, columnspan=2, rowspan=2, sticky="wens", padx=5, pady=5)


    #     # Btn for operation
    #     # btn_open_file = tk.Button(text='Open', command=import_item, bg='green', fg='white', font=('helvetica', 12, 'bold'))
    #     # btn_open_file.place(x=200, y=240)

    #     # text for dispaly load item
    #     # e = tk.Entry(window, show = None)#顯示成明文形式
    #     # e.pack()
    #     text_scrollbar_x = tk.Scrollbar(orient=tk.HORIZONTAL)
    #     text_scrollbar_x.grid(row=2,column=1, sticky='we') # ws = west to east
    #     # text_scrollbar_x.pack(side="bottom", fill="x")
    #     text_scrollbar_y = tk.Scrollbar(orient=tk.VERTICAL)
    #     text_scrollbar_y.grid(row=1,column=2, sticky='ns') # ns = north to south
    #     # text_scrollbar_y.pack(side="right", fill="y")
    #     text = tk.Text(state='disabled', wrap='none', font=("Arial",12), xscrollcommand=text_scrollbar_x.set,yscrollcommand=text_scrollbar_y.set)
    #     # text.pack(fill=tk.BOTH,expand=True) # expand置1 使能fill属性, fill=BOTH 当GUI窗体大小发生变化时，widget在X、Y两方向跟随GUI窗体变化
    #     text.grid(row=1,column=1)

    #     #
    #     window.config(menu=menubar)        
    #     text_scrollbar_x.config(command=text.xview) # tso that the nowrap contex can be view
    #     text_scrollbar_y.config(command=text.yview)

    #     # forever exec until quit
    #     window.mainloop()

    #     pass

    # # def do_item_manual_qt(self):
    # #     app = QApplication(sys.argv) 
    # #     myWin = MyWindow() #創建對象 
    # #     myWin.show() #顯示窗口 
    # #     sys.exit(app.exec_()) # `的對象，啟動即可。
    # #     pass 
        
             
if __name__ == "__main__":
    # for item in data_in:
    #     type = map_tab.find_item_type(item)
    #     print ("item: %s, type: %s" % (item,type))

    tony_func_proc_disp(msg=" Start to gen manual to .csv!")

    manual = map_item_manual()
    file_in_path = "../dat/manual/Untitled.csv" 
    manual.do_all_map(file_in=file_in_path,fileout_override=True)

    tony_func_proc_disp(msg=" Done gen manual to .csv!")