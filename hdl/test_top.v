`timescale 1ns/1ps
`define CYCLE 10
`define N 10
`define pat_n 1728

module test_top;


/**************************  instantiation *************************/
integer i, j ,k, m,p,r;
reg		clk;
reg		srst_n;
reg		enable;
reg   mode;
reg  [`N:0]  dct11, dct12, dct13, dct14, dct15, dct16, dct17, dct18, dct21, dct22, dct23, dct24;
reg  [`N:0]  dct25, dct26, dct27, dct28, dct31, dct32, dct33, dct34, dct35, dct36, dct37, dct38;
reg  [`N:0]  dct41, dct42, dct43, dct44, dct45, dct46, dct47, dct48, dct51, dct52, dct53, dct54;
reg  [`N:0]  dct55, dct56, dct57, dct58, dct61, dct62, dct63, dct64, dct65, dct66, dct67, dct68;
reg  [`N:0]  dct71, dct72, dct73, dct74, dct75, dct76, dct77, dct78, dct81, dct82, dct83, dct84;
reg  [`N:0]  dct85, dct86, dct87, dct88;

reg  [`N:0] dct_input [0:63];

wire [`N:0] DC;
wire		vaild;
wire [24-1:0] R;
wire [32-1:0] L;
wire [32-1:0] F;

wire [99-1:0] data_read;
wire [99-1:0] sram_wdata;
wire [11-1:0] sram_raddr;
wire [11-1:0] sram_waddr;
wire wen;

top t1(
    .clk(clk), 
    .srst_n(srst_n),
    .enable(enable),
    .mode(mode),
    .dct11(dct_input[0]),
    .dct12(dct_input[1]),
    .dct13(dct_input[2]),
    .dct14(dct_input[3]),
    .dct15(dct_input[4]),
    .dct16(dct_input[5]),
    .dct17(dct_input[6]),
    .dct18(dct_input[7]),
    .dct21(dct_input[8]),
    .dct22(dct_input[9]),
    .dct23(dct_input[10]),
    .dct24(dct_input[11]),
    .dct25(dct_input[12]),
    .dct26(dct_input[13]),
    .dct27(dct_input[14]),
    .dct28(dct_input[15]),
    .dct31(dct_input[16]),
    .dct32(dct_input[17]),
    .dct33(dct_input[18]),
    .dct34(dct_input[19]),
    .dct35(dct_input[20]),
    .dct36(dct_input[21]),
    .dct37(dct_input[22]),
    .dct38(dct_input[23]),
    .dct41(dct_input[24]),
    .dct42(dct_input[25]),
    .dct43(dct_input[26]),
    .dct44(dct_input[27]),
    .dct45(dct_input[28]),
    .dct46(dct_input[29]),
    .dct47(dct_input[30]),
    .dct48(dct_input[31]),
    .dct51(dct_input[32]),
    .dct52(dct_input[33]),
    .dct53(dct_input[34]),
    .dct54(dct_input[35]),
    .dct55(dct_input[36]),
    .dct56(dct_input[37]),
    .dct57(dct_input[38]),
    .dct58(dct_input[39]),
    .dct61(dct_input[40]),
    .dct62(dct_input[41]),
    .dct63(dct_input[42]),
    .dct64(dct_input[43]),
    .dct65(dct_input[44]),
    .dct66(dct_input[45]),
    .dct67(dct_input[46]),
    .dct68(dct_input[47]),
    .dct71(dct_input[48]),
    .dct72(dct_input[49]),
    .dct73(dct_input[50]),
    .dct74(dct_input[51]),
    .dct75(dct_input[52]),
    .dct76(dct_input[53]),
    .dct77(dct_input[54]),
    .dct78(dct_input[55]),
    .dct81(dct_input[56]),
    .dct82(dct_input[57]),
    .dct83(dct_input[58]),
    .dct84(dct_input[59]),
    .dct85(dct_input[60]),
    .dct86(dct_input[61]),
    .dct87(dct_input[62]),
    .dct88(dct_input[63]),
    .vaild(vaild),
    .DC(DC),
    .R(R),
	  .L(L),
	  .F(F),
    .sram_waddr(sram_waddr),
	.sram_wdata(sram_wdata),
	.wen(wen)
);

sram_1728x99b sram_1728x99b(
  .clk(clk),
  .csb(1'b0),
  .wsb(wen),
  .wdata(sram_wdata), 
  .waddr(sram_waddr), 
  .raddr(sram_raddr), 
  .rdata(data_read)
);

/********************************************************************************/



/********************************** Waveform ***********************************/
initial begin
    $fsdbDumpfile("test_top.fsdb");
    $fsdbDumpvars("+mda");
end
/*******************************************************************************/



/******** Read pattern from dctin/ with $readmemb() *********/
reg [704-1:0] DCT_pattern [0:1728-1];
reg [704-1:0] Q_pattern [0:1728-1];
reg [99-1:0] F_pattern [0:1728-1];

initial begin
  $readmemb("./dctin/SRAM_DCT.dat", DCT_pattern);
  $readmemb("./dctin/SRAM_Q.dat", Q_pattern);
  $readmemb("./dctin/SRAM_F.dat", F_pattern);
end
/*******************************************************************************/



/****************************** clock generation *******************************/
initial begin
    clk = 0;
    while(1) #(`CYCLE/2) clk = ~clk;
    #(`CYCLE*10000); $finish;
end
/*******************************************************************************/

/********************************* feed input **********************************/
initial begin
  srst_n = 1;
  enable = 0;
  // system reset
  #(`CYCLE) srst_n = 0;
  #(`CYCLE) srst_n = 1;
end

initial begin
  wait(srst_n == 0);
  wait(srst_n == 1);
  enable = 1;
  mode = 0;

for (m = 0; m < `pat_n; m = m + 1) begin
  @(negedge clk);
  for (i = 0; i < 64; i = i + 1) dct_input[i] = DCT_pattern[m][(703-i*11) -: 11];
end

end

/*******************************************************************************/



/******************************** check output  ********************************/
// * If output is incorrect, print it is wrong and finish the simulation
// * If all code_out is correct, print congratulations and finish the simulation
// initial begin
//   wait(srst_n==0);
//   wait(srst_n==1);
//   #(`CYCLE*2);
//   wait(vaild);
  
//   for (j = 0; j < `pat_n; j = j + 1) begin
//     @(negedge clk);
//     if (F_pattern[j] == {DC,R,L,F}) $display(" pass F");
//     else begin
//       $display("Fail F");
//       $finish;
//     end
//       // $write("DC: %3d", $signed(DC));
//       // $write("\nR: %h\n", R);
//       // $write("L: %h\n", L);
//       // $write("F: %h\n", F);
//   end
// $finish;
// end
/*******************************************************************************/


initial begin
  wait(srst_n==0);
  wait(srst_n==1);
  #(`CYCLE*2);
  wait(top.vaild_1);

  for (p = 0; p < `pat_n; p = p + 1) begin
    @(negedge clk);
    $write("\npattern %3d:", p);
    if (Q_pattern [p] == {top.q11, top.q12, top.q13, top.q14, top.q15, top.q16, top.q17, top.q18,
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
  enable = 0;
  
end

//
initial begin
  wait(srst_n==0);
  wait(srst_n==1);
  #(`CYCLE*2);
  wait(vaild);
  for (r = 0; r < `pat_n; r = r + 1) begin
    @(negedge clk);
    if (F_pattern[r] == sram_1728x99b.mem[r]) $display(" pass F");
    else begin
      $display("Fail F");
      $finish;
    end
      // $write("DC: %3d", $signed(DC));
      // $write("\nR: %h\n", R);
      // $write("L: %h\n", L);
      // $write("F: %h\n", F);
  end
  
$finish;
end
endmodule


