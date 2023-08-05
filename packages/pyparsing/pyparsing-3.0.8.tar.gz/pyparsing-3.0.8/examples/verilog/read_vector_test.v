/**********************************************************************
 * $read_test_vector example -- Verilog test bench source code
 *
 * Verilog test bench to test the $read_test_vector PLI application.
 * NOTE: this test uses two data file, "read_vector_test1.pat" and
 * "read_vector_test2.pat".  Each file has several 8-bit binary values
 * (represented in ASCII).
 *
 * For the book, "The Verilog PLI Handbook" by Stuart Sutherland
 *  Book copyright 1999, Kluwer Academic Publishers, Norwell, MA, USA
 *   Contact: www.wkap.il
 *  Example copyright 1998, Sutherland HDL Inc, Portland, Oregon, USA
 *   Contact: www.sutherland.com or (503) 692-0898
 *********************************************************************/
`timescale 1ns / 1ns
module test;

  reg [7:0] vector;
  reg       clk;

  initial
    begin
      $monitor("at %d: clk = %b  vector = %b", $stime, clk, vector);
      clk = 0;
      forever #10 clk = ~clk;
    end

  always @(posedge clk)
    $read_test_vector("read_vector_test1.pat", vector);
 
  always @(negedge clk)
    $read_test_vector("read_vector_test2.pat", vector);
 
 endmodule
/**********************************************************************/

