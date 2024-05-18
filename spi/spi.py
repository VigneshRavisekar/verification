import cocotb
import logging as _log
from cocotb.clock import Clock
from cocotb.triggers import RisingEdge,FallingEdge,Timer,ClockCycles
from spi_if import *

class spi:

        def __init__(self,dut,char_len,lsb):
                
                self.dut        = dut
                self.char_len   = char_len
                self.lsb        = lsb
                self.ss_pad     = getattr(self.dut,getattr(spi_if,"%s_ss_pad"%"spi"))
                self.sclk       = getattr(self.dut,getattr(spi_if,"%s_sclk"%"spi"))
                self.mosi       = getattr(self.dut,getattr(spi_if,"%s_mosi"%"spi"))
                self.miso       = getattr(self.dut,getattr(spi_if,"%s_miso"%"spi"))
                self.data_list  = []
                self.data       = 0

        async def master_in_slave_out(self,dut,tx_data):
                
                dut._log.info("******Inside Master-In Slave-Out Function****")
                if self.lsb == 0:
                        data= str(bin(tx_data))[2:]
                        for data_bit in data:

                                await RisingEdge(self.sclk)
                                self.miso.value = int(data_bit)           
                else:
                       data= str(bin(tx_data))[2:][::-1]
                       for data_bit in data:

                                await RisingEdge(self.sclk)
                                self.miso.value = int(data_bit)   
                               
                print("Data Bit {0}".format(data))

        async def master_out_slave_in(self):

                self.dut._log.info("*****Inside Master-Out Slave-In Function*****")  
                if self.lsb == 0:
                    for data_bit in range(self.char_len):

                            await RisingEdge(self.sclk)
                            data_bit = str(self.mosi.value)
                            print("Data Bit {0}".format(data_bit))
                            self.data_list.append(data_bit)
                else:
                       for data_bit in range(self.char_len):

                            await RisingEdge(self.sclk)
                            data_bit = str(self.mosi.value)
                            print("Data Bit {0}".format(data_bit))
                            self.data_list.append(data_bit)  
                            reverse_list = list(reversed(self.data_list))
                       self.data_list = reverse_list

                self.dut._log.info("Data List {0}".format(self.data_list))
                self.data= ''.join(self.data_list)
                print("MOSI Function--> Data {0}".format(self.data))
