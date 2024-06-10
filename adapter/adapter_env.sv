class adapter_env;

    //Declaration all the Virutal instances of the Interfaces
    virtual cpu_if.MEM_WR_DRIV wr_drv_if;
    virtual cpu_if.MEM_RD_DRIV rd_drv_if;
    virtual cpu_if.MEM_WR_MON  wr_mon_if;
    virtual cpu_if.MEM_RD_MON  rd_mon_if;
    
    virtual wb_if.WB_DRIV      wb_drv_if;
    virtual wb_if.WB_MON       wb_mon_if;

    //Declaration of Memory Driver
    // mem_driver mem_driv_h;


    function new(virtual cpu_if.MEM_WR_DRIV wr_drv_if,
        virtual cpu_if.MEM_WR_MON  wr_mon_if,
        virtual cpu_if.MEM_RD_DRIV rd_drv_if,
        virtual cpu_if.MEM_RD_MON  rd_mon_if,
        virtual wb_if.WB_DRIV      wb_drv_if,
        virtual wb_if.WB_MON       wb_mon_if);

                this.wr_drv_if = wr_drv_if;
                this.wr_mon_if = wr_mon_if;
                this.rd_drv_if = rd_drv_if;
                this.rd_mon_if = rd_mon_if;
                this.wb_drv_if = wb_drv_if;
                this.wb_mon_if = wb_mon_if;

    endfunction:new

    //Reseting Logic
    task reset_dut();

            wr_drv_if.wr_drv_cb.resetn.value <= 1;
            repeat(3)
                @(wr_drv_if.wr_drv_cb);

            wr_drv_if.wr_drv_cb.resetn.value    <=0
            wr_drv_if.wr_drv_cb.memAdr.value    <=0;
            wr_drv_if.wr_drv_cb.memwrData.value <=0;
            rd_drv_if.rd_drv_cb.memrdData.value <=0;
            wr_drv_if.wr_drv_cb.memWe.value     <=0;
            rd_drv_if.rd_drv_cb.memRd.value     <=0;

            repeat(2)
                @(wr_drv_if.wr_drv_cb);

    endtask

    // Task which is used to run other tasks(reset,start)
    task run();
            reset_dut();
    endtask

endclass

