// Verilog HDL for "gates.lib", "sig_gen" "_functional"
// Module sig pulse generator
module sig_gen(out);

output
	out;
reg
	out;

// Declaration of data types
parameter
	sig_delay=10,
	sig_period=100;

initial		// Execute at time 0
	begin	
		out = 0;
		#(sig_delay -1) out = 1;
		#2 out = 0;

		forever		// Repeat forever
		  begin
			#(sig_period - 2) out = 1;
			#2 out = 0;
		  end

	end

endmodule
