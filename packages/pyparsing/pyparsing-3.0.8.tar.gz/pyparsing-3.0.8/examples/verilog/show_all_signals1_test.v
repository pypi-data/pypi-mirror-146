/**********************************************************************
 * $show_all_signals example -- Verilog test bench source code
 *
 * Verilog test bench to test the $show_all_signals PLI application on
 * a 1-bit adder modeled using RTL code.
 *
 * For the book, "The Verilog PLI Handbook" by Stuart Sutherland
 *  Book copyright 1999, Kluwer Academic Publishers, Norwell, MA, USA
 *   Contact: www.wkap.il
 *  Example copyright 1998, Sutherland HDL Inc, Portland, Oregon, USA
 *   Contact: www.sutherland.com or (503) 692-0898
 *********************************************************************/
`timescale 1ns / 1ns
module top;
  integer    test;
  tri  [1:0] results;

  addbit i1 (test[0], test[1], test[2], results[0], results[1]);

  initial
    begin
      test = 3'b000;
      #10 test = 3'b001;

      #10 $show_all_signals1(top);
      #10 $show_all_signals1(i1);

      #10 $stop;
      #10 $finish;
    end
endmodule

/*** An RTL level 1 bit adder model ***/
`timescale 1ns / 1ns
module addbit (a, b, ci, sum, co);
  input  a, b, ci;
  output sum, co;

  wire  a, b, ci;
  reg   sum, co;

  always @(a or b or ci)
    {co, sum} = a + b + ci;

endmodule
/*********************************************************************/

