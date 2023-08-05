// Verilog HDL for "gates.lib", "and_gate" "_functional"
// Module AND gate
module and_gate (a, b, clk, out);

input
	a, b, clk;

output
	out;
reg 
	out;

parameter
	t_hold	= 12,
	t_setup	=  1,
	delay	= 25,

	warning_file=3;  // multichannel description of a warning file

reg
	a_internal, b_internal, clk_internal,
	a_state, b_state,          // internal state at inputs a and b
	a_set, b_set;		   // signals determining the moment when
				   // the state of the a,b inputs changes to "1"
integer
	data_delay, 	// delay between a (b) and a_internal (b_internal)
	clk_delay, 	// delay between clk and clk_internal
	out_delay, 	// delay between clk_internal and out
	out_value,	// output value in a given clock cycle
	last_clk_time;	// time when the last clock pulse appeared

initial 
	begin
// define delays between inputs & outputs and the corresponding
//  internal auxiliary registers
	  	if(t_hold<0)
		  begin
	    		data_delay = -t_hold;
	    	  	clk_delay = 0;
		  	out_delay = delay;
		  end
	  	else
		  begin
	    	  	data_delay = 0;
	    	  	clk_delay = t_hold;
		  	out_delay=delay-t_hold;
		  end

// clear internal registers and the output signal
		a_internal = 0;
		b_internal = 0;
		clk_internal = 0;
		last_clk_time = 0;
		a_state = 0;
		b_state = 0;
		a_set = 0;
		b_set = 0;
		out = 0;
	end

always @(posedge a) 	// Execute at positive edge of a
	  a_internal <= #(data_delay) a;

always @(posedge b) 	// Execute at positive edge of b
	  b_internal <= #(data_delay) b;

always @(posedge clk) 	// Execute at positive edge of clk
	  clk_internal <= #(clk_delay) clk;

always @(posedge a_internal)
	begin
// setting an internal state at the input a
                a_state <= a_state | 1'bx;
		if (a_internal === 1)
		  a_set <= #(t_hold+t_setup) 1;

		a_internal <= 0;
	end

always @(posedge b_internal)
	begin
// setting an internal state at the input a
                b_state <= b_state | 1'bx;
		if (b_internal === 1)
		  b_set <= #(t_hold+t_setup) 1;

		b_internal <= 0;
	end

always @(posedge a_set)
	begin
		if ($stime - last_clk_time >= t_hold+t_setup)
			a_state = 1;
		else
		  begin
			a_state = 1'bx;

		  // generating a warning
		  	$fwrite(warning_file, 
			 "Violation of hold/setup time in module %m.\n");
			$fwrite(warning_file,
			"Input A pulse at %0d,",
			 $stime-data_delay-t_hold-t_setup);
			$fwrite(warning_file,
			"\tClock pulse at %0d.\n", last_clk_time-clk_delay);
		  end

		a_set <= 0;
	end

always @(posedge b_set)
	begin
		if ($stime - last_clk_time >= t_hold+t_setup)
			b_state = 1;
		else
		  begin
			b_state = 1'bx;

		  // generating a warning
		  	$fwrite(warning_file, 
			 "Violation of hold/setup time in module %m.\n");
			$fwrite(warning_file,
			"Input B pulse at %0d,",
			 $stime-data_delay-t_hold-t_setup);
			$fwrite(warning_file,
			"\tClock pulse at %0d.\n", last_clk_time-clk_delay);
		  end

		b_set <= 0;
	end


always @(posedge clk_internal)	
	begin
// computing the output
		if (clk_internal === 1'bx)
		  out_value = 1'bx;
		else
		  out_value = a_state & b_state;

// transfering the result to the output
		out <= #(out_delay) out_value;
		out <= #(out_delay+2) 0;

// clearing the internal state of A and B inputs
		a_state  <= 0;
		b_state  <= 0;

		clk_internal <= 0;
		last_clk_time = $stime;
	end

endmodule
