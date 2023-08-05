module TestCtr3sr;

reg Clk;		// Clock: rising edge
reg Reset;		// synchronous reset
wire [1:0] Out;		// output

	Ctr3sr c(Clk, Reset, Out); // design for test
	initial 
	begin
		$dumpfile("TestCtr3sr.vcd"); // command to generate a dumpfile
		$dumpvars(0); 		     // put all variables in the dumpfile
			Reset = 0;	
			#50 Reset = 1;	// reset not activ
			#20 Reset = 0;	// reset activ
			#200 Reset = 1; // after 1 periode reset not activ
			#20 Reset = 0; 	// after a while again
		$finish;
	end
	initial // generate clock
	begin
		Clk = 0; 
		while (1)
			#10 Clk = !Clk;
	end
endmodule
