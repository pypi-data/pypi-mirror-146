module count_bits8(I, C);

   input   [7:0]  I;
   output  [5:0]  C;

    assign         C = (I[0] +  I[1] +  I[2] +  I[3]) +
                   ( I[4] +  I[5] +  I[6] +  I[7] );

endmodule