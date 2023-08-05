/**********************************************************************
 * $list_pathout_ports example -- Verilog test bench source code
 *
 * Verilog test bench to test the $list_pathout_ports PLI application.
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
  wire sum, co, foo;

  addbit i1 (a, b, ci, sum, co, foo);

  initial
    begin
      $monitor("At %0d: \t a=%b  b=%b  ci=%b  sum=%b  co=%b",
               $time, a, b, ci, sum, co);
      clk = 0;
      a = 0;
      b = 0;
      ci = 0;
      #10 a = 1;
      #10 b = 1;

      #10 $list_pathout_ports(i1);

      #10 $finish;
    end
endmodule

/*** A gate level 1 bit adder model ***/
`timescale 1ns / 1ns
module addbit (a, b, ci, sum, co, foo);
  input  a, b, ci;
  output sum, co, foo;

  wire  a, b, ci, sum, co, foo,
        n1, n2, n3;

  xor    (n1, a, b);
  xor    (sum, n1, ci);
  and    (n2, a, b);
  and    (n3, n1, ci);
  or     (co, n2, n3);

  specify
    (a,b,ci => sum) = 2;
    (a,b,ci => co)  = 3;
  endspecify

endmodule
/*********************************************************************/

