`timescale 1ps / 1ps
module test_counter();
    parameter CLK = 10; 
    // for input
    reg clk;
    reg reset;
    // for output
    wire[7:0] count;
    // module
    counter counter0( .clk (clk), .reset (reset), .count (count));

    // clockの動き方
    always begin
        clk = 1'b1;
        #(CLK/2);
        clk = 1'b0;
        #(CLK/2);
    end
    
    initial begin
        //$dumpvars;
        reset = 1;
        //count = 0;
        #(20*CLK); reset = 0;
        #(CLK/2); reset = 1;
        #(120*CLK); reset = 0;
        #(5*CLK); reset = 1;

    $finish;
    end

endmodule