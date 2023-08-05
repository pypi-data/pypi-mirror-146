// Module sig pulse generator
module period_sig(sig_out);

output
	sig_out;
reg
	sig_out;

// Declaration of data types
parameter
	sig_delay=1,
	sig_period=100;

initial		// Execute at time 0
	begin	
		sig_out = 0;
		#(sig_delay -1) sig_out = 1;
		#2 sig_out = 0;

		forever		// Repeat forever
		  begin
			#(sig_period - 2) sig_out = 1;
			#2 sig_out = 0;
		  end

	end

endmodule


// Module sig pulse generator
module period_doubled_sig(sig_out);

output
	sig_out;
reg
	sig_out;

// Declaration of data types
parameter
	sig_delay=1,
	sig_period=100,
	sig_interval=5;

initial		// Execute at time 0
	begin	
		sig_out = 0;
		#(sig_delay -1) sig_out = 1;
		#2 sig_out = 0;
		#(sig_interval-2) sig_out = 1;
		#2 sig_out = 0;

		forever		// Repeat forever
		  begin
			#(sig_period - 2) sig_out = 1;
			#2 sig_out = 0;
			#(sig_interval-2) sig_out = 1;
			#2 sig_out = 0;
		  end

	end

endmodule
