// pipe2.v      Verilog version using modules in this file
//              basic five stage pipeline of just Instruction Register
//              The 411 course pipeline has the same five stages
//              IF Instruction Fetch includes PC and instruction memory
//              ID Instruction Decode and registers
//              EX Execution including the ALU Arithmetic Logic Unit
//              MEM data Memory
//              WB Write Back into registers
//
// This self contained Verilog file defines:
//
//     a 32 bit adder module using behavioral code
//     32 and 5 bit register module with clock and clear inputs
//     an instruction memory module using behavioral code
//     a data memory module using behavioral code
//     a general register module using behavioral code
//     32 and 5 bit multiplexor module using behavioral code
//
//     a top level module, pipe2, test bench
//     the wires for interconnecting the entities
//     the modules instantiated to connect the wires
//     printout that shows the registers in the pipeline each clock
//

`timescale 1ps/1ps // times in pico seconds

module add32(a, b, cin, sum, cout);
  parameter n=31;
  input  [n:0] a;     // a input
  input  [n:0] b;     // b input
  input        cin;   // carry-in
  output [n:0] sum;   // sum output
  output       cout;  // carry-out
  assign #250 {cout, sum} = a + b + cin;
endmodule // add32


module register_32(clk, clear, inp, out);
  input         clk;    // accept  inp  on posedge
  input         clear;  // clear when high
  input  [31:0] inp;    // input data
  output [31:0] out;    // output of register
  wire   [31:0] inp;
  wire   [31:0] out;
  reg    [31:0] stored;        // temporary variable

  initial stored = 32'h00000000;

  assign out = stored;  // set output wire

  always @(posedge clk) #200 stored <= inp;
endmodule // register_32


module register_5(clk, clear, inp, out);
  input        clk;    // accept  inp  on posedge
  input        clear;  // clear when high
  input  [4:0] inp;    // input data
  output [4:0] out;    // output of register
  wire   [4:0] out;
  reg    [4:0] stored;        // temporary variable

  initial stored = 5'b00000;

  assign out = stored;  // set output wire

  always @(posedge clk) #200 stored <= inp;
endmodule // register_5


module instruction_memory(addr, inst);
  input [31:0] addr;
  output [31:0] inst;
  integer word_addr;
  reg [31:0] memory [0:15];
  reg [31:0] inst_word;

  assign inst = inst_word;

  function [31:0] to_integer;
    input [31:0] argument;
    to_integer = argument;
  endfunction // to_integer

  initial
    begin
      memory[0] = 32'b10001100000000010000000000000100;  // lw
      memory[1] = 32'b10001100000000100000000000001000;  // lw
      memory[2] = 32'b00000000000000000000000000000000;  // nop
      memory[3] = 32'b00000000000000000000000000000000;  // nop
      memory[4] = 32'b00000000001000100001100000100000;  // add
      memory[5] = 32'b00000000011000100010000000100010;  // sub
      memory[6] = 32'b00000000000000010010101111000001;  // sll
      memory[7] = 32'b00000000000000100011010000000010;  // srl
      memory[8] = 32'b00000000000000110011100000000100;  // cmpl
      memory[9] = 32'b10101100000000010000000000001000;  // sw
      memory[10]= 32'b00000000000000000000000000000000;  // nop
      memory[11]= 32'b00000000000000000000000000000000;  // nop
      memory[12]= 32'b00000000000000000000000000000000;  // nop
      memory[13]= 32'b00000000000000000000000000000000;  // nop
      memory[14]= 32'b00000000000000000000000000000000;  // nop
      memory[15]= 32'b00000000000000000000000000000000;  // nop
    end

  always @(addr)
    begin  // behavior
      word_addr = to_integer(addr)/4;
      #250 inst_word = memory[word_addr];
    end
endmodule // instruction_memory


module data_memory(address, write_data, read_enable, write_enable,
                   write_clk, read_data);
  input  [31:0] address;
  input  [31:0] write_data;
  input         read_enable;
  input         write_enable;
  input         write_clk;
  output [31:0] read_data;
  wire   [31:0] read_data;

  integer word_addr;
  integer write_addr;
  reg [31:0] memory [0:1000];
  reg [31:0] data_word;

  assign read_data = data_word;

  function [31:0] to_integer;
    input [31:0] argument;
    to_integer = argument;
  endfunction // to_integer

  initial
    begin
      memory[0] = 32'b00010001000100010001000100010001; // h0
      memory[1] = 32'b00100010001000100010001000100010; // h4
      memory[2] = 32'b00110011001100110011001100110011; // h8
    end // rest is XXXXXXXXXX

  always @(address or posedge read_enable)
    begin  // behavior
      word_addr = to_integer(address)/4;
      if(read_enable==1)
        #250 data_word <= memory[word_addr];
    end

  always @(negedge read_enable)
         #200 data_word = 32'b00000000000000000000000000000000;

  always @(posedge write_clk)
    begin
      if(write_enable==1)
        begin
          write_addr = to_integer(address)/4;
          memory[write_addr] = write_data;
        end
    end
endmodule // data_memory


module registers(read_reg_1, read_reg_2, write_reg,
                 write_data, write_enable, write_clk,
                 read_data_1, read_data_2);
  input   [4:0] read_reg_1;    // 5 bit register address to read data 1
  input   [4:0] read_reg_2;    // 5 bit register address to read data 2
  input   [4:0] write_reg;     // 5 bit register address to write
  input  [31:0] write_data;    // 32 bit word to write into register
  input         write_enable;  // rising clock and enable
  input         write_clk;     // required to write
  output [31:0] read_data_1;   // register content of read_reg_1
  output [31:0] read_data_2;   // register content of read_reg_2
  wire   [31:0] read_data_1;
  wire   [31:0] read_data_2;

  integer reg_addr_1;
  integer reg_addr_2;
  integer write_addr;
  integer i;
  reg [31:0] memory [0:31];
  reg [31:0] reg_word_1;
  reg [31:0] reg_word_2;

  assign read_data_1 = reg_word_1;
  assign read_data_2 = reg_word_2;

  function [5:0] to_integer;
    input [5:0] argument;
    to_integer = argument;
  endfunction // to_integer

  initial
    begin
      for(i=0; i<32; i=i+1) memory[i] = 32'h00000000;
      reg_word_1 = 32'h00000000;
      reg_word_2 = 32'h00000000;
    end

  always @(read_reg_1)
    begin
      reg_addr_1 = to_integer(read_reg_1);
      #50 reg_word_1 <= memory[reg_addr_1];
    end

  always @(read_reg_2)
    begin
      reg_addr_2 = to_integer(read_reg_2);
      #50 reg_word_2 <= memory[reg_addr_2];
    end

  always @(posedge write_clk)
    begin  // behavior
      write_addr = to_integer(write_reg);
      if(write_enable==1)
        begin
          #100 memory[write_addr] = write_data;
          if(write_reg==read_reg_1) reg_word_1 = write_data;
          if(write_reg==read_reg_2) reg_word_2 = write_data;
        end
    end
endmodule // registers


module mux_32(in0, in1, ctl, result);
  parameter n=31;
  input  [n:0] in0;     // 0 input
  input  [n:0] in1;     // 1 input
  input        ctl;     // control
  output [n:0] result;  // output
  assign result = (ctl==0) ? in0 : in1;
endmodule // mux_32


module mux_5(in0, in1, ctl, result);
  parameter n=4;
  input  [n:0] in0;     // 0 input
  input  [n:0] in1;     // 1 input
  input        ctl;     // control
  output [n:0] result;  // output
  assign result = (ctl==0) ? in0 : in1;
endmodule // mux_5

module alu_32(inA, inB, inst, result);
  input  [31:0] inA;
  input  [31:0] inB;
  input  [31:0] inst;
  output [31:0] result;
  wire   [31:0] result;
  reg           cin; //=0
  wire          cout;

  initial cin=0;

  add32 adder(inA, inB, cin, result, cout);

endmodule // alu_32

 
module pipe2;  // test bench
  // signals used in test bench (the interconnections)
  
  reg [31:0] zero_32; // = 32'h00000000;   // 32 bit zero
  reg        zero;    // = 0;              // one bit zero
  reg [31:0] four_32; // = 32'h00000004;   // four

  reg        clear;   // = 1;    // one shot clear
  reg        clk;     // = 0;    // master clock
  wire       clk_bar;            // split phase for mem write
  integer    counter; // = 0;    // master clock counter, raising edge
  wire       nc1;                // a No-Connection for unused output

  wire [31:0] PC_next;        // next value of PC 
  wire [31:0] PC;             // Program Counter
  wire [31:0] inst;              // instruction fetched


  wire [31:0] ID_IR;             // ID Instruction Register
  wire [31:0] ID_read_data_1;    // ID Register read data 1
  wire [31:0] ID_read_data_2;    // ID Register read data 2
  wire [31:0] ID_sign_ext;       // ID sign extension
  wire  [4:0] ID_rd;             // ID register destination
  wire [15:0] ID_addr;           // ID_IR[15:0] address
  wire        RegDst; //=0       // ID selects destination register
  wire        S;                 // ID for sign extend

  wire [31:0] EX_IR;             // EX Instruction Register
  wire [31:0] EX_A;              // EX data A
  wire [31:0] EX_B;              // EX data B
  wire [31:0] EX_C;              // EX data C
  wire  [4:0] EX_rd;             // EX register destination
  wire [31:0] EX_aluB;           // EX into ALU B
  wire        ALUSrc; //=1       // EX ALU B side source control
  wire [31:0] EX_result;         // EX ALU output


  wire [31:0] MEM_IR;            // MEM Instruction Register
  wire [31:0] MEM_addr;          // MEM address
  wire [31:0] MEM_data;          // MEM write data
  wire [31:0] MEM_read_data;     // MEM read data
  wire  [4:0] MEM_rd;            // MEM register destination
  wire        MEMRead;           // MEM enable read
  wire        MEMWrite; //=0;    // MEM enable write

  wire [31:0] WB_IR;             // WB Instruction Register
  wire [31:0] WB_read;           // WB read data
  wire [31:0] WB_pass;           // WB pass data
  wire  [4:0] WB_rd;             // WB register destination
  wire        MemtoReg;          // WB mux control
  wire [31:0] WB_result;         // WB mux output
  wire        WB_write_enb; //=1 // WB enable register write

  function [31:0] to_integer;
    input [31:0] argument;
    to_integer = argument;
  endfunction // to_integer
  
  initial
    begin
      zero_32 = 32'h00000000;    // 32 bit zero
      zero    = 0;               // one bit zero
      four_32 = 32'h00000004;    // four
      clear   = 1;               // one shot clear
      clk     = 0;               // master clock
      counter = 0;               // master clock counter, raising edge
      #200 clear = 0;            // clear time finished
      forever #5000 clk = ~clk;  // run clock 10ns period
    end

  initial #140000 $finish;       // stop after 140 ns

  assign ALUSrc = 1;             // change to correct expression
  assign RegDst = 0;             // change to correct expression
  assign MEMWrite = 0;           // change to correct expression
  assign WB_write_enb = 1;       // change to correct expression

  // schematic of pipe2, behavior and test bench
  assign  clk_bar = ~clk;        // for split phase registers

  // IF, Instruction Fetch pipeline stage
  register_32 PC_reg(clk, clear, PC_next, PC);
  add32 PC_incr(PC, four_32, zero, PC_next, nc1);
  instruction_memory inst_mem(PC, inst);

  // ID, Instruction Decode and register stack pipeline stage
  register_32 ID_IR_reg(clk, clear, inst, ID_IR);
  registers ID_regs(.read_reg_1(ID_IR[25:21]),
                    .read_reg_2(ID_IR[20:16]),
                    .write_reg(WB_rd),
                    .write_data(WB_result),
                    .write_enable(WB_write_enb),
                    .write_clk(clk_bar),
                    .read_data_1(ID_read_data_1),
                    .read_data_2(ID_read_data_2));
  mux_5 ID_mux_rd(.in0(ID_IR[20:16]),
                  .in1(ID_IR[15:11]),
                  .ctl(RegDst),
                  .result(ID_rd));
             assign ID_sign_ext[15:0] = ID_IR[15:0];  // just wiring
             assign ID_sign_ext[31:16] =
                    {S,S,S,S,S,S,S,S,S,S,S,S,S,S,S,S};
             assign S = ID_IR[15];
  // EX, Execute pipeline stage
  register_32 EX_IR_reg(clk, clear, ID_IR, EX_IR);
  register_32 EX_A_reg(clk, clear, ID_read_data_1, EX_A);
  register_32 EX_B_reg(clk, clear, ID_read_data_2, EX_B);
  register_32 EX_C_reg(clk, clear, ID_sign_ext, EX_C);
  register_5  EX_rd_reg(clk, clear, ID_rd, EX_rd);
  mux_32 EX_mux1(.in0(EX_B), .in1(EX_C), .ctl(ALUSrc), .result(EX_aluB));
  alu_32 ALU(.inA(EX_A),
             .inB(EX_aluB),
             .inst(EX_IR),
             .result(EX_result));

  // MEM Data Memory pipeline stage
  register_32 MEM_IR_reg(clk, clear, EX_IR, MEM_IR);
  register_32 MEM_addr_reg(clk, clear, EX_result, MEM_addr);
  register_32 MEM_data_reg(clk, clear, EX_B, MEM_data);
  register_5  MEM_rd_reg(clk, clear, EX_rd, MEM_rd);
              assign MEMRead = (MEM_IR[31:26] == 6'b100011 );
  data_memory data_mem(.address(MEM_addr),
                       .write_data(MEM_data),
                       .read_enable(MEMRead),
                       .write_enable(MEMWrite),
                       .write_clk(clk_bar),
                       .read_data(MEM_read_data));

  // WB, Write Back pipeline stage
  register_32 WB_IR_reg(clk, clear, MEM_IR, WB_IR);
  register_32 WB_read_reg(clk, clear, MEM_read_data, WB_read);
  register_32 WB_pass_reg(clk, clear, MEM_addr, WB_pass);
  register_5  WB_rd_reg(clk, clear, MEM_rd, WB_rd);
              assign MemtoReg = (WB_IR[31:26] == 6'b100011 );
  mux_32 WB_mux(.in0(WB_pass),
                .in1(WB_read),
                .ctl(MemtoReg),
                .result(WB_result));

             


             

  always @(posedge clk) // to show state of registers in pipeline
    begin
      $write("clock %0d", counter);
      $write("  inst=%h", inst);
      $write("  PC   =%h", PC);
      $write(" PCnext=%h", PC_next);
      $write("\n");
      $write("ID  stage  IR=%h", ID_IR);
      if((WB_write_enb==1)&&(WB_rd!=5'b00000))
        begin
          $write("  write=%h", WB_result);
          $write("  into =000000%h", {3'b000,WB_rd});
          $write("               ");
        end
      else
        $write("                                               ");

      $write("  rd=%b", ID_rd);
      $write("\n");
      $write("EX  stage  IR=%h", EX_IR);
      $write("  EX_A =%h", EX_A);
      $write("  EX_B =%h", EX_B);
      $write("  EX_C =%h", EX_C);
      $write(" rd=%b", EX_rd);
      $write("\n");
      $write("EX  stage             ");
      $write("EX_aluB=%h", EX_aluB);
      $write(" EX_res=%h", EX_result);
      $write("\n");
      $write("MEM stage  IR=%h", MEM_IR);
      $write("  addr =%h", MEM_addr);
      $write("  data =%h", MEM_data);
      if(MEMRead==1)
        $write("  read =%h", MEM_read_data);
      else if(MEMWrite==1)
        $write("  wrote=%h", MEM_data);
      else
        $write("                ");

      $write(" rd=%b", MEM_rd);
      $write("\n");
      $write("WB  stage  IR=%h", WB_IR);
      $write("  read =%h", WB_read);
      $write("  pass =%h", WB_pass);
      $write(" result=%h", WB_result);
      $write(" rd=%b", WB_rd);
      $write("\n");
      $write("control RegDst=%b", RegDst);
      $write("  ALUSrc=%b", ALUSrc);
      $write("  MemtoReg=%b", MemtoReg);
      $write("  MEMRead=%b", MEMRead);
      $write("  MEMWrite=%b", MEMWrite);
      $write("  WB_write_enb=%b", WB_write_enb);
      $write("\n");
      $write("\n");         // blank line
      counter = counter+1;
    end
endmodule // pipe2
