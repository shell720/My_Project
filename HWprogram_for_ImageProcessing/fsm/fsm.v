module fsm( clk, reset, start, stop, mode, state);

    input clk;
    input reset;
    input start;
    input stop;
    input mode;
    output[1:0] state;

    reg [1:0] st_reg = 0;

    parameter INIT = 2'd0;
    parameter RUN  = 2'd1;
    parameter WAIT = 2'd2;

    always @(posedge clk or negedge reset) begin 
        if (reset == 0)
            st_reg <= INIT;

        if (clk == 1) begin 
            if (st_reg == INIT) begin
                if (start ==1) begin
                    st_reg <= RUN;
                end
            end

            if (st_reg == RUN) begin
                if (mode == 1) 
                    st_reg <= INIT;
                else if (mode == 0)
                    st_reg <= WAIT;
            end

            if (st_reg == WAIT) begin
                if (stop == 0)
                    st_reg <= INIT;
            end
        end
    end

    assign state = st_reg;

endmodule