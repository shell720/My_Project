`timescale 1ps / 1ps

module test_top();

   parameter CLK = 1000000/10; // 10MHz

   parameter PIXEL_NUM = 128 * 128;

   reg [7:0]  imem [0:PIXEL_NUM-1];
   reg [7:0]  omem [0:PIXEL_NUM-1];

   wire [7:0] h,l;
   // receive port (SLAVE)
   reg [7:0] pixel_in;
   wire      rcv_req;
   reg 	     rcv_ack;

   // send port (MASTER)
   wire [7:0] pixel_out;
   reg 	      snd_req;
   wire       snd_ack;

   // input for adjust_v
   reg [7:0]  adjust_from_v;
   reg [7:0]  adjust_to_v;

   // clock, reset
   reg 	      clk;
   reg 	      xrst;

   integer start_time;
   integer i;

   // clock generation
   always begin
      clk = 1'b1;
      #(CLK/2);
      clk = 1'b0;
      #(CLK/2);
   end

   // test senario
   initial begin
      $dumpvars;
      // reset
      #(CLK/2);
      xrst = 1'b0;
      read_image;
      #(CLK);
      xrst = 1'b1;
      rcv_ack = 1'b0;
      snd_req = 1'b0;

      adjust_from_v = 8'd50;
      adjust_to_v = 8'd100;

      start_time = $time;

      // data input
      while (rcv_req == 1'b0) #(CLK);
      #(CLK);
      for (i = 0; i < PIXEL_NUM; i = i + 1) begin
	 rcv_ack = 1'b1;
	 pixel_in = imem[i];
	 #(CLK);
      end
      rcv_ack = 1'b0;
      
      // data output
      snd_req = 1'b1;
      while (snd_ack == 1'b0) #(CLK);
      snd_req = 1'b0;
      for (i = 0; i < PIXEL_NUM; i = i + 1) begin
	 omem[i] = pixel_out;
	 #(CLK);
      end

      $display("Simulation time: %d ns", ($time-start_time)/1000);

      #(CLK*10);
      
      save_image;
      $finish;
   end

   // module
   top top0(// Outputs
	    .rcv_req		(rcv_req),
	    .pixel_out		(pixel_out[7:0]),
	    .snd_ack		(snd_ack), .h(h[7:0]), .l(l[7:0]),
	    // Inputs
	    .pixel_in		(pixel_in[7:0]),
	    .rcv_ack		(rcv_ack),
	    .snd_req		(snd_req),
	    .adjust_from_v	(adjust_from_v),
	    .adjust_to_v	(adjust_to_v),
	    .clk		(clk),
	    .xrst		(xrst));

   task read_image;
      reg [7:0] val;
      integer fd;
      integer i;
      integer c;
      reg [127:0] str;
      begin
	 fd = $fopen("input.pgm", "r");
	 // skip header lines
	 c = $fgets(str, fd);
	 c = $fgets(str, fd);
	 c = $fgets(str, fd);
	 // read pixels
	 for (i = 0; i < PIXEL_NUM; i = i + 1) begin
            c = $fscanf(fd, "%d", val);
	    imem[i] = val;
         end
	 $fclose(fd);
      end
   endtask

   task save_image;
      integer fd;
      integer i;
      reg [127:0] str;
      begin
	 fd = $fopen("output.pgm", "w");
	 // write headers
	 $fdisplay(fd, "P2");
	 $fdisplay(fd, "128 128");
	 $fdisplay(fd, "255");
	 // write pixels
	 for (i = 0; i < PIXEL_NUM; i = i + 1) begin
	    $fdisplay(fd, "%d", omem[i]);
         end
	 $fclose(fd);
      end
   endtask

endmodule
