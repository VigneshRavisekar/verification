import os,cocotb,random
from cocotb.clock import Clock
from cocotb.regression import TestFactory
from cocotb.triggers import RisingEdge,FallingEdge,Timer,ClockCycles
from core_master import *

test_factory_variable = os.getenv('TF_EN','0') == '1'

async def spi_write_tf(dut, char_len, lsb, tx_neg, rx_neg, tx_data):
    ''' Test Function for SPI Write Operation '''
    if test_factory_variable and tx_data is None:
        
        tx_data = random.getrandbits(char_len)
    
    core = core_master(dut, char_len, lsb, tx_neg, rx_neg, tx_data)
    await core.write_reg_config()

if test_factory_variable:
    
    ''' Test Factory Generation '''
    tf = TestFactory(spi_write_tf)
    tf.add_option("char_len", [random.randint(8, 128) for _ in range(10)])
    tf.add_option("lsb", [random.randint(0, 1) for _ in range(10)])
    tf.add_option("tx_neg", [0])
    tf.add_option("rx_neg", [1])
    tf.add_option("tx_data", [None])
    tf.generate_tests()

else:
    
    ''' Individual Tests for SPI '''
    @cocotb.test()
    async def base_write(dut):
         
         char_len = 8
         lsb      = 0
         tx_neg   = 0
         rx_neg   = 1
         tx_data  = 0x8f
         await spi_write_tf(dut, char_len, lsb, tx_neg, rx_neg, tx_data)
 
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
