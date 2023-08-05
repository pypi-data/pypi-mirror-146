/**********************************************************************
 * $read_strengthval example -- Verilog HDL test bench.
 *
 * Verilog test bench to test the $read_strengthval PLI application.
 *
 * For the book, "The Verilog PLI Handbook" by Stuart Sutherland
 *  Book copyright 1999, Kluwer Academic Publishers, Norwell, MA, USA
 *   Contact: www.wkap.il
 *  Example copyright 1998, Sutherland HDL Inc, Portland, Oregon, USA
 *   Contact: www.sutherland.com or (503) 692-0898
 *********************************************************************/
`timescale 1ns / 1ns
module test;
  wire a = 1'b0;
  wire b = 1'b1;
  wire c = 1'bz;
  wire d = 1'bx;
  wire e;
  assign (pull0, pull1) e = 1'b1;  /* wired logic on e */
  assign (pull1, pull0) e = 1'b0;
  
  wire f;
  bufif1 (f, 1'b0, 1'bx); /* ambiguous output 'L' */
  
  wire g;
  notif1 (g, 1'b0, 1'bx); /* ambiguous output 'H' */
  
  initial
    begin
      #1 
      $read_strengthval(a);
      $read_strengthval(b);
      $read_strengthval(c);
      $read_strengthval(d);
      $read_strengthval(e);
      $read_strengthval(f);
      $read_strengthval(g);
      #1 $finish;
    end
endmodule

/*********************************************************************/

