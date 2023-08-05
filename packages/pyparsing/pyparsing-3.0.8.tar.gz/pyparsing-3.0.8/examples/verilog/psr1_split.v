// Verilog HDL for "gates.lib", "splitter" "_functional"

module psr1_split (out1, out2, in);

input
	in;

output
	out1, out2;
reg 
	out1, out2;

parameter
	delay=10,

// multichannel description of a warning file
	warning_file=2,  
// multichannel description of a delay file
	delay_file = warning_file<<1;

integer
	vdelay;		 // variable delay


`include "INIT"

`ifdef RANDOM_DELAYS
 `include "RANDOM_GATE"
`endif


initial 
	begin
		vdelay = delay;

`ifdef RANDOM_DELAYS
		delay_dev = psr1_split_variation*delay;
		vdelay = $dist_normal(psr1_dro_seed, delay, delay_dev);
`endif

		#1 $fdisplay(delay_file, "module=%m, nom_delay=%0d, delay=%0d", delay, vdelay);

		out1 = 0;
		out2 = 0;
	end

always @(posedge in) 	// Execute at positive edge of in
	begin
	  out1 <= #vdelay in;
	  out1 <= #(vdelay+2) 0;
	  out2 <= #vdelay in;
	  out2 <= #(vdelay+2) 0;
	end

endmodule
