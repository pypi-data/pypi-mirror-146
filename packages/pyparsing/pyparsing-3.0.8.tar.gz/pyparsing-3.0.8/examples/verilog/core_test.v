`timescale 100ps/10ps
/* Core Tester */
// Author Andrew Laffely
// Last modified: 12 Feb 03

module core_test;

reg gclock, reset, hold;
wire [2:0] in_ready, out_ready;
wire [31:0] data_in, data_out;
reg [31:0]  temp, temp2;
reg [32:0] data_to_core;
wire [32:0] data_from_core; 
wire read, write;   
wire [1:0] in_addr, out_addr;
reg [1:0] to_addr, from_addr;
reg valid_next;
wire valid_back;
reg start, start2;
integer count, fp, fpin;

/************************** INTERCONNECT ****************************/
in_port IN_PORT_TILE1(gclock, reset, to_addr, data_to_core, in_addr, 
			read, data_in, valid_back, in_ready);
out_port OUT_PORT_TILE1(gclock, reset, from_addr, data_out, out_addr, 
			write, valid_next, data_from_core, out_ready);
/************************** END INTERCONNECT *************************/

/***********************************CORE*****************************/
adder_core CORE_TILE1(reset, hold, in_ready, out_ready, data_in, data_out, 
			read, write, in_addr, out_addr);
/*********************************END CORE***************************/

/********************* TEST BENCH ******************************/
initial
begin
	gclock = 1'b0;
	forever #10 gclock = ~gclock;
end
initial
begin
	count=0;
	start=0; start2=0;
	fp=$fopen("results.dat");  //open a file pointer	
	fpin=$fopen("inputs.dat");  //open a file pointer
	reset = 1'b1;
	hold = 1'b0;
	data_to_core[32]=0;
	temp=32'h00000000;
	temp2=32'h00000000;
	data_to_core[31:0]=32'h00000000;
	valid_next=0;
	to_addr=2'b00;
	from_addr=2'b00;
	#2 reset = 1'b0;
	#26 start=1;
	#4000 $fclose(fp);
	$fclose(fpin);
	$finish;
end

always @ (posedge gclock)
  begin
	count=count+1;
	//Inputs
	to_addr[0] = ~to_addr[0];
	if((!valid_back)&&(start))
	  begin
		#1 if (!to_addr[0])
		  begin
			data_to_core={1'b1,temp};
			temp=temp+1;
			$fdisplay(fpin, "Cycle=%d: InputA=%h",count,data_to_core);
			start2=1;	
		  end
		else 
		  begin
		    if (start2)
		      begin
			data_to_core={1'b1,temp2};
			temp2=temp2+256;
			$fdisplay(fpin, "Cycle=%d: InputB=%h",count,data_to_core);	
		      end
		  end
	  end
	//Output
	if (from_addr==2'b00)
		from_addr=2'b11;
	else
		from_addr=2'b00;
	if (data_from_core[32])
		$fdisplay(fp, "Cycle = %d: Output = %h",count,data_from_core);
  end
endmodule
