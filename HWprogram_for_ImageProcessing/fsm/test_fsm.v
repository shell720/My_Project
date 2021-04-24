`timescale 1ps / 1ps
module test_fsm();
    parameter CLK = 10;//1000000/10; // 10MHz
    // for input
    reg clk;
    reg reset;
    reg start;
    reg stop;
    reg mode;
    // for output
    wire [1:0] state;
    // module
    fsm fsm0( .clk (clk), .reset (reset), .start (start), .stop (stop), .mode (mode), .state (state) );
    
    always begin
        //clkの動き方を示している、1サイクルが一周期
        clk = 1'b1;
        #(CLK/2);
        clk = 1'b0;
        #(CLK/2);
    end

    initial begin
        //$dumpvars;
        reset = 1;
        start = 0;
        stop = 0;
        #(CLK/2); reset = 0;
        #(CLK); reset = 1;
        // mode 0 test
        mode = 0;
        #(CLK); start = 1;
        #(CLK); start = 0;
        #(CLK*3); stop = 1;
        #(CLK); stop = 0;
        #(CLK*3);
        // mode 1 test
        mode = 1;
        #(CLK); start = 1;
        #(CLK); start = 0;
        #(CLK*3);
        $finish;
        end
endmodule