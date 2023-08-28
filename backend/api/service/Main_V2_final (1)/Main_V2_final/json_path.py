import json

data = {
    
    "lcr": {
        "borrowing": "Main_V2_final\LCR\Borrowings\input",
        "investment": "Main_V2_final\LCR\Investment_Trading_Securities\input",
        "otheritems": "Main_V2_final\LCR\Other_Items\input",
        "deposit": "Main_V2_final\LCR\Deposit\input",
        "issuedsecurities": "Main_V2_final\LCR\Issued_Securities\input",
        "securities_fin_trans": "Main_V2_final\LCR\Securities_Financial_Trans\input",
        "derivatives": "Main_V2_final\LCR\Derivatives\input",
        "facility": "Main_V2_final\LCR\Facility\input",
        "offbalancesheet": "Main_V2_final\LCR\Off_Balance_Sheet\input",
        "loan_advances": "Main_V2_final\LCR\Loans_Advances\input",
        "deposits_w_otherbanks": "Main_V2_final\LCR\Deposits_with_other_banks\input",
        "sanctionedloans": "Main_V2_final\LCR\Sanctioned Loans\input"
     },
    "nsfr": {
        "borrowing": "Main_V2_final\\NSFR\\Borrowings\\input",
        "investment": "Main_V2_final\\NSFR\\Investment_Trading_Securitie\\input",
        "otheritems": "Main_V2_final\\NSFR\\Other_Items\\input",
        "deposit": "Main_V2_final\\NSFR\\Deposits\\input",
        "issuedsecurities": "Main_V2_final\\NSFR\\Issued_Securitie\\input",
        "securities_fin_trans": "Main_V2_final\\NSFR\\Securities_Financial_Tran\\input",
        "derivatives": "Main_V2_final\\NSFR\\Derivatives\\input",
        "facility": "Main_V2_final\\NSFR\\Facility\\input",
        "offbalancesheet": "Main_V2_final\\NSFR\\Off_Balance_Sheet\\input",
        "loan_advances": "Main_V2_final\\NSFR\\Loan_Advance\\input",
        "deposits_w_otherbanks": "Main_V2_final\\NSFR\\Deposits_with_Other_Bank\\input",
        "colleloans": "Main_V2_final\\NSFR\\Collateral_for_Loans\\input"
    }
}


with open('paths.json', 'w') as json_file:
    json.dump(data, json_file, indent=4)
