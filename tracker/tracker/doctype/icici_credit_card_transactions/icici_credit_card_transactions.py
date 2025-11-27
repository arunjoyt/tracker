# Copyright (c) 2025, Arun Joy Thekkiniyath and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from datetime import datetime


class ICICICreditCardTransactions(Document):
    def after_insert(self):

        # convert "17-11-2025" to date object
        date = datetime.strptime(self.transaction_date, "%d-%m-%Y").date()
        doc = frappe.get_doc(
            {
                "doctype": "Money Transactions",
                "date": date,
                "description": self.details,
                "source_type": "Credit Card",
            }
        )
        if "Dr." in self.amount_inr:
            doc.incomeexpense = "Expense"
            doc.amount = float(self.amount_inr.replace("Dr.", "").strip())
        if "Cr." in self.amount_inr:
            doc.incomeexpense = "Income"
            doc.amount = float(self.amount_inr.replace("Cr.", "").strip())
        doc.insert()
        self.db_set("extracted_to", doc.name)
