module foo
  (/*AUTOARG*/
  // Outputs
  ACK_OUT, THIS_IS_LONGER_NAME_OUT, THIS_IS_ANOTHER_LONG_NAME_OUT,
  // Inputs
  MY_ADDR_IN, REQ_IN, THIS_NAME_LONGER_IN
  );

  input [1:0] MY_ADDR_IN;
  input       REQ_IN;
  output      ACK_OUT;
  input       THIS_NAME_LONGER_IN;
  output      THIS_IS_LONGER_NAME_OUT;
  output      THIS_IS_ANOTHER_LONG_NAME_OUT;

  /* AUTOWIRE */

endmodule
