/**********************************************************************
 * $hello example -- Verilog HDL test bench.
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
      $hello;
      #10 $stop;
      $finish;
    end
endmodule
/**********************************************************************/
