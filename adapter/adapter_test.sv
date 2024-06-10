import adapter_pkg::*;
class adapter_test;

        //Virtual Interfaces for CPU and WB
        virtual cpu_if.MEM_WR_DRIV wr_drv_if;
        virtual cpu_if.MEM_RD_DRIV rd_drv_if;
        virtual cpu_if.MEM_WR_MON  wr_mon_if;
        virtual cpu_if.MEM_RD_MON  rd_mon_if;
        
        virtual wb_if.WB_DRIV      wb_drv_if;
        virtual wb_if.WB_MON       wb_mon_if;

        //Declaration of handle for Environment
        adapter_env env_h;

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
                env_h = new(wr_drv_if,wr_mon_if,rd_drv_if,rd_mon_if,wb_drv_if,wb_mon_if);

        endfunction:new
  
  task build_and_run();
        
        env_h.run();
    	#1000;
    	$finish;
  endtask

endclass






