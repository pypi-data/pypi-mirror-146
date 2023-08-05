// Verilog HDL for "gates.lib", "dro_cell" "_functional"
// Module DRO cell
module dro_cell (d, clk, out);

input
	d, clk;

output
	out;
reg 
	out;

parameter
	t_hold	= -3,
	t_setup	= 8,
	delay	= 9,

	warning_file=3;  // multichannel description of a warning file

reg
	d_internal, clk_internal,
	d_state,          	   // internal state at the input d
	d_set;		   	   // signal determining the moment when
				   // the state of the d input changes to "1"

integer
	data_delay,  // delay between d and d_internal
	clk_delay,   // delay between clk and clk_internal
	out_delay,   // delay between clk_internal and out
	out_value,   // output value in a given clock cycle
	last_clk_time;	// time when the last clock pulse appeared

initial 
	begin
// define delays between inputs & outputs and the corresponding
//  internal auxiliary registers
	  	if(t_hold<0)
		  begin
	    	  	data_delay = -t_hold;
	    		clk_delay  = 0;
			out_delay  = delay;
		  end
	  	else
		  begin
	   	  	data_delay = 0;
	    		clk_delay  = t_hold;
		  	out_delay  = delay-t_hold;
		  end

// clear internal registers and the output signal
		d_internal = 0;
		clk_internal = 0;
		last_clk_time = 0;
		d_state = 0;
		d_set = 0;
		out = 0;
	end



always @(posedge d) 	// Execute at positive edge of d
	  d_internal <= #(data_delay) d;

always @(posedge clk)  // Execute at positive edge of clk
	  clk_internal <= #(clk_delay) clk;


always @(posedge d_internal)
	begin
// setting the state of the d input
                d_state <= d_state | 1'bx;
		if (d_internal === 1)
		  d_set <= #(t_hold+t_setup) 1;

		d_internal <= 0;
	end

always @(posedge d_set)
	begin
		if ($stime - last_clk_time >= t_hold+t_setup)
			d_state = 1;
		else
		  begin
			d_state = 1'bx;

		  // generating a warning
		  	$fwrite(warning_file, 
			 "Violation of hold/setup time in module %m.\n");
			$fwrite(warning_file,
			"Input D pulse at %0d,",
			 $stime-data_delay-t_hold-t_setup);
			$fwrite(warning_file,
			"\tClock pulse at %0d.\n", last_clk_time-clk_delay);
		  end

		d_set <= 0;
	end


always @(posedge clk_internal)	
	begin
// computing the output
		if (clk_internal === 1'bx)
		  out_value = 1'bx;
		else
		  out_value = d_state;

// transfering the result to the output
		out <= #(out_delay) out_value;
		out <= #(out_delay+2) 0;

// clearing the internal state of the DRO
		d_state  <= 0;

		clk_internal <= 0;
		last_clk_time = $stime;
	end

endmodule
