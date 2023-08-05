// Verilog HDL for "RSFQ.lib", "ndro_cell" "_functional"
// Module NDRO cell

module ndro_cell (on, off, sig, out, dout);

input
	on, off, sig;

output
	out, dout;
reg 
	out, dout;

parameter
	off_sig_hold	= -3,
	off_sig_setup	= 8,
	on_sig_hold	= 10,
	on_sig_setup	= 7,
	on_off_hold	= 6,
	on_off_setup	= 10,
	sig_out_delay	= 12,
	off_dout_delay  = 10,

	warning_file=3;  // multichannel description of a warning file

reg
	on_internal, off_internal, sig_internal,
	ndro_state,          	   // internal state
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



always @(posedge on) 	// Execute at positive edge of on
	  on_internal <= #(data_delay) on;

always @(posedge off)  // Execute at positive edge of off
	  off_internal <= #(clk_delay) off;

always @(posedge sig)  // Execute at positive edge of sig
	  sig_internal <= #(clk_delay) sig;


always @(posedge on_internal)
	begin
                ndro_state <= ndro_state | 1'bx;
		if (on_internal === 1)
		  on_sig_set <= #(on_sig_hold+on_sig_setup) 1;

		on_internal <= 0;
	end

always @(posedge on_set)
	begin
		if ($stime - last_sig_time >= on_sig_hold+on_sig_setup)
			ndro_state = 1;
		else
		  begin
			ndro_state = 1'bx;

		  // generating a warning
		  	$fwrite(warning_file, 
			 "Violation of hold/setup time in module %m.\n");
			$fwrite(warning_file,
			"Input ON pulse at %0d,",
			 $stime-data_delay-t_hold-t_setup);
			$fwrite(warning_file,
			"\tSIG pulse at %0d.\n", last_clk_time-clk_delay);
		  end

		on_set <= 0;
	end


always @(posedge sig_internal)	
	begin
// computing the output
		if (sig_internal === 1'bx)
		  out_value = 1'bx;
		else
		  out_value = ndro_state;

// transfering the result to the output
		out <= #(out_delay) out_value;
		out <= #(out_delay+2) 0;

                ndro_state <= ndro_state | 1'bx;
		if (sig_internal === 1)
		  sig_off_set <= #(sig_off_hold+sig_off_setup) 1;

		sig_internal <= 0;
		last_sig_time = $stime;
	end


always @(posedge off_internal)	
	begin
// computing the output
		if (off_internal === 1'bx)
		  out_value = 1'bx;
		else
		  out_value = ndro_state;

// transfering the result to the output
		out <= #(out_delay) out_value;
		out <= #(out_delay+2) 0;

// clearing the internal state of the NDRO
		ndro_state  <= 0;

		off_internal <= 0;
		last_off_time = $stime;
	end


endmodule
