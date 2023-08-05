module fubar
  (/*AUTOARG*/
  // Outputs
  ThisIsAnotherLongName, THIS_IS_ANOTHER_LONG_NAME_OUT,
  // Inputs
  MY_ADDR_IN
  );

  input [1:0] MY_ADDR_IN;
  output      THIS_IS_ANOTHER_LONG_NAME_OUT;

  //------------------------------------------------------------------


  /*AUTOREGINPUT*/

  /*AUTOREG*/

  /*AUTOWIRE*/
  // Beginning of automatic wires (for undeclared instantiated-module outputs)
  wire                  Ack;                    // From foo of foo.v
  wire                  Req;                    // From bar of bar.v
  wire                  ThisIsLongerName;       // From foo of foo.v
  wire                  ThisNameLonger;         // From bar of bar.v
  // End of automatics

  //
  // inputs sort of work
  //

  /*AUTOUNUSED*/

  /*AUTOINPUT*/

  wire                  MyAddr;
  assign                MyAddr = MY_ADDR_IN;

  //
  // outputs dont work
  //

  /*AUTOOUTPUT*/
  // Beginning of automatic outputs (from unused autoinst outputs)
  output                ThisIsAnotherLongName;  // From foo of foo.v
  // End of automatics

  wire                  THIS_IS_ANOTHER_LONG_NAME_OUT;
  assign                THIS_IS_ANOTHER_LONG_NAME_OUT = ThisIsAnotherLongName;

  //------------------------------------------------------------------

  /*AUTO_LISP(defun underscore_to_camelcase (s)
               "Convert NAMES_LIKE_THIS to NamesLikeThis"
               (setq r "")
               (setq l (split-string s "_"))
               (while l
                 (setq r (concat r (upcase-initials (downcase (car l)))))
                 (setq l (cdr l)))
               r)*/

  /* foo AUTO_TEMPLATE (
   .\(.+\)_\(IN\|OUT\) (@"(underscore_to_camelcase \\"\1\\")"),
   ); */

  foo foo
    (/*AUTOINST*/
     // Outputs
     .ACK_OUT                           (Ack),                   // Templated
     .THIS_IS_LONGER_NAME_OUT           (ThisIsLongerName),      // Templated
     .THIS_IS_ANOTHER_LONG_NAME_OUT     (ThisIsAnotherLongName), // Templated
     // Inputs
     .MY_ADDR_IN                        (MyAddr),                // Templated
     .REQ_IN                            (Req),                   // Templated
     .THIS_NAME_LONGER_IN               (ThisNameLonger));        // Templated

  /* bar AUTO_TEMPLATE (
   .\(.+\)_\(IN\|OUT\) (@"(underscore_to_camelcase \\"\1\\")"),
   ); */

  bar bar
    (/*AUTOINST*/
     // Outputs
     .REQ_OUT                           (Req),                   // Templated
     .THIS_NAME_LONGER_OUT              (ThisNameLonger),        // Templated
     // Inputs
     .MY_ADDR_IN                        (MyAddr),                // Templated
     .ACK_IN                            (Ack),                   // Templated
     .THIS_IS_LONGER_NAME_IN            (ThisIsLongerName));      // Templated

  //------------------------------------------------------------------

endmodule
