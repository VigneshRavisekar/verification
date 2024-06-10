interface cpu_if #(parameter PC_WIDTH = 32,REG_WIDTH=32) (input bit clk);


        // Memory Side Signals
        bit   resetn,memWe,memRd;
        logic [PC_WIDTH-1:0] memAdr;
        logic [REG_WIDTH-1:0] memwrData;
        logic [REG_WIDTH-1:0] memrdData; 

        //Memory Write Driver Clocking Block
        clocking wr_drv_cb@(posedge clk);
                default input #1 output #0;
                output  memWe,resetn;
                output  memAdr,memwrData;
        endclocking:wr_cb

        //Memory Read Driver Clocking Block
        clocking rd_drv_cb@(posedge clk);
                
                default input #1 output #0;
                output memRd,memAdr,resetn;
                input memrdData;
        endclocking:rd_drv_cb

        //Memory Write Monitor Clocking Block
        clocking wr_mon_cb@(posedge clk);

                default input #1 output #0;
                input memWe,memAdr,memwrData;
        endclocking:wr_mon_cb

        //Memory Read Monitor Clocking Block
        clocking rd_mon_cb@(posedge clk);

                default input #1 output #0;
                input memRd,memAdr,memrdData;

        endclocking:rd_mon_cb
        

        modport MEM_WR_DRIV(output  memWe,resetn,memAdr,memwrData);

        modport MEM_RD_DRIV(output memRd,memAdr,resetn,input memrdData);

        modport MEM_WR_MON(input memWe,memAdr,memwrData);

        modport MEM_RD_MON(input memRd,memAdr,memrdData);

endinterface    