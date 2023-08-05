// Verilog HDL for "LIB", "hadd" "_functional"

module hadd (clock, A_in, B_in, carry, sum);

// Default values for the timing parameters
parameter
	delay_carry = 33,
	delay_sum = 37,
	t_hold = 1,
	t_setup = 31,
	t_sep = 11,
	warning_file = 2;

// Declaration of data types
input
	clock,
	A_in,
	B_in;

output
	carry,
	sum;

reg
	trig,
	carry,
	sum,
	data_A,
	data_B,
	extra_A,
	extra_B;	// Multi-pulse indicators

integer
	current_time,
	holdtime,
	sep_time,
	left_bound,
	right_bound,
	time_A,
	time_B;

initial
  begin		// Initialization
	trig = 0;
	left_bound = 0;
	{data_A, data_B} = 0;
	{carry, sum} = 0;
	#0 holdtime = (t_hold < 0) ? 0 : t_hold;
  end	// initial

always @(posedge A_in)
  begin
    // Store the time position of the data (center of the pulse)
    time_A = $time + 1;
    // Store the value of the data input
    data_A = A_in;

    // Display warning if more than 1 data pulse comes in 1 clock cycle
    if (extra_A == 'b1)
      $fdisplay(warning_file, "Extra pulse detected in module %m at input A at %0d ps.\n", time_A);

    extra_A = 1;	// Set after 1 data pulse comes
  end	// always

always @(posedge B_in)
  begin
    // Store the time position of the data (center of the pulse)
    time_B = $time + 1;
    // Store the value of the data input
    data_B = B_in;

    // Display warning if more than 1 data pulse comes in 1 clock cycle
    if (extra_B == 'b1)
      $fdisplay(warning_file, "Extra pulse detected in module %m at input B at %0d ps.\n", time_B);

    extra_B = 1;	// Set after 1 data pulse comes
  end	// always

always @(posedge clock)
// Trigger after clock+holdtime
  trig <= #(holdtime-1) 1;

always @(posedge trig)
  begin
    current_time = $time+1-(holdtime-1);	// Present time of clock
// Delay = 0.5 so that clock cycles do not overlap
    #0.5 trig = 0;

    // Generate output only if there are input pulses
    if ((data_A !== 'b0) | (data_B !== 'b0))
      begin
	// Reset to receive data input in a new clock cycle
	extra_A = 0;
	extra_B = 0;
	// Determine the right boundary of the time range in which there is no timing violation
	right_bound = current_time - t_setup;

	casex ({(data_A !== 'b0), (data_B !== 'b0), ((time_A >= left_bound) & (time_A <= right_bound)), ((time_B >= left_bound) & (time_B <= right_bound))})

	// Two data inputs and no timing violation
	  4'b1111:
	    begin
	      sep_time = time_A - time_B;
	      sep_time = (sep_time < 0) ? -sep_time : sep_time;
	      // Separation time violation?
	      if (sep_time < t_sep)
		begin
		  carry <= #(delay_carry - holdtime) 'bx;
		  sum <= #(delay_sum - holdtime) 'bx;
		  $fdisplay(warning_file, "Violation of separation time in module %m.\nInput A at %0d ps, input B at %0d ps.\n", time_A, time_B);
		end
	      else
		carry <= #(delay_carry - holdtime) (data_A & data_B);
	      // Reset to receive new data values in a new clock cycle
	      {data_A, data_B} = 0;
	    end

	// One data input and no timing violation
	  4'b101x:
	    begin
	      sum <= #(delay_sum - holdtime) data_A;
	      data_A = 0;
	    end

	// One data input and no timing violation
	  4'b01x1:
	    begin
	      sum <= #(delay_sum - holdtime) data_B;
	      data_B = 0;
	    end

	// Two data inputs and there is timing violation
	  4'b1100:
	    begin
	      carry <= #(delay_carry - holdtime) 'bx;
	      sum <= #(delay_sum - holdtime) 'bx;
	      // Issue a warning
	      if ((time_A > right_bound) & (time_B > right_bound))
		$fdisplay(warning_file, "Violation of hold/setup time in module %m. \nInput A at %0d ps, input B at %0d ps, clock at %0d ps.\n", time_A, time_B, current_time);
	      else if (time_A > right_bound)
		begin
		  $fdisplay(warning_file, "Violation of hold/setup time in module %m. \nInput A at %0d ps, clock at %0d ps.\n", time_A, current_time);
		  data_B = 0;
		end
	      else if (time_B > right_bound)
		begin
		  $fdisplay(warning_file, "Violation of hold/setup time in module %m. \nInput B at %0d ps, clock at %0d ps.\n", time_B, current_time);
		  data_A = 0;
		end
	      // If a warning has been issued before
	      else
		{data_A, data_B} = 0;
	    end

	// One data input and there is timing violation
	  4'b100x:
	    begin
	      sum <= #(delay_sum - holdtime) 'bx;
	      // Issue a warning
	      if (time_A > right_bound)
		$fdisplay(warning_file, "Violation of hold/setup time in module %m. \nInput A at %0d ps, clock at %0d ps.\n", time_A, current_time);
	      // If a warning has been issued before
	      else
		data_A = 0;
	    end

	// One data input and there is timing violation
	  4'b01x0:
	    begin
	      sum <= #(delay_sum - holdtime) 'bx;
	      // Issue a warning
	      if (time_B > right_bound)
		$fdisplay(warning_file, "Violation of hold/setup time in module %m. \nInput B at %0d ps, clock at %0d ps.\n", time_B, current_time);
	      // If a warning has been issued before
	      else
		data_B = 0;
	    end

	// Two data inputs and there is timing violation
	  4'b1110:
	    begin
	      carry <= #(delay_carry - holdtime) 'bx;
	      sum <= #(delay_sum - holdtime) 'bx;
	      // Issue a warning
	      if (time_A > right_bound)
		$fdisplay(warning_file, "Violation of hold/setup time in module %m. \nInput A at %0d ps, clock at %0d ps.\n", time_A, current_time);
	      // If a warning has been issued before
	      else
		data_A = 0;
	    end

	// Two data inputs and there is timing violation
	  4'b1101:
	    begin
	      carry <= #(delay_carry - holdtime) 'bx;
	      sum <= #(delay_sum - holdtime) 'bx;
	      // Issue a warning
	      if (time_B > right_bound)
		$fdisplay(warning_file, "Violation of hold/setup time in module %m. \nInput B at %0d ps, clock at %0d ps.\n", time_B, current_time);
	      // If a warning has been issued before
	      else
		data_B = 0;
	    end

	endcase

	// Reset the outputs after 2ps
	carry <= #(delay_carry - holdtime + 2) 0;
	sum <= #(delay_sum - holdtime + 2) 0;
      end	// if

     // Determine the left boundary of the time range in which there is no timing violation
    left_bound = current_time + t_hold;
  end	// always
			
endmodule
