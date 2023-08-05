module count2bit(cnt, clk, res_, en);
    output [1:0] cnt; // the counter value
    reg [1:0] cnt;
    input clk, res_, en;
    reg [1:0] next_cnt; // the next state
    
    parameter S0=2'b00, // the states
    S1=2'b01,
    S2=2'b10,
    S3=2'b11;
    
    always @(posedge clk or negedge res_)
        if (res_ == 1'b0)
            cnt <= 2'b00;
        else
            cnt <= next_cnt;
    
    always @(en or cnt)
        case (cnt)
            S0: if (en == 1'b1) // full if-then-else implem.
                    next_cnt = S1;
                else
                    next_cnt = S0;
            S1: if (en == 1'b1) // the else path is not needed
                    next_cnt = S2;
            S2: next_cnt = (en == 1'b1) ? S3 : S2; // shorter
            S3: next_cnt = (en) ? S0 : S3; // even shorter
        endcase
endmodule
