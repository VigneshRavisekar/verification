class spi_if(object):
    

    # Wishbone Signals
        

         
          spi_CLK     = "wb_clk_i"
          spi_RST     = "wb_rst_i"
          spi_adr     = "wb_adr_i"
          spi_data_in = "wb_dat_i"
          spi_data_out= "wb_dat_o"
          spi_sel     = "wb_sel_i"
          spi_we      = "wb_we_i"
          spi_stb     = "wb_stb_i"
          spi_cyc     = "wb_cyc_i"
          spi_ack     = "wb_ack_o"
          spi_err     = "wb_err_o"
          spi_intr    = "wb_int_o"
                  
    #SPI Signals
          spi_ss_pad  =  "ss_pad_o"
          spi_sclk    =  "sclk_pad_o"
          spi_mosi    =  "mosi_pad_o"
          spi_miso    =  "miso_pad_i"
          

                  