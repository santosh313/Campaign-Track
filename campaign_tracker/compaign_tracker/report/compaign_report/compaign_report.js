// Copyright (c) 2024, Santosh Sutar and contributors
// For license information, please see license.txt

frappe.query_reports["Compaign Report"] = {
	filters: [
		{
            "fieldname": "campaign_manager",
            "label": __("Campaign Manager"),
            "fieldtype": "Link",
            "options": "User",
            "reqd": 0,
            "default": frappe.session.user
        },
        {
            "fieldname": "from_date",
            "label": __("From Date"),
            "fieldtype": "Date",
            "reqd": 0,
            "default": frappe.datetime.add_months(frappe.datetime.get_today(), -1)
        },
        {
            "fieldname": "to_date",
            "label": __("To Date"),
            "fieldtype": "Date",
            "reqd": 0,
            "default": frappe.datetime.get_today()
        }
		
	],
};
