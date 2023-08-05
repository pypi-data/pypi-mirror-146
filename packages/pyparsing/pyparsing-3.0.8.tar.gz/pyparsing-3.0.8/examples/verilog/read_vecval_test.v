/**********************************************************************
 * $read_vecval example -- Verilog HDL test bench.
 *
 * Verilog test bench to test the $read_vecval PLI application.
 *
 * For the book, "The Verilog PLI Handbook" by Stuart Sutherland
 *  Book copyright 1999, Kluwer Academic Publishers, Norwell, MA, USA
 *   Contact: www.wkap.il
 *  Example copyright 1998, Sutherland HDL Inc, Portland, Oregon, USA
 *   Contact: www.sutherland.com or (503) 692-0898
 *********************************************************************/
`timescale 1ns / 1ns
module test;
  reg [39:0] data;

  initial
    begin
      data     = 40'b0;
      data[0]  = 1'b1;
      data[16] = 1'bz;
      data[39] = 1'bx;
      #1 $read_vecval(data);
      #1 $finish;
    end
endmodule

/*********************************************************************/

