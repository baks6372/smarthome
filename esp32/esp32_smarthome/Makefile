# 
# This is a project Makefile. It is assumed the directory this Makefile resides in is a
# project subdirectory.
#

PROJECT_NAME := esp32_smarthome
BOARD_NAME := esp32_Core_board_V2
FW_VER := 1
FW_REV := 0
FW_BUILD := 1
HW_VER := 0
HW_REV := 2
CFLAGS += -D LOG_LOCAL_LEVEL=ESP_LOG_DEBUG -D FW_VER=$(FW_VER) -D FW_REV=$(FW_REV) -D FW_BUILD=$(FW_BUILD) -D HW_VER=$(HW_VER) -D HW_REV=$(HW_REV)
include project.mk
