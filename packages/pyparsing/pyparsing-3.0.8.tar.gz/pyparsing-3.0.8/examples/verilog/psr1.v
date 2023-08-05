// Verilog HDL for "gates.lib", "psr1" "_functional"
// Module Parallel Shift Register 1
module psr1 (sin, pin, clk, sout, pout);

input
	sin, pin, clk;

output
	sout, pout;
wire
	sout, pout;

parameter
	t_hold	= -14,
	t_setup	= 23,
	delay	= 20,
	t_separation = 10;

defparam
	psr1conf.t_separation = t_separation,
	psr1conf.delay  = 15,
	psr1split.delay = 10,
	psr1dro.t_hold 	= t_hold + 15,
	psr1dro.t_setup = t_setup - 15,
	psr1dro.delay 	= delay - 10;

wire
	din, dout;

conf_buff psr1conf(sin, pin, din);
dro_cell  psr1dro(din, clk, dout);
splitter  psr1split(dout, sout, pout);

endmodule
	
