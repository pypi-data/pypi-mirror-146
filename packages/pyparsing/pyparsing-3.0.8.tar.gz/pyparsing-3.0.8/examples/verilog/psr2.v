// Verilog HDL for "gates.lib", "psr2" "_functional"
// Module Parallel Shift Register 2
module psr2 (sin, clr, clk, sout, pout);

input
	sin, clr, clk;

output
	sout, pout;
wire
	sout, pout;

parameter
	t_hold	= 14,
	t_setup	= -3,
	delay	= 31;

defparam
	psr2split.delay = 10,
	psr2and.t_hold = t_hold,
	psr2and.t_setup = t_setup,
	psr2and.delay = delay - 10;

wire
	aout;

and_gate  psr2and(sin, clr, clk, aout);
splitter  psr2split(aout, sout, pout);

endmodule
	
