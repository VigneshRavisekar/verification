import cocotb
from cocotb.clock import Clock
from cocotb.triggers import RisingEdge,FallingEdge,Timer,ClockCycles
from core_master import *

@cocotb.test()
async def spi_basic_read(dut):

        char_len = 8
        lsb      = 0
        tx_neg   = 0
        rx_neg   = 1
        tx_data  = 0x8f
        core = core_master(dut,char_len,lsb,tx_neg,rx_neg,tx_data)
        await core.read_reg_config()   
        # await ClockCycles(dut.wb_clk_i,500,rising=True)

@cocotb.test()
async def spi_basic_write(dut):

        char_len =  40
        lsb      =  0
        tx_neg   =  0
        rx_neg   =  1
        tx_data  =  0x8f1230f514

        core = core_master(dut,char_len,lsb,tx_neg,rx_neg,tx_data)
        await core.write_reg_config()
    


