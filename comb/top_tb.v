`timescale 1ns/100ps
`define End_CYCLE 1000

`define Golden_RGB "SRAM_RGB.dat"
`define Golden_YCbCr "SRAM_YCbCr.dat"
`define Golden_DCT "SRAM_DCT.dat"
`define Golden_Q "SRAM_Q.dat"
`define CYCLE 10
`define pat_n 10
module top_tb;
//====== nWave ================
initial begin
    $fsdbDumpfile("top.fsdb");
    $fsdbDumpvars;
    $fsdbDumpMDA();
end

//====== module I/O =====
integer p;
reg clk;
reg rst_n;
reg enable;
wire [511:0] data_read;
wire [511:0] data_write;
wire [11-1:0] sram_raddr;
wire [11-1:0] sram_waddr;
wire wen;
wire valid;

//====== clock generation =====
initial begin : proc_system
    clk = 0; //
    rst_n = 1;
    // system reset
    #(`CYCLE) rst_n = 0;
    #(`CYCLE) rst_n = 1;
    #(`CYCLE * 10000000) $finish;
end
always #(`CYCLE/2) clk=~clk;
//====== top connection =====
top top(
    .clk(clk),
    .rst_n(rst_n),
    .enable(enable),
    .data_read(data_read),
    .sram_raddr(sram_raddr),
    .sram_waddr(sram_waddr),
    .data_write(data_write),
    .wen(wen),
    .valid(valid)
);

//====== SRAM ===========
sram_1728x512b sram_1728x512b(
.clk(clk),
.csb(1'b0),
.wsb(wen),
.wdata(data_write), 
.waddr(sram_waddr), 
.raddr(sram_raddr), 
.rdata(data_read)
);

//====== LOAD PATTERN =====
reg [511:0] RGB_pattern [0:1728-1];
reg [511:0] YCbCr_pattern [0:1728-1];
reg [704-1:0] DCT_pattern [0:1728-1];
reg [704-1:0] Q_pattern [0:1728-1];

initial begin
    $readmemb(`Golden_RGB, RGB_pattern);
    $readmemb(`Golden_YCbCr, YCbCr_pattern);
    $readmemb(`Golden_DCT, DCT_pattern);
    $readmemb(`Golden_Q, Q_pattern);
end

//====== LOAD SRAM ========
initial begin
    load_RGB;
end
integer m;
task load_RGB;
    begin
        for(m=0; m<1728; m=m+1) begin
            sram_1728x512b.load_param(m, RGB_pattern[m]);
        end
    end
endtask



//======== FEED ===========
initial begin
    wait(rst_n == 0);
    wait(rst_n == 1);
    enable = 1;
    // wait(valid);
    // enable = 0;
    #(`CYCLE*10000000) $finish;
end    
//========= OUTPUT CONCAT ===
wire [704-1:0] dct;
integer i;
// assign dct = {dct00, dct01, dct02, dct03, dct04, dct05, dct06, dct07, dct10, dct11, dct12, dct13, dct14, dct15, dct16, dct17, dct20, dct21, dct22, dct23, dct24, dct25, dct26, dct27, dct30, dct31, dct32, dct33, dct34, dct35, dct36, dct37, dct40, dct41, dct42, dct43, dct44, dct45, dct46, dct47, dct50, dct51, dct52, dct53, dct54, dct55, dct56, dct57, dct60, dct61, dct62, dct63, dct64, dct65, dct66, dct67, dct70, dct71, dct72, dct73, dct74, dct75, dct76, dct77};
//======== TEST ===========
integer f, j, k, l, p,r;
integer index;

initial begin
    wait(top.valid_dct);
    for(l=0; l<3; l=l+1) begin
        for(j=0; j<1728; j=j+3) begin
            @(negedge clk);
            index = l+j;
            // $display("%d, %d",l , j);
            if (top.dct !== DCT_pattern[index]) begin
                $display("fuck! %d line \n", index);
                $finish;
                // $display("GOL : %b \n",DCT_pattern[index]);
                // $display("RTL : %b \n",top.dct);
    //                $display("%4d, %4d, %4d, %4d, %4d, %4d, %4d, %4d, %4d, %4d, %4d, %4d, %4d, %4d, %4d, %4d, %4d, %4d, %4d, %4d, %4d, %4d, %4d, %4d, %4d, %4d, %4d, %4d, %4d, %4d, %4d, %4d, %4d, %4d, %4d, %4d, %4d, %4d, %4d, %4d, %4d, %4d, %4d, %4d, %4d, %4d, %4d, %4d, %4d, %4d, %4d, %4d, %4d, %4d, %4d, %4d, %4d, %4d, %4d, %4d, %4d, %4d", dct00, dct01, dct02, dct03, dct04, dct05, dct06, dct07, dct10, dct11, dct12, dct13, dct14, dct15, dct16, dct17, dct20, dct21, dct22, dct23, dct24, dct25, dct26, dct27, dct30, dct31, dct32, dct33, dct34, dct35, dct36, dct37, dct40, dct41, dct42, dct43, dct44, dct45, dct46, dct47, dct50, dct51, dct52, dct53, dct54, dct55, dct56, dct57, dct60, dct61, dct62, dct63, dct64, dct65, dct66, dct67, dct70, dct71, dct72, dct73, dct74, dct75, dct76, dct77);
            end
            else begin
                // $write("\nDCT pattern %3d: \n", index);
                // $write("%3d%3d%3d%3d%3d%3d%3d%3d\n", $signed(top.dct00), $signed(top.dct01), $signed(top.dct02), $signed(top.dct03), $signed(top.dct04), $signed(top.dct05), $signed(top.dct06), $signed(top.dct07));
                // $write("%3d%3d%3d%3d%3d%3d%3d%3d\n", $signed(top.dct10), $signed(top.dct11), $signed(top.dct12), $signed(top.dct13), $signed(top.dct14), $signed(top.dct15), $signed(top.dct16), $signed(top.dct17));
                // $write("%3d%3d%3d%3d%3d%3d%3d%3d\n", $signed(top.dct20), $signed(top.dct21), $signed(top.dct22), $signed(top.dct23), $signed(top.dct24), $signed(top.dct25), $signed(top.dct26), $signed(top.dct27));
                // $write("%3d%3d%3d%3d%3d%3d%3d%3d\n", $signed(top.dct30), $signed(top.dct31), $signed(top.dct32), $signed(top.dct33), $signed(top.dct34), $signed(top.dct35), $signed(top.dct36), $signed(top.dct37));
                // $write("%3d%3d%3d%3d%3d%3d%3d%3d\n", $signed(top.dct40), $signed(top.dct41), $signed(top.dct42), $signed(top.dct43), $signed(top.dct44), $signed(top.dct45), $signed(top.dct46), $signed(top.dct47));
                // $write("%3d%3d%3d%3d%3d%3d%3d%3d\n", $signed(top.dct50), $signed(top.dct51), $signed(top.dct52), $signed(top.dct53), $signed(top.dct54), $signed(top.dct55), $signed(top.dct56), $signed(top.dct57));
                // $write("%3d%3d%3d%3d%3d%3d%3d%3d\n", $signed(top.dct60), $signed(top.dct61), $signed(top.dct62), $signed(top.dct63), $signed(top.dct64), $signed(top.dct65), $signed(top.dct66), $signed(top.dct67));
                // $write("%3d%3d%3d%3d%3d%3d%3d%3d\n", $signed(top.dct70), $signed(top.dct71), $signed(top.dct72), $signed(top.dct73), $signed(top.dct74), $signed(top.dct75), $signed(top.dct76), $signed(top.dct77));

            end
        end
        if(l==0) $display("pass Y");
        if(l==1) $display("pass Cb");
        if(l==2) $display("pass Cr");
    end
    $display("pass all!");
    $finish;
end

initial begin
  wait(rst_n==0);
  wait(rst_n==1);
  #(`CYCLE*2);
  wait(top.valid_quan);

  for(p=0; p<3; p=p+1) begin
        for(r=0; r<1728; r=r+3) begin
            @(negedge clk);
    $write("\npattern %3d:", p+r);
    if (Q_pattern [p+r] == {top.q11, top.q12, top.q13, top.q14, top.q15, top.q16, top.q17, top.q18,
                          top.q21, top.q22, top.q23, top.q24, top.q25, top.q26, top.q27, top.q28,
                          top.q31, top.q32, top.q33, top.q34, top.q35, top.q36, top.q37, top.q38,
                          top.q41, top.q42, top.q43, top.q44, top.q45, top.q46, top.q47, top.q48,
                          top.q51, top.q52, top.q53, top.q54, top.q55, top.q56, top.q57, top.q58,
                          top.q61, top.q62, top.q63, top.q64, top.q65, top.q66, top.q67, top.q68,
                          top.q71, top.q72, top.q73, top.q74, top.q75, top.q76, top.q77, top.q78,
                          top.q81, top.q82, top.q83, top.q84, top.q85, top.q86, top.q87, top.q88}) begin
      $write(" pass!");
    end else begin
      $display(" fail!");
      $write("\nerror pattern %3d: \n", p);
      $write("%3d%3d%3d%3d%3d%3d%3d%3d\n", $signed(top.q11), $signed(top.q12), $signed(top.q13), $signed(top.q14), $signed(top.q15), $signed(top.q16), $signed(top.q17), $signed(top.q18));
      $write("%3d%3d%3d%3d%3d%3d%3d%3d\n", $signed(top.q21), $signed(top.q22), $signed(top.q23), $signed(top.q24), $signed(top.q25), $signed(top.q26), $signed(top.q27), $signed(top.q28));
      $write("%3d%3d%3d%3d%3d%3d%3d%3d\n", $signed(top.q31), $signed(top.q32), $signed(top.q33), $signed(top.q34), $signed(top.q35), $signed(top.q36), $signed(top.q37), $signed(top.q38));
      $write("%3d%3d%3d%3d%3d%3d%3d%3d\n", $signed(top.q41), $signed(top.q42), $signed(top.q43), $signed(top.q44), $signed(top.q45), $signed(top.q46), $signed(top.q47), $signed(top.q48));
      $write("%3d%3d%3d%3d%3d%3d%3d%3d\n", $signed(top.q51), $signed(top.q52), $signed(top.q53), $signed(top.q54), $signed(top.q55), $signed(top.q56), $signed(top.q57), $signed(top.q58));
      $write("%3d%3d%3d%3d%3d%3d%3d%3d\n", $signed(top.q61), $signed(top.q62), $signed(top.q63), $signed(top.q64), $signed(top.q65), $signed(top.q66), $signed(top.q67), $signed(top.q68));
      $write("%3d%3d%3d%3d%3d%3d%3d%3d\n", $signed(top.q71), $signed(top.q72), $signed(top.q73), $signed(top.q74), $signed(top.q75), $signed(top.q76), $signed(top.q77), $signed(top.q78));
      $write("%3d%3d%3d%3d%3d%3d%3d%3d\n", $signed(top.q81), $signed(top.q82), $signed(top.q83), $signed(top.q84), $signed(top.q85), $signed(top.q86), $signed(top.q87), $signed(top.q88));
    end
  end
  end
end

endmodule