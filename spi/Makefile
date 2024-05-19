SIM = verilator
TOPLEVEL_LANG = verilog
PWD=$(shell pwd)
RTL_PATH ?= $(PWD)
RTL_INCLUDE ?= $(PWD)
RTL_TOP ?= spi_top
TOPLEVEL := $(RTL_TOP)
MODULE := test_spi
DUMP_EN ?= 1
CVG_EN ?= 1
TIMING_EN ?= 1
TF_EN ?= 0

ifeq ($(TOPLEVEL_LANG),verilog)
    VERILOG_SOURCES = $(RTL_PATH)/rtl/*.v
    VERILOG_INCLUDE_DIRS =  $(RTL_INCLUDE)/rtl_include
else
    $(error A valid value (verilog or vhdl) was not provided for TOPLEVEL_LANG=$(TOPLEVEL_LANG))
endif

ifeq ($(DUMP_EN),1)
    EXTRA_ARGS += --trace --trace-structs 
endif

ifeq ($(CVG_EN),1)
    EXTRA_ARGS += --coverage
    
endif

ifeq ($(TIMING_EN),1)
    EXTRA_ARGS += --timing
else
    EXTRA_ARGS += --no-timing
endif

export TF_EN

include $(shell cocotb-config --makefiles)/Makefile.sim

.PHONY: coverage clean_coverage 

# Target to generate coverage report
coverage: SIM_ARGS += --coverage
coverage: $(SIM_BUILD)
	verilator_coverage -write-info coverage.info coverage.dat
	genhtml coverage.info --output-directory coverage

# Target to clean coverage files
clean_coverage:
	rm -f coverage.dat coverage.info
	rm -rf coverage