/* Input port */
// Author Andrew Laffely
// Last modified: 12 Feb 03
//!!!!!!!!!!!!!!!! DO NOT CHANGE THIS FILE !!!!!!!!!!!!!!!!!!!!!
module in_port (gclock, reset, i_addr, data_in, c_addr, c_read, c_data, valid_back, ready);

input gclock, reset;
input [1:0] i_addr;      // buffer address requested by ccm
input [1:0] c_addr;      // buffer address requested by core
input [32:0] data_in;    // the data to be buffered from interface
input c_read;	         // read singal from core

output valid_back;       // flow control bit sent upstream to block data
output [31:0] c_data;    // the data sent to the core
output [2:0] ready;      // flow control, port "ready" signal, sent to core
reg valid_back;
reg [31:0] c_data;
reg [2:0] ready;   

reg [5:0] valid;         // contains the valid bits of the data in the port
reg [31:0] data [5:0];   // the data in the cdm
reg [2:0] i_addr_hold;   // hold the buf addr while evaluating
reg [2:0] c_addr_hold;   // hold the buf addr while evaluating
reg [2:0] i_buf_state, c_buf_state; // first or second buf in each port

reg faketiming;  // Makes level sensitive transitions work properly
initial
begin
	faketiming = 1'b0;
	forever #1 faketiming = ~faketiming;
end

// *********************** INTERCONNECT *********************** //
always @ (posedge gclock)  //interconnect side
begin
  if(!reset)
    begin
      //update valid from last transfer
      if(!(i_addr_hold[2:1] == 2'b11))  
	begin
	  if(!valid_back)
	    begin
		valid[i_addr_hold]=data_in[32];  //glitch set
		if (data_in[32])
		   i_buf_state[i_addr_hold[2:1]]=~i_buf_state[i_addr_hold[2:1]];
	    end
	end
	#1 i_addr_hold = {i_addr,i_buf_state[i_addr]};

	//Send data
	if(i_addr == 2'b11)  //default no data
	  begin
		#1 valid_back = 0;//upstream flow control
	  end
	else
	  begin
	 	#1 valid_back = valid[i_addr_hold];
		 //upstream flow control
	  end
    end
end
// ******************** END INTERCONNECT *********************** //

// *************************** CORE **************************** //
always @ (posedge c_read)
begin
	c_addr_hold = {c_addr, c_buf_state[c_addr]};
end
always @ (negedge c_read) //Core
  begin
    if(!reset)
      begin
	valid[c_addr_hold]=0;  //glitch reset
	c_buf_state[c_addr_hold[2:1]]=~c_buf_state[c_addr_hold[2:1]];
      end
end
// ************************** END CORE ************************* //

always @ (faketiming)
  begin
    if (reset)
      begin
	valid = 4'b0000;
	valid_back = 1'b0;
	i_addr_hold = 3'b111;
	i_buf_state=3'b000;
	c_buf_state=3'b000;
      end
    else
      begin
	ready[0]=valid[c_buf_state[0]];
	ready[1]=valid[c_buf_state[1]];
	ready[2]=valid[c_buf_state[2]];

	// ********************* Interconnect side **************** //
	if (!gclock)
	  begin
		//if valid port # and not blocked store new data in port
		if(!(i_addr_hold[2:1] == 2'b11)&&(!valid_back)) 
		  begin
			data[i_addr_hold] = data_in[31:0];
		  end
	  end
	// ****************** End Interconnect side **************** //

	// *************************** CORE ************************ //
	if (c_read)
	  begin
		c_data = data[c_addr_hold];
	  end
        // ************************ END CORE ********************** //
  end
end

endmodule
