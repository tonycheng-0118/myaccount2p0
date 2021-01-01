# myaccount2p0

****
|作者|Tony Cheng|
|---|---
|日期|20201209|
|版本|v1.1|
|GitHub|https://github.com/tonycheng-0118/myaccount2p0|

****
# 1. Purpose:
* Make the financial activity log to be added easily.
* A centralized account db for data extract, analysis, and disply.
* A backend system for better maintainence and extension.

# 2. Directory structure:

* [dat/](#dat)
* [distrubute/](#distrubute)
* [document/](#document)
* [exe/](#exe)
* [release/](#release)
* [src/](#src)
* [workdir/](#workdir)
* [README](#README)
* [makefile](#makefile)

# 3. Operation step:
* [initial operation](#initial_operation)
* [followup operation](#followup_operation)

# 4. Reports:
* [mapped_item_readable](#mapped_item_readable)
* [mapped_item_diff](#mapped_item_diff)
* [dayaccount](#dayaccount)
* [mon/year/total_expense](#mon_year_total_expense)

# 5. Features:
* [v1.0](#feature_v1p0)
* [v1.1](#feature_v1p1)
* [TODO](#feature_todo)

# 6. Source codes structure:
* [source_code_structure](#source_code_structure)


****
dat/
---
###
    * 用來存放使用者的記帳source file
        all_item_backup/
            andromoney/
                - 自動產生文件
                - 可以當作AndroMoney import的文件
                - 內容已排除../../andromoney/*.csv內非原生andromoney的部分 
        all_item_backup/
            - 自動產生文件
            - 以當下使用日期為單位，把全部parsing過的檔案用.csv的方式備份起來。
            - 在gen_rpt中的mapped_item_diff會使用到。
        excel/
            - 使用者輸入
            - 使用type\date展開格式的excel文件
            - 有*_inc.xlsx的檔案,內容的date部分可以接受跳號或是空白，方便使用者專注於需要紀錄的日期。
        invoice/
            - 使用者輸入
            - 使用手機APP"發票存摺"匯出的.csv
        littlebox/
            - 使用者輸入
            - 使用手機APP"小票盒"匯出的.csv
        manual/
            - 使用者輸入
            - 使用此GUI輸出的.csv
        andromoney/
            - 使用者輸入
            - 使用手機APP"AndroMoney"匯出的.csv
    * 不需要放入GitHub追蹤，因為屬於使用者個人資料 

distrubute/
---
###
    * 置放pyinstaller產生的執行檔  
    * 不需要放入GitHub追蹤，因為可以透過script產生

document/
---
###
    * 置放一些開發文件

exe/
---
###
    * 置放給使用者安裝與啟動程式的地方
        - install.bat: 在Win10環境下，根據目前的./src版本產生對應的執行檔
        - *.exe: 當install.bat完成後，後自動產生一個連結指到./distrubute/*.exe。
    * 不需要放入GitHub追蹤，因為可以透過script產生

release/
---
###
    * 置放此source code對應的conda env、python版本、install pkg list與Github對應的版號。 

src/
---
###
    * 置放此source code

workdir/
---
###
    * 置放此開發環境的所有東西，可以在這裡開VSCode執行開發。
    * 不需要放入GitHub追蹤，因為開發過程的東西不需要被追蹤,除非是新的開發工具。

makefile
---
###
    * 置放協助管理的make指令。
```bash
make help # for more information!
```
___
initial_operation
---
###
    1. After install the myaccount, please try run the myaccount.exe first and click the Gen_report for env test.
    2. Collect all the export data.csv from "發票存摺", "小票盒", and "AndroMoney" into ./data/invoice, ./dat/littlebox, ./dat/andromoney/ respectively.
    3. If you have a type\date format like data，try to map those data to ./excel/*xlxs。Please copy the "My_account_example.xlsx" to "your_account_inc.xlsx", and start to enter the data. As the date can be be discontinuous ot empty，but type have to be completely unchagned。 
    4. Double click myaccount.exe。
    5. Click the help at menu bar and refer to steps.
    6. Click the BIG BLUE button "Gen report"，and wait for the process bar to 100%。
    7. in ./report/gen_report.xslx，you have all of the report。
    8. 把./dat/all_item_export/andromoney/AndroMoney_export.csv匯入AndroMoney的原生csv，並在完成後再匯入手機。

followup_operation
---
###
    1. Assume you have done the initial operation and successfully generate the report。
    2. Put the latest data.csv from "發票存摺", "小票盒", and "AndroMoney" into ./data/invoice, ./dat/littlebox, ./dat/andromoney/ respectively.
    3. Or enter it manually through ./excel/***_inc.xlsx。 
    4. Or enter it manually after activating GUI。
    5. Double click myaccount.exe and start to "Gen report"。
    6. 把./dat/all_item_export/andromoney/AndroMoney_export.csv匯入AndroMoney的原生csv，並在完成後再匯入手機。

___
mapped_item_readable
---
###
    1. It shows all of your items into the long list。
    2. If the items is red-filled, it means the item is highly propably duplicate to other item, usually the duplicated item is right above the red-filled one, please check the the source file.

mapped_item_diff
---
###
    1. It shows teh increase item from the recent last time input.
    2. It help the user to confirm the increase items.

dayaccount
---
###
    1. It shows the type\date format account.
    2. Each number is link the item in the mapped_item_readable.

mon_year_total_expense
---
###
    1. It shows the expense summation of month-based / year-based, and finally the total expense.


___
feature_v1p0
---
```diff
+  how to detect to duplicated item bwt different source
+  hthe record of ETC auto refill: if the the ETC registered by company, no einvoice is available
+ upload into github
+  hin new add item list
+  hdat is classified by source
+  hauto find the previous all_item for diff
+  hadd monthaccount, yearaccount, summary
+  Add gui for item input manually
+  Add session restore option, to save all_df and gen_rpt.xlsx for analysis only operation
+ Integrate all of action into gui
```
___
feature_v1p1
---
```diff
+ gen_gpt don msg box.
+ custimized item_type.
+ custimized item_category.
+ custimized item_type2category.
+ modified daily report, only record the day with item.
- no link in daily report
+ exe/instal.bat ANACONDA_PATH from user config
+ exe/instal.bat can auto pull GitHub
! Dynamic sizing GUI
+ dat/all_item_export for andromoney export format 
+ dat/andromoney for andromoney import, will be extract the diff first 
+ fix typo type: Electicity, Transpotation, Entertainmant,  
+ rewrite csv import part by using pd.read_csv 
+ add cond to when andromoney's output note have problem, assumed that the note in andromoney item MUST have something!
+ fix potential func call by share issue 
+ Show error log in GUI textBrowser
```

feature_todo
---
```diff
! add refund classify
! graphical data present
! cal budget
! windows version for othere user, package all into *.exe in windows and linux, only check in script to gen the *.exe
! auto upload to google drive
! Google Apps Script???
! Line chat robot???
```

___
source_code_structure
---
###
***
    //---------------
    // Structure
    //---------------
    gen_rpt_xlsx.py
        to generate the readable sheet and dayaccount sheet
        A. readable have two purpose
            1. easy to analysis the item by using the filter in excel
               and the also the verbose infomation link to dayaccount
            2. incremental mode will use this sheet to transfer to .all.item and merge with old .all.item.
        B. dayaccount have two peupose
            1. easy to analysis the item by using excel tool
            2. verify mode will use this sheet to regenerate the dayaccount again, wich should have the same amount of total number as the original one.
               By doing this, the stability of the env is guaranteed. 

    map_item.py
    map_excel.py
    map_invoice.py
    map_littlebox.py
    map_item_all.py
        the gen .all.item based on different source

    map_tab.py
        the mapping tab bwt ori and mapped 
