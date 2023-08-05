// Verilog HDL for "gates.lib", "jtl2" "_functional"

module jtl2(in, out);

input
	in;

output
	out;
reg 
	out;

parameter
	delay=6;

initial 
	begin
		out = 0;
	end

always @(posedge in) 	// Execute at positive edge of in
	begin
	  out <= #delay in;
	  out <= #(delay+2) 0;
	end

endmodule
