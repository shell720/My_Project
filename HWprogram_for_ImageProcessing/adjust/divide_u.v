module div_u(i1, i2, o1);
    parameter   BWI1    = 8;    // dividend bit width, >= 1
    parameter   BWI2    = 8;    // divisor bit width,  >= 1
    parameter   BWO1    = 8;    // quotient bit width, >= 1

    input   [BWI1-1:0]  i1;     // dividend, UNSIGNED
    input   [BWI2-1:0]  i2;     // divisor,  UNSIGNED
    output  [BWO1-1:0]  o1;     // quotient, UNSIGNED

    ////////////////////////
    // declarations
    ////////////////////////
    reg     [0:BWI1-1]  i1_r;
    reg     [0:BWI2-1]  i2_r;
    wire    [0:BWO1-1]  o1_r;
    reg     [BWO1-1:0]  o1_nd;

    wire    [0:BWI2+1]  divisor_x1;
    wire    [0:BWI2+1]  divisor_x2;
    wire    [0:BWI2+1]  divisor_x3;

    reg     [0:BWI1-1]  dividend_sft;
    reg     [0:BWI1-1]  quotient;   // internal quotient
    reg     [0:BWI2+1]  remainder;
    reg     [0:BWI2+2]  subst_x1;
    reg     [0:BWI2+2]  subst_x2;
    reg     [0:BWI2+2]  subst_x3;

    integer I;

    //-------> to avoid synthesizer/simulator error
    parameter   BWI1_CONST2     = (BWI1 >= 3) ? 2 : 0;
    parameter   BWI1_CONST1     = (BWI1 >= 2) ? 1 : 0;
    parameter   BWI1_MINUS_3    = (BWI1 >= 3) ? (BWI1 - 3) : 0;
    parameter   BWI1_MINUS_2    = (BWI1 >= 2) ? (BWI1 - 2) : 0;
    parameter   BWI1_MINUS_1    = (BWI1 >= 1) ? (BWI1 - 1) : 0;
    parameter   BWI1_MINUS_BWO1 = (BWO1 < BWI1) ? (BWI1 - BWO1) : 0;
    parameter   BWO1_MINUS_BWI1 = (BWO1 > BWI1) ? (BWO1 - BWI1) : 1;
    //-------< to avoid synthesizer/simulator error

    ////////////////////////
    // PI
    ////////////////////////
    always @(i1) begin
        for (I = 0; I < BWI1; I = I + 1) begin
            i1_r[I] <= i1[BWI1 - 1 - I];
        end
    end

    always @(i2) begin
        for (I = 0; I < BWI2; I = I + 1) begin
            i2_r[I] <= i2[BWI2 - 1 - I];
        end
    end

    assign  divisor_x1  = {2'b00, i2_r};            // dividend x 1
    assign  divisor_x2  = {1'b0, {i2_r, 1'b0}};     // dividend x 2
    assign  divisor_x3  = divisor_x1 + divisor_x2;  // dividend x 3

    ////////////////////////
    // main loop
    ////////////////////////
    always @(i1_r or divisor_x1 or divisor_x2 or divisor_x3) begin
        dividend_sft    = i1_r;
        remainder       = {(BWI2 + 2){1'b0}};
        quotient        = {(BWI1){1'b0}};

        ////////////////////////
        // rounds (remaining bits > 2)
        ////////////////////////
        for (I = 0; I < (BWI1 - 1) / 2; I = I + 1) begin
            remainder   = {remainder[2:BWI2+1], dividend_sft[0:BWI1_CONST1]};   // shift in
            dividend_sft[0:BWI1_MINUS_3]    = dividend_sft[BWI1_CONST2:BWI1_MINUS_1];
            quotient[0:BWI1_MINUS_3]        = quotient[BWI1_CONST2:BWI1_MINUS_1];

            subst_x1    = {1'b0, remainder} - {1'b0, divisor_x1};
            subst_x2    = {1'b0, remainder} - {1'b0, divisor_x2};
            subst_x3    = {1'b0, remainder} - {1'b0, divisor_x3};

            // select partial quotient
            if (subst_x3[0] == 1'b0 || subst_x2[0] == 1'b0) begin
                if (subst_x3[0] == 1'b0) begin  // select x3
                    quotient[BWI1_MINUS_2:BWI1_MINUS_1] = 2'b11;
                    remainder   = subst_x3[1:BWI2+2];
                end else begin                  // select x2
                    quotient[BWI1_MINUS_2:BWI1_MINUS_1] = 2'b10;
                    remainder   = subst_x2[1:BWI2+2];
                end
            end else begin
                if (subst_x1[0] == 1'b0) begin  // select x1
                    quotient[BWI1_MINUS_2:BWI1_MINUS_1] = 2'b01;
                    remainder   = subst_x1[1:BWI2+2];
                end else begin                  // select x0
                    quotient[BWI1_MINUS_2:BWI1_MINUS_1] = 2'b00;
                end
            end // end of if
        end // end of for

        ////////////////////////
        // final round (remaining bits <= 2)
        ////////////////////////
        if ((BWI1 % 2) == 0) begin      // 2-bit remaining
            if (BWI1 == 2) begin
                remainder   = dividend_sft[0:BWI1_CONST1];
            end else begin
                remainder   = {remainder[2:BWI2+1], dividend_sft[0:BWI1_CONST1]};   // shift in
                quotient[0:BWI1_MINUS_3]    = quotient[BWI1_CONST2:BWI1_MINUS_1];
            end
        end else begin                  // 1-bit remaining
            if (BWI1 == 1) begin
                remainder   = dividend_sft[0];
            end else begin
                remainder   = {remainder[1:BWI2+1], dividend_sft[0]};   // shift in
                quotient[0:BWI1_MINUS_2]    = quotient[BWI1_CONST1:BWI1_MINUS_1];
            end
        end // end of if

        subst_x1    = {1'b0, remainder} - {1'b0, divisor_x1};
        subst_x2    = {1'b0, remainder} - {1'b0, divisor_x2};
        subst_x3    = {1'b0, remainder} - {1'b0, divisor_x3};

        // select partial quotient
        if ((BWI1 % 2) == 0
                && (subst_x3[0] == 1'b0 || subst_x2[0] == 1'b0)) begin
            if (subst_x3[0] == 1'b0) begin  // select x3
                quotient[BWI1_MINUS_2:BWI1_MINUS_1] = 2'b11;
            end else begin                  // select x2
                quotient[BWI1_MINUS_2:BWI1_MINUS_1] = 2'b10;
            end
        end else begin
            if (subst_x1[0] == 1'b0) begin  // select x1
                if ((BWI1 % 2) == 0) begin
                    quotient[BWI1_MINUS_2:BWI1_MINUS_2] = 1'b0;
                end
                quotient[BWI1-1:BWI1-1] = 1'b1;
            end else begin                  // select x0
                if ((BWI1 % 2) == 0) begin
                    quotient[BWI1_MINUS_2:BWI1_MINUS_2] = 1'b0;
                end
                quotient[BWI1-1:BWI1-1] = 1'b0;
            end
        end // end of if

    end // end of always

    ////////////////////////
    // PO
    ////////////////////////
    assign  o1_r    = {{(BWO1_MINUS_BWI1){1'b0}}, quotient[BWI1_MINUS_BWO1:BWI1-1]};

    always @(o1_r) begin
        for (I = 0; I < BWO1; I = I + 1) begin
            o1_nd[I]    <= o1_r[BWO1 - 1 - I];
        end
    end

    assign  o1      = o1_nd;

endmodule
