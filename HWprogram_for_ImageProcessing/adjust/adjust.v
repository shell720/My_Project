module adjust (pixel_v_in, from_v, to_v, recv_ack, recv_req, 
pixel_v_out, send_ack, send_req, clk ,reset);

    input clk, reset;
    
    input [7:0] pixel_v_in; //明度 0~255まで
    output [7:0] pixel_v_out;
    input  [7:0] from_v, to_v; //平均明度、目標明度

    input recv_ack, send_req;
    output recv_req, send_ack;

    //パイプラインステージ1
    reg [7:0] s1_pixel_in, s1_from, s1_to;
    reg s1_recv_ack;
    always @(posedge clk or negedge reset) begin
        if (reset == 0) begin
            s1_pixel_in <= 0;
            s1_from <= 0;
            reg_to <= 0;
            reg_recv_ack <= 0;
        end
        else begin
            s1_pixel_in <= pixel_v_in;
            s1_from <= from_v;
            reg_to <= from_to;
            reg_recv_ack <= recv_ack;
        end
    end

    //パイプライン処理2
    reg [7:0] s2_pixel_out;
    reg s2_ack;
    

endmodule