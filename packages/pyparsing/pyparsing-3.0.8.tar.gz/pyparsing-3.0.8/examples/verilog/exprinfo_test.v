/**********************************************************************
 * $exprinfo_test example -- Verilog HDL test bench.
 *
 * Verilog test bench to test the $exprinfo_test PLI application.
 *
 * For the book, "The Verilog PLI Handbook" by Stuart Sutherland
 *  Book copyright 1999, Kluwer Academic Publishers, Norwell, MA, USA
 *   Contact: www.wkap.il
 *  Example copyright 1998, Sutherland HDL Inc, Portland, Oregon, USA
 *   Contact: www.sutherland.com or (503) 692-0898
 *********************************************************************/
`timescale 1ns / 1ns
module test;
  reg        reg1;
  reg [31:0] reg2;
  reg [0:51] reg3;
  real       r1;

  initial
    begin
      reg1 = 1'b0;
      reg2 = 32'hF0F0F0F0;
      reg3 = {13{4'b01zx}};
      r1   = 3.1415;

      #1 $exprinfo_test("Hello world");
      #1 $exprinfo_test(r1);
      #1 $exprinfo_test(reg1);
      #1 $exprinfo_test(reg2);
      #1 $exprinfo_test(reg3);
      #1 $exprinfo_test(reg3[1]);
      #1 $exprinfo_test(reg3[4:48]);

      #1 $finish;
    end

endmodule

/**********************************************************************/

