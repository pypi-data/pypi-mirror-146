/**********************************************************************
 * $my_strobe example -- Verilog HDL test bench.
 *
 * Verilog test bench to test the $my_strobe PLI application.
 *
 * For the book, "The Verilog PLI Handbook" by Stuart Sutherland
 *  Book copyright 1999, Kluwer Academic Publishers, Norwell, MA, USA
 *   Contact: www.wkap.il
 *  Example copyright 1998, Sutherland HDL Inc, Portland, Oregon, USA
 *   Contact: www.sutherland.com or (503) 692-0898
 *********************************************************************/
`timescale 1ns / 1ns
module test;
  reg  a, b, ci, clk;
  reg  sum, co;

  always @(a or b or ci)
    {co,sum} = a + b + ci;

  initial
    begin
      $strobe ("$strobe   : At %0d: \t %m.sum = %d",$time, sum);
      $display("$display  : At %0d: \t %m.sum = %d",$time, sum);
      $my_strobe(sum);
      a = 0; b = 0; ci = 0;

      #10 $display("");
      a = 1;
      $my_strobe(sum);
      $strobe ("$strobe   : At %0d: \t %m.sum = %d",$time, sum);
      $display("$display  : At %0d: \t %m.sum = %d",$time, sum);
      
      #10 $display("");
      a = 0;
      $my_strobe(sum);
      $display("$display  : At %0d: \t %m.sum = %d",$time, sum);
      $strobe ("$strobe   : At %0d: \t %m.sum = %d",$time, sum);

      #10 $display("");
      b = 1;
      $strobe ("$strobe   : At %0d: \t %m.sum = %d",$time, sum);
      $my_strobe(sum);
      $display("$display  : At %0d: \t %m.sum = %d",$time, sum);
      a = 1;
      $my_strobe(sum);
      $strobe ("$strobe   : At %0d: \t %m.sum = %d",$time, sum);
      $display("$display  : At %0d: \t %m.sum = %d",$time, sum);

      #10 $display("");
      $finish;
    end

  initial
      $monitor("$monitor  : At %0d: \t %m.sum = %d",$time, sum);
  
endmodule

/*** A gate level 1 bit adder model ***/
`timescale 1ns / 1ns
module addbit (a, b, ci, sum, co);
  input  a, b, ci;
  output sum, co;

  wire  a, b, ci, sum, co,
        n1, n2, n3;

  xor    (n1, a, b);
  xor    (sum, n1, ci);
  and    (n2, a, b);
  and    (n3, n1, ci);
  or     (co, n2, n3);

endmodule
/*********************************************************************/

