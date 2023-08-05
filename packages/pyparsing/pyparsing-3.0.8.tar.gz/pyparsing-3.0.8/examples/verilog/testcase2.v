module tap_controller (tms,
   tck,
   trst,
   sel,
   enable,
   test_logic_reset,
   idle,
   resetn,
   shift_ir,
   update_ir,
   clock_ir,
   shift_dr,
   capture_dr,
   clock_dr,
   update_dr);

input   tms;
input   tck;
input   trst;
output  sel;
output  enable;
output  test_logic_reset;
output  idle;
output  resetn;
output  shift_ir;
output  update_ir;
output  clock_ir;
output  shift_dr;
output  capture_dr;
output  clock_dr;
output  update_dr;
wire    sel;
reg     enable;
wire    test_logic_reset;
wire    idle;
reg     resetn;
reg     shift_ir;
wire    update_ir;
wire    clock_ir;
reg     shift_dr;
wire    capture_dr;
wire    clock_dr;
wire    update_dr;
reg     D;
reg     C;
reg     B;
reg     A;
wire    NA;
wire    NB;
wire    NC;
wire    ND;
wire    GRST;
wire    GENB;
wire    GSIR;
wire    GSDR;
wire    tckd;
wire    trsthi;
wire    tmsbuf;
wire    trstnbuf;

initial 
   begin
   A = 'b 1;
   end

initial 
   begin
   B = 'b 1;
   end

initial 
   begin
   C = 'b 1;
   end

initial 
   begin
   D = 'b 1;
   end

always @(posedge trsthi or posedge tckd)
   begin
   if (trsthi == 'b 1)

      resetn <= 'b 0; else if (tckd== 'b 1 ) resetn <=GRST; 
	  
   end 
	  
always @(posedge trsthi or posedge tckd) begin 
      if (trsthi== 'b 1) enable <='b 0;

      else if (tckd ==  'b 1 ) enable <=GENB; end 

always @(posedge trsthi or posedge tckd) begin 
      if (trsthi== 'b 1) shift_ir <='b 1;

      else if (tckd ==  'b 1 ) shift_ir <=GSIR; end 
	  

always @(posedge trsthi or posedge tckd) begin 
      if (trsthi== 'b 1) shift_dr <='b 1;

      else if (tckd ==  'b 1 ) shift_dr <=GSDR; end 
	  

always @(posedge trsthi or posedge tck) begin 
      if (trsthi== 'b 1) D <='b 1;

      else if (tck ==  'b 1 ) D <=ND; end 

always @(posedge trsthi or posedge tck) begin 
      if (trsthi== 'b 1) C <='b 1;

      else if (tck ==  'b 1 ) C <=NC; end 
	  

always @(posedge trsthi or posedge tck) begin 
      if (trsthi== 'b 1) B <='b 1;

      else if (tck ==  'b 1 ) B <=NB; end 
	  

always @(posedge trsthi or posedge tck) begin 
      if (trsthi== 'b 1) A <='b 1;

      else if (tck ==  'b 1 ) A <=NA; end 


  assign trsthi=~trstnbuf; assign sel=D; assign tckd=~tck; 
  assign clock_ir=~(~A & B & D & tckd); assign update_ir=A & ~B & C & D & tckd; 
  assign clock_dr=~(~A & B & ~D & tckd); assign test_logic_reset=A & B & C & D; 
  assign idle=~A & ~B & C & D; 
  assign update_dr=A & ~B & C & ~D & tckd; 
  assign capture_dr=~A & B & C & ~D; 
  assign tmsbuf=tms; assign trstnbuf=trst; 
  assign NA=~(~(~tmsbuf & ~C & A) & ~(tmsbuf & ~B) & ~(tmsbuf & ~A) & ~(tmsbuf & C & D)); 
  assign NB=~(~(~tmsbuf & B & ~A) & ~(~tmsbuf & ~C) & ~(~tmsbuf & ~D & B) 
       & ~(~tmsbuf & ~D & ~A) & ~(tmsbuf & C & ~B) & ~(tmsbuf & D & C & A)); 
  assign NC=~(~(C & ~B) & ~(C & A) & ~(tmsbuf & ~B)); 
  assign ND=~(~(D & ~C) & ~(D & B) & ~(~tmsbuf & C & ~B) & ~(~D & C & ~B & ~A)); 
  assign GRST=~(A & B & C & D); assign GSIR=~A & B & ~C & D; 
  assign GSDR=~A & B & ~C & ~D; assign GENB=GSIR | GSDR; 

endmodule // module tap_controller 
