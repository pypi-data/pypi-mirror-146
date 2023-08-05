primitive multi21(o, a, b, s);
output o;
input a, b, s;
initial o = x;
table
// a b s : o
   0 ? 0 : 0;
   1 ? 0 : 1;
   ? 0 1 : 0;
   ? 1 1 : 1;
endtable
endprimitive
 