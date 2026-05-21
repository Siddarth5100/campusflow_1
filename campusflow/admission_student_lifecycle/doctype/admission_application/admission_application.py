# Copyright (c) 2026, JC Siddarth and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
import time

class AdmissionApplication(Document):

	def before_insert(self):
		if frappe.db.exists(
			"Admission Application",
			{"email": self.email}
		):
			frappe.throw("Email already exists")
	
	def validate(self):
		if self.pincode and len(self.pincode) != 6:
			frappe.throw("Pincode should be exact 6 digits")

		if self.city and not self.city.replace(" ", "").isalpha():
			frappe.throw("City should countain only alphabets")

		if self.state and not self.state.replace(" ", "").isalpha():
			frappe.throw("State should contain only alphabets")

		if self.overall_percentage and (self.overall_percentage > 100 or self.overall_percentage < 0):
			frappe.throw("Percentage should be greater than 0 & less than 100")

	
	def after_insert(self):
		
		# admission application confirmation mail
		frappe.sendmail(
        recipients= [self.email],
        subject= f"Admission Application Received: {self.name}",
        message= f"""
        Hello {self.father_name},<br><br>
        &nbsp;We received your admission application, Admission Id: {self.name}<br><br>
        &nbsp;Once verified, will revert back
        """
    )						

	def on_submit(self):

		# admission application status mail
		frappe.enqueue(
			"campusflow.tasks.send_confirmation_email",
			queue = "short",
			doc_name = self.name,
			enqueue_after_commit = True
		)
