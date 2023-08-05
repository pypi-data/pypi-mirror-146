/**********************************************************************
 * $set_mipd_delays example -- Verilog HDL test bench.
 *
 * Verilog test bench to test the $set_mipd_delays PLI application.
 *
 * For the book, "The Verilog PLI Handbook" by Stuart Sutherland
 *  Book copyright 1999, Kluwer Academic Publishers, Norwell, MA, USA
 *   Contact: www.wkap.il
 *  Example copyright 1998, Sutherland HDL Inc, Portland, Oregon, USA
 *   Contact: www.sutherland.com or (503) 692-0898
 *********************************************************************/
`timescale 1ns / 10ps
module test;
  reg  a, b, ci, clk;
  wire sum, co;

  addbit i1 (a, b, ci, sum, co);

  initial
    begin
      $set_mipd_delays(i1.a, 2.3, 2.4, 2.5);
      a = 0; b = 0; ci = 0;
      #10 a = 1;
      #10 b = 1;
      #10 a = 0;
      #1 $finish;
    end
    
  initial
    $monitor("At %0.2f: a=%d b=%d ci%d sum=%d co=%d",
             $realtime, a, b, ci, sum, co);
    
endmodule

/*** A gate level 1 bit adder model ***/
`timescale 1ns / 10ps
module addbit (a, b, ci, sum, co);
  input  a, b, ci;
  output sum, co;

  wire  a, b, ci, sum, co,
        n1, n2, n3;

  xor  (n1, a, b);
  xor  (sum, n1, ci);
  and  (n2, a, b);
  and  (n3, n1, ci);
  or   (co, n2, n3);
  
endmodule
/*********************************************************************/

