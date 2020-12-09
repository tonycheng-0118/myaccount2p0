# +FHDR--------------------------------------------------------------------------
# FILE NAME        : makefile
# TYPE             : make 
# AUTHOR'S EMAIL   :
# -------------------------------------------------------------------------------
# Release history
# VERSION Date         AUTHOR      DESCRIPTION
# -------------------------------------------------------------------------------
# KEYWORDS         : 
# -------------------------------------------------------------------------------
# PURPOSE          : 
# -------------------------------------------------------------------------------
# REUSE ISSUES     : 
# -------------------------------------------------------------------------------
# NOTE :
# $@: 目前的目標項目名稱。
# $<: 代表目前的相依性項目。
# $*: 代表目前的相依性項目，但不含副檔名。
# $?: 代表需要重建（被修改）的相依性項目。
# ?=: 代表該變數沒有被指定時候的預設值 
# -FHDR--------------------------------------------------------------------------

SHELL=/bin/bash


#--------------------------------------------------------------------------------
# User Var 
#--------------------------------------------------------------------------------

TOP_MODULE_NAME ?= myaccount
CONDA_ENV ?= env_myaccount2p0_v1.0
PYTHON_VER ?= 3.6.9
RELEASE_VER ?= v1.0



#--------------------------------------------------------------------------------
# Makefile Var 
#--------------------------------------------------------------------------------
# Need to specify bash in order for conda activate to work.
CONDA_ACTIVATE_BASH=/home/tonychenglx/anaconda3/etc/profile.d/conda.sh



#--------------------------------------------------------------------------------
# Command 
#--------------------------------------------------------------------------------
.PHONY: clean

hello:
	# -------------------------------------------------------------------------------
	# --Purpose
	# Test makefikle only
	# --Arguments
	# GREETING: for greeting. i.e. HAHA
	# -------------------------------------------------------------------------------
	@echo $@
	@echo $(CONDA_ACTIVATE_BASH)
	@echo "HELLO $(GREETING)!!"

init_env:
	# -------------------------------------------------------------------------------
	# --Purpose
	# to how the initial env flow only
	# --Arguments
	# *CONDA_ENV: the conda env list; i.e. ENV=env_myaccount2p0_v1.0
	# -------------------------------------------------------------------------------
	@echo conda activate $(CONDA_ENV)

gen_dist:
	# -------------------------------------------------------------------------------
	# --Purpose
	# to generate the execute file based on the current ../src/* version
	# --Arguments
	# *CONDA_ENV: the conda env list; i.e. ENV=env_myaccount2p0_v1.0
	# -------------------------------------------------------------------------------
	@echo $@
	cd ./distrubute; \
		rm -rf *; \
		source $(CONDA_ACTIVATE_BASH); \
		conda activate $(CONDA_ENV); \
		pyinstaller -F -p ../src/ --distpath . ../src/$(TOP_MODULE_NAME).py


install_new_pkg:
	# -------------------------------------------------------------------------------
	# --Purpose
	# to install new package to the certain env
	# --Arguments
	# PKG: the package to install. i.e. PKG=pyinstaller
	# *RELEASE_VER: the release path for this installment. i.e. RELEASE_VER=v1.0
	# -------------------------------------------------------------------------------
	@echo $@
ifneq ($(wildcard ./release/$(RELEASE_VER)/requirements.txt),)
	@echo "[INFO] Found $(RELEASE_VER)"
	@pip install $(PKG)
	@pip freeze > ./release/$(RELEASE_VER)/requirements.txt
else
	@echo "[ERROR] Found no $(RELEASE_VER)"
endif


clean:
	@echo "Clean!!"
