module bar
  (/*AUTOARG*/
  // Outputs
  REQ_OUT, THIS_NAME_LONGER_OUT,
  // Inputs
  MY_ADDR_IN, ACK_IN, THIS_IS_LONGER_NAME_IN
  );

  input [1:0] MY_ADDR_IN;
  output      REQ_OUT;
  input       ACK_IN;
  input       THIS_IS_LONGER_NAME_IN;
  output      THIS_NAME_LONGER_OUT;

  /* AUTOWIRE */

endmodule
