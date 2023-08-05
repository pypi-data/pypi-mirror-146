// Verilog HDL for "gates.lib", "splitter" "_functional"
// SPLITTER
module splitter (in, out1, out2);

input
	in;

output
	out1, out2;
reg 
	out1, out2;

parameter
	delay	= 10;

initial 
	begin
		out1 = 0;
		out2 = 0;
	end

always @(posedge in) 	// Execute at positive edge of in
	begin
	  out1 <= #delay in;
	  out1 <= #(delay+2) 0;
	  out2 <= #delay in;
	  out2 <= #(delay+2) 0;
	end

endmodule
