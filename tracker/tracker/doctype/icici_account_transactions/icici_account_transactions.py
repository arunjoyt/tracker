# Copyright (c) 2025, Arun Joy Thekkiniyath and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from datetime import datetime

class ICICIAccountTransactions(Document):
	def after_insert(self):
		if self.deposit_amountinr and self.deposit_amountinr > 0:
			incomeexpense = "Income"
			amount = self.deposit_amountinr
		if self.withdrawal_amountinr and self.withdrawal_amountinr > 0:
			incomeexpense = "Expense"
			amount = self.withdrawal_amountinr
		# Convert "25-Nov-2025" → date object
		date = datetime.strptime(self.transaction_date, "%d-%b-%Y").date()
		doc = frappe.get_doc({
			"doctype": "Money Transactions",
			"date": date,
			"amount": amount,
			"description": self.transaction_remarks,
			"incomeexpense": incomeexpense,
			"source_type": "Bank Account"
		})
		doc.insert()
		self.db_set("extracted_to", doc.name)
