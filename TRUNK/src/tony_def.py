import logging
import sys
import time

TONY_DEF_DEBUG = "[DEBUG] "
TONY_DEF_INFO  = "[INFO] "
TONY_DEF_WARN  = "[WARN] "
TONY_DEF_ERROR = "[ERROR] "

TONY_ALLOUT_DIR = "./all_out/"

TONY_LOG_LEVEL = logging.DEBUG # DEBUG, INFO, WARNING, ERROR, CRITICAL
TONY_LOG_MSG_FORMAT = "[%(levelname)-5s]: %(message)-128s <%(asctime)s, %(filename)s, %(funcName)s, %(lineno)d, %(pathname)s>"
TONY_LOG_DATE_FORMAT = '%Y%m%d%H%M%S'
TONY_LOG_NAME = "mylog.log"
logging.basicConfig(level=TONY_LOG_LEVEL, format=TONY_LOG_MSG_FORMAT, datefmt=TONY_LOG_DATE_FORMAT,filename=TONY_LOG_NAME, filemode='w')

TONY_CURRENT_TIME = time.strftime("%Y_%m_%d_%H:%M:%S", time.localtime())

def tony_func_proc_disp(msg):
    """
    teh msg show on the terminal
    """
    module_name = sys._getframe(1).f_globals['__name__']  # Obtain calling frame
    function_name = sys._getframe(1).f_code.co_name
    print (TONY_DEF_INFO + "%-64s <%s, %s>" % (msg,module_name,function_name))

# other def
# for myaccount2p0
ANDROMONEY_RSV_CATEGORY = "SYSTEM"
ANDROMONEY_VALID_KEYWD = "Valid_AndroMoney"
ANDROMONEY_EXPORT_COMMA_REPLACE = '@@'

