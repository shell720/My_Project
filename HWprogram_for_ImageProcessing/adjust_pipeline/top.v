module top(
   // Outputs
   rcv_req, pixel_out, snd_ack, h, l,
   // Inputs
   clk, xrst, pixel_in, rcv_ack, snd_req, adjust_from_v, adjust_to_v
   );

   output[7:0] h, l;
   // clock, reset
   input 	clk;
   input 	xrst;

   // receive port (MASTER)
   input [7:0] pixel_in;
   output      rcv_req;
   input       rcv_ack;

   // send port (SLAVE)
   output [7:0] pixel_out;
   input 	snd_req;
   output 	snd_ack;

   // input for adjust_v
   input [7:0] 	adjust_from_v;
   input [7:0] 	adjust_to_v;

   // wire (buf0 <-> adjust)
   wire [7:0] buf0_adjust_pixel;
   wire       buf0_adjust_ack;
   wire       adjust_buf0_req;

   // wire (adjust <-> buf1)
   wire [7:0] adjust_buf1_pixel;
   wire       adjust_buf1_ack;
   wire       buf1_adjust_req;

   framebuf buf0(// Outputs
		 .rcv_req	(rcv_req),
		 .pixel_out	(buf0_adjust_pixel[7:0]),
		 .snd_ack	(buf0_adjust_ack),
		 // Inputs
		 .pixel_in	(pixel_in[7:0]),
		 .rcv_ack	(rcv_ack),
		 .snd_req	(adjust_buf0_req),
		 .clk		(clk),
		 .xrst		(xrst));

   adjust_v adj0(// Outputs
		 .rcv_req	(adjust_buf0_req),
		 .pixel_v_out	(adjust_buf1_pixel[7:0]),
		 .snd_ack	(adjust_buf1_ack), .h (h), .l (l),
		 // Inputs
		 .pixel_v_in	(buf0_adjust_pixel[7:0]),
		 .from_v	(adjust_from_v),
		 .to_v		(adjust_to_v),
		 .rcv_ack	(buf0_adjust_ack),
		 .snd_req	(buf1_adjust_req),
		 .clk		(clk),
		 .xrst		(xrst));

   framebuf buf1(// Outputs
		 .rcv_req	(buf1_adjust_req),
		 .pixel_out	(pixel_out[7:0]),
		 .snd_ack	(snd_ack),
		 // Inputs
		 .pixel_in	(adjust_buf1_pixel[7:0]),
		 .rcv_ack	(adjust_buf1_ack),
		 .snd_req	(snd_req),
		 .clk		(clk),
		 .xrst		(xrst));

endmodule
