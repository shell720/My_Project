module adjust_v(
   // Outputs
   rcv_req, pixel_v_out, snd_ack,
   // Inputs
   clk, xrst, pixel_v_in, rcv_ack, snd_req, from_v, to_v
, h, l);

   output[7:0] h,l;
   // clock, reset
   input clk;
   input xrst;

   // receive port (MASTER)
   input [7:0]  pixel_v_in;
   output 	rcv_req;
   input 	rcv_ack;

   // send port (SLAVE)
   output [7:0] pixel_v_out;
   input 	snd_req;
   output 	snd_ack;
   
    // parameter values
   input [7:0] 	from_v;
   input [7:0] 	to_v;

   //////////////////////////////////////////////////////////
   // stage 0 (registered primary input)
   //////////////////////////////////////////////////////////
   reg [7:0] 	s0_v_reg;
   reg [7:0] 	s0_from_v_reg;
   reg [7:0] 	s0_to_v_reg;
   reg 		s0_ack_reg;

   always @(posedge clk or negedge xrst) begin
      if (xrst == 1'b0)
	s0_v_reg <= 8'd0;
      else
	s0_v_reg <= pixel_v_in;
   end

   always @(posedge clk or negedge xrst) begin
      if (xrst == 1'b0)
	s0_from_v_reg <= 8'd0;
      else
	s0_from_v_reg <= from_v;
   end

   always @(posedge clk or negedge xrst) begin
      if (xrst == 1'b0)
	s0_to_v_reg <= 8'd0;
      else
	s0_to_v_reg <= to_v;
   end

   always @(posedge clk or negedge xrst) begin
      if (xrst == 1'b0)
	s0_ack_reg <= 1'b0;
      else
	s0_ack_reg <= rcv_ack;
   end
   
   //////////////////////////////////////////////////////////
   // stage 1 パイプライン化
   //////////////////////////////////////////////////////////
   reg 		s1_ack_reg;
   reg s2_ack_reg, s3_ack_reg, s4_ack_reg; //s5_ack_reg, s6_ack_reg, s7_ack_reg;
   reg [15:0] s1_divid_l;
   reg [7:0] s1_minus_from, s1_minus_to;
   reg[7:0] s1_from_v_reg, s2_from_v_reg, s3_from_v_reg, s4_from_v_reg;
   reg[7:0] s1_v_reg, s2_v_reg, s3_v_reg, s4_v_reg;

   /*assign s1_dividend_l = (8'd255 - s0_to_v_reg) * s0_v_reg + (s0_to_v_reg - s0_from_v_reg) * 8'd255;
   assign s1_dividend_s = s0_v_reg * s0_to_v_reg;
   assign s1_divisor_l  = 8'd255 - s0_from_v_reg;
   assign s1_divisor_s  = s0_from_v_reg;

   div_u #(16,8,8) div0(.i1(s1_dividend_l), .i2(s1_divisor_l), .o1(s1_quotient_l));
   div_u #(16,8,8) div1(.i1(s1_dividend_s), .i2(s1_divisor_s), .o1(s1_quotient_s));

   assign s5_quotient_h_sel = (s0_from_v_reg != 8'd0) ? s1_quotient_s : 8'd0;
   assign s1_quotient_l_sel = (s0_from_v_reg != 8'd255) ? s1_quotient_l : 8'd0;
   assign s1_quotient_sel = (s0_v_reg > s0_from_v_reg) ? s1_quotient_l_sel : s5_quotient_h_sel;
   assign s1_v = (s1_quotient_sel > 8'd255) ? 8'd255 : s1_quotient_sel;*/

   always @(posedge clk or negedge xrst) begin
      if (xrst == 0) begin
            s1_divid_l <= 8'd0;
            s1_minus_from <= 0;
            s1_minus_to <= 0;
      end
      else begin
            s1_divid_l <= s0_v_reg * s0_to_v_reg;
            s1_minus_from <= s0_to_v_reg -s0_from_v_reg;
            s1_minus_to <= 8'd255 - s0_from_v_reg;
      end
   end

   always @(posedge clk or negedge xrst) begin
      if (xrst == 0) begin
      s1_ack_reg <= 0;
      s1_from_v_reg <= 8'd0;
      s1_v_reg <= 8'd0;
      end
      else begin
         s1_ack_reg <= s0_ack_reg;
         s1_from_v_reg <= s0_from_v_reg;
         s1_v_reg <= s0_v_reg;
      end
   end


   reg [15:0] s2_mul1, s2_mul2, s2_divid_l;
   always @(posedge clk or negedge xrst) begin
      if (xrst == 0) begin
            s2_mul1 <=0;
            s2_mul2 <=0;
            s2_divid_l <= 0;
      end
      else begin
            s2_mul1 <= s0_v_reg * s1_minus_to;
            s2_mul2 <= s1_minus_from * 255;
            s2_divid_l <= s1_divid_l;
      end
   end

   always @(posedge clk or negedge xrst) begin
      if (xrst == 0) begin
      s2_ack_reg <=0;
      s2_from_v_reg <=0;
      s2_v_reg <= 0;
      end
      else begin
         s2_ack_reg <= s1_ack_reg;
         s2_from_v_reg <= s1_from_v_reg;
         s2_v_reg <= s1_v_reg;
      end
   end
   assign h = s3_divorsor_h, l = s3_from_v_reg;


   reg [15:0] s3_divid_h, s3_divid_l;
   reg [7:0]  s3_divorsor_h;
   always @(posedge clk or negedge xrst) begin
      if (xrst == 0) begin
         s3_divid_h <=0;
         s3_divorsor_h <= 0;
         s3_divid_l <=0;
      end
      else begin
         s3_divid_h <=s2_mul1 + s2_mul2;
         s3_divorsor_h <= 8'd255 - s2_from_v_reg;
         s3_divid_l <= s2_divid_l;
      end
   end
   always @(posedge clk or negedge xrst) begin
      if (xrst == 0) begin
      s3_ack_reg <=0;
      s3_from_v_reg <=0;
      s3_v_reg <= 0;
      end
      else begin
         s3_ack_reg <= s2_ack_reg;
         s3_from_v_reg <= s2_from_v_reg;
         s3_v_reg <= s2_v_reg;
      end
   end

   wire [7:0] div_result_h, div_result_l;
   div_u #(16,8,8) div0(.i1(s3_divid_h), .i2(s3_divisor_h), .o1(div_result_h));
   div_u #(16,8,8) div1(.i1(s3_divid_l), .i2(s3_from_v_reg), .o1(div_result_l));
   reg [7:0] s4_result_h, s4_result_l;
   always @(posedge clk or negedge xrst) begin
      if (xrst == 0) begin
         s4_result_h <= 0;
         s4_result_l <= 0;
      end
      else begin
         s4_result_h <= div_result_h;
         s4_result_l <= div_result_l;
      end
   end
   always @(posedge clk or negedge xrst) begin
      if (xrst == 0) begin
      s4_ack_reg <=0;
      s4_from_v_reg <=0;
      s4_v_reg <= 0;
      end
      else begin
         s4_ack_reg <= s3_ack_reg;
         s4_from_v_reg <= s3_from_v_reg;
         s4_v_reg <= s3_v_reg;
      end
   end

   wire s5_quotient_l_sel, s5_quotient_h_sel, s5_quotient_sel, s5_v;
   reg s5_v_reg;

   assign s5_quotient_h_sel = (s4_from_v_reg != 8'd0) ? s4_result_h : 8'd0;
   assign s5_quotient_l_sel = (s4_from_v_reg != 8'd255) ? s4_result_l : 8'd0;
   assign s5_quotient_sel = (s4_v_reg > s4_from_v_reg) ? s5_quotient_l_sel : s5_quotient_h_sel;
   assign s5_v = (s5_quotient_sel > 8'd255) ? 8'd255 : s5_quotient_sel;

   always @(posedge clk or negedge xrst) begin
      if (xrst == 1'b0)
	s5_v_reg <= 8'd0;
      else
	s5_v_reg <= s5_v;
   end

   /*reg [7:0] s5_result_l, s5_result_h;
   always @(posedge clk or negedge xrst) begin
      if (xrst == 0) begin
         s5_result_l <=0;
         s5_result_h <=0;
      end
      else begin
         if (from_v == 0) begin
               s5_result_l <= 0;
               s5_result_h <= s4_result_h;
         end else if (from_)
      end
   end*/

   //////////////////////////////////////////////////////////
   // output
   //////////////////////////////////////////////////////////
   assign pixel_v_out = s5_v_reg;
   assign snd_ack = s4_ack_reg;
   assign rcv_req = snd_req;

endmodule
