primitive dff(q, clk, d);
output q;
reg q; // storage element
input clk, d;
initial q = 0;
table
// clk d state next
  (01) 0 : ? : 0; // all positive transitions
  (01) 1 : ? : 1;
  (0x) 0 : ? : 0;
  (0x) 1 : ? : 1;
  (x1) 0 : ? : 0;
  (x1) 1 : ? : 1;
  // ignore negative edge
  n    ? : ? : -;
  // ignore data changes on steady clock
  (??) ? : ? : -;
endtable
endprimitive