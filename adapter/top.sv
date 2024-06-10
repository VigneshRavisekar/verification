`include "test.sv"
`include "cpu_if.sv"
`include "wb_if.sv"


module top();

        paramter cycle = 10;
        reg clock;
  		initial begin
          	clock = 1'b0;
  		    forever #(cycle/2) clock = ~clock;
        end
        //Instantiate the Interface
        cpu_if CPU_IF(clock);
        wb_if  WB_IF(clock);
        //Handle for Test
        adapter_test test_h;
        //Instantiate the DUT
        cpu_to_wb ADAPTER(.clk(clock),
                          .resetn(CPU_IF.resetn),
                          .memAdr(CPU_IF.memAdr),
                          .memwrData(CPU_IF.memwrData),
                          .memrdData(CPU_IF.memrdData),
                          .memWe(CPU_IF.memWe),
                          .memRd(CPU_IF.memRd),
                          .wb_adr_o(WB_IF.wb_adr_o),
                          .wb_dat_o(WB_IF.wb_dat_o),
                          .wb_dat_i(WB_IF.wb_dat_i),
                          .we_o(WB_IF.we_o),
                          .stb_o(WB_IF.stb_o),
                          .sel_o(WB_IF.sel_o),
                          .cyc_o(WB_IF.cyc_o),
                          .ack_i(WB_IF.ack_i));

        initial 
            begin
                    //Create the object for test and pass the interface instance as arguments
                    test_h = new(CPU_IF,CPU_IF,CPU_IF,CPU_IF,WB_IF,WB_IF);
					test_h.build_and_run();
            end
        // Waveform Generation
  
        initial 
            begin
              		$dumpvars;
    				$dumpfile("dump.vcd");
            end 
  
 
endmodule:top