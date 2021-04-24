module counter(clk, reset, count);
    input reset;
    input clk;
    output[7:0]  count;

    reg[7:0]  reg_cnt=7'd0;
    parameter max_cnt = 7'd100;


    always @(posedge clk or negedge reset) begin
        if (reset == 0)
            reg_cnt <= 7'd0;
        else if (reg_cnt == max_cnt)
            reg_cnt <= 7'd0;
        else 
            reg_cnt <= reg_cnt + 7'd1;
    end

    assign count = reg_cnt;

endmodule