`define N 10
`define M 12

module top(
	input		clk,
	input		srst_n,
	input		enable,
	input		mode,
	input  [`N:0]  dct11, dct12, dct13, dct14, dct15, dct16, dct17, dct18, 
	input  [`N:0]  dct21, dct22, dct23, dct24, dct25, dct26, dct27, dct28,
	input  [`N:0]  dct31, dct32, dct33, dct34, dct35, dct36, dct37, dct38,
	input  [`N:0]  dct41, dct42, dct43, dct44, dct45, dct46, dct47, dct48, 
	input  [`N:0]  dct51, dct52, dct53, dct54, dct55, dct56, dct57, dct58,
	input  [`N:0]  dct61, dct62, dct63, dct64, dct65, dct66, dct67, dct68,
	input  [`N:0]  dct71, dct72, dct73, dct74, dct75, dct76, dct77, dct78,
	input  [`N:0]  dct81, dct82, dct83, dct84, dct85, dct86, dct87, dct88,
	output vaild,
	output  [`N:0] DC,
	output  [32-1:0] R,
	output  [32-1:0] L,
	output  [32-1:0] F,
	output  [10-1:0] sram_waddr,
    output  [107-1:0] sram_wdata,
    output  wen
);

wire  [`N:0]  q11, q12, q13, q14, q15, q16, q17, q18, q21, q22, q23, q24;
wire  [`N:0]  q25, q26, q27, q28, q31, q32, q33, q34, q35, q36, q37, q38;
wire  [`N:0]  q41, q42, q43, q44, q45, q46, q47, q48, q51, q52, q53, q54;
wire  [`N:0]  q55, q56, q57, q58, q61, q62, q63, q64, q65, q66, q67, q68;
wire  [`N:0]  q71, q72, q73, q74, q75, q76, q77, q78, q81, q82, q83, q84;
wire  [`N:0]  q85, q86, q87, q88;
wire vaild_1;

quantizer q1(
    .clk(clk), 
    .srst_n(srst_n),
    .enable(enable),
    .mode(mode),
    .dct11(dct11),
    .dct12(dct12),
    .dct13(dct13),
    .dct14(dct14),
    .dct15(dct15),
    .dct16(dct16),
    .dct17(dct17),
    .dct18(dct18),
    .dct21(dct21),
    .dct22(dct22),
    .dct23(dct23),
    .dct24(dct24),
    .dct25(dct25),
    .dct26(dct26),
    .dct27(dct27),
    .dct28(dct28),
    .dct31(dct31),
    .dct32(dct32),
    .dct33(dct33),
    .dct34(dct34),
    .dct35(dct35),
    .dct36(dct36),
    .dct37(dct37),
    .dct38(dct38),
    .dct41(dct41),
    .dct42(dct42),
    .dct43(dct43),
    .dct44(dct44),
    .dct45(dct45),
    .dct46(dct46),
    .dct47(dct47),
    .dct48(dct48),
    .dct51(dct51),
    .dct52(dct52),
    .dct53(dct53),
    .dct54(dct54),
    .dct55(dct55),
    .dct56(dct56),
    .dct57(dct57),
    .dct58(dct58),
    .dct61(dct61),
    .dct62(dct62),
    .dct63(dct63),
    .dct64(dct64),
    .dct65(dct65),
    .dct66(dct66),
    .dct67(dct67),
    .dct68(dct68),
    .dct71(dct71),
    .dct72(dct72),
    .dct73(dct73),
    .dct74(dct74),
    .dct75(dct75),
    .dct76(dct76),
    .dct77(dct77),
    .dct78(dct78),
    .dct81(dct81),
    .dct82(dct82),
    .dct83(dct83),
    .dct84(dct84),
    .dct85(dct85),
    .dct86(dct86),
    .dct87(dct87),
    .dct88(dct88),
    .q11(q11),
    .q12(q12),
    .q13(q13),
    .q14(q14),
    .q15(q15),
    .q16(q16),
    .q17(q17),
    .q18(q18),
    .q21(q21),
    .q22(q22),
    .q23(q23),
    .q24(q24),
    .q25(q25),
    .q26(q26),
    .q27(q27),
    .q28(q28),
    .q31(q31),
    .q32(q32),
    .q33(q33),
    .q34(q34),
    .q35(q35),
    .q36(q36),
    .q37(q37),
    .q38(q38),
    .q41(q41),
    .q42(q42),
    .q43(q43),
    .q44(q44),
    .q45(q45),
    .q46(q46),
    .q47(q47),
    .q48(q48),
    .q51(q51),
    .q52(q52),
    .q53(q53),
    .q54(q54),
    .q55(q55),
    .q56(q56),
    .q57(q57),
    .q58(q58),
    .q61(q61),
    .q62(q62),
    .q63(q63),
    .q64(q64),
    .q65(q65),
    .q66(q66),
    .q67(q67),
    .q68(q68),
    .q71(q71),
    .q72(q72),
    .q73(q73),
    .q74(q74),
    .q75(q75),
    .q76(q76),
    .q77(q77),
    .q78(q78),
    .q81(q81),
    .q82(q82),
    .q83(q83),
    .q84(q84),
    .q85(q85),
    .q86(q86),
    .q87(q87),
    .q88(q88),
    .vaild(vaild_1)
);


RLC e1(
	.clk(clk), 
    .srst_n(srst_n),
    .q11(q11),
    .q12(q12),
    .q13(q13),
    .q14(q14),
    .q15(q15),
    .q16(q16),
    .q17(q17),
    .q18(q18),
    .q21(q21),
    .q22(q22),
    .q23(q23),
    .q24(q24),
    .q25(q25),
    .q26(q26),
    .q27(q27),
    .q28(q28),
    .q31(q31),
    .q32(q32),
    .q33(q33),
    .q34(q34),
    .q35(q35),
    .q36(q36),
    .q37(q37),
    .q38(q38),
    .q41(q41),
    .q42(q42),
    .q43(q43),
    .q44(q44),
    .q45(q45),
    .q46(q46),
    .q47(q47),
    .q48(q48),
    .q51(q51),
    .q52(q52),
    .q53(q53),
    .q54(q54),
    .q55(q55),
    .q56(q56),
    .q57(q57),
    .q58(q58),
    .q61(q61),
    .q62(q62),
    .q63(q63),
    .q64(q64),
    .q65(q65),
    .q66(q66),
    .q67(q67),
    .q68(q68),
    .q71(q71),
    .q72(q72),
    .q73(q73),
    .q74(q74),
    .q75(q75),
    .q76(q76),
    .q77(q77),
    .q78(q78),
    .q81(q81),
    .q82(q82),
    .q83(q83),
    .q84(q84),
    .q85(q85),
    .q86(q86),
    .q87(q87),
    .q88(q88),
    .enable(vaild_1),
	.DC_reg(DC),
	.R_reg(R),
	.L_reg(L),
	.F_reg(F),
	.sram_waddr(sram_waddr),
	.sram_wdata(sram_wdata),
	.wen(wen),
	.vaild(vaild)
);


endmodule