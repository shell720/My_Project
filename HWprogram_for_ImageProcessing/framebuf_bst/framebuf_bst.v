module framebuf_bst (clk, reset, pixel_a_in, pixel_b_in, pixel_c_in,
pixel_a_out, pixel_b_out, pixel_c_out, receiv_ack, receiv_req, send_ack, send_req,
state, address);

input clk, reset;
output [2:0] state;
output [13:0] address;

input [7:0] pixel_a_in, pixel_b_in, pixel_c_in;
output receiv_req;
input receiv_ack;

output [7:0] pixel_a_out, pixel_b_out, pixel_c_out;
input send_req;
output send_ack;

reg [2:0] state_reg;
parameter st_free = 3'b0;
parameter st_wait_receivAck = 3'b1;
parameter st_receiving = 3'b10;
parameter st_get_sendReq = 3'b11;
parameter st_sending = 3'b100;

parameter imageSize = 128*128;
reg [23:0] buffer[imageSize:0];
reg [13:0] memAddress;
reg [23:0] pixelOut;

//状態遷移
always @(posedge clk or negedge reset) begin
    if (reset == 0) 
        state_reg <= st_free;
    else begin
        if (state_reg == st_free)
            state_reg <= st_wait_receivAck;
        else if (state_reg == st_wait_receivAck && receiv_ack == 1)
            state_reg <= st_receiving;
        else if (state_reg == st_receiving && memAddress == imageSize-1 && receiv_ack == 0)
            state_reg <= st_get_sendReq;
        else if (state_reg == st_get_sendReq && send_req == 1)
            state_reg <= st_sending;
        else if (state_reg == st_sending && memAddress == imageSize-1 && send_req == 0)
            state_reg <= st_free;
    end
end

//メモリの変化
always @(posedge clk or negedge reset) begin
    if (reset == 0)
        memAddress <= 0;
    else begin
        if (state_reg == st_receiving || state == st_wait_receivAck && receiv_ack == 1)begin
            buffer[memAddress] <= {pixel_a_in, pixel_b_in, pixel_c_in};
            if (memAddress == imageSize)
                memAddress <= 0;
            else if (memAddress != imageSize-1)
                memAddress <= memAddress + 14'd1;
        end
        else if (state_reg == st_sending || send_ack == 1 && state_reg == st_get_sendReq) begin
            pixelOut = buffer[memAddress];
            if (memAddress == imageSize-1)
                memAddress <=0;
            else
                memAddress <= memAddress + 1;
        end
    end
end

assign receiv_req = (reset == 1 && (state_reg == st_free || state_reg == st_wait_receivAck))? 1: 0;
assign send_ack = ((state_reg == st_get_sendReq && send_req == 1) || state_reg == st_sending)? 1: 0;
assign state = state_reg;
assign address = memAddress;

assign pixel_a_out = pixelOut[23:16];
assign pixel_b_out = pixelOut[15:8];
assign pixel_c_out = pixelOut[7:0];

endmodule