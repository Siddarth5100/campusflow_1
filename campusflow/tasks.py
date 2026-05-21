import frappe

# once the admission application got created will send email
def send_admission_email(admission_name):
    doc = frappe.get_doc(
        "Admission Application",
        admission_name
    )

    frappe.sendmail(
        recipients= [doc.email],
        subject= "Admission Application Received",
        message= f"""
        Hello {doc.father_name},
            We received your admission application, Admission Id: {admission_name}
            Once verified, will revert back
        """
    )

# once the workflow state got approved will send email
def send_confirmation_email(doc_name):
    doc = frappe.get_doc(
        "Admission Application",
        doc_name
    )

    if doc.workflow_state in ["Approved", "Rejected"]:

        frappe.sendmail(
            recipients = [doc.email],
            subject = f"Application Status ID: {doc.name}",
            message = f"""
                Hello {doc.father_name}, 
                your admissison application ID: {doc.name}, got: {doc.workflow_state}
            """
        )