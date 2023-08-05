/**********************************************************************
 * $nodeinfo_test example -- Verilog HDL test bench.
 *
 * Verilog test bench to test the $nodeinfo_test PLI application.
 *
 * For the book, "The Verilog PLI Handbook" by Stuart Sutherland
 *  Book copyright 1999, Kluwer Academic Publishers, Norwell, MA, USA
 *   Contact: www.wkap.il
 *  Example copyright 1998, Sutherland HDL Inc, Portland, Oregon, USA
 *   Contact: www.sutherland.com or (503) 692-0898
 *********************************************************************/
`timescale 1ns / 1ns
module test;
  reg     reg1;
  reg [39:0] reg2;
  integer int1;
  time    time1;
  real    real1;
  wire (strong0, weak1) w1 = reg1;
  wire [0:39] w2 = reg2;
  parameter param1 = 1;
  parameter [7:0] param2 = 2;
  parameter [47:0] param3 = 3;
  parameter param4 = 4.1;

  reg [23:0] RAM [0:3];
  integer ARRAY [1:0];

  initial
    begin
      reg1 = 1'bx;
      reg2 = {10{4'b01ZX}};
      int1 = "ABCD";
      time1 = 'h25;
      real1 = 3.1415;
      RAM[0] = "EFG";

      #1 $nodeinfo_test(reg1);
      #1 $nodeinfo_test(reg2);
      #1 $nodeinfo_test(reg2[29:20]);
      #1 $nodeinfo_test(int1[9:2]);
      #1 $nodeinfo_test(time1[3]);
      #1 $nodeinfo_test(real1);
      #1 $nodeinfo_test(w1);
      #1 $nodeinfo_test(w2);
      #1 $nodeinfo_test(param1);
      #1 $nodeinfo_test(param2);
      #1 $nodeinfo_test(param3);
      #1 $nodeinfo_test(param4);
      #1 $nodeinfo_test(RAM[0]);
      #1 $nodeinfo_test(ARRAY[0]);

      //unsupported expressions
      #1 $nodeinfo_test(w2[39]);
      #1 $nodeinfo_test(w2[36:39]);
      #1 $nodeinfo_test();
      #1 $nodeinfo_test(5);
      #1 $nodeinfo_test("foobar");

      #1 $finish;
    end

endmodule

/**********************************************************************/

