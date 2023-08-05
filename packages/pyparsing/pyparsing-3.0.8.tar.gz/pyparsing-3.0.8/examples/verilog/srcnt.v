// Verilog HDL for "RSFQ.lib", "srcnt" "_functional"

// Module counterflow shift register cell
module srcnt (din, clkin, dout, clkout);

input
	din, clkin;

output
	dout, clkout;
reg 
	dout, clkout;

parameter
	t_hold	= -3,
	t_setup	= 8,
	delay = 9,        // delay between clkin and dout
	delay_clk = 12,   // delay between clkin and clkout

	warning_file=3;   // multichannel description of a warning file

reg
	dinternal, clkinternal,
	d_state,          	   // internal state at the input d
	d_set;		   	   // signal determining the moment when
				   // the state of the d input changes to "1"

integer
	data_delay,  // delay between d and dinternal
	clk_delay,   // delay between clk and clkinternal
	out_delay,   // delay between clkinternal and out
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
		dinternal = 0;
		clkinternal = 0;
		last_clk_time = 0;
		d_state = 0;
		d_set = 0;
		dout = 0;
		clkout = 0;
	end



always @(posedge din) 	// Execute at positive edge of din
	  dinternal <= #(data_delay) din;

always @(posedge clkin)  // Execute at positive edge of clkin
	  clkinternal <= #(clk_delay) clkin;


always @(posedge dinternal)
	begin
// setting the state of the d input
                d_state <= d_state | 1'bx;
		if (dinternal === 1)
		  d_set <= #(t_hold+t_setup) 1;

		dinternal <= 0;
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


always @(posedge clkinternal)	
	begin
// computing the output
		if (clkinternal === 1'bx)
		  out_value = 1'bx;
		else
		  out_value = d_state;

// transfering the result to the output
		dout <= #(out_delay) out_value;
		dout <= #(out_delay+2) 0;

		clkout <= #(delay_clk-clk_delay) clkinternal;
		clkout <= #(delay_clk-clk_delay+2) 0;

// clearing the internal state of the DRO
		d_state  <= 0;

		clkinternal <= 0;
		last_clk_time = $stime;
	end

endmodule
