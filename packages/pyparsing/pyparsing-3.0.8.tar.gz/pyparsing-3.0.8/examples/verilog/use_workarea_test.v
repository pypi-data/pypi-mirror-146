/**********************************************************************
 * $test_vpiworkarea example -- Verilog HDL test bench.
 *
 * Verilog test bench to test the $test_vpiworkarea PLI application.
 *
 * For the book, "The Verilog PLI Handbook" by Stuart Sutherland
 *  Book copyright 1999, Kluwer Academic Publishers, Norwell, MA, USA
 *   Contact: www.wkap.il
 *  Example copyright 1998, Sutherland HDL Inc, Portland, Oregon, USA
 *   Contact: www.sutherland.com or (503) 692-0898
 *********************************************************************/
`timescale 1ns / 1ns
module test;

  initial
    begin
      #1 repeat (2) $test_vpiworkarea(1);
      #1 $test_vpiworkarea(2);
      #1 $test_vpiworkarea(3);
      #1 $test_vpiworkarea(4);
      #1 $finish;
    end
 
endmodule
/*********************************************************************/

