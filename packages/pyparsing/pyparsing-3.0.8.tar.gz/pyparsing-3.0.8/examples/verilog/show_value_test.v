/**********************************************************************
 * $show_value example -- Verilog HDL test bench.
 *
 * Verilog test bench to test the $show_value PLI application on a 
 * 1-bit adder modeled using gate primitives.
 *
 * For the book, "The Verilog PLI Handbook" by Stuart Sutherland
 *  Book copyright 1999, Kluwer Academic Publishers, Norwell, MA, USA
 *   Contact: www.wkap.il
 *  Example copyright 1998, Sutherland HDL Inc, Portland, Oregon, USA
 *   Contact: www.sutherland.com or (503) 692-0898
 *********************************************************************/
`timescale 1ns / 1ns
module test;
  reg  a, b, ci, clk;
  wire sum, co;

  addbit i1 (a, b, ci, sum, co);

  initial
    begin
//      $monitor("At %0d: \t a=%b  b=%b  ci=%b  sum=%b  co=%b",
//               $time, a, b, ci, sum, co);
      clk = 0;
      a = 0;
      b = 0;
      ci = 0;
      #10 a = 1;
      #10 b = 1;

      $show_value(sum);
      $show_value(co);
      $show_value(i1.n3);

      #10 $stop;
      $finish;
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

