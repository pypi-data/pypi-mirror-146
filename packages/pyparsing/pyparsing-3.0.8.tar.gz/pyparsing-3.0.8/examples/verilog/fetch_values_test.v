/**********************************************************************
 * $test_acc_fetch_value example -- Verilog test bench source code
 *
 * Verilog test bench to test the $test_acc_fetch_value PLI application
 *
 * For the book, "The Verilog PLI Handbook" by Stuart Sutherland
 *  Book copyright 1999, Kluwer Academic Publishers, Norwell, MA, USA
 *   Contact: www.wkap.il
 *  Example copyright 1998, Sutherland HDL Inc, Portland, Oregon, USA
 *   Contact: www.sutherland.com or (503) 692-0898
 *********************************************************************/
`timescale 1ns / 1ns
module top;
  reg  [15:0] reg1;
  real        real1;

  initial
    begin
      reg1  = "Hi";
      real1 = 3.1415;

      #1 $test_acc_fetch_value(reg1);
//      #1 $test_acc_fetch_value(real1);

      #10 $finish;
    end
endmodule

/*********************************************************************/

