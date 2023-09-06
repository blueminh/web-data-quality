"""
@Author: Khanh Hung & Tuan Kiet & Minh Anh
@Status: Completed
"""
import os
import pandas as pd
import numpy as np


from .Borrowings import Borrowings_NSFR_output
from .Investment_Trading_Securities import Investment_Trading_Securities_NSFR_output
from .Deposits import Deposits_NSFR_output
from .Facility import Facility_NSFR_output
from .Other_Items import Other_NSFR_Items
from .Issued_Securitie import Issued_NSFR_Securities
from .Securities_Financial_Tran import Securities_Financial_Trans_NSFR
from .Derivatives import Derivatives_NSFR_output
from .Off_Balance_Sheet import Off_Balance_Sheet_NSFR_output
from .Loan_Advance import Loans_Advances_NSFR
from .Deposits_with_Other_Bank import Deposits_with_other_banks_NSFR_output


def set_output_df(): 
    """
    Create output dataframe
    @Return: output dataframe
    """
    data = {
        'Item': [
            '1 Capital:', '1.1 Regulatory capital', '1.2 Other capital instruments',
            '2 Retail deposits and deposits from small business customers:', '2.1 Stable deposits', '2.2 Less stable deposits',
            '3 Wholesale funding:', '3.1 Operational deposits', '3.2 Other wholesale funding',
            '4 Liabilities with matching interdependent assets',
            '5 Other liabilities:', '5.1 NSFR derivative liabilities', '5.2 All other liabilities and equity not included in the above categories',
            '6 Total ASF',
            'Required stable funding (RSF) item',
            '1 Total NSFR high-quality liquid assets (HQLA) including encumbered and unencumbered', '2 Deposits held at other financial institutions for operational purposes',
            '3 Performing loans and securities:', '3.1 Performing loans to financial institutions secured by Level 1 HQLA',
            '3.2 Performing loans to financial institutions secured by non-Level 1 HQLA and unsecured performing loans to financial institutions',
            '3.3 Performing loans to non-financial corporate clients, retail and small business customers, sovereigns, central banks and PSEs with RW >35% under the Basel II standardised approach for credit risk',
            '3.4 Performing loans to non-financial corporate clients, retail and small business customers, sovereigns, central banks and PSEs with RW<=35% under the Basel II standardised approach for credit risk',
            '3.5 Performing residential mortgages with RW >35% under the Basel II standardised approach for credit risk Performing residential mortgages, of which:',
            '3.6 Performing residential mortgages with RW <= 35% under the Basel II standardised approach for credit risk Performing residential mortgages, of which:',
            '3.7 Securities that are not in default and do not qualify as HQLA, including exchange-traded equities Performing residential mortgages, of which:',
            '4 Assets with matching interdependent liabilities',
            '5 Other assets:', '5.1 Physical traded commodities, including gold',
            '5.2 Assets posted as initial margin for derivative contracts and contributions to default funds of CCPs'
        ],
        'Description': [
            'Vốn:', 'Vốn tự có', 'Các công cụ vốn khác',
            'Tiền gửi của khách hàng bán lẻ và khách hàng kinh doanh nhỏ:', 'Tiền gửi ổn định', 'Tiền gửi kém ổn định',
            'Vốn bán buôn:', 'Tiền gửi hoạt động', 'Nguồn vốn huy động từ bán buôn khác 3,383,088,260,107',
            'Các khoản nợ phải trả phụ thuộc vào tài sản',
            'Các khoản nợ phải trả khác', 'Nợ phái sinh NSFR', 'Tất cả các khoản nợ và vốn chủ sở hữu khác không bao gồm trong các loại trên',
            'Tổng giá trị ASF',
            '',
            'Tổng tài sản thanh khoản có chất lượng cao (HQLA), bao gồm ràng buộc và không ràng buộc, thuộc NSFR', 'Tiền gửi tại các tổ chức tài chính khác cho mục đích hoạt động',
            'Các khoản cho vay và chứng khoán không phải nợ xấu (performing):', 'Các khoản cho vay không phải nợ xấu (performing loans) đối với các TCTC được bảo đảm bằng tài sản HQLA cấp 1',
            'Các khoản cho vay không phải nợ xấu (performing loans), bao gồm được đảm bảo bằng tài sản khác không phải tài sản HQLA cấp 1 và không bảo đảm (unsecured performing loans) đối với các TCTC',
            'Các khoản cho vay không phải nợ xấu (performing loans) đối với các khách hàng doanh nghiệp phi tài chính, khách hàng bán lẻ và kinh doanh nhỏ, các chính phủ, NHTW và tổ chức công lập với hệ số rủi ro >35% theo phương pháp chuẩn hóa (SA) đối với rủi ro tín dụng',
            'Các khoản cho vay không phải nợ xấu (performing loans) đối với các khách hàng doanh nghiệp phi tài chính, khách hàng bán lẻ và kinh doanh nhỏ, các chính phủ, NHTW và tổ chức công lập với hệ số rủi ro ≤35% theo phương pháp chuẩn hóa (SA) đối với rủi ro tín dụng',
            'Các khoản cho vay thế chấp nhà ở không phải nợ xấu, với hệ số rủi ro >35% theo phương pháp chuẩn hóa (SA) đối với rủi ro tín dụng - - - - -',
            'Các khoản cho vay thế chấp nhà ở không phải nợ xấu, với hệ số rủi ro ≤35% theo phương pháp chuẩn hóa (SA) đối với rủi ro tín dụng - - - - -',
            'Chứng khoán không vỡ nợ và không đủ điều kiện là tài sản HQLA, bao gồm cả cổ phiếu được giao dịch trên sàn',
            'Các tài sản với các khoản nợ phải trả phụ thuộc',
            'Các tài sản khác:', 'Các hàng hóa được giao dịch trực tiếp, bao gồm vàng.',
            'Các tài sản được đặt làm ký quỹ ban đầu (initial margin) cho các hợp đồng tài chính phái sinh và đóng góp vào quỹ đảm bảo của tổ chức giao dịch trung gian (CCP).'
        ]
    }

    new_rows = {
        'Item': [
            '5.3 NSFR derivative assets', '5.4 NSFR derivative liabilities before deduction of variation margin posted',
            '5.5 All other assets not included in the above categories', '6 Off-balance sheet items',
            '7 Total RSF', '8 Net Stable Funding Ratio (%)'
        ],
        'Description': [
            'Tài sản phái sinh NSFR', 'NPT phái sinh trước khi giảm trừ ký quỹ biến đổi (variation margin) được đặt',
            'Tất cả các tài sản khác không có thuộc các khoản mục trên', 'Các khoản mục ngoại bảng',
            'Tổng lượng vốn ổn định yêu cầu', 'Tỷ lệ Nguồn vốn ổn định ròng (%)'
        ]
    }
    df = pd.DataFrame(data)
    for i, row in enumerate(zip(new_rows['Item'], new_rows['Description'])):
        df.loc[len(df)] = row
        
    df["Blank 1"] = np.nan
    df["Blank 2"] = np.nan
    df["Blank 3"] = np.nan
    df["Blank 4"] = np.nan
    df["Blank 5"] = np.nan

    return df






def calc_sum1(df, start_row, end_row, col_name):
    """
    Row 14 Blank 1,2,3,4,5
    Row 17 Blank 1,2,3,4,5
    14: SUM(F15:F16) also for G,H,I,J 
    17: SUM(F18:F19) also for G,H,I,J
    """
    return df.loc[start_row:end_row, col_name].sum()

def get_value1(other_items, All_Maturity):
    """
    Row 15 Blank 1
    'Other Items'!$C$32
    """
    # The below line will return the value present at row index 31 (32 in excel as it starts from 1) and column C
    return other_items.loc[19, All_Maturity]

def get_value2(other_items, More_than_1_Year):
    """
    Row 15 Blank 4 (blank 2,3 = 0)
    ='Other Items'!$F$33
    """
    # The below line will return the value present at row index 32 (33 in excel as it starts from 1) and column F
    return other_items.loc[20, More_than_1_Year]

def calc_sum6(other_items, Weighted_ASF_Amount):
    """
    Row 15 Blank 5
    ='Other Items'!$O$32+'Other Items'!$O$33
    """
    # The below line will return the sum of values present at row index 31 and 32 (32 and 33 in excel as it starts from 1) and column O
    return other_items.loc[19, Weighted_ASF_Amount] + other_items.loc[20, Weighted_ASF_Amount]

def calc_sum7(issued_securities, securities_financial_trans, Book_value, Remaining_Maturity, ASF_Amount, Book_Value, Transaction_Category, Days_To_Maturity):
    """
    Row 16 Blank 2 (Blank 1 = 0)
    =SUMIFS('Issued Securities'!$E:$E,'Issued Securities'!$Z:$Z,"Less than 6 months",'Issued Securities'!$AB:$AB,"<>"&0)
    +SUMIFS('Securities Financial Trans.'!$F:$F,'Securities Financial Trans.'!$C:$C,"Issued Securities",'Securities Financial Trans.'!$AN:$AN,"Less than 6 months")
    """

    sum1 = issued_securities.loc[(issued_securities[Remaining_Maturity] == "Less than 6 months") & (issued_securities[ASF_Amount] != 0), Book_value].sum()
    sum2 = securities_financial_trans.loc[(securities_financial_trans[Transaction_Category] == "Issued Securities") & (securities_financial_trans[Days_To_Maturity] == "Less than 6 months"), Book_Value].sum()

    return sum1 + sum2

def calc_sum8(issued_securities, securities_financial_trans, Book_value, Remaining_Maturity, ASF_Amount, Book_Value, Transaction_Category, Days_To_Maturity):
    """
    Row 16 Blank 3
    =SUMIFS('Issued Securities'!$E:$E,'Issued Securities'!$Z:$Z,"6 months to 1 year",'Issued Securities'!$AB:$AB,"<>"&0)
    +SUMIFS('Securities Financial Trans.'!$F:$F,'Securities Financial Trans.'!$C:$C,"Issued Securities",'Securities Financial Trans.'!$AN:$AN,"6 months to 1 year")
    """

    sum1 = issued_securities.loc[(issued_securities[Remaining_Maturity] == "6 months to 1 year") & (issued_securities[ASF_Amount] != 0), Book_value].sum()
    sum2 = securities_financial_trans.loc[(securities_financial_trans[Transaction_Category] == "Issued Securities") & (securities_financial_trans[Days_To_Maturity] == "6 months to 1 year"), Book_Value].sum()

    return sum1 + sum2

def calc_sum9(issued_securities, securities_financial_trans, Book_value, Remaining_Maturity, ASF_Amount, Book_Value, Transaction_Category, Days_To_Maturity):
    """
    Row 16 Blank 4
    =SUMIFS('Issued Securities'!$E:$E,'Issued Securities'!$Z:$Z,"More than 1 year",'Issued Securities'!$AB:$AB,"<>"&0)
    +SUMIFS('Securities Financial Trans.'!$F:$F,'Securities Financial Trans.'!$C:$C,"Issued Securities",'Securities Financial Trans.'!$AN:$AN,"More than 1 year")
    """
    sum1 = issued_securities.loc[(issued_securities[Remaining_Maturity] == "More than 1 year") & (issued_securities[ASF_Amount] != 0), Book_value].sum()
    sum2 = securities_financial_trans.loc[(securities_financial_trans[Transaction_Category] == "Issued Securities") & (securities_financial_trans[Days_To_Maturity] == "More than 1 year"), Book_Value].sum()

    return sum1 + sum2

def calc_sum10(issued_securities, securities_financial_trans, ASF_Amount, Total_ASF_Amount, Transaction_Category):
    """
    Row 16 Blank 5
    =SUM('Issued Securities'!$AB:$AB)+SUMIFS('Securities Financial Trans.'!$AZ:$AZ,'Securities Financial Trans.'!$C:$C,"Issued Securities")
    """
    sum1 = issued_securities[ASF_Amount].sum()
    sum2 = securities_financial_trans.loc[securities_financial_trans[Transaction_Category] == "Issued Securities", Total_ASF_Amount].sum()


    return sum1 + sum2

def calc_sum16(deposit, Principal_Stable_Amount, Product_Type, Retail_Wholesale, Days_to_Maturity):
    """
    Row 18 Blank 1
    =SUMIFS(Deposits!$AJ:$AJ,Deposits!$S:$S,"Demand Deposit",Deposits!$T:$T,"Retail",Deposits!$AG:$AG,"No Maturity")
    +SUMIFS(Deposits!$AJ:$AJ,Deposits!$S:$S,"Demand Deposit",Deposits!$T:$T,"Small Business Customer",Deposits!$AG:$AG,"No Maturity")
    """
    conditions = ((deposit[Product_Type] == "Demand Deposit") & 
                  (deposit[Retail_Wholesale].isin(["Retail", "Small Business Customer"])) & 
                  (deposit[Days_to_Maturity] == "No Maturity"))

    return deposit.loc[conditions, Principal_Stable_Amount].sum()

def calc_sum17(deposit, Principal_Stable_Amount, Retail_Wholesale, Days_to_Maturity):
    """
    Row 18 Blank 2
    =SUMIFS(Deposits!$AJ:$AJ,Deposits!$T:$T,"Retail",Deposits!$AG:$AG,"Less than 6 months")
    +SUMIFS(Deposits!$AJ:$AJ,Deposits!$T:$T,"Small Business Customer",Deposits!$AG:$AG,"Less than 6 months")
    """
    conditions = ((deposit[Retail_Wholesale].isin(["Retail", "Small Business Customer"])) & 
                  (deposit[Days_to_Maturity] == "Less than 6 months"))

    return deposit.loc[conditions, Principal_Stable_Amount].sum()

def calc_sum18(deposit, Principal_Stable_Amount, Retail_Wholesale, Days_to_Maturity):
    """
    Row 18 Blank 3
    =SUMIFS(Deposits!$AJ:$AJ,Deposits!$T:$T,"Retail",Deposits!$AG:$AG,"6 months to 1 year")
    +SUMIFS(Deposits!$AJ:$AJ,Deposits!$T:$T,"Small Business Customer",Deposits!$AG:$AG,"6 months to 1 year")
    """

    conditions = ((deposit[Retail_Wholesale].isin(["Retail", "Small Business Customer"])) & 
                  (deposit[Days_to_Maturity] == "6 months to 1 year"))

    return deposit.loc[conditions, Principal_Stable_Amount].sum()

def calc_sum19(deposit, Principal_Stable_Amount, Retail_Wholesale, Days_to_Maturity):
    """
    Row 18 Blank 4 
    =SUMIFS(Deposits!$AJ:$AJ,Deposits!$T:$T,"Retail",Deposits!$AG:$AG,"More than 1 year")
    +SUMIFS(Deposits!$AJ:$AJ,Deposits!$T:$T,"Small Business Customer",Deposits!$AG:$AG,"More than 1 year")
    """
    conditions = ((deposit[Retail_Wholesale].isin(["Retail", "Small Business Customer"])) & 
                  (deposit[Days_to_Maturity] == "More than 1 year"))

    return deposit.loc[conditions, Principal_Stable_Amount].sum()

def calc_sum20(deposit, Weighted_Stable_Amount, Retail_Wholesale):
    """
    Row 18 Blank 5
    =SUMIFS(Deposits!$AL:$AL,Deposits!$T:$T,"Retail")
    +SUMIFS(Deposits!$AL:$AL,Deposits!$T:$T,"Small Business Customer")
    """

    conditions = deposit[Retail_Wholesale].isin(["Retail", "Small Business Customer"])

    return deposit.loc[conditions, Weighted_Stable_Amount].sum()

def calc_sum21(deposit, Product_Type, Retail_Wholesale, Days_to_Maturity, Principal_Unstable_Amount):
    """
    Row 19 Blank 1
    =SUMIFS(Deposits!$AK:$AK,Deposits!$S:$S,"Demand Deposit",Deposits!$T:$T,"Retail",Deposits!$AG:$AG,"No Maturity")
    +SUMIFS(Deposits!$AK:$AK,Deposits!$S:$S,"Demand Deposit",Deposits!$T:$T,"Small Business Customer",Deposits!$AG:$AG,"No Maturity")
    """
    conditions = ((deposit[Product_Type] == "Demand Deposit") & 
                  (deposit[Retail_Wholesale].isin(["Retail", "Small Business Customer"])) & 
                  (deposit[Days_to_Maturity] == "No Maturity"))

    return deposit.loc[conditions, Principal_Unstable_Amount].sum()

def calc_sum22(deposit, Retail_Wholesale, Days_to_Maturity, Principal_Unstable_Amount):
    """
    Row 19 Blank 2
    =SUMIFS(Deposits!$AK:$AK,Deposits!$T:$T,"Retail",Deposits!$AG:$AG,"Less than 6 months")
    +SUMIFS(Deposits!$AK:$AK,Deposits!$T:$T,"Small Business Customer",Deposits!$AG:$AG,"Less than 6 months")
    """
    conditions = (deposit[Retail_Wholesale].isin(["Retail", "Small Business Customer"]) & 
                  (deposit[Days_to_Maturity] == "Less than 6 months"))


    return deposit.loc[conditions, Principal_Unstable_Amount].sum()

def calc_sum23(deposit, Retail_Wholesale, Days_to_Maturity, Principal_Unstable_Amount):
    """
    Row 19 Blank 3
    =SUMIFS(Deposits!$AK:$AK,Deposits!$T:$T,"Retail",Deposits!$AG:$AG,"6 months to 1 year")
    +SUMIFS(Deposits!$AK:$AK,Deposits!$T:$T,"Small Business Customer",Deposits!$AG:$AG,"6 months to 1 year")
    """

    conditions = (deposit[Retail_Wholesale].isin(["Retail", "Small Business Customer"]) & 
                  (deposit[Days_to_Maturity] == "6 months to 1 year"))

    return deposit.loc[conditions, Principal_Unstable_Amount].sum()

def calc_sum24(deposit, Retail_Wholesale, Days_to_Maturity, Principal_Unstable_Amount):
    """
    Row 19 Blank 4
    =SUMIFS(Deposits!$AK:$AK,Deposits!$T:$T,"Retail",Deposits!$AG:$AG,"More than 1 year")
    +SUMIFS(Deposits!$AK:$AK,Deposits!$T:$T,"Small Business Customer",Deposits!$AG:$AG,"More than 1 year")
    """
    conditions = (deposit[Retail_Wholesale].isin(["Retail", "Small Business Customer"]) & 
                  (deposit[Days_to_Maturity] == "More than 1 year"))

    return deposit.loc[conditions, Principal_Unstable_Amount].sum()

def calc_sum25(deposits, Retail_Wholesale, Weighted_Unstable_Amount):
    """
    =SUMIFS(Deposits!$AM:$AM,Deposits!$T:$T,"Retail")
    +SUMIFS(Deposits!$AM:$AM,Deposits!$T:$T,"Small Business Customer")

    Row 19 - Blank 5
    """

    conditions = ['Retail', 'Small Business Customer']

    return deposits.loc[deposits[Retail_Wholesale].isin(conditions), Weighted_Unstable_Amount].sum()


def calc_sum30(deposits, Product_Type, Remaining_Maturity_for_Accrued_Interest):
    """
    =SUMIFS(Deposits!$AJ:$AJ,Deposits!$S:$S,"Operational Deposit",Deposits!$AN:$AN,"No maturity")
    +SUMIFS(Deposits!$AK:$AK,Deposits!$S:$S,"Operational Deposit",Deposits!$AN:$AN,"No maturity")

    Row 21 - Blank 1
    """
    condition1 = deposits[Product_Type] == "Operational Deposit"
    condition2 = deposits[Remaining_Maturity_for_Accrued_Interest] == "No maturity"
    sum_AJ = deposits.loc[condition1 & condition2, 'Principal Stable Amount'].sum()

    condition3 = deposits[Product_Type] == "Operational Deposit"
    condition4 = deposits[Remaining_Maturity_for_Accrued_Interest] == "No maturity"
    sum_AK = deposits.loc[condition3 & condition4, 'Principal Unstable Amount'].sum()

    return sum_AJ + sum_AK

def calc_sum31(deposits, Principal_Stable_Amount, Principal_Unstable_Amount, Product_Type, Remaining_Maturity_for_Accrued_Interest):
    """
    This function replicates the following Excel operation in Python:
    =SUMIFS(Deposits!$AJ:$AJ,Deposits!$S:$S,"Operational Deposit",Deposits!$AN:$AN,"Less than 6 months")
    +SUMIFS(Deposits!$AK:$AK,Deposits!$S:$S,"Operational Deposit",Deposits!$AN:$AN,"Less than 6 months")

    Row 21 - Blank 2
    """
    condition1 = deposits[Product_Type] == "Operational Deposit"
    condition2 = deposits[Remaining_Maturity_for_Accrued_Interest] == "Less than 6 months"

    sum_AJ = deposits.loc[condition1 & condition2, Principal_Stable_Amount].sum()
    sum_AK = deposits.loc[condition1 & condition2, Principal_Unstable_Amount].sum()

    return sum_AJ + sum_AK

def calc_sum32(deposits, Principal_Stable_Amount, Principal_Unstable_Amount, Product_Type, Remaining_Maturity_for_Accrued_Interest):
    """
    This function replicates the following Excel operation in Python:
    =SUMIFS(Deposits!$AJ:$AJ,Deposits!$S:$S,"Operational Deposit",Deposits!$AN:$AN,"6 months to 1 year")
    +SUMIFS(Deposits!$AK:$AK,Deposits!$S:$S,"Operational Deposit",Deposits!$AN:$AN,"6 months to 1 year")

    Row 21 - Blank 3
    """
    condition1 = deposits[Product_Type] == "Operational Deposit"
    condition2 = deposits[Remaining_Maturity_for_Accrued_Interest] == "6 months to 1 year"

    sum_AJ = deposits.loc[condition1 & condition2, Principal_Stable_Amount].sum()
    sum_AK = deposits.loc[condition1 & condition2, Principal_Unstable_Amount].sum()

    return sum_AJ + sum_AK

def calc_sum33(deposits, Principal_Stable_Amount, Principal_Unstable_Amount, Product_Type, Remaining_Maturity_for_Accrued_Interest):
    """
    This function replicates the following Excel operation in Python:
    =SUMIFS(Deposits!$AJ:$AJ,Deposits!$S:$S,"Operational Deposit",Deposits!$AN:$AN,"More than 1 year")
    +SUMIFS(Deposits!$AK:$AK,Deposits!$S:$S,"Operational Deposit",Deposits!$AN:$AN,"More than 1 year")

    Row 21 - Blank 4
    """

    condition1 = deposits[Product_Type] == "Operational Deposit"
    condition2 = deposits[Remaining_Maturity_for_Accrued_Interest] == "More than 1 year"

    sum_AJ = deposits.loc[condition1 & condition2, Principal_Stable_Amount].sum()
    sum_AK = deposits.loc[condition1 & condition2, Principal_Unstable_Amount].sum()

    return sum_AJ + sum_AK

def calc_sum34(deposits, Weighted_Stable_Amount, Weighted_Unstable_Amount, Product_Type):
    """
    This function replicates the following Excel operation in Python:
    =SUMIFS(Deposits!$AL:$AL,Deposits!$S:$S,"Operational Deposit")
    +SUMIFS(Deposits!$AM:$AM,Deposits!$S:$S,"Operational Deposit")

    Row 21 - Blank 5
    """
    condition = deposits[Product_Type] == "Operational Deposit"

    sum_AL = deposits.loc[condition, Weighted_Stable_Amount].sum()
    sum_AM = deposits.loc[condition, Weighted_Unstable_Amount].sum()

    return sum_AL + sum_AM

def calc_sum35(deposits, df, Principal_Stable_Amount, Principal_Unstable_Amount, Days_to_Maturity, row_F18, row_F19, row_F21):
    """
    This function replicates the following Excel operation in Python:
    =SUMIFS(Deposits!$AJ:$AJ,Deposits!$AG:$AG,"No Maturity")
    +SUMIFS(Deposits!$AK:$AK,Deposits!$AG:$AG,"No Maturity")
    -NSFR!$F$18-NSFR!$F$19-NSFR!$F$21

    Row 22 - Blank 1
    """

    condition = deposits[Days_to_Maturity] == "No Maturity"

    sum_AJ = deposits.loc[condition, Principal_Stable_Amount].sum()
    sum_AK = deposits.loc[condition, Principal_Unstable_Amount].sum()

    # Subtract values from the NSFR DataFrame using the specific rows
    result = sum_AJ + sum_AK - df.loc[row_F18, 'Blank 1'] - df.loc[row_F19, 'Blank 1'] - df.loc[row_F21, 'Blank 1']

    return result

def calc_sum36(deposit, borrowings, securities_financial_trans, df, Principal_Stable_Amount, Principal_Unstable_Amount, Days_to_Maturity, Principal_Amount_Less_than_6_months, Next_Principal_Payment_Amount, Transaction_Type, Days_To_Maturity, row_G18, row_G19, row_G21):
    """
    This function replicates the following Excel operation in Python:
    =SUMIFS(Deposits!$AJ:$AJ,Deposits!$AG:$AG,"Less than 6 months")
    +SUMIFS(Deposits!$AK:$AK,Deposits!$AG:$AG,"Less than 6 months")
    +SUM(Borrowings!$P:$P)
    +SUMIFS('Securities Financial Trans.'!$G:$G,'Securities Financial Trans.'!$AB:$AB,"Secured Borrowing",'Securities Financial Trans.'!$AN:$AN,"Less than 6 months")
    -NSFR!$G$18-NSFR!$G$19-NSFR!$G$21
    """
    condition_deposits = deposit[Days_to_Maturity] == "Less than 6 months"
    condition_sec_fin_trans = (securities_financial_trans[Transaction_Type] == "Secured Borrowing") & (securities_financial_trans[Days_To_Maturity] == "Less than 6 months")

    sum_AJ = deposit.loc[condition_deposits, Principal_Stable_Amount].sum()
    sum_AK = deposit.loc[condition_deposits, Principal_Unstable_Amount].sum()
    sum_P = borrowings[Principal_Amount_Less_than_6_months].sum()
    sum_G = securities_financial_trans.loc[condition_sec_fin_trans, Next_Principal_Payment_Amount].sum()

 

    # Subtract values from the NSFR DataFrame using the specific rows
    result = sum_AJ + sum_AK + sum_P + sum_G -  df.loc[row_G18, 'Blank 2'] -  df.loc[row_G19, 'Blank 2'] -  df.loc[row_G21, 'Blank 2']

 

    return result

def calc_sum37(deposit, borrowings, securities_financial_trans, df, Principal_Stable_Amount, Principal_Unstable_Amount, Days_to_Maturity, Principal_Amount_6_months_to_1_year, Next_Principal_Payment_Amount, Transaction_Type, Days_To_Maturity, row_H18, row_H19, row_H21):
    """
    This function replicates the following Excel operation in Python:
    =SUMIFS(Deposits!$AJ:$AJ,Deposits!$AG:$AG,"6 months to 1 year")
    +SUMIFS(Deposits!$AK:$AK,Deposits!$AG:$AG,"6 months to 1 year")
    +SUM(Borrowings!$Q:$Q)
    +SUMIFS('Securities Financial Trans.'!$G:$G,'Securities Financial Trans.'!$AB:$AB,"Secured Borrowing",'Securities Financial Trans.'!$AN:$AN,"6 months to 1 year")
    -NSFR!$H$18-NSFR!$H$19-NSFR!$H$21

    Row 22 - Blank 3
    """

 

    condition_deposits = deposit[Days_To_Maturity] == "6 months to 1 year"
    condition_sec_fin_trans = (securities_financial_trans[Transaction_Type] == "Secured Borrowing") & (securities_financial_trans[Days_To_Maturity] == "6 months to 1 year")

    sum_AJ = deposit.loc[condition_deposits, Principal_Stable_Amount].sum()
    sum_AK = deposit.loc[condition_deposits, Principal_Unstable_Amount].sum()
    sum_Q = borrowings[Principal_Amount_6_months_to_1_year].sum()
    sum_G = securities_financial_trans.loc[condition_sec_fin_trans, Next_Principal_Payment_Amount].sum()

 

    # Subtract values from the NSFR DataFrame using the specific rows
    result = sum_AJ + sum_AK + sum_Q + sum_G - df.loc[row_H18, 'Blank 3'] - df.loc[row_H19, 'Blank 3'] - df.loc[row_H21, 'Blank 3']


    return result

def calc_sum38(deposit, borrowings, securities_financial_trans, df, Principal_Stable_Amount, Principal_Unstable_Amount, Days_to_Maturity, Principal_Amount_More_than_1_year, Next_Principal_Payment_Amount, Transaction_Type, Days_To_Maturity, row_I18, row_I19, row_I21):
    """
    This function replicates the following Excel operation in Python:
    =SUMIFS(Deposits!$AJ:$AJ,Deposits!$AG:$AG,"More than 1 year")
    +SUMIFS(Deposits!$AK:$AK,Deposits!$AG:$AG,"More than 1 year")
    +SUM(Borrowings!$R:$R)
    +SUMIFS('Securities Financial Trans.'!$G:$G,'Securities Financial Trans.'!$AB:$AB,"Secured Borrowing",'Securities Financial Trans.'!$AN:$AN,"More than 1 year")
    -NSFR!$I$18-NSFR!$I$19-NSFR!$I$21

    Row 22 - Blank 4
    """

 

    condition_deposits = deposit[Days_to_Maturity] == "More than 1 year"
    condition_sec_fin_trans = (securities_financial_trans[Transaction_Type] == "Secured Borrowing") & (securities_financial_trans[Days_To_Maturity] == "More than 1 year")

    sum_AJ = deposit.loc[condition_deposits, Principal_Stable_Amount].sum()
    sum_AK = deposit.loc[condition_deposits, Principal_Unstable_Amount].sum()
    sum_R = borrowings[Principal_Amount_More_than_1_year].sum()
    sum_G = securities_financial_trans.loc[condition_sec_fin_trans, Next_Principal_Payment_Amount].sum()

 

    # Subtract values from the NSFR DataFrame using the specific rows
    result = sum_AJ + sum_AK + sum_R + sum_G - df.loc[row_I18, 'Blank 4'] - df.loc[row_I19, 'Blank 4'] - df.loc[row_I21, 'Blank 4']

 
    return result

def calc_sum39(deposits, borrowings, securities_financial_trans, df, row_J18, row_J19, row_J21):
    """
    This function replicates the following Excel operation in Python:
    =SUM(Deposits!$AL:$AL)+SUM(Deposits!$AM:$AM)+SUM(Borrowings!AD:AD)
    +SUMIFS('Securities Financial Trans.'!$AZ:$AZ,'Securities Financial Trans.'!$AB:$AB,"Secured Borrowing",'Securities Financial Trans.'!$C:$C,"<>"&"Issued Securities")
    -$J$18-$J$19-$J$21

    Row 22 - Blank 5
    """

    # Sum of the values in Deposits DataFrame columns AL and AM
    sum_AL = deposits['Weighted Stable Amount'].sum()
    sum_AM = deposits['Weighted Unstable Amount'].sum()

    # Sum of the values in Borrowings DataFrame column AD
    sum_AD = borrowings['Total Principal ASF Amount'].sum()

    # Condition for 'Securities Financial Trans.' DataFrame
    condition_sec_fin_trans = (securities_financial_trans['Transaction Type'] == "Secured Borrowing") & (securities_financial_trans['Transaction Category'] != "Issued Securities")

    # Sum of the values in 'Securities Financial Trans.' DataFrame column AZ meeting the condition
    sum_AZ = securities_financial_trans.loc[condition_sec_fin_trans, 'Total ASF Amount'].sum()

    # Subtracting values at specific rows in column J (replace with actual column name if needed)
    result = sum_AL + sum_AM + sum_AD + sum_AZ -df.loc[row_J18, 'Blank 5'] - df.loc[row_J19, 'Blank 5'] - df.loc[row_J21, 'Blank 5']

    return result

def calc_sum40(df, start_row, end_row):
    """
    This function replicates the following Excel operation in Python:
    =SUM(F25:F26)
    Row 24 Blank 1
    """
    return df.loc[start_row:end_row, 'No maturity'].sum()

def calc_sum41(df, start_row, end_row):
    """
    This function replicates the following Excel operation in Python:
    =SUM(G25:G26,H26:I26)
    Row 24 Blank 2,3,4
    """
    sum_g = df.loc[start_row:end_row, 'Blank 2'].sum()
    sum_h_i = df.loc[end_row, 'Blank 3':'Blank 4'].sum()
    return sum_g + sum_h_i

def calc_sum42(df, start_row, end_row):
    """
    This function replicates the following Excel operation in Python:
    =SUM(J25:J26)
    Row 24 Blank 5
    """
    return df.loc[start_row:end_row, 'Blank 5'].sum()

def get_valueu9(derivatives):
    """
    This function replicates the following Excel operation in Python:
    =Derivatives!$U$9

    :param derivatives: DataFrame containing the 'Derivatives' data
    :return: Value from cell U9
    Row 44 - Blank 2,3,4
    """
    return derivatives['Total Derivatives Liabiilities'].iloc[0]

def get_value_u9(derivatives):
    """
    This function replicates the following Excel operation in Python:
    =Derivatives!$U$9
    Row 25 Blank 2,3,4
    """
    return -derivatives['Total Derivatives Liabiilities'].iloc[0]


def get_value_c35(other_items):
    """
    This function replicates the following Excel operation in Python:
    =Other Items!$C$35
    Row 26 Blank 1
    """
    return other_items.loc[23, 'AMOUNT ALL MATURITY']

def calc_sum43(issued_securities, borrowings, deposit, other_items):
    """
    Replicates the following Excel operation:
    =SUMIFS('Issued Securities'!$O:$O,'Issued Securities'!$AC:$AC,"Less than 6 months")
    +SUMIFS(Borrowings!$J:$J,Borrowings!$AE:$AE,"Less than 6 months")
    +SUMIFS(Deposits!$N:$N,Deposits!$AN:$AN,"Less than 6 months")
    +'Other Items'!$D$29+'Other Items'!$D$30
    """

    condition = "Less than 6 months"

    sum_issued_securities = issued_securities.loc[issued_securities['Remaining Maturity for Accrued Interest'] == condition, 'Accrued Interest'].sum()
    sum_borrowings = borrowings.loc[borrowings['Remaining Maturity for Accrued Interest'] == condition, 'Accrued Interest'].sum()
    sum_deposits = deposit.loc[deposit['Remaining Maturity for Accrued Interest'] == condition, ' Accrued Interest '].sum()
    other_items_d29 = other_items.loc[18, 'AMOUNT UNDER 6M']
    other_items_d30 = other_items.loc[19, 'AMOUNT UNDER 6M']

    total_sum = sum_issued_securities + sum_borrowings + sum_deposits + other_items_d29 + other_items_d30
    return total_sum

def calc_sum44(issued_securities, borrowings, deposit, other_items):
    """
    Replicates the following Excel operation:
    =SUMIFS('Issued Securities'!$O:$O,'Issued Securities'!$AC:$AC,"6 months to 1 year")
    +SUMIFS(Borrowings!$J:$J,Borrowings!$AE:$AE,"6 months to 1 year")
    +SUMIFS(Deposits!$N:$N,Deposits!$AN:$AN,"6 months to 1 year")
    +'Other Items'!$E$29+'Other Items'!$E$30

    Row 26 - Blank 3
    """

    condition = "6 months to 1 year"

    sum_issued_securities = issued_securities.loc[issued_securities['Remaining Maturity for Accrued Interest'] == condition, 'Accrued Interest'].sum()
    sum_borrowings = borrowings.loc[borrowings['Remaining Maturity for Accrued Interest'] == condition, 'Accrued Interest'].sum()
    sum_deposits = deposit.loc[deposit['Remaining Maturity for Accrued Interest'] == condition, ' Accrued Interest '].sum()
    other_items_e29 = other_items.loc[18, 'AMOUNT 6M TO 1Y']
    other_items_e30 = other_items.loc[19, 'AMOUNT 6M TO 1Y']

    total_sum = sum_issued_securities + sum_borrowings + sum_deposits + other_items_e29 + other_items_e30
    return total_sum

def calc_sum45(issued_securities, borrowings, deposit, other_items):
    """
    Replicates the following Excel operation:
    =SUMIFS('Issued Securities'!$O:$O,'Issued Securities'!$AC:$AC,"More than 1 year")
    +SUMIFS(Borrowings!$J:$J,Borrowings!$AE:$AE,"More than 1 year")
    +SUMIFS(Deposits!$N:$N,Deposits!$AN:$AN,"More than 1 year")
    +'Other Items'!$F$29+'Other Items'!$F$30

    Row 26 Blank 4
    """

    condition = "More than 1 year"

    sum_issued_securities = issued_securities.loc[issued_securities['Remaining Maturity for Accrued Interest'] == condition, 'Accrued Interest'].sum()
    sum_borrowings = borrowings.loc[borrowings['Remaining Maturity for Accrued Interest'] == condition, 'Accrued Interest'].sum()
    sum_deposits = deposit.loc[deposit['Remaining Maturity for Accrued Interest'] == condition, ' Accrued Interest '].sum()
    other_items_f29 = other_items.loc[18, 'AMOUNT ABOVE 1Y']
    other_items_f30 = other_items.loc[19, 'AMOUNT ABOVE 1Y']

    total_sum = sum_issued_securities + sum_borrowings + sum_deposits + other_items_f29 + other_items_f30
    return total_sum

def calc_sum46(issued_securities, borrowings, deposit, other_items):
    """
    Replicates the following Excel operation:
    =SUM('Issued Securities'!$AE:$AE)+SUM(Borrowings!$AG:$AG)+SUM(Deposits!$AP:$AP)
    +'Other Items'!$O$29+'Other Items'!$O$30+'Other Items'!$O$35

    Row 26 - Blank 5
    """

    sum_issued_securities = issued_securities['ASF Amount for Accrued Interest'].sum()
    sum_borrowings = borrowings['Total Interest ASF Amount'].sum()
    sum_deposits = deposit['ASF Amount for Accrued Interest'].sum()

    other_items_o29 = other_items.loc[18, 'WEIGHTED ASF AMOUNT']
    other_items_o30 = other_items.loc[19, 'WEIGHTED ASF AMOUNT']
    other_items_o35 = other_items.loc[23, 'WEIGHTED ASF AMOUNT']

    total_sum = sum_issued_securities + sum_borrowings + sum_deposits + other_items_o29 + other_items_o30 + other_items_o35
    return total_sum

def calc_sum47(df, J_row14, J_row17, J_row20, J_row23, J_row24):
    """
    This function replicates the following Excel operation:
    =SUM(J14,J17,J20,J23,J24)
    Row 27 Blank 5
    """
    return df.loc[J_row14, 'Blank 5'] + df.loc[J_row17, 'Blank 5'] + df.loc[J_row20, 'Blank 5'] + df.loc[J_row23, 'Blank 5'] + df.loc[J_row24, 'Blank 5']

def calc_sum48(investment_trading_securities, other_items):
    """
    =SUMIFS('Investment&Trading Securities'!$AT:$AT,'Investment&Trading Securities'!$AD:$AD,"L1")
    +SUMIFS('Investment&Trading Securities'!$AT:$AT,'Investment&Trading Securities'!$AD:$AD,"L2A")
    +SUMIFS('Investment&Trading Securities'!$AT:$AT,'Investment&Trading Securities'!$AD:$AD,"L2B",'Investment&Trading Securities'!$Y:$Y,"<>"&"Equity")
    +SUM('Other Items'!$K$11:$K$12)
    :param df_investment_trading: DataFrame containing 'Investment&Trading Securities' data
    :param df_other_items: DataFrame containing 'Other Items' data
    :return: Calculated sum
    Row 29 Blank 5
    """
    sum_l1 = investment_trading_securities[(investment_trading_securities['HQLA Asset'] == "L1")]['RSF Amount'].sum()
    sum_l2a = investment_trading_securities[(investment_trading_securities['HQLA Asset'] == "L2A")]['RSF Amount'].sum()
    sum_l2b = investment_trading_securities[(investment_trading_securities['HQLA Asset'] == "L2B") & (investment_trading_securities['Mapped Product Type'] != "Equity")]['RSF Amount'].sum()
    sum_other_items = other_items.loc[1:2, 'WEIGHTED RSF AMOUNT'].sum()

    return sum_l1 + sum_l2a + sum_l2b + sum_other_items

def calc_sum49(dep_w_other_banks_nsfr):
    """
    :param deposits_with_banks: DataFrame containing 'Deposits with Other Banks' data
    :return: Calculated sum
    Row 30 - Blank 1
    """
    sum_result = dep_w_other_banks_nsfr[
        (dep_w_other_banks_nsfr['Maturity Bucket'] == "No Maturity") & 
        (dep_w_other_banks_nsfr['Operational'] == "Yes")
    ]['Deposit balance'].sum()

    return sum_result

def calc_sum50(dep_w_other_banks_nsfr):
    """
    :param df_deposits_with_banks: DataFrame containing 'Deposits with Other Banks' data
    :return: Calculated sum

    Row 30 - Blank 2
    """
    sum_result = dep_w_other_banks_nsfr[
        (dep_w_other_banks_nsfr['Maturity Bucket'] == "Less than 6 months") & 
        (dep_w_other_banks_nsfr['Operational'] == "Yes")
    ]['Deposit balance'].sum()

    return sum_result

def calc_sum51(dep_w_other_banks_nsfr):
    """
    =SUMIFS('Deposits with Other Banks'!$F:$F,'Deposits with Other Banks'!$Q:$Q,"6 months to 1 year",'Deposits with Other Banks'!$C:$C,"Yes")
    This function calculates the sum of deposits with other banks that have a maturity of "6 months to 1 year" and meet a specific condition.

    :param df_deposits_with_banks: DataFrame containing 'Deposits with Other Banks' data
    :return: Calculated sum

    Row 30 - Blank 3
    """
    sum_result = dep_w_other_banks_nsfr[
        (dep_w_other_banks_nsfr['Maturity Bucket'] == "6 months to 1 year") & 
        (dep_w_other_banks_nsfr['Operational'] == "Yes")
    ]['Deposit balance'].sum()

    return sum_result

def calc_sum52(dep_w_other_banks_nsfr):
    """

    =SUMIFS('Deposits with Other Banks'!$F:$F,'Deposits with Other Banks'!$Q:$Q,"More than 1 year",'Deposits with Other Banks'!$C:$C,"Yes")
    This function calculates the sum of deposits with other banks that have a maturity of "More than 1 year" and meet a specific condition.

 

    :param df_deposits_with_banks: DataFrame containing 'Deposits with Other Banks' data
    :return: Calculated sum

    Row 30 - Blank 4
    """
    sum_result = dep_w_other_banks_nsfr[
        (dep_w_other_banks_nsfr['Maturity Bucket'] == "More than 1 year") & 
        (dep_w_other_banks_nsfr['Operational'] == "Yes")
    ]['Deposit balance'].sum()

    return sum_result

def calc_sum53(dep_w_other_banks_nsfr):
    """

    =SUMIFS('Deposits with Other Banks'!$S:$S,'Deposits with Other Banks'!$C:$C,"Yes")
    This function calculates the sum of a specific column in the 'Deposits with Other Banks' data that meets a specific condition.

    :param df_deposits_with_banks: DataFrame containing 'Deposits with Other Banks' data
    :return: Calculated sum

    Row 30 - Blank 5
    """
    sum_result = dep_w_other_banks_nsfr[dep_w_other_banks_nsfr['Operational'] == "Yes"]['RSF Amount'].sum()

    return sum_result

def calc_sum54(df, start_row, end_row):
    """
    =SUM(F32:F38)
    :param df: DataFrame containing the data
    :param start_row: Starting row index (0-based)
    :param end_row: Ending row index (0-based)
    :return: Calculated sum

    Row 31 - Blank 1
    """
    sum_result = df.loc[start_row:end_row, 'Blank 1'].sum()

    return sum_result

def calc_sum55(df, start_row, end_row):
    """
    =SUM(G32:G38)
    :param df: DataFrame containing the data
    :param start_row: Starting row index (0-based)
    :param end_row: Ending row index (0-based)
    :return: Calculated sum

    Row 31 - Blank 2
    """
    sum_result = df.loc[start_row:end_row, 'Blank 2'].sum()

    return sum_result

def calc_sum56(df, start_row, end_row):
    """
    =SUM(H32:H38)
    :param df: DataFrame containing the data
    :param start_row: Starting row index (0-based)
    :param end_row: Ending row index (0-based)
    :return: Calculated sum

    Row 31 - Blank 3
    """
    sum_result = df.loc[start_row:end_row, 'Blank 3'].sum()

    return sum_result

def calc_sum57(df, start_row, end_row):
    """
    =SUM(I32:I38)
    :param df: DataFrame containing the data
    :param start_row: Starting row index (0-based)
    :param end_row: Ending row index (0-based)
    :return: Calculated sum

    Row 31 - Blank 4
    """
    sum_result = df.loc[start_row:end_row, 'Blank 4'].sum()

    return sum_result

def calc_sum58(df, start_row, end_row):
    """
    =SUM(J32:J38)
    :param df: DataFrame containing the data
    :param start_row: Starting row index (0-based)
    :param end_row: Ending row index (0-based)
    :return: Calculated sum

    Row 31 - Blank 5
    """
    sum_result = df.loc[start_row:end_row, 'Blank 5'].sum()

    return sum_result

def calc_sum59(securities_financial_trans, loans_and_advances):
    """
    =SUMIFS('Securities Financial Trans.'!$G:$G,'Securities Financial Trans.'!$AP:$AP,"L1",'Securities Financial Trans.'!$AN:$AN,"Less than 6 months")+SUMIFS('Loans & Advances'!$F:$F,'Loans & Advances'!$AB:$AB,"L1",'Loans & Advances'!$AA:$AA,"Less than 6 months",'Loans & Advances'!$I:$I,">"&"0",'Loans & Advances'!$I:$I,"<"&"3")
    :param df_securities: DataFrame containing the 'Securities Financial Trans.' data
    :param df_loans: DataFrame containing the 'Loans & Advances' data
    :return: Calculated sum

    Row 32 - Blank 2
    """
    # Sum from 'Securities Financial Trans.'
    sum_securities = securities_financial_trans[
        (securities_financial_trans['Collateral Asset level'] == "L1") & 
        (securities_financial_trans['Days To Maturity'] == "Less than 6 months")
    ]['Next Principal Payment Amount'].sum()

    # Sum from 'Loans & Advances'
    sum_loans = loans_and_advances[
        (loans_and_advances['Collateral Asset level'] == "L1") &
        (loans_and_advances['Days to Maturity'] == "Less than 6 months") &
        (loans_and_advances['Loan Group'] > 0) &
        (loans_and_advances['Loan Group'] < 3)
    ]['Loan Outstanding'].sum()

    total_sum = sum_securities + sum_loans

    return total_sum

def calc_sum60(securities_financial_trans, loans_and_advances):
    """
    =SUMIFS('Securities Financial Trans.'!$G:$G,'Securities Financial Trans.'!$AP:$AP,"L1",'Securities Financial Trans.'!$AN:$AN,"6 months to 1 year")+SUMIFS('Loans & Advances'!$F:$F,'Loans & Advances'!$AB:$AB,"L1",'Loans & Advances'!$AA:$AA,"6 months to 1 year",'Loans & Advances'!$I:$I,">"&"0",'Loans & Advances'!$I:$I,"<"&"3")
    :param df_securities: DataFrame containing the 'Securities Financial Trans.' data
    :param df_loans: DataFrame containing the 'Loans & Advances' data
    :return: Calculated sum

    Row 32 - Blank 3
    """
    # Sum from 'Securities Financial Trans.'
    sum_securities = securities_financial_trans[
        (securities_financial_trans['Collateral Asset level'] == "L1") & 
        (securities_financial_trans['Days To Maturity'] == "6 months to 1 year")
    ]['Next Principal Payment Amount'].sum()

    # Sum from 'Loans & Advances'
    sum_loans = loans_and_advances[
        (loans_and_advances['Collateral Asset level'] == "L1") &
        (loans_and_advances['Days to Maturity'] == "6 months to 1 year") &
        (loans_and_advances['Loan Group'] > 0) &
        (loans_and_advances['Loan Group'] < 3)
    ]['Loan Outstanding'].sum()

    total_sum = sum_securities + sum_loans

    return total_sum

def calc_sum61(securities_financial_trans, loans_and_advances):
    """
    =SUMIFS('Securities Financial Trans.'!$G:$G,'Securities Financial Trans.'!$AP:$AP,"L1",'Securities Financial Trans.'!$AN:$AN,"More than 1 year")+SUMIFS('Loans & Advances'!$F:$F,'Loans & Advances'!$AB:$AB,"L1",'Loans & Advances'!$AA:$AA,"More than 1 year",'Loans & Advances'!$I:$I,">"&"0",'Loans & Advances'!$I:$I,"<"&"3")
    :param df_securities: DataFrame containing the 'Securities Financial Trans.' data
    :param df_loans: DataFrame containing the 'Loans & Advances' data
    :return: Calculated sum

    Row 32 - Blank 4
    """
    # Sum from 'Securities Financial Trans.'
    sum_securities = securities_financial_trans[
        (securities_financial_trans['Collateral Asset level'] == "L1") & 
        (securities_financial_trans['Days To Maturity'] == "More than 1 year")
    ]['Next Principal Payment Amount'].sum()

    # Sum from 'Loans & Advances'
    sum_loans = loans_and_advances[
        (loans_and_advances['Collateral Asset level'] == "L1") &
        (loans_and_advances['Days to Maturity'] == "More than 1 year") &
        (loans_and_advances['Loan Group'] > 0) &
        (loans_and_advances['Loan Group'] < 3)
    ]['Loan Outstanding'].sum()

    total_sum = sum_securities + sum_loans

    return total_sum

def calc_sum62(securities_financial_trans, loans_and_advances):
    """
    =SUMIFS('Securities Financial Trans.'!$AT:$AT,'Securities Financial Trans.'!$AP:$AP,"L1")+SUMIFS('Loans & Advances'!$AE:$AE,'Loans & Advances'!$AB:$AB,"L1",'Loans & Advances'!$I:$I,">"&"0",'Loans & Advances'!$I:$I,"<"&"3")
    :param df_securities: DataFrame containing the 'Securities Financial Trans.' data
    :param df_loans: DataFrame containing the 'Loans & Advances' data
    :return: Calculated sum

    Row 32 - Blank 5
    """
    # Sum from 'Securities Financial Trans.'
    sum_securities = securities_financial_trans[
        (securities_financial_trans['Collateral Asset level'] == "L1")
    ]['Total RSF Amount'].sum()

    # Sum from 'Loans & Advances'
    sum_loans = loans_and_advances[
        (loans_and_advances['Collateral Asset level'] == "L1") &
        (loans_and_advances['Loan Group'] > 0) &
        (loans_and_advances['Loan Group'] < 3)
    ]['RSF Amount'].sum()

    total_sum = sum_securities + sum_loans

    return total_sum

def calc_sum63(dep_w_other_banks_nsfr):
    """
    =SUMIFS('Deposits with Other Banks'!$F:$F,'Deposits with Other Banks'!$Q:$Q,"No Maturity") 

    :param df: DataFrame containing the 'Deposits with Other Banks' data
    :return: Calculated sum

    Row 33 - Blank 1
    """
    return dep_w_other_banks_nsfr.loc[dep_w_other_banks_nsfr['Maturity Bucket'] == "No Maturity", 'Deposit balance'].sum()

def calc_sum64(securities_financial_trans, loans_and_advances, dep_w_other_banks_nsfr):
    """
    =SUMIFS('Securities Financial Trans.'!$G:$G,'Securities Financial Trans.'!$AP:$AP,"<>"&"L1",'Securities Financial Trans.'!$AN:$AN,"Less than 6 months",'Securities Financial Trans.'!$AD:$AD,"FIs")
    +SUMIFS('Loans & Advances'!$F:$F,'Loans & Advances'!$AB:$AB,"<>"&"L1",'Loans & Advances'!$AA:$AA,"Less than 6 months",'Loans & Advances'!$I:$I,">"&"0",'Loans & Advances'!$I:$I,"<"&"3",'Loans & Advances'!$S:$S,"FIs")
    +SUMIFS('Deposits with Other Banks'!$F:$F,'Deposits with Other Banks'!$Q:$Q,"Less than 6 months")

    :param securities_financial_trans: DataFrame containing the 'Securities Financial Trans.' data
    :param loans_and_advances: DataFrame containing the 'Loans & Advances' data
    :param deposits_with_other_banks: DataFrame containing the 'Deposits with Other Banks' data
    :return: Calculated sum
    Row 33 - Blank 2
    """
    sum_part1 = securities_financial_trans.loc[
        (securities_financial_trans['Collateral Asset level'] != 'L1') &
        (securities_financial_trans['Days To Maturity'] == 'Less than 6 months') &
        (securities_financial_trans['Underlying Asset Counterparty'] == 'FIs'),
        'Next Principal Payment Amount'].sum()

    sum_part2 = loans_and_advances.loc[
        (loans_and_advances['Collateral Asset level'] != 'L1') &
        (loans_and_advances['Days to Maturity'] == 'Less than 6 months') &
        (loans_and_advances['Loan Group'] > 0) &
        (loans_and_advances['Loan Group'] < 3) &
        (loans_and_advances['Counterparty Category'] == 'FIs'),
        'Loan Outstanding'].sum()

    sum_part3 = dep_w_other_banks_nsfr.loc[
        dep_w_other_banks_nsfr['Maturity Bucket'] == 'Less than 6 months',
        'Deposit balance'].sum()

    return sum_part1 + sum_part2 + sum_part3

def calc_sum65(securities_financial_trans, loans_and_advances, dep_w_other_banks_nsfr):
    """
    =SUMIFS('Securities Financial Trans.'!$G:$G,'Securities Financial Trans.'!$AP:$AP,"<>"&"L1",'Securities Financial Trans.'!$AN:$AN,"6 months to 1 year",'Securities Financial Trans.'!$AD:$AD,"FIs")
    +SUMIFS('Loans & Advances'!$F:$F,'Loans & Advances'!$AB:$AB,"<>"&"L1",'Loans & Advances'!$AA:$AA,"6 months to 1 year",'Loans & Advances'!$I:$I,">"&"0",'Loans & Advances'!$I:$I,"<"&"3",'Loans & Advances'!$S:$S,"FIs")
    +SUMIFS('Deposits with Other Banks'!$F:$F,'Deposits with Other Banks'!$Q:$Q,"6 months to 1 year")

    :param securities_financial_trans: DataFrame containing the 'Securities Financial Trans.' data
    :param loans_and_advances: DataFrame containing the 'Loans & Advances' data
    :param deposits_with_other_banks: DataFrame containing the 'Deposits with Other Banks' data
    :return: Calculated sum

    Row 33 - Blank 3
    """
    sum_part1 = securities_financial_trans.loc[
        (securities_financial_trans['Collateral Asset level'] != 'L1') &
        (securities_financial_trans['Days To Maturity'] == '6 months to 1 year') &
        (securities_financial_trans['Underlying Asset Counterparty'] == 'FIs'),
        'Next Principal Payment Amount'].sum()

    sum_part2 = loans_and_advances.loc[
        (loans_and_advances['Collateral Asset level'] != 'L1') &
        (loans_and_advances['Days to Maturity'] == '6 months to 1 year') &
        (loans_and_advances['Loan Group'] > 0) &
        (loans_and_advances['Loan Group'] < 3) &
        (loans_and_advances['Counterparty Category'] == 'FIs'),
        'Loan Outstanding'].sum()

    sum_part3 = dep_w_other_banks_nsfr.loc[
        dep_w_other_banks_nsfr['Maturity Bucket'] == '6 months to 1 year',
        'Deposit balance'].sum()

    return sum_part1 + sum_part2 + sum_part3

def calc_sum66(securities_financial_trans, loans_and_advances, dep_w_other_banks_nsfr):
    """
    This function replicates the following Excel operation in Python:
    =SUMIFS('Securities Financial Trans.'!$G:$G,'Securities Financial Trans.'!$AP:$AP,"<>"&"L1",'Securities Financial Trans.'!$AN:$AN,"More than 1 year",'Securities Financial Trans.'!$AD:$AD,"FIs")
    +SUMIFS('Loans & Advances'!$F:$F,'Loans & Advances'!$AB:$AB,"<>"&"L1",'Loans & Advances'!$AA:$AA,"More than 1 year",'Loans & Advances'!$I:$I,">"&"0",'Loans & Advances'!$I:$I,"<"&"3",'Loans & Advances'!$S:$S,"FIs")
    +SUMIFS('Deposits with Other Banks'!$F:$F,'Deposits with Other Banks'!$Q:$Q,"More than 1 year")

 

    :param securities_financial_trans: DataFrame containing the 'Securities Financial Trans.' data
    :param loans_and_advances: DataFrame containing the 'Loans & Advances' data
    :param deposits_with_other_banks: DataFrame containing the 'Deposits with Other Banks' data
    :return: Calculated sum

    Row 33 - Blank 4
    """
    sum_part1 = securities_financial_trans.loc[
        (securities_financial_trans['Collateral Asset level'] != 'L1') &
        (securities_financial_trans['Days To Maturity'] == 'More than 1 year') &
        (securities_financial_trans['Underlying Asset Counterparty'] == 'FIs'),
        'Next Principal Payment Amount'].sum()

    sum_part2 = loans_and_advances.loc[
        (loans_and_advances['Collateral Asset level'] != 'L1') &
        (loans_and_advances['Days to Maturity'] == 'More than 1 year') &
        (loans_and_advances['Loan Group'] > 0) &
        (loans_and_advances['Loan Group'] < 3) &
        (loans_and_advances['Counterparty Category'] == 'FIs'),
        'Loan Outstanding'].sum()

    sum_part3 = dep_w_other_banks_nsfr.loc[
        dep_w_other_banks_nsfr['Maturity Bucket'] == 'More than 1 year',
        'Deposit balance'].sum()

    return sum_part1 + sum_part2 + sum_part3

def calc_sum67(securities_financial_trans, loans_and_advances, dep_w_other_banks_nsfr):
    """
    This function replicates the following Excel operation in Python:
    =SUMIFS('Securities Financial Trans.'!$AT:$AT,'Securities Financial Trans.'!$AP:$AP,"<>"&"L1",'Securities Financial Trans.'!$AD:$AD,"FIs")
    +SUMIFS('Loans & Advances'!$AE:$AE,'Loans & Advances'!$AB:$AB,"<>"&"L1",'Loans & Advances'!$I:$I,">"&"0",'Loans & Advances'!$I:$I,"<"&"3",'Loans & Advances'!$S:$S,"FIs")
    +SUM('Deposits with Other Banks'!$S:$S)

 

    :param securities_financial_trans: DataFrame containing the 'Securities Financial Trans.' data
    :param loans_and_advances: DataFrame containing the 'Loans & Advances' data
    :param deposits_with_other_banks: DataFrame containing the 'Deposits with Other Banks' data
    :return: Calculated sum

    Row 33 - Blank 5
    """
    sum_part1 = securities_financial_trans.loc[
        (securities_financial_trans['Collateral Asset level'] != 'L1') &
        (securities_financial_trans['Underlying Asset Counterparty'] == 'FIs'),
        'Total RSF Amount'].sum()

    sum_part2 = loans_and_advances.loc[
        (loans_and_advances['Collateral Asset level'] != 'L1') &
        (loans_and_advances['Loan Group'] > 0) &
        (loans_and_advances['Loan Group'] < 3) &
        (loans_and_advances['Counterparty Category'] == 'FIs'),
        'RSF Amount'].sum()

    sum_part3 = dep_w_other_banks_nsfr['RSF Amount'].sum()

    return sum_part1 + sum_part2 + sum_part3

def calc_sum68(securities_financial_trans, loans_and_advances):
    """
    This function replicates the following Excel operation in Python:
    =SUM(SUMIFS('Securities Financial Trans.'!$G:$G,'Securities Financial Trans.'!$AN:$AN,"Less than 6 months",'Securities Financial Trans.'!$AD:$AD,{"Domestic Sovereign","Foreign Sovereign","Small Business Customer","Retail","Corp","PSEs"},'Securities Financial Trans.'!$U:$U,">"&"35%"))
    +SUM(SUMIFS('Loans & Advances'!$F:$F,'Loans & Advances'!$AA:$AA,"Less than 6 months",'Loans & Advances'!$I:$I,">"&"0",'Loans & Advances'!$I:$I,"<"&"3",'Loans & Advances'!$S:$S,{"Domestic Sovereign","Foreign Sovereign","Small Business Customer","Retail","Corp","PSEs"},'Loans & Advances'!$O:$O,">"&"35%"))

 

    :param securities_financial_trans: DataFrame containing the 'Securities Financial Trans.' data
    :param loans_and_advances: DataFrame containing the 'Loans & Advances' data
    :return: Calculated sum

    Row 34 - Blank 2
    """
    criteria_values = ["Domestic Sovereign", "Foreign Sovereign", "Small Business Customer", "Retail", "Corp", "PSEs"]

    sum_part1 = securities_financial_trans.loc[
        (securities_financial_trans['Days To Maturity'] == 'Less than 6 months') &
        (securities_financial_trans['Underlying Asset Counterparty'].isin(criteria_values)) &
        (securities_financial_trans['Underlying Asset Issuer C41 Risk Weight'] > 0.35),
        'Next Principal Payment Amount'].sum()

    sum_part2 = loans_and_advances.loc[
        (loans_and_advances['Days to Maturity'] == 'Less than 6 months') &
        (loans_and_advances['Loan Group'] > 0) &
        (loans_and_advances['Loan Group'] < 3) &
        (loans_and_advances['Counterparty Category'].isin(criteria_values)) &
        (loans_and_advances['Risk Weight  as per C41'] > 0.35),
        'Loan Outstanding'].sum()

    return sum_part1 + sum_part2

def calc_sum69(securities_financial_trans, loans_and_advances):
    """
    This function replicates the following Excel operation in Python:
    =SUM(SUMIFS('Securities Financial Trans.'!$G:$G,'Securities Financial Trans.'!$AN:$AN,"6 months to 1 year",'Securities Financial Trans.'!$AD:$AD,{"Domestic Sovereign","Foreign Sovereign","Small Business Customer","Retail","Corp","PSEs"},'Securities Financial Trans.'!$U:$U,">"&"35%"))
    +SUM(SUMIFS('Loans & Advances'!$F:$F,'Loans & Advances'!$AA:$AA,"6 months to 1 year",'Loans & Advances'!$I:$I,">"&"0",'Loans & Advances'!$I:$I,"<"&"3",'Loans & Advances'!$S:$S,{"Domestic Sovereign","Foreign Sovereign","Small Business Customer","Retail","Corp","PSEs"},'Loans & Advances'!$O:$O,">"&"35%"))

 

    :param securities_financial_trans: DataFrame containing the 'Securities Financial Trans.' data
    :param loans_and_advances: DataFrame containing the 'Loans & Advances' data
    :return: Calculated sum

    Row 34 - Blank 3
    """
    criteria_values = ["Domestic Sovereign", "Foreign Sovereign", "Small Business Customer", "Retail", "Corp", "PSEs"]

    sum_part1 = securities_financial_trans.loc[
        (securities_financial_trans['Days To Maturity'] == '6 months to 1 year') &
        (securities_financial_trans['Underlying Asset Counterparty'].isin(criteria_values)) &
        (securities_financial_trans['Underlying Asset Issuer C41 Risk Weight'] > 0.35),
        'Next Principal Payment Amount'].sum()

    sum_part2 = loans_and_advances.loc[
        (loans_and_advances['Days to Maturity'] == '6 months to 1 year') &
        (loans_and_advances['Loan Group'] > 0) &
        (loans_and_advances['Loan Group'] < 3) &
        (loans_and_advances['Counterparty Category'].isin(criteria_values)) &
        (loans_and_advances['Risk Weight  as per C41'] > 0.35),
        'Loan Outstanding'].sum()

    return sum_part1 + sum_part2

def calc_sum70(securities_financial_trans, loans_and_advances):
    """
    This function replicates the following Excel operation in Python:
    =SUM(SUMIFS('Securities Financial Trans.'!$G:$G,'Securities Financial Trans.'!$AN:$AN,"More than 1 year",'Securities Financial Trans.'!$AD:$AD,{"Domestic Sovereign","Foreign Sovereign","Small Business Customer","Retail","Corp","PSEs"},'Securities Financial Trans.'!$U:$U,">"&"35%"))
    +SUM(SUMIFS('Loans & Advances'!$F:$F,'Loans & Advances'!$AA:$AA,"More than 1 year",'Loans & Advances'!$I:$I,">"&"0",'Loans & Advances'!$I:$I,"<"&"3",'Loans & Advances'!$S:$S,{"Domestic Sovereign","Foreign Sovereign","Small Business Customer","Retail","Corp","PSEs"},'Loans & Advances'!$O:$O,">"&"35%"))

 

    :param securities_financial_trans: DataFrame containing the 'Securities Financial Trans.' data
    :param loans_and_advances: DataFrame containing the 'Loans & Advances' data
    :return: Calculated sum

    Row 34 - Blank 4
    """
    criteria_values = ["Domestic Sovereign", "Foreign Sovereign", "Small Business Customer", "Retail", "Corp", "PSEs"]

    sum_part1 = securities_financial_trans.loc[
        (securities_financial_trans['Days To Maturity'] == 'More than 1 year') &
        (securities_financial_trans['Underlying Asset Counterparty'].isin(criteria_values)) &
        (securities_financial_trans['Underlying Asset Issuer C41 Risk Weight'] > 0.35),
        'Next Principal Payment Amount'].sum()

    sum_part2 = loans_and_advances.loc[
        (loans_and_advances['Days to Maturity'] == 'More than 1 year') &
        (loans_and_advances['Loan Group'] > 0) &
        (loans_and_advances['Loan Group'] < 3) &
        (loans_and_advances['Counterparty Category'].isin(criteria_values)) &
        (loans_and_advances['Risk Weight  as per C41'] > 0.35),
        'Loan Outstanding'].sum()

    return sum_part1 + sum_part2

def calc_sum71(securities_financial_trans, loans_and_advances):
    """
    This function replicates the following Excel operation in Python:
    =SUM(SUMIFS('Securities Financial Trans.'!$AT:$AT,'Securities Financial Trans.'!$AD:$AD,{"Domestic Sovereign","Foreign Sovereign","SMEs","Retail","Corp","PSEs"},'Securities Financial Trans.'!$U:$U,">"&"35%"))
    +SUM(SUMIFS('Loans & Advances'!$AE:$AE,'Loans & Advances'!$I:$I,">"&"0",'Loans & Advances'!$I:$I,"<"&"3",'Loans & Advances'!$S:$S,{"Domestic Sovereign","Foreign Sovereign","SMEs","Retail","Corp","PSEs"},'Loans & Advances'!$O:$O,">"&"35%"))

 

    :param securities_financial_trans: DataFrame containing the 'Securities Financial Trans.' data
    :param loans_and_advances: DataFrame containing the 'Loans & Advances' data
    :return: Calculated sum

    Row 34 - Blank 5
    """
    criteria_values = ["Domestic Sovereign", "Foreign Sovereign", "SMEs", "Retail", "Corp", "PSEs"]

    sum_part1 = securities_financial_trans.loc[
        (securities_financial_trans['Underlying Asset Counterparty'].isin(criteria_values)) &
        (securities_financial_trans['Underlying Asset Issuer C41 Risk Weight'] > 0.35),
        'Total RSF Amount'].sum()

    sum_part2 = loans_and_advances.loc[
        (loans_and_advances['Loan Group'] > 0) &
        (loans_and_advances['Loan Group'] < 3) &
        (loans_and_advances['Counterparty Category'].isin(criteria_values)) &
        (loans_and_advances['Risk Weight  as per C41'] > 0.35),
        'RSF Amount'].sum()

    return sum_part1 + sum_part2

def calc_sum72(securities_financial_trans, loans_and_advances):
    """
    This function replicates the following Excel operation in Python:
    =SUM(SUMIFS('Securities Financial Trans.'!$G:$G,'Securities Financial Trans.'!$AN:$AN,"Less than 6 months",'Securities Financial Trans.'!$AD:$AD,{"Domestic Sovereign","Foreign Sovereign","SMEs","Retail","Corp","PSEs"},'Securities Financial Trans.'!$U:$U,"<="&"35%"))
    +SUM(SUMIFS('Loans & Advances'!$F:$F,'Loans & Advances'!$AA:$AA,"Less than 6 months",'Loans & Advances'!$I:$I,">"&"0",'Loans & Advances'!$I:$I,"<"&"3",'Loans & Advances'!$S:$S,{"Domestic Sovereign","Foreign Sovereign","SMEs","Retail","Corp","PSEs"},'Loans & Advances'!$O:$O,"<="&"35%"))

 

    :param securities_financial_trans: DataFrame containing the 'Securities Financial Trans.' data
    :param loans_and_advances: DataFrame containing the 'Loans & Advances' data
    :return: Calculated sum

    Row 35 - Blank 2
    """
    criteria_values = ["Domestic Sovereign", "Foreign Sovereign", "SMEs", "Retail", "Corp", "PSEs"]

    sum_part1 = securities_financial_trans.loc[
        (securities_financial_trans['Days To Maturity'] == 'Less than 6 months') &
        (securities_financial_trans['Underlying Asset Counterparty'].isin(criteria_values)) &
        (securities_financial_trans['Underlying Asset Issuer C41 Risk Weight'] <= 0.35),
        'Next Principal Payment Amount'].sum()

    sum_part2 = loans_and_advances.loc[
        (loans_and_advances['Days to Maturity'] == 'Less than 6 months') &
        (loans_and_advances['Loan Group'] > 0) &
        (loans_and_advances['Loan Group'] < 3) &
        (loans_and_advances['Counterparty Category'].isin(criteria_values)) &
        (loans_and_advances['Risk Weight  as per C41'] <= 0.35),
        'Loan Outstanding'].sum()

    return sum_part1 + sum_part2

def calc_sum73(securities_financial_trans, loans_and_advances):
    """
    =SUM(SUMIFS('Securities Financial Trans.'!$G:$G,'Securities Financial Trans.'!$AN:$AN,"6 months to 1 year",'Securities Financial Trans.'!$AD:$AD,{"Domestic Sovereign","Foreign Sovereign","SMEs","Retail","Corp","PSEs"},'Securities Financial Trans.'!$U:$U,"<="&"35%"))
    +SUM(SUMIFS('Loans & Advances'!$F:$F,'Loans & Advances'!$AA:$AA,"6 months to 1 year",'Loans & Advances'!$I:$I,">"&"0",'Loans & Advances'!$I:$I,"<"&"3",'Loans & Advances'!$S:$S,{"Domestic Sovereign","Foreign Sovereign","SMEs","Retail","Corp","PSEs"},'Loans & Advances'!$O:$O,"<="&"35%"))

    :param securities_financial_trans: DataFrame containing the 'Securities Financial Trans.' data
    :param loans_and_advances: DataFrame containing the 'Loans & Advances' data
    :return: Calculated sum

    Row 35 - Blank 3
    """
    criteria_values = ["Domestic Sovereign", "Foreign Sovereign", "SMEs", "Retail", "Corp", "PSEs"]

    sum_part1 = securities_financial_trans.loc[
        (securities_financial_trans['Days To Maturity'] == '6 months to 1 year') &
        (securities_financial_trans['Underlying Asset Counterparty'].isin(criteria_values)) &
        (securities_financial_trans['Underlying Asset Issuer C41 Risk Weight'] <= 0.35),
        'Next Principal Payment Amount'].sum()

    sum_part2 = loans_and_advances.loc[
        (loans_and_advances['Days to Maturity'] == '6 months to 1 year') &
        (loans_and_advances['Loan Group'] > 0) &
        (loans_and_advances['Loan Group'] < 3) &
        (loans_and_advances['Counterparty Category'].isin(criteria_values)) &
        (loans_and_advances['Risk Weight  as per C41'] <= 0.35),
        'Loan Outstanding'].sum()

    return sum_part1 + sum_part2

def calc_sum74(securities_financial_trans, loans_and_advances):
    """
    =SUM(SUMIFS('Securities Financial Trans.'!$G:$G,'Securities Financial Trans.'!$AN:$AN,"More than 1 year",'Securities Financial Trans.'!$AD:$AD,{"Domestic Sovereign","Foreign Sovereign","SMEs","Retail","Corp","PSEs"},'Securities Financial Trans.'!$U:$U,"<="&"35%"))
    +SUM(SUMIFS('Loans & Advances'!$F:$F,'Loans & Advances'!$AA:$AA,"More than 1 year",'Loans & Advances'!$I:$I,">"&"0",'Loans & Advances'!$I:$I,"<"&"3",'Loans & Advances'!$S:$S,{"Domestic Sovereign","Foreign Sovereign","SMEs","Retail","Corp","PSEs"},'Loans & Advances'!$O:$O,"<="&"35%"))

    :param securities_financial_trans: DataFrame containing the 'Securities Financial Trans.' data
    :param loans_and_advances: DataFrame containing the 'Loans & Advances' data
    :return: Calculated sum
    Row 35 Blank 4
    """
    criteria_values = ["Domestic Sovereign", "Foreign Sovereign", "SMEs", "Retail", "Corp", "PSEs"]

    sum_part1 = securities_financial_trans.loc[
        (securities_financial_trans['Days To Maturity'] == 'More than 1 year') &
        (securities_financial_trans['Underlying Asset Counterparty'].isin(criteria_values)) &
        (securities_financial_trans['Underlying Asset Issuer C41 Risk Weight'] <= 0.35),
        'Next Principal Payment Amount'].sum()

    sum_part2 = loans_and_advances.loc[
        (loans_and_advances['Days to Maturity'] == 'More than 1 year') &
        (loans_and_advances['Loan Group'] > 0) &
        (loans_and_advances['Loan Group'] < 3) &
        (loans_and_advances['Counterparty Category'].isin(criteria_values)) &
        (loans_and_advances['Risk Weight  as per C41'] <= 0.35),
        'Loan Outstanding'].sum()

    return sum_part1 + sum_part2

def calc_sum75(securities_financial_trans, loans_and_advances):
    """
    =SUM(SUMIFS('Securities Financial Trans.'!$AT:$AT,'Securities Financial Trans.'!$AD:$AD,{"Domestic Sovereign","Foreign Sovereign","SMEs","Retail","Corp","PSEs"},'Securities Financial Trans.'!$U:$U,"<="&"35%"))
    +SUM(SUMIFS('Loans & Advances'!$AE:$AE,'Loans & Advances'!$I:$I,">"&"0",'Loans & Advances'!$I:$I,"<"&"3",'Loans & Advances'!$S:$S,{"Domestic Sovereign","Foreign Sovereign","SMEs","Retail","Corp","PSEs"},'Loans & Advances'!$O:$O,"<="&"35%"))

    :param securities_financial_trans: DataFrame containing the 'Securities Financial Trans.' data
    :param loans_and_advances: DataFrame containing the 'Loans & Advances' data
    :return: Calculated sum
    Row 35 Blank 5
    """
    criteria_values = ["Domestic Sovereign", "Foreign Sovereign", "SMEs", "Retail", "Corp", "PSEs"]

    sum_part1 = securities_financial_trans.loc[
        (securities_financial_trans['Underlying Asset Counterparty'].isin(criteria_values)) &
        (securities_financial_trans['Underlying Asset Issuer C41 Risk Weight'] <= 0.35),
        'Total RSF Amount'].sum()

    sum_part2 = loans_and_advances.loc[
        (loans_and_advances['Loan Group'] > 0) &
        (loans_and_advances['Loan Group'] < 3) &
        (loans_and_advances['Counterparty Category'].isin(criteria_values)) &
        (loans_and_advances['Risk Weight  as per C41'] <= 0.35),
        'RSF Amount'].sum()

    return sum_part1 + sum_part2

def calc_sum76(investment_trading_securities):
    """
    =SUMIFS('Investment&Trading Securities'!$E:$E,'Investment&Trading Securities'!$Y:$Y,"Equity")

    :param investment_trading_securities: DataFrame containing the 'Investment&Trading Securities' data
    :return: Calculated sum

    Row 38 - Blank 1
    """
    result = investment_trading_securities.loc[
        (investment_trading_securities['Mapped Product Type'] == "Equity"),
        'Book Value'
    ].sum()

    return result

def calc_sum77(investment_trading_securities):
    """
    =SUMIFS('Investment&Trading Securities'!$E:$E,'Investment&Trading Securities'!$AD:$AD,"NA",'Investment&Trading Securities'!$AP:$AP,"Less than 6 months")
    :param investment_trading_securities: DataFrame containing the 'Investment&Trading Securities' data
    :return: Calculated sum

    Row 38 - Blank 2
    """
    result = investment_trading_securities.loc[
        (investment_trading_securities['HQLA Asset'] == "NA") & 
        (investment_trading_securities['Instrument Maturity bucket'] == "Less than 6 months"),
        'Book Value'
    ].sum()

    return result

def calc_sum78(investment_trading_securities):
    """
    =SUMIFS('Investment&Trading Securities'!$E:$E,'Investment&Trading Securities'!$AD:$AD,"NA",'Investment&Trading Securities'!$AP:$AP,"6 months to 1 year")

    :param investment_trading_securities: DataFrame containing the 'Investment&Trading Securities' data
    :return: Calculated sum

    Row 38 - Blank 3
    """
    result = investment_trading_securities.loc[
        (investment_trading_securities['HQLA Asset'] == "NA") &
        (investment_trading_securities['Instrument Maturity bucket'] == "6 months to 1 year"),
        'Book Value'
    ].sum()

    return result

def calc_sum79(investment_trading_securities):
    """
    =SUMIFS('Investment&Trading Securities'!$E:$E,'Investment&Trading Securities'!$AD:$AD,"NA",'Investment&Trading Securities'!$AP:$AP,"More than 1 year")

    :param investment_trading_securities: DataFrame containing the 'Investment&Trading Securities' data
    :return: Calculated sum

    Row 38 - Blank 4
    """
    result = investment_trading_securities.loc[
        (investment_trading_securities['HQLA Asset'] == "NA") &
        (investment_trading_securities['Instrument Maturity bucket'] == "More than 1 year"),
        'Book Value'
    ].sum()

    return result

def calc_sum80(investment_trading_securities):
    """
    =SUMIFS('Investment&Trading Securities'!$AT:$AT,'Investment&Trading Securities'!$AD:$AD,"NA",'Investment&Trading Securities'!$Y:$Y,"<>"&"Equity")
    +SUMIFS('Investment&Trading Securities'!$AT:$AT,'Investment&Trading Securities'!$Y:$Y,"Equity")

    :param investment_trading_securities: DataFrame containing the 'Investment&Trading Securities' data
    :return: Calculated sum

    Row 38 - Blank 5
    """
    sum_part1 = investment_trading_securities.loc[
        (investment_trading_securities['HQLA Asset'] == "NA") &
        (investment_trading_securities['Mapped Product Type'] != "Equity"),
        'RSF Amount'
    ].sum()

    sum_part2 = investment_trading_securities.loc[
        investment_trading_securities['Mapped Product Type'] == "Equity",
        'RSF Amount'
    ].sum()

    return sum_part1 + sum_part2

def calc_sum81(df, F_row41, F_row45):
    """
    =SUM(F41:F45)

    :param dataframe: Pandas DataFrame containing the data
    :return: Calculated sum

    Row 40 - Blank 1
    """
    return df.loc[F_row41:F_row45, 'Blank 1'].sum()

def calc_sum82(df, start_row, end_row):
    """
    Replicates the Excel operation =SUM(G42:I45)
    
    :param df: Pandas DataFrame containing the data
    :param start_row: Starting row index
    :param end_row: Ending row index
    :return: Calculated sum
    """
    # Sum over the range of cells analogous to G42:I45 in Excel
    sum_range = df.loc[start_row:end_row, ['Blank 2', 'Blank 3', 'Blank 4']].sum().sum()
    return sum_range

def calc_sum83(df, J_row41, J_row45):
    """
    =SUM(J41:J45)

    :param dataframe: Pandas DataFrame containing the data
    :return: Calculated sum

    Row 40 - Blank 5
    """
    return df.loc[J_row41:J_row45, 'Blank 5'].sum()

def get_value_c13(other_items):
    """
    This function replicates the following Excel operation in Python:
    ='Other Items'!$C$13

    :param other_items: DataFrame containing the 'Other Items' data
    :return: Value from cell C13
    Row 41 - Blank 1
    """
    return other_items.at[2, 'AMOUNT ALL MATURITY']

def get_value_k13(other_items):
    """
    This function replicates the following Excel operation in Python:
    ='Other Items'!$K$13

    :param other_items: DataFrame containing the 'Other Items' data
    :return: Value from cell K13
    Row 41 - Blank 5
    """
    return other_items.at[2, 'WEIGHTED RSF AMOUNT']

def get_value_t9(derivatives):
    """
    This function replicates the following Excel operation in Python:
    =Derivatives!$T$9

    :param derivatives: DataFrame containing the 'Derivatives' data
    :return: Value from cell T9
    Row 43 - Blank 2,3,4
    """
    return derivatives['Total Derivatives Assets'].iloc[0]


def calc_value(df, G_row43):
    """
    This function replicates the following Excel operation in Python:
    =100%*G43

    :param dataframe: DataFrame containing the relevant data
    :return: 100% of the value in cell G43
    Row 43 - Blank 5
    """
    return 1 * df.loc[G_row43, 'Blank 2']




def calc_value1(df, G_row44):
    """
    This function replicates the following Excel operation in Python:
    =5%*G44

    :param dataframe: DataFrame containing the relevant data
    :return: 5% of the value in cell G44
    Row 44 - Blank 5
    """
    return 0.05 * df.loc[G_row44, 'Blank 2']

def calc_sum84(other_items):
    """
    This function replicates the following Excel operation in Python:
    =SUM('Other Items'!$C$14:$C$27)

    :param other_items: DataFrame containing the 'Other Items' data
    :return: Calculated sum
    Row 45 - Blank 1
    """
    return other_items.loc[3:17, 'AMOUNT ALL MATURITY'].sum()

def calc_sum85(loans_and_advances, investment_and_trading_securities, dep_w_other_banks_nsfr):
    """
    This function replicates the following Excel operation in Python:
    =SUM(SUMIFS('Loans & Advances'!$F:$F,'Loans & Advances'!$I:$I,{3,4,5},'Loans & Advances'!$AA:$AA,"Less than 6 months"))
    +SUMIFS('Investment&Trading Securities'!$R:$R,'Investment&Trading Securities'!$AU:$AU,"Less than 6 months")
    +SUMIFS('Loans & Advances'!$P:$P,'Loans & Advances'!$AA:$AA,"Less than 6 months")
    +SUMIFS('Deposits with Other Banks'!$K:$K,'Deposits with Other Banks'!$T:$T,"Less than 6 months")

    :param loans_and_advances: DataFrame containing the 'Loans & Advances' data
    :param investment_and_trading_securities: DataFrame containing the 'Investment&Trading Securities' data
    :param deposits_with_other_banks: DataFrame containing the 'Deposits with Other Banks' data
    :return: Calculated sum
    Row 45 - Blank 2
    """
    sum_part1 = loans_and_advances.loc[
        loans_and_advances['Loan Group'].isin([3, 4, 5]) &
        (loans_and_advances['Days to Maturity'] == 'Less than 6 months'),
        'Loan Outstanding'].sum()

    sum_part2 = investment_and_trading_securities.loc[
        (investment_and_trading_securities['Maturity Bucket for Accrued Interest'] == 'Less than 6 months'),
        'Accrued Interest'].sum()

    sum_part3 = loans_and_advances.loc[
        (loans_and_advances['Days to Maturity'] == 'Less than 6 months'),
        'Accrued Interest'].sum()

    sum_part4 = dep_w_other_banks_nsfr.loc[
        (dep_w_other_banks_nsfr['Remaining Maturity for Accrued Interest'] == 'Less than 6 months'),
        'Accrued Interest'].sum()

    return sum_part1 + sum_part2 + sum_part3 + sum_part4

def calc_sum86(loans_and_advances, investment_and_trading_securities, dep_w_other_banks_nsfr):
    """
    This function replicates the following Excel operation in Python:
    =SUM(SUMIFS('Loans & Advances'!$F:$F,'Loans & Advances'!$I:$I,{3,4,5},'Loans & Advances'!$AA:$AA,"6 months to 1 year"))
    +SUMIFS('Investment&Trading Securities'!$R:$R,'Investment&Trading Securities'!$AU:$AU,"6 months to 1 year")
    +SUMIFS('Loans & Advances'!$P:$P,'Loans & Advances'!$AA:$AA,"6 months to 1 year")
    +SUMIFS('Deposits with Other Banks'!$F:$F,'Deposits with Other Banks'!$Q:$Q,"6 months to 1 year")
    +SUMIFS('Deposits with Other Banks'!$K:$K,'Deposits with Other Banks'!$T:$T,"6 months to 1 year")

    :param loans_and_advances: DataFrame containing the 'Loans & Advances' data
    :param investment_and_trading_securities: DataFrame containing the 'Investment&Trading Securities' data
    :param deposits_with_other_banks: DataFrame containing the 'Deposits with Other Banks' data
    :return: Calculated sum
    Row 45 - Blank 3
    """
    sum_part1 = loans_and_advances.loc[
        loans_and_advances['Loan Group'].isin([3, 4, 5]) &
        (loans_and_advances['Days to Maturity'] == '6 months to 1 year'),
        'Loan Outstanding'].sum()

    sum_part2 = investment_and_trading_securities.loc[
        (investment_and_trading_securities['Maturity Bucket for Accrued Interest'] == '6 months to 1 year'),
        'Accrued Interest'].sum()

    sum_part3 = loans_and_advances.loc[
        (loans_and_advances['Days to Maturity'] == '6 months to 1 year'),
        'Accrued Interest'].sum()

    sum_part4 = dep_w_other_banks_nsfr.loc[
        (dep_w_other_banks_nsfr['Maturity Bucket'] == '6 months to 1 year'),
        'Deposit balance'].sum()

    sum_part5 = dep_w_other_banks_nsfr.loc[
        (dep_w_other_banks_nsfr['Remaining Maturity for Accrued Interest'] == '6 months to 1 year'),
        'Accrued Interest'].sum()

    return sum_part1 + sum_part2 + sum_part3 + sum_part4 + sum_part5

def calc_sum87(loans_and_advances, investment_and_trading_securities, dep_w_other_banks_nsfr):
    """
    This function replicates the following Excel operation in Python:
    =SUM(SUMIFS('Loans & Advances'!$F:$F,'Loans & Advances'!$I:$I,{3,4,5},'Loans & Advances'!$AA:$AA,"More than 1 year"))
    +SUMIFS('Investment&Trading Securities'!$R:$R,'Investment&Trading Securities'!$AU:$AU,"More than 1 year")
    +SUMIFS('Loans & Advances'!$P:$P,'Loans & Advances'!$AA:$AA,"More than 1 year")
    +SUMIFS('Deposits with Other Banks'!$F:$F,'Deposits with Other Banks'!$Q:$Q,"More than 1 year")
    +SUMIFS('Deposits with Other Banks'!$K:$K,'Deposits with Other Banks'!$T:$T,"More than 1 year")

    :param loans_and_advances: DataFrame containing the 'Loans & Advances' data
    :param investment_and_trading_securities: DataFrame containing the 'Investment&Trading Securities' data
    :param deposits_with_other_banks: DataFrame containing the 'Deposits with Other Banks' data
    :return: Calculated sum

    Row 45 - Blank 4
    """
    sum_part1 = loans_and_advances.loc[
        loans_and_advances['Loan Group'].isin([3, 4, 5]) &
        (loans_and_advances['Days to Maturity'] == 'More than 1 year'),
        'Loan Outstanding'].sum()

    sum_part2 = investment_and_trading_securities.loc[
        (investment_and_trading_securities['Maturity Bucket for Accrued Interest'] == 'More than 1 year'),
        'Accrued Interest'].sum()

    sum_part3 = loans_and_advances.loc[
        (loans_and_advances['Days to Maturity'] == 'More than 1 year'),
        'Accrued Interest'].sum()

    sum_part4 = dep_w_other_banks_nsfr.loc[
        (dep_w_other_banks_nsfr['Maturity Bucket'] == 'More than 1 year'),
        'Deposit balance'].sum()

    sum_part5 = dep_w_other_banks_nsfr.loc[
        (dep_w_other_banks_nsfr['Remaining Maturity for Accrued Interest'] == 'More than 1 year'),
        'Accrued Interest'].sum()

    return sum_part1 + sum_part2 + sum_part3 + sum_part4 + sum_part5

def calc_sum88(loans_and_advances, investment_and_trading_securities, other_items, dep_w_other_banks_nsfr):
    """
    This function replicates the following Excel operation in Python:
    =SUM(SUMIFS('Loans & Advances'!$AE:$AE,'Loans & Advances'!$I:$I,{3,4,5}))
    +SUM('Investment&Trading Securities'!$AW:$AW)
    +SUM('Loans & Advances'!$AG:$AG)
    +SUM('Other Items'!$K$14:$K$27)
    +SUM('Deposits with Other Banks'!$V:$V)

    :param loans_and_advances: DataFrame containing the 'Loans & Advances' data
    :param investment_and_trading_securities: DataFrame containing the 'Investment&Trading Securities' data
    :param other_items: DataFrame containing the 'Other Items' data
    :param deposits_with_other_banks: DataFrame containing the 'Deposits with Other Banks' data
    :return: Calculated sum

    Row 45 - Blank 5
    """
    sum_part1 = loans_and_advances.loc[
        loans_and_advances['Loan Group'].isin([3, 4, 5]),
        'RSF Amount'].sum()

    sum_part2 = investment_and_trading_securities['RSF Amount for Accrued Interest'].sum()
    sum_part3 = loans_and_advances['RSF Amount for Accrued Interest'].sum()
    sum_part4 = other_items.loc[3:16, 'WEIGHTED RSF AMOUNT'].sum() # Assuming 0-based index
    sum_part5 = dep_w_other_banks_nsfr['RSF Amount for Accrued Interest'].sum()

    return sum_part1 + sum_part2 + sum_part3 + sum_part4 + sum_part5

def calc_sum89(off_balance_sheet, facility):
    """
    This function replicates the following Excel operation in Python:
    =SUM('Off Balance Sheet'!$F:$F)+SUM(Facility!$I:$I)

    :param off_balance_sheet: DataFrame containing the 'Off Balance Sheet' data
    :param facility: DataFrame containing the 'Facility' data
    :return: Calculated sum

    Row 46 - Blank 1
    """
    sum_off_balance_sheet = off_balance_sheet[' Unutilised Value '].sum()
    sum_facility = facility[' Undrawn Credit Line '].sum()

    return sum_off_balance_sheet + sum_facility

def calc_sum90(off_balance_sheet, facility):
    """
    This function replicates the following Excel operation in Python:
    =SUM(Facility!$R:$R)+SUM('Off Balance Sheet'!$O:$O)

    :param off_balance_sheet: DataFrame containing the 'Off Balance Sheet' data
    :param facility: DataFrame containing the 'Facility' data
    :return: Calculated sum

    Row 46 - Blank 5
    """
    sum_facility = facility['RSF Amount Undrawn'].sum()
    sum_off_balance_sheet = off_balance_sheet['RSF Amount'].sum()

    return sum_facility + sum_off_balance_sheet

def calc_sum91(df, J_row29, J_row30, J_row31, J_row39, J_row40, J_row46):
    """
    This function replicates the following Excel operation in Python:
    =SUM(J29:J31,J39,J40,J46)

    :param dataframe: DataFrame containing the relevant data in column 'J'
    :return: Calculated sum

    Row 47 - Blank 5
    """
    rows_to_select = [J_row29, J_row30, J_row31, J_row39, J_row40, J_row46]
    sum_values = df.loc[rows_to_select, 'Blank 5'].sum()

    return sum_values

def get_value_nsfr(df, J_row27, J_row47):
    """
    This function replicates the following Excel operation in Python:
    =IFERROR(J27/J47,0)

    :param dataframe: DataFrame containing the relevant data in column 'J'
    :return: Result of the division or 0 if an error occurs

    Row 48 - Blank 5
    """
    try:
        result = df.at[J_row27, 'Blank 5'] / df.at[J_row47, 'Blank 5']
        if pd.isna(result) or np.isinf(result):
            return 0
    except ZeroDivisionError:
        return 0

    return result

def main():
    path = os.path.dirname(os.path.realpath(__file__))
    path_borrowings = os.path.join(path, 'Borrowings')
    path_investment = os.path.join(path, 'Investment_Trading_Securitie')
    path_otheritems = os.path.join(path, 'Other_Items')
    path_deposit = os.path.join(path, 'Deposits')
    path_issuedsecurities = os.path.join(path, 'Issued_Securitie')
    path_securities_fin_trans = os.path.join(path, 'Securities_Financial_Tran')
    path_derivatives = os.path.join(path, 'Derivatives')
    path_facility = os.path.join(path, 'Facility')
    path_offbalancesheet = os.path.join(path, 'Off_Balance_Sheet')
    path_loan_advances = os.path.join(path, 'Loan_Advance')
    path_deposits_w_otherbanks = os.path.join(path, 'Deposits_with_Other_Bank')

    borrowings = Borrowings_NSFR_output.nsfr_borrowings()
    investment = Investment_Trading_Securities_NSFR_output.nsfr_investmentandtradingsecurities()
    securities_financial_trans = Securities_Financial_Trans_NSFR.nsfr_securitiesfinancialtrans()
    derivatives = Derivatives_NSFR_output.nsfr_derivatives(path_derivatives)
    facility = Facility_NSFR_output.nsfr_facility(path_facility)
    offbalancesheet = Off_Balance_Sheet_NSFR_output.nsfr_offbalancesheet(path_offbalancesheet)
    other_items = Other_NSFR_Items.nsfr_New_Other_Items(path_otheritems)
    issued_securities = Issued_NSFR_Securities.Issued_Securities_NSFR(path_issuedsecurities)
    deposit = Deposits_NSFR_output.nsfr_deposits(path_deposit)
    dep_w_other_banks_nsfr = Deposits_with_other_banks_NSFR_output.NSFR_Deposits_with_Other_Banks(path_deposits_w_otherbanks)
    loans_and_advances = Loans_Advances_NSFR.Loans_Advances_NSFR(path_loan_advances)
    #collecteral = 
    output_df = set_output_df()

    #Row index = Row - 14

    #Row index 1 - Row 15
    output_df.at[1, 'Blank 1'] = get_value1(other_items, 'AMOUNT ALL MATURITY')
    output_df.at[1, 'Blank 2'] = 0.0
    output_df.at[1, 'Blank 3'] = 0.0
    output_df.at[1, 'Blank 4'] = get_value2(other_items, 'Amount Above 1Y')
    output_df.at[1, 'Blank 5'] = calc_sum6(other_items, 'Weighted ASF Amount')

    #Row index 2 - Row 16
    output_df.at[2, 'Blank 1'] = 0.0
    output_df.at[2, 'Blank 2'] = calc_sum7(issued_securities,
                                           securities_financial_trans,
                                           'Book Value',
                                           'Remaining Maturity',
                                           'ASF Amount',
                                           'Book Value',
                                           'Transaction Category',
                                           'Days To Maturity')
    output_df.at[2, 'Blank 3'] = calc_sum8(issued_securities,
                                           securities_financial_trans,
                                           'Book Value',
                                           'Remaining Maturity',
                                           'ASF Amount',
                                           'Book Value',
                                           'Transaction Category',
                                           'Days To Maturity')
    output_df.at[2, 'Blank 4']= calc_sum9(issued_securities,
                                           securities_financial_trans,
                                           'Book Value',
                                           'Remaining Maturity',
                                           'ASF Amount',
                                           'Book Value',
                                           'Transaction Category',
                                           'Days To Maturity')
    output_df.at[2, 'Blank 5'] = calc_sum10(issued_securities,
                                            securities_financial_trans,
                                            'ASF Amount',
                                            'Total ASF Amount',
                                            'Transaction Category')
    output_df.at[0, 'Blank 1'] = calc_sum1(output_df, 1, 2, 'Blank 1') # F15:F16 is F15-14:F16-14
    output_df.at[0, 'Blank 2'] = calc_sum1(output_df, 1,2, 'Blank 2')
    output_df.at[0, 'Blank 3'] = calc_sum1(output_df, 1,2, 'Blank 3')
    output_df.at[0, 'Blank 4'] = calc_sum1(output_df, 1,2, 'Blank 4')
    output_df.at[0, 'Blank 5'] = calc_sum1(output_df, 1,2, 'Blank 5')
    
    #Row index 3 - Row 1

    #Row index 4 - Row 18
    output_df.at[4, 'Blank 1'] = calc_sum16(deposit,
                                            'Principal Stable Amount',
                                            'Product type',
                                            'Retail/Wholesale',
                                            'Days to Maturity')
    output_df.at[4, 'Blank 2'] = calc_sum17(deposit,
                                            'Principal Stable Amount',
                                            'Retail/Wholesale',
                                            'Days to Maturity')
    output_df.at[4, 'Blank 3'] = calc_sum18(deposit,
                                            'Principal Stable Amount',
                                            'Retail/Wholesale',
                                            'Days to Maturity')
    output_df.at[4, 'Blank 4'] = calc_sum19(deposit,
                                            'Principal Stable Amount',
                                            'Retail/Wholesale',
                                            'Days to Maturity')
    output_df.at[4, 'Blank 5'] = calc_sum20(deposit,
                                            'Weighted Stable Amount',
                                            'Retail/Wholesale')
    
    #Row index 5 - Row 19
    output_df.at[5, 'Blank 1'] = calc_sum21(deposit, 
                                            'Product type',
                                            'Retail/Wholesale',
                                            'Days to Maturity',
                                            'Principal Unstable Amount')
    
    output_df.at[5, 'Blank 2'] = calc_sum22(deposit, 
                                            'Retail/Wholesale',
                                            'Days to Maturity',
                                            'Principal Unstable Amount')
    output_df.at[5, 'Blank 3'] = calc_sum23(deposit, 
                                            'Retail/Wholesale',
                                            'Days to Maturity',
                                            'Principal Unstable Amount')
    output_df.at[5, 'Blank 4'] = calc_sum24(deposit, 
                                            'Retail/Wholesale',
                                            'Days to Maturity',
                                            'Principal Unstable Amount')
    output_df.at[5, 'Blank 5'] = calc_sum25(deposit, 
                                            'Retail/Wholesale',
                                            'Weighted Unstable Amount')
    output_df.at[3, 'Blank 1'] = calc_sum1(output_df, 4, 5, 'Blank 1')
    output_df.at[3, 'Blank 2'] = calc_sum1(output_df, 4, 5, 'Blank 2')
    output_df.at[3, 'Blank 3'] = calc_sum1(output_df, 4, 5, 'Blank 3')
    output_df.at[3, 'Blank 4'] = calc_sum1(output_df, 4, 5, 'Blank 4')
    output_df.at[3, 'Blank 5'] = calc_sum1(output_df, 4, 5, 'Blank 5')
    
    #Row index 6 - Row 20


    #Row index 7 - Row 21
    output_df.at[7, 'Blank 1'] = calc_sum30(deposit,
                                            'Product type',
                                            'Remaining Maturity for Accrued Interest')
    output_df.at[7, 'Blank 2'] = calc_sum31(deposit,
                                            'Principal Stable Amount',
                                            'Principal Unstable Amount',
                                            'Product type',
                                            'Remaining Maturity for Accrued Interest')
    output_df.at[7, 'Blank 3'] = calc_sum32(deposit, 
                                            'Principal Stable Amount',
                                            'Principal Unstable Amount',
                                            'Product type',
                                            'Remaining Maturity for Accrued Interest')
    output_df.at[7, 'Blank 4'] = calc_sum33(deposit, 
                                            'Principal Stable Amount',
                                            'Principal Unstable Amount',
                                            'Product type',
                                            'Remaining Maturity for Accrued Interest')
    output_df.at[7, 'Blank 5'] = calc_sum34(deposit,
                                            'Weighted Stable Amount',
                                            'Weighted Unstable Amount',
                                            'Product type')
    
    #Row index 8 - Row 22
    output_df.at[8, 'Blank 1'] = calc_sum35(deposit,
                                            output_df,
                                            'Principal Stable Amount',
                                            'Principal Unstable Amount',
                                            'Days to Maturity',
                                            4,5,7
                                            )
    output_df.at[8, 'Blank 2'] = calc_sum36(deposit,
                                            borrowings,
                                            securities_financial_trans,
                                            output_df,
                                            'Principal Stable Amount',
                                            'Principal Unstable Amount',
                                            'Days to Maturity',
                                            'Principal Amount Less than 6 months',
                                            'Next Principal Payment Amount',
                                            'Transaction Type',
                                            'Days To Maturity',
                                            4,5,7)
    
    output_df.at[8, 'Blank 3'] = calc_sum37(deposit,
                                            borrowings,
                                            securities_financial_trans,
                                            output_df,
                                            'Principal Stable Amount',
                                            'Principal Unstable Amount',
                                            'Days to Maturity',
                                            'Principal Amount 6 months to 1 year',
                                            'Next Principal Payment Amount',
                                            'Transaction Type',
                                            'Days To Maturity',
                                            4,5,7)
    output_df.at[8, 'Blank 4'] = calc_sum38(deposit,
                                            borrowings,
                                            securities_financial_trans,
                                            output_df,
                                            'Principal Stable Amount',
                                            'Principal Unstable Amount',
                                            'Days to Maturity',
                                            'Principal Amount More than 1 year',
                                            'Next Principal Payment Amount',
                                            'Transaction Type',
                                            'Days To Maturity',
                                            4,5,7
                                            )
    output_df.at[8, 'Blank 5'] = calc_sum39(deposit,
                                                borrowings,
                                                securities_financial_trans,
                                                output_df,
                                                4,5,7)
    output_df.at[6, 'Blank 1'] = calc_sum1(output_df, 7,8,'Blank 1')
    output_df.at[6, 'Blank 2'] = calc_sum1(output_df, 7,8,'Blank 2')
    output_df.at[6, 'Blank 3'] = calc_sum1(output_df, 7,8,'Blank 3')
    output_df.at[6, 'Blank 4'] = calc_sum1(output_df, 7,8,'Blank 4')
    output_df.at[6, 'Blank 5'] = calc_sum1(output_df, 7,8,'Blank 5')
    
    output_df.at[9, 'Blank 1'] = 0.0
    output_df.at[9, 'Blank 2'] = 0.0
    output_df.at[9, 'Blank 3'] = 0.0
    output_df.at[9, 'Blank 4'] = 0.0
    output_df.at[9, 'Blank 5'] = 0.0


    #Row index 11 - Row 25
    
    output_df.at[11, 'Blank 1'] = 0.0
    output_df.at[11, 'Blank 2'] = get_valueu9(derivatives)
    output_df.at[11, 'Blank 3'] = 0.0
    output_df.at[11, 'Blank 4'] = 0.0
    output_df.at[11, 'Blank 5'] = 0.0

    #Row index 12 - Row 26
    output_df.at[12, 'Blank 1'] = get_value_c35(other_items)
    output_df.at[12, 'Blank 2'] = calc_sum43(issued_securities,
                                             borrowings,
                                             deposit,
                                             other_items)
    output_df.at[12, 'Blank 3'] = calc_sum44(issued_securities,
                                             borrowings,
                                             deposit,
                                             other_items)
    output_df.at[12, 'Blank 4'] = calc_sum45(issued_securities,
                                             borrowings,
                                             deposit,
                                             other_items)
    output_df.at[12, 'Blank 5'] = calc_sum46(issued_securities,
                                             borrowings,
                                             deposit,
                                             other_items)
    #Row index 10 - Row 24
    output_df.at[10, 'Blank 1'] = calc_sum1(output_df, 11, 12, 'Blank 1')
    output_df.at[10, 'Blank 2'] = calc_sum41(output_df, 11, 12)
    output_df.at[10, 'Blank 5'] = calc_sum1(output_df, 11,12, 'Blank 5')

    #Row index 13 - Row 27
    output_df.at[13, 'Blank 5'] = calc_sum47(output_df, 0, 3, 6, 9, 10)
    #Row index 15 - Row 29
    output_df.at[15, 'Blank 1'] = 0.0
    output_df.at[15, 'Blank 2'] = 0.0
    output_df.at[15, 'Blank 3'] = 0.0
    output_df.at[15, 'Blank 4'] = 0.0
    output_df.at[15, 'Blank 5'] = calc_sum48(investment, other_items)

    #Row index 16 - Row 30
    output_df.at[16, 'Blank 1'] = calc_sum49(dep_w_other_banks_nsfr)
    output_df.at[16, 'Blank 2'] = calc_sum50(dep_w_other_banks_nsfr)
    output_df.at[16, 'Blank 3'] = calc_sum51(dep_w_other_banks_nsfr)
    output_df.at[16, 'Blank 4'] = calc_sum52(dep_w_other_banks_nsfr)
    output_df.at[16, 'Blank 5'] = calc_sum53(dep_w_other_banks_nsfr)


    #Row index 18 - Row 32
    output_df.at[18, 'Blank 1'] = 0.0
    output_df.at[18, 'Blank 2'] = calc_sum59(securities_financial_trans, loans_and_advances)
    output_df.at[18, 'Blank 3'] = calc_sum60(securities_financial_trans, loans_and_advances)
    output_df.at[18, 'Blank 4'] = calc_sum61(securities_financial_trans, loans_and_advances)
    output_df.at[18, 'Blank 5'] = calc_sum62(securities_financial_trans, loans_and_advances)

    #Row index 19 - Row 33
    output_df.at[19, 'Blank 1'] = calc_sum63(dep_w_other_banks_nsfr)
    output_df.at[19, 'Blank 2'] = calc_sum64(securities_financial_trans, loans_and_advances,
                                             dep_w_other_banks_nsfr)
    output_df.at[19, 'Blank 3'] = calc_sum65(securities_financial_trans, loans_and_advances,
                                             dep_w_other_banks_nsfr)
    output_df.at[19, 'Blank 4'] = calc_sum66(securities_financial_trans, loans_and_advances,
                                             dep_w_other_banks_nsfr)
    output_df.at[19, 'Blank 5'] = calc_sum67(securities_financial_trans, loans_and_advances,
                                             dep_w_other_banks_nsfr)
    
    #Row index 20 - Row 34
    output_df.at[20, 'Blank 1'] = 0.0
    output_df.at[20, 'Blank 2'] = calc_sum68(securities_financial_trans, loans_and_advances)
    output_df.at[20, 'Blank 3'] = calc_sum69(securities_financial_trans, loans_and_advances)
    output_df.at[20, 'Blank 4'] = calc_sum70(securities_financial_trans, loans_and_advances)
    output_df.at[20, 'Blank 5'] = calc_sum71(securities_financial_trans, loans_and_advances)

    #Row index 21 - Row 35
    output_df.at[21, 'Blank 1'] = 0.0
    output_df.at[21, 'Blank 2'] = calc_sum72(securities_financial_trans, loans_and_advances)
    output_df.at[21, 'Blank 3'] = calc_sum73(securities_financial_trans, loans_and_advances)
    output_df.at[21, 'Blank 4'] = calc_sum74(securities_financial_trans, loans_and_advances)
    output_df.at[21, 'Blank 5'] = calc_sum75(securities_financial_trans, loans_and_advances)
    output_df.at[22, 'Blank 1'] = 0.0
    output_df.at[22, 'Blank 2'] = 0.0
    output_df.at[22, 'Blank 3'] = 0.0
    output_df.at[22, 'Blank 4'] = 0.0
    output_df.at[22, 'Blank 5'] = 0.0
    output_df.at[23, 'Blank 1'] = 0.0
    output_df.at[23, 'Blank 2'] = 0.0
    output_df.at[23, 'Blank 3'] = 0.0
    output_df.at[23, 'Blank 4'] = 0.0
    output_df.at[23, 'Blank 5'] = 0.0
    #Row index 24 - Row 38
    output_df.at[24, 'Blank 1'] = calc_sum76(investment)
    output_df.at[24, 'Blank 2'] = calc_sum77(investment)
    output_df.at[24, 'Blank 3'] = calc_sum78(investment)
    output_df.at[24, 'Blank 4'] = calc_sum79(investment)
    output_df.at[24, 'Blank 5'] = calc_sum80(investment)
    output_df.at[25, 'Blank 1'] = 0.0
    output_df.at[25, 'Blank 2'] = 0.0
    output_df.at[25, 'Blank 3'] = 0.0
    output_df.at[25, 'Blank 4'] = 0.0
    output_df.at[25, 'Blank 5'] = 0.0

    #Row index 17 - Row 31

    output_df.at[17, 'Blank 1'] = calc_sum54(output_df, 18, 24)
    output_df.at[17, 'Blank 2'] = calc_sum55(output_df, 18, 24)
    output_df.at[17, 'Blank 3'] = calc_sum56(output_df, 18, 24)
    output_df.at[17, 'Blank 4'] = calc_sum57(output_df, 18, 24)
    output_df.at[17, 'Blank 5'] = calc_sum58(output_df, 18, 24)



    #Row index 27 - Row 41
    output_df.at[27, 'Blank 1'] = get_value_c13(other_items)
    output_df.at[27, 'Blank 2'] = 0.0
    output_df.at[27, 'Blank 3'] = 0.0
    output_df.at[27, 'Blank 4'] = 0.0
    output_df.at[27, 'Blank 5'] = get_value_k13(other_items)

    #Row index 29 - Row 43
    output_df.at[28, 'Blank 2'] = 0.0
    output_df.at[28, 'Blank 5'] = 0.0
    output_df.at[29, 'Blank 1'] = 0.0
    output_df.at[29, 'Blank 2'] = get_value_t9(derivatives)
    output_df.at[29, 'Blank 5'] = calc_value(output_df, 29)

    #Row index 30 - Row 44
    output_df.at[30, 'Blank 1'] = 0.0
    output_df.at[30, 'Blank 2'] = get_value_u9(derivatives)
    output_df.at[30, 'Blank 5'] = calc_value1(output_df, 30)

    #Row index 31 - Row 45
    output_df.at[31, 'Blank 1'] = calc_sum84(other_items)
    output_df.at[31, 'Blank 2'] = calc_sum85(loans_and_advances, investment, dep_w_other_banks_nsfr)
    output_df.at[31, 'Blank 3'] = calc_sum86(loans_and_advances, investment, dep_w_other_banks_nsfr)
    output_df.at[31, 'Blank 4'] = calc_sum87(loans_and_advances, investment, dep_w_other_banks_nsfr)
    output_df.at[31, 'Blank 5'] = calc_sum88(loans_and_advances, investment, other_items, dep_w_other_banks_nsfr)
    #Row index 26 - Row 40
    output_df.at[26, 'Blank 1'] = calc_sum81(output_df, 27, 31)
    output_df.at[26, 'Blank 2'] = calc_sum82(output_df, 27, 31)
    output_df.at[26, 'Blank 3'] = 0.0 
    output_df.at[26, 'Blank 4'] = 0.0
    output_df.at[26, 'Blank 5'] = calc_sum83(output_df, 28, 31)
    #Row index 32 - Row 46
    output_df.at[32, 'Blank 1'] = calc_sum89(offbalancesheet, facility)
    output_df.at[32, 'Blank 2'] = 0.0
    output_df.at[32, 'Blank 3'] = 0.0
    output_df.at[32, 'Blank 4'] = 0.0
    output_df.at[32, 'Blank 5'] = calc_sum90(offbalancesheet, facility)

    #Row index 33 - Row 47
    output_df.at[33, 'Blank 5'] = calc_sum91(output_df, 15, 16, 17, 25, 26, 32)

    #Row index 34 - Row 48
    output_df.at[34, 'Blank 5'] = get_value_nsfr(output_df, 13, 33)
    return output_df
    



if __name__ == "__main__":
    main()