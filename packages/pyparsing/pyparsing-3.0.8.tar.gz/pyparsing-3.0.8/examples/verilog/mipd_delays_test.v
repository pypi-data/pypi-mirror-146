/**********************************************************************
 * $append_gate_delays example -- Verilog test bench source code
 *
 * Verilog test bench to test the $append_gate_delays PLI application.
 *
 * For the book, "The Verilog PLI Handbook" by Stuart Sutherland
 *  Book copyright 1999, Kluwer Academic Publishers, Norwell, MA, USA
 *   Contact: www.wkap.il
 *  Example copyright 1998, Sutherland HDL Inc, Portland, Oregon, USA
 *   Contact: www.sutherland.com or (503) 692-0898
 *********************************************************************/
`timescale 1ns / 100ps
module top;
  reg  [2:0] test;
  wire [1:0] results;

  addbit i1 (test[0], test[1], test[2], results[0], results[1]);

  initial
    begin
      $mipd_delays(i1.ci, 1.4, 1.6, 1.9, 1.1, 1.3, 1.5, 0.6, 0.8, 0.9);
      #1 $finish;
    end
endmodule

/*** A gate level 1 bit adder model ***/
`timescale 1ns / 10ps
module addbit (a, b, ci, sum, co);
  input  a, b, ci;
  output sum, co;

  wire  a, b, ci, sum, co, n1, n2, n3, n4;

  xor #1.87       p1 (n1, a, b);    // all transitions have same delay
  xor #(1.8, 2.2) p2 (sum, n1, ci); //rise, fall delays
  and             p3 (n2, a, b);
  and             p4 (n3, n1, ci);
  or  #4          p5 (co, n2, n3);  //integer delay
  
endmodule
/*********************************************************************/

