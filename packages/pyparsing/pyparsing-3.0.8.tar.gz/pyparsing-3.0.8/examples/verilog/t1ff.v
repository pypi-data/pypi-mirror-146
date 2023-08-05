// Verilog HDL for "gates.lib", "t1ff" "_functional"
// Module T1 flip-flop
module t1ff (t, wr0, out, rd1);

input
	t, wr0;

output
	out, rd1;
reg 
	out, rd1;

parameter
	t_separation = 10,
	delay=8,
	t_hold = 7,
	t_setup = 6,
	rd1_delay=10,

	warning_file=3;  // multichannel description of a warning file

reg
	t_internal, wr0_internal, // signals at inputs after i/o stage
	t_state,  // internal state of T flip-flop
	sep_clr,  // signal marking the end of the separation zone
	hs_clr;	  // signal marking the end of the hold/setup zone


integer
	data_delay, 	// delay between t and t_internal
	wr0_delay, 	// delay between rd and rd_internal
	t_out_delay, 	// delay between t_internal and out
	wr0_out_delay,  // delay between rd_internal and out
	last_t_time,    // time when the last t pulse appeared
	last_wr0_time,  // time when the last wr0 pulse appeared
	in_hs,    // number of t pulses in hold/setup zone
	in_sep,	 // number of pulses within an interval t_sep before 
		 //  the last data pulse;
	out_value; // value at the output;

initial 
	begin
// define delays between inputs & outputs and the corresponding
//  internal auxiliary registers
	  	if(t_hold<0)
		  begin
	    	  	data_delay = -t_hold;
	    		wr0_delay  = 0;
		  end
	  	else
		  begin
	   	  	data_delay = 0;
	    		wr0_delay  = t_hold;
		  end
		t_out_delay  = delay-data_delay;
		wr0_out_delay = rd1_delay-wr0_delay;

// clear internal registers and the output signal
		t_internal = 0;
		wr0_internal = 0;
		t_state = 0;
		in_hs = 0;
		in_sep = 0;
		sep_clr = 0;
		hs_clr = 0;
		out = 0;
		rd1 = 0;
	end


always @(posedge t) 	// Execute at positive edge of t
	  t_internal <= #(data_delay) t;

always @(posedge wr0) 	// Execute at positive edge of t
	  wr0_internal <= #(wr0_delay) wr0;


always @(posedge t_internal)
	begin
	  if (in_sep>0)
	    begin
	      t_state = 1'bx;

	    // generating a warning
	      $fwrite(warning_file, 
	       "Violation of separation time in module %m.\n");
	      $fwrite(warning_file,
	       "Input T pulses at %0d and at %0d.\n", last_t_time, 
	       $stime-data_delay);
	    end
	  last_t_time <= $stime-data_delay;

	  out <= #t_out_delay t_state;
	  out <= #(t_out_delay+2) 0;

	  t_state = t_state ^ 1;
	  if (t_internal === 1)
	    begin
	      in_sep = in_sep + 1;
	      sep_clr <= #(t_separation) 1;
	    end
	  else
	    t_state = 1'bx;

// setting the state of the t input
	  if (t_internal === 1)
	    begin
	      in_hs = in_hs+1;
	      hs_clr <= #(t_hold+t_setup) 1;
	    end
	  else
	    t_state = 1'bx;

	  t_internal <= 0;
	end


always @(posedge hs_clr)
	begin
		if ($stime - last_wr0_time < t_hold+t_setup)
		  begin
			t_state = 1'bx;

		  // generating a warning
		  	$fwrite(warning_file, 
			 "Violation of hold/setup time in module %m.\n");
			$fwrite(warning_file,
			"Input T pulse at %0d,",
			 $stime-data_delay-t_hold-t_setup);
			$fwrite(warning_file,
			"\tInput WRITE0 pulse at %0d.\n",
			 last_wr0_time-wr0_delay);
		  end

		in_hs = in_hs-1;
		hs_clr <= 0;
	end

always @(posedge sep_clr)
	begin
	  	in_sep = in_sep - 1;
		sep_clr <= 0;
	end


always @(posedge wr0_internal)	
	begin
// computing the output
		if ((wr0_internal === 1'bx) || (in_hs>0))
		  out_value = 1'bx;
		else
		  out_value = t_state;

// transfering the result to the output
		rd1 <= #(wr0_out_delay) out_value;
		rd1 <= #(wr0_out_delay+2) 0;

// clearing the internal state of T1 flip-flop
		if(in_hs == 0)
		  t_state  = 0;
		else
		  t_state = 1'bx;

		wr0_internal <= 0;
		last_wr0_time = $stime;
	end


endmodule
