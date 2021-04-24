`timescale 1ps/1ps

module test_framebuf();

   parameter CLK = 10;

   parameter imageSize = 128 * 128;

   reg [7:0]  imem_r [0:imageSize-1];
   reg [7:0]  imem_g [0:imageSize-1];
   reg [7:0]  imem_b [0:imageSize-1];

   reg [7:0]  omem_r [0:imageSize-1];
   reg [7:0]  omem_g [0:imageSize-1];
   reg [7:0]  omem_b [0:imageSize-1];

   // receive port (SLAVE)
   reg [7:0] pixel_a_in, pixel_b_in, pixel_c_in;
   wire      recev_req;
   reg 	     recev_ack;

   // send port (MASTER)
   wire [7:0] pixel_a_out, pixel_b_out, pixel_c_out;
   reg 	      send_req;
   wire       send_ack;

   // clock, reset
   reg 	      clk;
   reg 	      reset;
   wire [13:0] address;
   wire [2:0] state;

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

      reset = 1'b1;
      recev_ack = 1'b0;
      send_req = 1'b0;
      start_time = $time;
      // data input
      //for文になるのは、recev_reqが立ち上がる瞬間(recev_reqは0と判定される)
      for (i = 0; i < imageSize; i = i + 1) begin
      //$display("receiv_req: %d, rece_ack %d", recev_req, recev_ack);
	    if (recev_req == 1'b0) begin
            #(CLK*2);
	    recev_ack = 1'b1;
	    pixel_a_in = imem_r[i];
	    pixel_b_in = imem_g[i];
	    pixel_c_in = imem_b[i];
        end 
        if (recev_req == 1'b1) begin //先のifが実行された後に実行される
            #(CLK*3);
	    recev_ack = 1'b0;
        end
      end
      
      // data output
      for (i = 0; i < imageSize; i = i + 1) begin
	   send_req = 1'b1;
	      while (send_ack == 1'b0) begin
         #(CLK*3);
	      send_req = 1'b0;
         end
	      while (send_ack == 1'b1) begin
            #(CLK*2);
         end
         //$display("pixel_a: %d, pixel_b %d, pixel_c %d", pixel_a_out, pixel_b_out, pixel_c_out);
    	   omem_r[i] = pixel_a_out;
    	   omem_g[i] = pixel_b_out;
	      omem_b[i] = pixel_c_out;
      end

      $display("Simulation time: %d ns", ($time-start_time)/1000);

      #(CLK*10);
      
      $display("OK5");
      save_image;
      $finish;
   end

   // module
   framebuf framebuf0(
		      .recev_req		(recev_req),
		      .pixel_a_out	(pixel_a_out[7:0]),
		      .pixel_b_out	(pixel_b_out[7:0]),
		      .pixel_c_out	(pixel_c_out[7:0]),
		      .send_ack		(send_ack),
		      .pixel_a_in	(pixel_a_in[7:0]),
		      .pixel_b_in	(pixel_b_in[7:0]),
		      .pixel_c_in	(pixel_c_in[7:0]),
		      .recev_ack		(recev_ack),
		      .send_req		(send_req),
		      .clk		(clk),
		      .reset		(reset),
              .address  (address[13:0]),
              .state_out    (state[2:0]));

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
	 for (i = 0; i < imageSize; i = i + 1) begin
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
	 for (i = 0; i < imageSize; i = i + 1) begin
      $display("omem_a: %d, omem_g %d, omem_b %d", omem_r[i], omem_g[i], omem_b[i]);
	    $fdisplay(fd, "%d %d %d", omem_r[i], omem_g[i], omem_b[i]);
         end
	 $fclose(fd);
      end
   endtask

endmodule