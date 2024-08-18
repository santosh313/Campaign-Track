# Copyright (c) 2024, Santosh Sutar and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class ReformiqoMilestone(Document):
    def on_update(self):
        if self.status == 'Closed':
            campaign = frappe.get_doc('Campaign', self.campaign)
            milestones = frappe.get_all('Reformiqo Milestone', filters={'campaign': self.campaign}, fields=['status'])
            
            if all(milestone['status'] == 'Closed' for milestone in milestones):
                campaign.status = 'Completed'
                campaign.save()

			
	