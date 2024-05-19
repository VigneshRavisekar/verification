import cocotb
from cocotb.clock import Clock
from cocotb.triggers import RisingEdge,FallingEdge,Timer,ClockCycles
from spi_if import *
from spi import *

#### Configuration of Registers ###

def set_data_transmit_register(data):
      return data

def set_control_status_register(ASS,IE,LSB,TX_N,RX_N,GO_BSY,CHAR_LEN):
      
        L = [ int(i) for i in [ASS,IE,LSB,TX_N,RX_N,GO_BSY,CHAR_LEN]]
        data = L[0]<<13 | L[1]<<12 | L[2]<<11 | L[3]<<10 | L[4]<<9 | L[5]<<8 |L[6]
        return data

def set_clock_divider_register(DIVIDER):
      
      data = DIVIDER
      return data

def set_slave_select_register(SS):

     data = SS
     return data      

def set_register_add(addr):
      
     register_map =  {"RX0":0x00,"RX1":0x04,"RX2":0x08,"RX3":0x0c,"TX0":0x00,"TX1":0x04,"TX2":0x08,"TX3":0x0c,"CSR":0x10,"CR":0x14,"SS":0x18}
     register_add = register_map[addr]
     return register_add

def split_char_len(char_len): ### Splitting Character_Length according to 32 bit chunks
    chunk_len = []
    while char_len > 0:
        if char_len <= 32:
            chunk_len.append(char_len)
            char_len = 0  
        else:
            chunk_len.append(32)
            char_len -= 32
    print("Chunk Len {0}".format(chunk_len))
    return chunk_len
     
def split_tx_data(tx_data,chunk_len):### Split Data according to the chunk_len
    
    
    tx_data = str(bin(tx_data))[2:]
    print("tx_data {0}".format(tx_data))
    chunk = []
    start = 0
    for i in chunk_len:
            data = tx_data[start:start+i]
            start+=i
            data = int(hex(int(data,2)),16)
            chunk.append(data)
    print("Chunk {0}".format(chunk))
    return chunk

def compare_data(data,chunk_len): #### Write Transfer::  Decoding of Received Data
     
     chunk_len = chunk_len[::-1]
     split_data = []
     start = 0
     for i in chunk_len:

            d = data[start:start+i]
            start+=i
            split_data.append(d)

     data = int(''.join(split_data[::-1]),2)
     return data

def decode_data(data): #### Read Transfer:: Decoding of MISO Data

    rx_data = ''.join(data[::-1])
    return int(rx_data,2)
    
class core_master:

    def __init__(self,dut,char_len,lsb,tx_neg,rx_neg,tx_data):


        self.char_len = char_len
        self.lsb      = lsb
        self.tx_neg   = tx_neg
        self.rx_neg   = rx_neg
        self.tx_data  = tx_data
            
        #### Wishbone Signals #####
        self.dut        = dut
        self.CLK        = getattr(self.dut,getattr(spi_if,"%s_CLK"%"spi"))
        self.sclk       = getattr(self.dut,getattr(spi_if,"%s_sclk"%"spi"))
        self.RST        = getattr(self.dut,getattr(spi_if,"%s_RST"%"spi"))
        self.adr        = getattr(self.dut,getattr(spi_if,"%s_adr"%"spi"))
        self.data_in    = getattr(self.dut,getattr(spi_if,"%s_data_in"%"spi"))
        self.data_out   = getattr(self.dut,getattr(spi_if,"%s_data_out"%"spi"))
        self.sel        = getattr(self.dut,getattr(spi_if,"%s_sel"%"spi"))
        self.we         = getattr(self.dut,getattr(spi_if,"%s_we"%"spi"))                
        self.stb        = getattr(self.dut,getattr(spi_if,"%s_stb"%"spi"))
        self.cyc        = getattr(self.dut,getattr(spi_if,"%s_cyc"%"spi"))
        self.ack        = getattr(self.dut,getattr(spi_if,"%s_ack"%"spi"))
        self.err        = getattr(self.dut,getattr(spi_if,"%s_err"%"spi"))
        self.intr       = getattr(self.dut,getattr(spi_if,"%s_intr"%"spi"))
        
        self.spi = spi(self.dut,self.char_len,self.lsb)

      

    async def intialize(self):

            cocotb.start_soon(Clock(self.CLK,1,"ns").start())
            await RisingEdge(self.CLK)
            self.RST.value = 1 
            self.data_in.value = 0
            await ClockCycles(self.CLK,4,rising=True)
            self.RST.value = 0
            
    async def write_reg_config(self):
        
        
        await self.intialize()
        cocotb.start_soon(self.spi.master_out_slave_in())

        #### Configuration of Control and Status Register ####
        ASS    =    0
        IE     =    0 
        GO_BSY =    1

        #### Configuration of Clock Divider Register ####
        DIVIDER =   0

        #### Configuration of Slave Select Register ####
        SS      =  0

        chunk_len  = split_char_len(self.char_len)
        chunk_data = split_tx_data(self.tx_data,chunk_len)


        await RisingEdge(self.CLK)
        self.we.value  = 1
        self.sel.value = 0xF
        self.cyc.value = 1
        self.stb.value = 1
        addr = set_register_add("CR")
        data = set_clock_divider_register(DIVIDER)
        self.adr.value = addr
        self.data_in.value = data
        
        await RisingEdge(self.ack)
        self.stb.value = 0

        await FallingEdge(self.ack)
        self.stb.value = 1

        await RisingEdge(self.CLK)
        addr = set_register_add("SS")
        data = set_slave_select_register(SS)
        self.adr.value = addr
        self.data_in.value = data

        await RisingEdge(self.ack)
        self.stb.value = 0

        await FallingEdge(self.ack)
        self.stb.value = 1
        
        for num in range(len(chunk_len)):

            await RisingEdge(self.CLK)
            addr = set_register_add(f"TX{num}")
            data = set_data_transmit_register(self.tx_data)
            self.adr.value = addr
            self.data_in.value = chunk_data[num]

            await RisingEdge(self.ack)
            self.stb.value = 0

            await FallingEdge(self.ack)
            self.stb.value = 1

        await RisingEdge(self.CLK)
        addr = set_register_add("CSR")
        data = set_control_status_register(ASS,IE,self.lsb,self.tx_neg,self.rx_neg,GO_BSY,self.char_len)
        self.adr.value = addr
        self.data_in.value = data

        await RisingEdge(self.CLK)
        self.we.value = 0 
        self.cyc.value = 0
        self.stb.value = 0
        
        ### Comparision Logic for Data ###
        count = 0
        while True:
            
            await RisingEdge(self.sclk)
            count+=1
            if count == self.char_len:
                  break

        self.data = self.spi.data
        final_data = compare_data(self.data,chunk_len)
        print("Transmitting Data--> Tx_Data {0}".format(self.tx_data))
        print("Compare_Data Comparsion--> FINAL_DATA {0}".format(final_data))
        assert self.tx_data == final_data,"Data sent from Master is not matching the Data received by Slave" 

        # while True:
             
        #      await RisingEdge(self.CLK)
        #      data_out = self.data_out.value
        #      if data_out[-9] == 0:#### Wait for GOBUSY
        #             break
        
    async def read_reg_config(self):
        
        
        await self.intialize()
        cocotb.start_soon(self.spi.master_in_slave_out(self.dut,self.tx_data))

        #### Configuration of Control and Status Register ####
        ASS    =    0
        IE     =    0 
        GO_BSY =    1

        #### Configuration of Clock Divider Register ####
        DIVIDER =   0

        #### Configuration of Slave Select Register ####
        SS      =  0

        await RisingEdge(self.CLK)
        self.we.value  = 1
        self.sel.value = 0xF
        self.cyc.value = 1
        self.stb.value = 1

        await RisingEdge(self.CLK)
        addr = set_register_add("CR")
        data = set_clock_divider_register(DIVIDER)
        self.adr.value = addr
        self.data_in.value = data

        await RisingEdge(self.ack)
        self.stb.value = 0

        await FallingEdge(self.ack)
        self.stb.value = 1


        await RisingEdge(self.CLK)
        addr = set_register_add("SS")
        data = set_slave_select_register(SS)
        self.adr.value = addr
        self.data_in.value = data

        await RisingEdge(self.ack)
        self.stb.value = 0

        await FallingEdge(self.ack)
        self.stb.value = 1

        await RisingEdge(self.CLK)
        addr = set_register_add("CSR")
        data = set_control_status_register(ASS,IE,self.lsb,self.tx_neg,self.rx_neg,GO_BSY,self.char_len)
        self.adr.value = addr
        self.data_in.value = data 

        await RisingEdge(self.CLK)
        self.we.value = 0
        self.stb.value = 0
        await RisingEdge(self.CLK)
        await RisingEdge(self.CLK)
        while True:
             
             await RisingEdge(self.CLK)
             data_out = self.data_out.value
             if data_out[-9] == 0:
                    break

        char_len = split_char_len(self.char_len)
        rx_data = []
        for num in range(len(char_len)):
            
            await RisingEdge(self.CLK)
            self.stb.value = 1
            addr = set_register_add(f"RX{num}")
            self.adr.value = addr   
            
            await RisingEdge(self.ack)
            self.stb.value = 0
            rx_data.append(str(self.data_out.value)) 
        
        self.cyc.value = 0
        self.dut._log.info("Rx Data {0}".format(rx_data))
        rx_data = decode_data(rx_data)
        self.dut._log.info("Decode Data {0}".format(rx_data))
        final_data = rx_data

        self.dut._log.info("Transmitting Data {0}".format(self.tx_data))
        self.dut._log.info("Final Data {0}".format(final_data))

        assert self.tx_data == final_data,"Data sent from slave is not equal to data received by master"

        '''while True:
              
              await FallingEdge(self.sclk)
              count+=1

              if count == self.char_len:
                  break
              
        await RisingEdge(self.CLK)
        addr = set_register_add("RX0")
        self.adr.value = addr
        #### NOTE: AFTER CONFIGURING RX REGISTER WE HAVE TO WAIT FOR 2 CLOCK CYCLES TO READ THE DATA FROM REGISTER ###
        await RisingEdge(self.CLK)
        await RisingEdge(self.CLK)    
        if self.lsb == 0:
            rx_data = self.data_out.value
        else:
             rx_data = int(str(self.data_out.value)[::-1][0:self.char_len],2)

        self.dut._log.info("Rx_Data {0}".format(rx_data))
        assert self.tx_data == rx_data, "Data sent from Slave is not matching Data Received by Master" '''
      
      