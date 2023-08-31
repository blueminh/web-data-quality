"""
@Author: Khanh Hung & Tuan Kiet & Minh Anh 
@Status: Completed
"""
import os
import pandas as pd
import numpy as np
from .Borrowings import Borrowings_output
from .Investment_Trading_Securities import Investment_Trading_Securities_output
from .Deposit import Deposits_output
from .Facility import Facility_output
from .Other_Items import Other_Items
from .Issued_Securities import Issued_Securities
from .Securities_Financial_Trans import Securities_Financial_Trans
from .Derivatives import Derivatives_output
from .Off_Balance_Sheet import Off_Balance_Sheet_output
from .Loans_Advances import Loans_Advances
from .Deposits_with_other_banks import Deposits_with_other_banks_output
def set_output_df():
    """
    Create output dataframe

    @Return: output dataframe
    """
    data = {
    "No.": [1, 2, 3, 4, 5, 6, 1, 1.1, 1.2, 2, 2.1, 2.2, 2.3, 3, 4, 4.1, 4.2, 4.3, 5, 6, 7, 1, 2, 3, 4, "", "A", "B-C", ""],
    "Items": ["Total Level 1 Assets", "Total Level 2A Assets", "Total Level 2B Assets", "Adjustment for 40% cap of Level 2A Assets", 
              "Adjustment for 15% cap of Level 2B Assets", "Total HQLA", "Retail deposits and deposits from small business customers, of which:", 
              "Stable deposits", "Less stable deposits", "Unsecured wholesale funding, of which:", 
              "Operational deposits (all counterparties) and deposits in networks of cooperative banks", 
              "Non-operational deposits (all counterparties)", "Unsecured debt", "Secured wholesale funding", "Additional requirements, of which:", 
              "Outflows related to derivative exposures and other collateral requirements", 
              "Outflows related to loss of funding on debt products", "Credit and liquidity facilities", "Other contractual funding obligations", 
              "Other contingent funding obligations", "TOTAL CASH OUTFLOWS", "Secured lending (reverse repos and securities borrowing)", 
              "Inflows from fully performing exposures", "Other cash inflows", "TOTAL CASH INFLOWS","", "Total HQLA", "Total net cash outflows", 
              "Liquidity Coverage Ratio (>=100%)"],
    "Khoản mục": ["Tổng tài sản thanh khoản Cấp 1", "Tổng tài sản thanh khoản Cấp 2A", "Tổng tài sản thanh khoản Cấp 2B", 
                  "Giá trị điều chỉnh theo ngưỡng trần 40% đối với tài sản thanh khoản cấp 2A", 
                  "Giá trị điều chỉnh theo ngưỡng trần 15% đối với tài sản thanh khoản cấp 2B", "Tổng tài sản thanh khoản có chất lượng cao", 
                  "Tiền gửi của khách hàng bán lẻ và khách hàng kinh doanh nhỏ", "Tiền gửi ổn định", "Tiền gửi kém ổn định", 
                  "Nguồn vốn huy động từ bán buôn không bảo đảm, trong đó:", 
                  "Tiền gửi hoạt động (tất cả các đối tác) và tiền gửi trong mạng lưới các ngân hàng hợp tác", 
                  "Tiền gửi không nhằm mục đích hoạt động (tất cả các đối tác)", "Chứng khoán nợ không bảo đảm", "Nguồn vốn huy động từ bán buôn được bảo đảm", 
                  "Các yêu cầu bổ sung, trong đó:", "Các dòng tiền ra từ các trạng thái phái sinh và các yêu cầu về TSBĐ khác", 
                  "Dòng tiền ra từ mất nguồn vốn huy động từ các công cụ nợ", "Các cam kết tín dụng và cam kết thanh khoản", 
                  "Các nghĩa vụ theo hợp đồng khác", "Các nghĩa vụ tài trợ tiềm ẩn khác", "TỔNG DÒNG TIỀN RA", 
                  "Các giao dịch cho vay được bảo đảm (bao gồm các giao dịch reverse repo và cho vay chứng khoán)", 
                  "Dòng tiền vào từ các khoản cho vay tốt (fully performing)", "Các dòng tiền vào khác", "TỔNG DÒNG TIỀN VÀO", 
                  "","Tổng tài sản thanh khoản chất lượng cao", "Tổng dòng tiền ra ròng", "Tỷ lệ đảm bảo khả năng thanh khoản LCR (giới hạn ≥100%)"]
    }
     
    output_df = pd.DataFrame(data)

    new_row = pd.DataFrame({"No.": [""], 
                            "Items": ["Cash outflows"], 
                            "Khoản mục": ["Các dòng tiền ra"]})
    output_df = pd.concat([output_df.iloc[:6], new_row, output_df.iloc[6:]]).reset_index(drop=True)

    new_row2 = pd.DataFrame({"No.": [""], 
                            "Items": ["Cash inflows"], 
                            "Khoản mục": ["Các dòng tiền vào"]})
    output_df = pd.concat([output_df.iloc[:22], new_row2, output_df.iloc[22:]]).reset_index(drop=True)

    output_df["Blank 1"] = np.nan
    output_df["Blank 2"] = np.nan

    return output_df

"""
Calculations:
@Return: the result of the cell in Row x, column Blank 1/2
"""

def calc_investment(df, column_AF, column_AD, condition):
    """
    =SUMIFS('Investment&Trading Securities'!$AF:$AF,'Investment&Trading Securities'!$AD:$AD,"L2A")
    Row 2,3 - blank 1,2
    """
    return df.loc[df[column_AD] == condition, column_AF].sum()

def calc_investment_other_items(investment_df, other_items_df, column_AF, column_AD, condition, cell1, cell2):
    """
    Row 1 - blank 1,2
    """
    sum_investment = investment_df.loc[investment_df[column_AD] == condition, column_AF].sum()
    sum_other_items = other_items_df.loc[cell1, 'Value'] + other_items_df.loc[cell2, 'Value']
    return sum_investment + sum_other_items

def calc_max1(df, R18, R19, R20, Blank):
    """
    Row 4 - Blank 2
    """
    value_G18 = df.loc[R18, Blank]
    value_G19 = df.loc[R19, Blank]
    value_G20 = df.loc[R20, Blank]
    return max(value_G19 + value_G20 - (2/3 * value_G18), value_G20 - (15/85 * (value_G18 + value_G19)), 0)

def calc_max2(df, R18, R19, R20, Blank):
    """
    Row 5 - Blank 2
    """
    value_G18 = df.loc[R18, Blank]
    value_G19 = df.loc[R19, Blank]
    value_G20 = df.loc[R20, Blank]
    return max(value_G20 - (15/85 * (value_G18 + value_G19)), value_G20 - (15/60 * value_G18), 0)

def calc_sum1(df, R_a, R_b, R_c, Blank):
    """
    =SUM(G18:G20)
    Row 6 - Blank 2
    """
    value_a = df.loc[R_a, Blank]
    value_b = df.loc[R_b, Blank]
    value_c = df.loc[R_c, Blank]
    return value_a + value_b + value_c

def calc_sum(df, R26, R27, Blank):
    """
    Row 25 - both Blank 1,2
    """
    value_26 = df.loc[R26, Blank]
    value_27 = df.loc[R27, Blank]
    return value_26 + value_27

def calc_sum2(df, T, Z):
    """ 
    =SUM(SUMIFS(Deposits!Z:Z,Deposits!T:T,{"Retail","Small Business Customer"})) 
    Row 26 - Blank 1
    """ 
    T = 'Retail/Wholesale'
    Z = 'Stable Amount (Principal + Interest)'
    conditions = ['Retail', 'Small Business Customer'] 

    return df.loc[df[T].isin(conditions), Z].sum()

def calc_sum3(df, T, AD):
    """
    =SUM(SUMIFS(Deposits!$AD:$AD,Deposits!$T:$T,{"Retail","Small Business Customer"}))
    Row 26 - Blank 2 
    """
    T = 'Retail/Wholesale'
    AD = 'Stable Run-Off Amount'
    conditions = ['Retail', 'Small Business Customer']
    return df.loc[df[T].isin(conditions), AD].sum()

def calc_sum4(deposits_df, borrowings_df, T_deposits, AA, U_borrowings, H, T_borrowings, I, X):
    """
    =SUM(SUMIFS(Deposits!$AA:$AA,Deposits!$T:$T,{"Retail","Small Business Customer"}))+
    SUM(SUMIFS(Borrowings!$H:$H,Borrowings!$U:$U,{"Retail","Small Business Customer"},Borrowings!$T:$T,"30 or Less"))+
    SUM(SUMIFS(Borrowings!$I:$I,Borrowings!$U:$U,{"Retail","Small Business Customer"},Borrowings!$X:$X,"30 or Less"))

    deposit[AA], borrowing[H], borrowing[I], borrowing[X]
    
    Row 27 - Blank 1 
    """
    conditions = ['Retail', 'Small Business Customer']
    AA = 'Unstable Amount (Principal + Interest)'
    deposit_sum = deposits_df.loc[deposits_df[T_deposits].isin(conditions), AA].sum()
    H = 'Next principal payment Amount'
    I = 'Next Interest Payment Amount'
    X = 'Days To Coupon'

    borrowings_condition = "30 or Less"
    borrowings_sum1 = borrowings_df.loc[(borrowings_df[U_borrowings].isin(conditions)) & (borrowings_df[T_borrowings] == borrowings_condition), H].sum()
    borrowings_sum2 = borrowings_df.loc[(borrowings_df[U_borrowings].isin(conditions)) & (borrowings_df[X] == borrowings_condition), I].sum()

    return deposit_sum + borrowings_sum1 + borrowings_sum2

def calc_sum5(deposits_df, borrowings_df, T_deposits, AE, U_borrowings, Z):
    """
    =SUM(SUMIFS(Deposits!$AE:$AE,Deposits!$T:$T,{"Retail","Small Business Customer"}))+
    SUM(SUMIFS(Borrowings!$Z:$Z,Borrowings!$U:$U,{"Retail","Small Business Customer"}))
    Row 27- Blank 2 
    """
    conditions = ['Retail', 'Small Business Customer']
    AE = 'Unstable Run-Off Amount'
    Z = 'Total Weighted Cash Outflow'

    deposit_sum = deposits_df.loc[deposits_df[T_deposits].isin(conditions), AE].sum()
    borrowings_sum = borrowings_df.loc[borrowings_df[U_borrowings].isin(conditions), Z].sum()

    return deposit_sum + borrowings_sum

def calc_sum6(df, R_a, R_b, R_c, Blank):
    """
    =SUM(F29:F31)
    Row 28 - Blank 1
    """
    value_a = df.loc[R_a, Blank]
    value_b = df.loc[R_b, Blank]
    value_c = df.loc[R_c, Blank]
    return value_a + value_b + value_c

def calc_sum7(df, R_a, R_b, R_c, Blank):
    """
    =SUM(G29:G31)
    Row 28 - Blank 2
    """
    value_a = df.loc[R_a, Blank]
    value_b = df.loc[R_b, Blank]
    value_c = df.loc[R_c, Blank]
    return value_a + value_b + value_c

def calc_sum8(df, S, E, F, R):
    """
    =SUMIFS(Deposits!$E:$E,Deposits!$S:$S,"Operational Deposit")+
    SUMIFS(Deposits!$F:$F,Deposits!$S:$S,"Operational Deposit",Deposits!$R:$R,"30 or Less")
    Row 29 - Blank 1 
    """
    condition1 = "Operational Deposit"
    condition2 = "30 or Less"

    sum1 = df.loc[df[S] == condition1, E].sum()
    sum2 = df.loc[(df[S] == condition1) & (df[R] == condition2), F].sum()

    return sum1 + sum2

def calc_sum9(df, S, AF):
    """
    =SUMIFS(Deposits!$AF:$AF,Deposits!$S:$S,"Operational Deposit")
    Row 29 - Blank 2
    """
    condition = "Operational Deposit"
    return df.loc[df[S] == condition, AF].sum()

def calc_sum10(deposits_df, borrowings_df, output_df, E, F_deposits, R, H, T_borrowings, I, X, F_row1, F_row2, F_row3):
    """
   =SUM(Deposits!$E:$E)+SUMIFS(Deposits!$F:$F,Deposits!$R:$R,"30 or Less")+SUMIFS(Borrowings!$H:$H,Borrowings!$T:$T,"30 or Less")
   +SUMIFS(Borrowings!$I:$I,Borrowings!$X:$X,"30 or Less")-$F$26-$F$27-$F$29

    Row 30 - Blank 1
    """
    condition = "30 or Less"

    sum1 = deposits_df[E].sum()
    sum2 = deposits_df[deposits_df[R] == condition][F_deposits].sum()

    sum3 = borrowings_df[borrowings_df[T_borrowings] == condition][H].sum()
    sum4 = borrowings_df[borrowings_df[X] == condition][I].sum()

    value1 = output_df.loc[F_row1, 'Blank 1']
    value2 = output_df.loc[F_row2, 'Blank 1']
    value3 = output_df.loc[F_row3, 'Blank 1']

    return sum1 + sum2 + sum3 + sum4 - value1 - value2 - value3

def calc_sum11(deposits_df, borrowings_df, output_df, AF, Z, G_row1, G_row2, G_row3):
    """
    =SUM(Deposits!$AF:$AF)+
    SUM(Borrowings!$Z:$Z)-
    $G$26-
    $G$27-
    $G$29

    Row 30 - Blank 2
    """
    sum1 = deposits_df[AF].sum()
    sum2 = borrowings_df[Z].sum()

    value1 = output_df.loc[G_row1, 'Blank 2']
    value2 = output_df.loc[G_row2, 'Blank 2']
    value3 = output_df.loc[G_row3, 'Blank 2']

    return sum1 + sum2 - value1 - value2 - value3

def calc_sum12(df, H, R, T, I, W):
    """
    =SUMIFS('Issued Securities'!$H:$H,'Issued Securities'!$R:$R,"30 or Less",'Issued Securities'!$T:$T,"<>"&"Retail",'Issued Securities'!$T:$T,"<>"&"Small Business Customer")+
    SUMIFS('Issued Securities'!$I:$I,'Issued Securities'!$W:$W,"30 or Less",'Issued Securities'!$T:$T,"<>"&"Retail",'Issued Securities'!$T:$T,"<>"&"Small Business Customer")+
    SUM(SUMIFS('Issued Securities'!$H:$H,'Issued Securities'!$T:$T,{"Retail","Small Business Customer"},'Issued Securities'!$R:$R,"30 or Less"))+
    SUM(SUMIFS('Issued Securities'!$I:$I,'Issued Securities'!$T:$T,{"Retail","Small Business Customer"},'Issued Securities'!$W:$W,"30 or Less"))
    Row 31 - Blank 1
    """
    condition1 = "30 or Less"
    conditions2 = ['Retail', 'Small Business Customer']

    # Chuyển đổi cột H thành số, chuyển đổi giá trị không thể chuyển đổi thành NaN
    df[H] = pd.to_numeric(df[H], errors='coerce')
    df[H].fillna(0, inplace=True)

    sum1 = df.loc[(df[R] == condition1) & (~df[T].isin(conditions2)), H].sum()
    sum2 = df.loc[(df[W] == condition1) & (~df[T].isin(conditions2)), I].sum()

    sum3 = df.loc[(df[T].isin(conditions2)) & (df[R] == condition1), H].sum()
    sum4 = df.loc[(df[T].isin(conditions2)) & (df[W] == condition1), I].sum()

    return sum1 + sum2 + sum3 + sum4

def calc_sum13(df, T, Y):
    """
    =SUMIFS('Issued Securities'!$Y:$Y,'Issued Securities'!$T:$T,"<>"&"Retail",'Issued Securities'!$T:$T,"<>"&"Small Business Customer")+
    SUM(SUMIFS('Issued Securities'!$Y:$Y,'Issued Securities'!$T:$T,{"Retail","Small Business Customer"}))
    Row 31 - Blank 2

   """
    conditions1 = ['Retail', 'Small Business Customer']

    sum1 = df.loc[~df[T].isin(conditions1), Y].sum()
    sum2 = df.loc[df[T].isin(conditions1), Y].sum()

    return sum1 + sum2

def calc_sum14(df, AM, AI):
    """
    =SUMIFS('Securities Financial Trans.'!$AM:$AM,'Securities Financial Trans.'!$AI:$AI,"<>"&"Retail")
    Row 32 - Blank 2
    """
    condition1 = "Retail"

    sum1 = df.loc[df[AI] != condition1, AM].sum()

    return sum1

def calc_sum15(output_df, F_row1, F_row2, F_row3):
    """
    =SUM(F34:F36)

    Row 33 - Blank 1
    """
    value1 = output_df.loc[F_row1, 'Blank 1']
    value2 = output_df.loc[F_row2, 'Blank 1']
    value3 = output_df.loc[F_row3, 'Blank 1']

    return value1 + value2 + value3

def calc_sum16(output_df, G_row1, G_row2, G_row3):
    """
    =SUM(G34:G36)

    Row 33 - Blank 2
    """
    value1 = output_df.loc[G_row1, 'Blank 2']
    value2 = output_df.loc[G_row2, 'Blank 2']
    value3 = output_df.loc[G_row3, 'Blank 2']

    return value1 + value2 + value3

def calc_sum17(df, N, Q):
    """
    =-SUMIFS(Derivatives!$N:$N,Derivatives!$N:$N,"<"&"0",Derivatives!$Q:$Q,"30 or Less")

    Row 34 - Blank 1
    """
    condition1 = "30 or Less"
    sum1 = df.loc[(df[N] < 0) & (df['Days to Maturity'] == condition1), 'MTM'].sum()

    return -sum1

def calc_sum18(df, S):
    """
    =-SUM(Derivatives!$S:$S)

    Row 34 - Blank 2
    """
    total_sum = df[S].sum()
    

    return -float(total_sum)


def calc_sum21(df, I):
    """
    =SUM(Facility!$I:$I)

    Row 36 - Blank 1
    """
    total_sum = df[I].sum()

    return total_sum

def calc_sum22(df, P):
    """
    =SUM(Facility!$P:$P)

    Row 36 - Blank 2
    """
    total_sum = df[P].sum()

    return total_sum

def get_value(df, R, column):

    """

    ='Other Items'!$C$37

 

    Row 37 - Blank 1

    """


    value = df.iloc[R, df.columns.get_loc(column)]

    return value

def calc_sum24(df, F):

    """

    =SUM('Off Balance Sheet'!$F:$F)




    Row 38 - Blank 1

    """

    total = df[F].sum()  # Sum all values in column 'F'

    return total

def calc_sum25(df, M):
    """
    =SUM('Off Balance Sheet'!$M:$M)

    Row 38 - Blank 2
    """
    
    total = df[M].sum()  # Sum all values in column 'M'
    return total

def calc_sum26(df, G, G25, G28, G32, G33, G37, G38):
    """
    =SUM(G25,G28,G32:G33,G37:G38)
    Row 39 - Blank 2
    """
    # Note that Excel's 1-indexing is converted to Python's 0-indexing
    value_25 = df.loc[G25, G]  # G25 in Excel
    value_28 = df.loc[G28, G]  # G28 in Excel
    value_32_33 = df.loc[G32:G33, G].sum()  # G32:G33 in Excel
    value_37_38 = df.loc[G37:G38, G].sum()  # G37:G38 in Excel

    return value_25 + value_28 + value_32_33 + value_37_38


def calc_sum27(df, G, AB, Z, H, AA):
    """
    =SUMIFS('Securities Financial Trans.'!$G:$G,'Securities Financial Trans.'!$AB:$AB,"Secured Lending",'Securities Financial Trans.'!$Z:$Z,"30 or Less")+SUMIFS('Securities Financial Trans.'!$H:$H,'Securities Financial Trans.'!$AB:$AB,"Secured Lending",'Securities Financial Trans.'!$AA:$AA,"30 or Less")

    Row 41- Blank 1
    """
    condition1 = df[AB] == "Secured Lending"
    condition2 = df[Z] == "30 or Less"
    sum_G = df.loc[condition1 & condition2, G].sum()

 

    condition3 = df[AB] == "Secured Lending"
    condition4 = df[AA] == "30 or Less"
    sum_H = df.loc[condition3 & condition4, H].sum()

    return sum_G + sum_H

def calc_sum28(df, AK, AB):
    """
    =SUMIFS('Securities Financial Trans.'!$AK:$AK,'Securities Financial Trans.'!$AB:$AB,"Secured Lending")

    Row 41 - Blank 2
    """
    condition = df[AB] == "Secured Lending"
    sum_AK = df.loc[condition, AK].sum()

    return sum_AK

def calc_sum29(df, Y):
    """
    =SUM('Loans & Advances'!$Y:$Y)

    Row 42 - Blank 1
    """
    sum_Y = df[Y].sum()
    return sum_Y

def calc_sum30(df, Z):
    """
    =SUM('Loans & Advances'!$Z:$Z)

    Row 42 - Blank 2
    """
    sum_Z = df[Z].sum()
    return sum_Z

def calc_sum31(its,derivatives,dep_w_other_banks,other_items, F, AH, AK, N, C, R):
    """
    =SUM('Investment&Trading Securities'!$AH:$AH)+SUM('Investment&Trading Securities'!$AK:$AK)+SUMIFS(Derivatives!$N:$N,Derivatives!$N:$N,">"&"0")+SUM('Deposits with Other Banks'!$F:$F)+'Other Items'!$C$38

    Row 43 - Blank 1
    """
    sum_AH = its[AH].sum()
    sum_AK = its[AK].sum()
    sum_N = derivatives.loc[derivatives[N] > 0, N].sum()
    dep_w_other_banks[F] = pd.to_numeric(dep_w_other_banks[F], errors='coerce')
    sum_F = dep_w_other_banks[F].sum()
    value_C = other_items.loc[R, C]

    return sum_AH + sum_AK + sum_N + sum_F + value_C

def calc_sum32(its, derivatives, dep_w_other_banks, other_items, P, AL, AM, R, I, R_index):
    """
    =SUM('Investment&Trading Securities'!$AL:$AL)+SUM('Investment&Trading Securities'!$AM:$AM)+SUM(Derivatives!$R:$R)+SUM('Deposits with Other Banks'!$P:$P)+'Other Items'!$I$38

    Row 43 - Blank 2
    """
    sum_AL = its[AL].sum()
    sum_AM = its[AM].sum()
    sum_R = derivatives[R].sum()
    sum_P = dep_w_other_banks[P].sum()
    value_I = other_items.loc[R_index, I]

    return sum_AL + sum_AM + sum_R + sum_P + value_I

def calc_sum33(df, F, F_row1, F_row2):
    """
    =SUM(F41:F43)

    Row 44 - Blank 1
    """
    sum_F = df.loc[F_row1:F_row2, F].sum()  # F41:F43 in Excel, adjusting for 0-indexing in Python
    return sum_F


def calc_sum34(df, G, G_row1, G_row2):
    """
    =SUM(G41:G43)

    Row 44 - Blank 2
    """
    sum_G = df.loc[G_row1:G_row2, G].sum()  # G41:G43 in Excel, adjusting for 0-indexing in Python
    return sum_G

def calc_difference1(df, G, G_row1, G_row2, G_row3):
    """
    =$G$23-$G$21-$G$22

    Row 46 - Blank 2
    """
    diff = df.loc[G_row1, G] - df.loc[G_row2, G] - df.loc[G_row3, G]  # Adjusting for 0-indexing in Python
    return diff

def calc_difference2(df, G, G_row39, G_row44):
    """
    =G39-MIN(G44,75%*G39)
    """
    g39 = df.at[G_row39, G]  # G39 in Excel, adjusting for 0-indexing in Python
    g44 = df.at[G_row44, G]  # G44 in Excel, adjusting for 0-indexing in Python
    diff = g39 - min(g44, 0.75 * g39)
    return diff

def calc_custom_sum(investment_trading_securities_df, other_items_df):

    """

    =SUMIFS('Investment&Trading Securities'!$AF:$AF,'Investment&Trading Securities'!$AD:$AD,"L1")+'Other Items'!$C$11+'Other Items'!$C$12

 

    Row 18 Blank 1

    """

    sum_ifs_result = investment_trading_securities_df.loc[investment_trading_securities_df['HQLA Asset'] == "L1"]['Unweighted Market Value Amount'].sum()

    other_items_result = other_items_df.loc[0, 'AMOUNT ALL MATURITY'] + other_items_df.loc[1, 'AMOUNT ALL MATURITY']

    return sum_ifs_result + other_items_result

 

def calculate_sum(investment_trading_securities_df, other_items_df):

    """

    Row 18 Blank 2
=SUMIFS('Investment&Trading Securities'!$AG:$AG,'Investment&Trading Securities'!$AD:$AD,"L1")
+'Other Items'!$I$11+'Other Items'!$I$12
    """
    investment_trading_securities_df['Weighted Amount for HQLA'] = pd.to_numeric(investment_trading_securities_df['Weighted Amount for HQLA'], errors='coerce')

    sum_ifs_result = investment_trading_securities_df.loc[investment_trading_securities_df['HQLA Asset'] == "L1"]['Weighted Amount for HQLA'].sum()
    
    other_items_result = other_items_df.at[0, 'WEIGHTED AMOUNT FOR HQLA'] + other_items_df.at[1, 'WEIGHTED AMOUNT FOR HQLA']

    return sum_ifs_result + other_items_result

def percent(df, G_row46, G_row47):
    try:
        result = df.at[G_row46, 'Blank 2'] / df.at[G_row47, 'Blank 2']
        if pd.isna(result) or np.isinf(result):
            return 0
        return result
    except ZeroDivisionError:
        return 0

"""
End of Calculations:
@Return: the result of the cell in Row x, column Blank 1/2
"""
def main(date_str):
    path = os.path.dirname(os.path.realpath(__file__))

   
   #Change path on your computer
   #------------------------------------------------Paths------------------------------------------------------------
    
    path_borrowings = os.path.join(path, 'Borrowings')
    path_investment = os.path.join(path, 'Investment_Trading_Securities')
    path_otheritems = os.path.join(path, 'Other_Items')
    path_deposit = os.path.join(path, 'Deposit')
    path_issuedsecurities =os.path.join(path, 'Issued_Securities')
    path_securities_fin_trans = os.path.join(path, 'Securities_Financial_Trans')
    path_derivatives = os.path.join(path, 'Derivatives')
    path_facility = os.path.join(path, 'Facility')
    path_offbalancesheet =os.path.join(path, 'Off_Balance_Sheet')
    path_loan_advances =os.path.join(path, 'Loans_Advances')
    path_deposits_w_otherbanks = os.path.join(path, 'Deposits_with_other_banks')
   #------------------------------------------------Paths------------------------------------------------------------
    borrowings = Borrowings_output.lcr_borrowing(path_borrowings, date_str)
    investment = Investment_Trading_Securities_output.lcr_investmentandtradingsecurities(path_investment, date_str)
    securities_fin_trans = Securities_Financial_Trans.lcr_securitiesfinancialtrans(path_securities_fin_trans, date_str)
    deposit = Deposits_output.Deposits_LCR(path_deposit, date_str)
    Derivatives = Derivatives_output.lcr_derivatives(path_derivatives, date_str)
    Facility = Facility_output.lcr_facility(path_facility, date_str)
    other_items = Other_Items.lcr_Other_Items(path_otheritems, date_str)
    off_balance_sheet = Off_Balance_Sheet_output.lcr_offbalancesheet(path_offbalancesheet, date_str)
    loans_advances = Loans_Advances.lcr_Loans_Advances(path_loan_advances, date_str)
    issued_securities = Issued_Securities.lcr_Issued_Securities(path_issuedsecurities, date_str)
    dep_w_other_banks = Deposits_with_other_banks_output.lcr_deposits(path_deposits_w_otherbanks, date_str)
    output_df = set_output_df()
    
   #------------------------------------------------Insertion-------------------------------------------------------------

    #Row index = Row - 18

    #Row index 0
    output_df.at[0, 'Blank 1'] = calc_custom_sum(investment, other_items)

    output_df.at[0, 'Blank 2'] = calculate_sum(investment, other_items)

    # #Row index 1
    output_df.at[1, 'Blank 1'] = calc_investment(investment, 'HQLA Asset', 'Unweighted Market Value Amount', "L2A")
    output_df.at[1, 'Blank 2'] = calc_investment(investment, 'HQLA Asset', 'Weighted Amount for HQLA', 'L2A')

    # #Row index 2
    output_df.at[2, 'Blank 1'] = calc_investment(investment, 'HQLA Asset', 'Unweighted Market Value Amount', "L2B")
    output_df.at[2, 'Blank 2'] = calc_investment(investment, 'HQLA Asset', 'Weighted Amount for HQLA', 'L2B')

    # #Row index 3 and 4
    output_df.at[3, 'Blank 2'] = calc_max1(output_df, 0, 1, 2, 'Blank 2') #=MAX($G$19+$G$20-(2/3*$G$18),$G$20-(15/85*($G$18+$G$19)),0)
    output_df.at[4, 'Blank 2'] = calc_max2(output_df, 0, 1, 2, 'Blank 2') #=MAX($G$20-(15/85*($G$18+$G$19)),$G$20-(15/60*$G$18),0)

    # #Row index 5
    output_df.at[5, 'Blank 2'] = calc_sum1(output_df, 0,1,2, 'Blank 2') #=SUM(G18:G20)



    # Row index 8
    output_df.at[8, 'Blank 1'] = calc_sum2(deposit, deposit['Retail/Wholesale'], deposit['Stable Amount (Principal + Interest)'])
    output_df.at[8, 'Blank 2'] = calc_sum3(deposit, deposit['Retail/Wholesale'], deposit['Stable Run-Off Amount'])

    output_df.at[9, 'Blank 1'] = calc_sum4(deposit, borrowings,
                                           'Retail/Wholesale',
                                           deposit['Unstable Amount (Principal + Interest)'],
                                           'Counterparty Category',
                                           borrowings['Next principal payment Amount'],
                                           'Days To Next Principal Payment',
                                           borrowings['Next Interest Payment Amount'],
                                           borrowings['Days To Coupon'])
    
    output_df.at[9, 'Blank 2'] = calc_sum5(deposit, borrowings,
                                           'Retail/Wholesale',
                                           deposit['Unstable Run-Off Amount'],
                                           'Counterparty Category',
                                           borrowings['Total Weighted Cash Outflow'])
    # #Row index 7(skip row index 6)
    output_df.at[7, 'Blank 1'] = calc_sum(output_df, 8, 9, 'Blank 1') #=SUM(F26:F27)
    output_df.at[7, 'Blank 2'] = calc_sum(output_df, 8, 9, 'Blank 2') #=SUM(G26:G27)


    # #Row index 10 - done
 

    # #Row index 11
    output_df.at[11, 'Blank 1'] = calc_sum8(deposit, 
                                            'Product type',
                                            'Deposit balance',
                                            'Interest Payable',
                                            'Days till next interet payment')

    output_df.at[11, 'Blank 2'] = calc_sum9(deposit, 
                                            'Product type',
                                            'Total Weighted Cash Outflow')
    #Row index 12
    output_df.at[12, 'Blank 1'] = calc_sum10(deposit, borrowings, output_df, 
                                             'Deposit balance',
                                             'Interest Payable',
                                             'Days till next interet payment',
                                             'Next principal payment Amount',
                                             'Days To Next Principal Payment',
                                             'Next Interest Payment Amount',
                                             'Days To Coupon',
                                             8, 9, 11
                                             )
    


    
    output_df.at[12, 'Blank 2'] = calc_sum11(deposit, borrowings, output_df,
                                             'Total Weighted Cash Outflow',
                                             'Total Weighted Cash Outflow',
                                             8,9,11
                                             )


    # #Row index 13
    output_df.at[13, 'Blank 1'] = calc_sum12(issued_securities,
                                             'Next Principal Payment Amount',
                                             'Days To Maturity',
                                             'Counterparty Category',
                                             'Next Interest Payment Amount',
                                             'Days To Coupon')
    output_df.at[13, 'Blank 2'] = calc_sum13(issued_securities, 
                                             'Counterparty Category',
                                             'Total Weighted Cash Outflow')
    
    output_df.at[10, 'Blank 1'] = calc_sum6(output_df, 11,12,13, 'Blank 1')
    output_df.at[10, 'Blank 2'] = calc_sum7(output_df, 11,12,13, 'Blank 2')
    # #Row index 14
    output_df.at[14,'Blank 2'] = calc_sum14(securities_fin_trans, 'Cash Outflow', 'Counterparty Category')
    output_df.at[14, 'Blank 2'] 



    # #Row index 16
    output_df.at[16,'Blank 1'] = calc_sum17(Derivatives, 'MTM', 'Days to Maturity')
    output_df.at[16,'Blank 2'] = calc_sum18(Derivatives, 'Outflow Amount')
    output_df.at[17, 'Blank 1'] = 0
    output_df.at[17, 'Blank 2'] = 0
   

    # #Row index 18
    output_df.at[18,'Blank 1'] = calc_sum21(Facility, ' Undrawn Credit Line ')

 
    # co dau cach o truoc Outflow?
    output_df.at[18,'Blank 2'] = calc_sum22(Facility, ' Outflow (undrawn portion resp) ')

    output_df.at[15,'Blank 1']= calc_sum15(output_df, 16, 17,18)
    output_df.at[15,'Blank 2'] = calc_sum16(output_df, 16, 17, 18)
    output_df.at[19,'Blank 1'] = get_value(other_items, 24, 'AMOUNT ALL MATURITY')

    output_df.at[19,'Blank 2'] = get_value(other_items, 24, 'WEIGHTED AMOUNT FOR HQLA')
    # #Row index 20
    output_df.at[20,'Blank 1'] = calc_sum24(off_balance_sheet, ' Unutilised Value ')
    output_df.at[20,'Blank 2'] = calc_sum25(off_balance_sheet, 'Cash Outflow')
    #Row index 21
    output_df.at[21,'Blank 2'] = calc_sum26(output_df, 'Blank 2',
                                            7, 10, 14, 15, 19, 20)

    # #Row index 23
    output_df.at[23,'Blank 1'] = calc_sum27(securities_fin_trans, 'Next Principal Payment Amount', 'Transaction Type', 'Days To Next Principal Payment', 'Next Interest Payment', 'Days to Interest Payment')
    output_df.at[23,'Blank 2'] = calc_sum28(securities_fin_trans, 'Cash Inflow', 'Transaction Type')
    # #Row index 24
    output_df.at[24,'Blank 1'] = calc_sum29(loans_advances, 'Total Unweighted Inflows')
    output_df.at[24,'Blank 2'] = calc_sum30(loans_advances, 'Weighted Inflows')
    
    # #Row index 25
    output_df.at[25,'Blank 1'] = calc_sum31(investment,

                                            Derivatives,

                                            dep_w_other_banks,

                                            other_items,

                                            'Deposit balance',

                                            'Unweighted Principal Cash Inflow',

                                            'Coupon Cash Inflow',

                                            'MTM',

                                            'Amount all maturity', 20)

    output_df.at[25,'Blank 2'] = calc_sum32(investment,

                                            Derivatives,

                                            dep_w_other_banks,

                                            other_items,

                                            'Inflow',

                                            'Weighted Coupon cash inflow',

                                            'Weighted Princial Cash Inflow',

                                            'Inflow Amount',

                                            'Weighted amount for HQLA', 20)  
    #Row index 26
    output_df.at[26,'Blank 1'] = calc_sum33(output_df, 'Blank 1', 23, 25)

    output_df.at[26,'Blank 2'] = calc_sum34(output_df, 'Blank 2', 23, 25)
    output_df.at[27, 'Blank 2'] = "Total adjusted value Giá trị sau điều chỉnh"

    #Row index 28
    output_df.at[28,'Blank 2'] = calc_difference1(output_df, 'Blank 2', 5, 3, 4)

    #Row index 29
    output_df.at[29,'Blank 2'] = calc_difference2(output_df, 'Blank 2', 21, 26)
    output_df.at[30, 'Blank 2'] = percent(output_df, 28, 29)

    return output_df

if __name__ == "__main__":
    main() 