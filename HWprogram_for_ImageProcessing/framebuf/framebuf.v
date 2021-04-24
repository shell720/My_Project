module framebuf (clk ,reset, pixel_a_in, pixel_b_in, pixel_c_in, 
pixel_a_out, pixel_b_out, pixel_c_out, recev_req, recev_ack, send_req, send_ack
, address, state_out);

input clk, reset;
input [7:0] pixel_a_in, pixel_b_in, pixel_c_in;
input recev_ack, send_req; //マスター・スレーブ関係による

output [7:0] pixel_a_out, pixel_b_out, pixel_c_out;
output recev_req, send_ack;
output [13:0] address;
output[2:0] state_out;

//マシンの状態
reg[2:0] state;
parameter st_free = 3'b0;  //どちらにもreqなし
parameter st_wait_recAck = 3'b1; //前からackがくるのを待つ
parameter st_receiving = 3'b10; //データを受け取る、自分のreqを下げて前も下げるのを待つ
parameter st_wait_sendReq = 3'b11; //後ろからのreqを待っている、reqがきたら送信
parameter st_need_sendAck = 3'b100; //後ろのデータを受け取った報告待ち

parameter imageSize = 128*128;
reg [23:0] buffer[ imageSize-1: 0]; // 8bit*3が128*128
reg [13:0] memAddress; //メモリ配列128*128のどこを今考えているか
reg [23:0] output_buf;

//状態変化を書く
//alwaysで使う変数にはreg変数の割り当て
always @(posedge clk or negedge reset) begin 
    if (reset == 0)
        state <= st_free;
    else begin // clk == 1
        if (state == st_free && recev_req == 1)
            state <= st_wait_recAck;
        else if (state == st_wait_recAck && recev_ack == 1)
            state <= st_receiving;
        else if (state == st_receiving) begin
            if (recev_ack == 0 && memAddress == imageSize-1)
                state <= st_wait_sendReq;
            else if (recev_ack == 0 && memAddress != imageSize-1)
                state <= st_free;
        end
        else if (state == st_wait_sendReq && send_req == 1)
            state <= st_need_sendAck;
        else if (state == st_need_sendAck) begin
            if (send_req == 0 && memAddress == imageSize-1)
                state <= st_free;
            else if (send_req == 0 && memAddress != imageSize-1)
                state <= st_wait_sendReq;
        end
    end
end

//バッファメモリの変化
always @(posedge clk or negedge reset) begin 
    if (reset == 0)
        memAddress <= 0;
    else begin
        if (state == st_receiving && recev_ack == 0)begin
            if (memAddress == imageSize-1)
                memAddress <= 0;
            else 
                memAddress <= memAddress + 14'd1;
        end else if (state == st_wait_recAck && recev_ack == 1)
            buffer[memAddress] <= {pixel_a_in, pixel_b_in, pixel_c_in};
        else if (state == st_need_sendAck && send_req == 0)begin
            output_buf <= buffer[memAddress];
            if (memAddress == imageSize-1)
                memAddress <= 0;
            else 
                memAddress <= memAddress + 14'd1;
        end
    end
end

assign recev_req = (reset == 1'b1 && (state == st_free || state == st_wait_recAck))? 1'b1: 1'b0;
assign send_ack = (state == st_need_sendAck)? 1:0;
assign address = memAddress;
assign state_out = state;

assign pixel_a_out = output_buf[23:16];
assign pixel_b_out = output_buf[15:8]; 
assign pixel_c_out = output_buf[7:0];


endmodule