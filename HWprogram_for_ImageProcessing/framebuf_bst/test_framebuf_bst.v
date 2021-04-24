`timescale 1ps / 1ps

module test_framebuf_bst();

   parameter CLK = 10;

   parameter PIXEL_NUM = 128 * 128;

   reg [7:0]  imem_r [0:PIXEL_NUM-1];
   reg [7:0]  imem_g [0:PIXEL_NUM-1];
   reg [7:0]  imem_b [0:PIXEL_NUM-1];

   reg [7:0]  omem_r [0:PIXEL_NUM-1];
   reg [7:0]  omem_g [0:PIXEL_NUM-1];
   reg [7:0]  omem_b [0:PIXEL_NUM-1];

   // receive port (SLAVE)
   reg [7:0] pixel_a_in;
   reg [7:0] pixel_b_in;
   reg [7:0] pixel_c_in;
   wire      receiv_req;
   reg 	     receiv_ack;

   // send port (MASTER)
   wire [7:0] pixel_a_out;
   wire [7:0] pixel_b_out;
   wire [7:0] pixel_c_out;
   reg 	      send_req;
   wire       send_ack;

   // clock, reset
   reg 	      clk;
   reg 	      reset;
   wire [2:0] state;
   wire [13:0] address;

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
      reset = 1'b0;
      read_image;
      #(CLK);

    start_time = $time;
      reset = 1'b1;
      receiv_ack = 1'b0;
      send_req = 1'b0;
      // data input
      while (receiv_req == 1'b0) begin
        $display("OK1");
        #(CLK*2);
      end
        for (i = 0; i < PIXEL_NUM; i = i + 1) begin
	        receiv_ack = 1'b1;
	    pixel_a_in = imem_r[i];
	    pixel_b_in = imem_g[i];
	    pixel_c_in = imem_b[i];
	    #(CLK);
        //$display("omem_a: %d, omem_g %d, omem_b %d", imem_r[i], imem_g[i], imem_b[i]);
        end
      receiv_ack = 1'b0;

      #(CLK*2)
      // data output
      send_req = 1'b1;
      while (send_ack == 1'b0) begin
        #(CLK*2);
        send_req = 0;
      end
        for (i = 0; i < PIXEL_NUM; i = i + 1) begin
	        omem_r[i] = pixel_a_out;
	    omem_g[i] = pixel_b_out;
	    omem_b[i] = pixel_c_out;
        #(CLK);
        end

      $display("Simulation time: %d ns", ($time-start_time)/1000);

      #(CLK*10);
      
      save_image;
      $finish;
   end

   // module
   framebuf_bst framebuf0(// Outputs
		      .receiv_req		(receiv_req),
		      .pixel_a_out	(pixel_a_out[7:0]),
		      .pixel_b_out	(pixel_b_out[7:0]),
		      .pixel_c_out	(pixel_c_out[7:0]),
		      .send_ack		(send_ack),
		      // Inputs
		      .pixel_a_in	(pixel_a_in[7:0]),
		      .pixel_b_in	(pixel_b_in[7:0]),
		      .pixel_c_in	(pixel_c_in[7:0]),
		      .receiv_ack		(receiv_ack),
		      .send_req		(send_req),
		      .clk		(clk),
		      .reset		(reset),
              .state (state[2:0]),
              .address (address[13:0]));

   task read_image;
      reg [8:0]  r;
      reg [8:0]  g;
      reg [8:0]  b;
      integer fd;
      integer i;
      integer c;
      reg [127:0] str;
      begin
	 fd = $fopen("input.ppm", "r");
	 // skip header lines
	 c = $fgets(str, fd);
	 c = $fgets(str, fd);
	 c = $fgets(str, fd);
	 // read pixels
	 for (i = 0; i < PIXEL_NUM; i = i + 1) begin
            c = $fscanf(fd, "%d %d %d", r, g, b);
	    imem_r[i] = r;
	    imem_g[i] = g;
	    imem_b[i] = b;
         end
	 $fclose(fd);
      end
   endtask

   task save_image;
      reg [8:0]  r;
      reg [8:0]  g;
      reg [8:0]  b;
      integer fd;
      integer i;
      integer c;
      reg [127:0] str;
      begin
	 fd = $fopen("output.ppm", "w");
	 // write headers
	 $fdisplay(fd, "P3");
	 $fdisplay(fd, "128 128");
	 $fdisplay(fd, "255");
	 // write pixels
	 for (i = 0; i < PIXEL_NUM; i = i + 1) begin
      //$display("omem_a: %d, omem_g %d, omem_b %d", omem_r[i], omem_g[i], omem_b[i]);
	    $fdisplay(fd, "%d %d %d", omem_r[i], omem_g[i], omem_b[i]);
         end
	 $fclose(fd);
      end
   endtask

endmodule
