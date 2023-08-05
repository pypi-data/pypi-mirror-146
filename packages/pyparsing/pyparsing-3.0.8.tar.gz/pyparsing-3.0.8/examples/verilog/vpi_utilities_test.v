/**********************************************************************
 * $vpi_util_test example -- Verilog HDL test bench.
 *
 * Verilog test bench to test the VPI utility applications. 
 *
 * For the book, "The Verilog PLI Handbook" by Stuart Sutherland
 *  Book copyright 1999, Kluwer Academic Publishers, Norwell, MA, USA
 *   Contact: www.wkap.il
 *  Example copyright 1998, Sutherland HDL Inc, Portland, Oregon, USA
 *   Contact: www.sutherland.com or (503) 692-0898
 *********************************************************************/
`timescale 1ns / 1ns
module test;
  reg  a, b, ci;
  wire sum, co;
  real r1;

  addbit i1 (a, b, ci, sum, co);

  initial
    begin
      a = 0; b = 1; ci = 1;
      r1 = 0.5;
      $vpi_util_test(i1, r1, ci, "Hello world", /*null arg*/ );
      #1 $finish;
    end
 
 endmodule

/*** A gate level 1 bit adder model ***/
`timescale 1ns / 1ns
module addbit (a, b, ci, sum, co);
  input  a, b, ci;
  output sum, co;

  wire  a, b, ci, sum, co,
        n1, n2, n3;

  xor    (n1, a, b);
  xor #2 (sum, n1, ci);
  and    (n2, a, b);
  and    (n3, n1, ci);
  or  #2 (co, n2, n3);

endmodule
/**********************************************************************/
