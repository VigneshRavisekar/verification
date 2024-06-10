interface wb_if#(parameter REG_WIDTH=32)(input bit clk);

        //Wishbone Side Signals
        logic [4:0]           wb_adr_o;
        logic [REG_WIDTH-1:0] wb_dat_o;
        logic [REG_WIDTH-1:0] wb_dat_i;
        logic [3:0]           sel_o;
        bit   we_o,stb_o,cyc_o,ack_i;


        clocking wb_drv@(posedge clk);

                default input #1 output #0;
                input wb_adr_o,wb_dat_o,wb_dat_i;
                input we_o,stb_o,sel_o,cyc_o;
                output ack_i;

        endclocking:wb_drv


        clocking wb_mon@(posedge clk);

                default input#1 output #0;
                input wb_adr_o,wb_dat_o,wb_dat_i,we_o,stb_o,sel_o,cyc_o,ack_i;
        endclocking:wb_mon

        modport WB_DRIV(clocking wb_drv);

        modport WB_MON(clocking wb_mon);

endinterface


        