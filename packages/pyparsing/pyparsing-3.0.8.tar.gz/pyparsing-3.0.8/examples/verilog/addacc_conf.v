// Verilog HDL for "RSFQ.lib", "conf_buff" "_functional"

// Module CONFLUENCE BUFFER
module addacc_conf (in1, in2, out);

input
	in1, in2;

output
	out;
reg 
	out;

parameter
	t_separation = 10,
	delay=20,

// multichannel description of a warning file
	warning_file=2,  
// multichannel description of a delay file
	delay_file = warning_file<<1;

reg
	sep_clr; // signal marking the end of the min separation zone
		 //  for the last pulse

integer
	last_in_time,    // time when the last t pulse appeared
	in_sep,	 // number of pulses within an interval t_sep before 
		 //  the last data pulse;
	vdelay;		 // variable delay


`include "INIT"

`ifdef RANDOM_DELAYS
 `include "RANDOM_GATE"
`endif


initial 
	begin
		vdelay = delay;

`ifdef RANDOM_DELAYS
		delay_dev = addacc_conf_variation*delay;
		vdelay = $dist_normal(addacc_conf_seed, delay, delay_dev);
`endif

		#1 $fdisplay(delay_file, "module=%m, nom_delay=%0d, delay=%0d", delay, vdelay);

// clear internal registers and the output signal
		last_in_time = 0;
		in_sep = 0;
		sep_clr = 0;
		out = 0;
	end

always @(posedge in1)
	begin
		out <= #vdelay ((in_sep > 0) || (in2 == 1)) ? 1'bx : 1;
		out <= #(vdelay+2) 0;
		
		if((in_sep>0) || (in2 == 1))
	          begin
	        // generating a warning
	            $fwrite(warning_file, 
	            "Violation of separation time in module %m.\n");
	            $fwrite(warning_file,
	            "Input pulses at ");
		    if(in_sep>0)
			$fwrite(warning_file,
			"%0d and at %0d.\n", last_in_time, $stime);
		    else
			$fwrite(warning_file,
			"%0d and at %0d.\n", $stime, $stime);
	    	  end
	  	last_in_time <= $stime;

		in_sep <= in_sep + 1;
		sep_clr <= #(t_separation-1) 1;
	end

always @(posedge in2)
	begin
		out <= #vdelay ((in_sep > 0) || (in1 == 1)) ? 1'bx : 1;
		out <= #(vdelay+2) 0;

		if((in_sep>0) || (in1 == 1))
	          begin
	        // generating a warning
	            $fwrite(warning_file, 
	            "Violation of separation time in module %m.\n");
	            $fwrite(warning_file,
	            "Input pulses at ");
		    if(in_sep>0)
			$fwrite(warning_file,
			"%0d and at %0d.\n", last_in_time, $stime);
		    else
			$fwrite(warning_file,
			"%0d and at %0d.\n", $stime, $stime);
	    	  end
	  	last_in_time <= $stime;

		in_sep <= in_sep + 1;
		sep_clr <= #(t_separation-1) 1;
	end

always @(posedge sep_clr)
	begin
	  	in_sep <= in_sep - 1;
		sep_clr <= 0;
	end


endmodule
