# Copyright (c) 2024, Santosh Sutar and contributors
# For license information, please see license.txt

import frappe
from frappe import _


def execute(filters: dict | None = None):
	"""Return columns and data for the report.

	This is the main entry point for the report. It accepts the filters as a
	dictionary and should return columns and data. It is called by the framework
	every time the report is refreshed or a filter is updated.
	"""
	columns = get_columns()
	data = get_data()

	return columns, data


def get_columns() -> list[dict]:
	"""Return columns for the report.

	One field definition per column, just like a DocType field definition.
	"""
	return [
		{
			"label": _("Column 1"),
			"fieldname": "column_1",
			"fieldtype": "Data",
		},
		{
			"label": _("Column 2"),
			"fieldname": "column_2",
			"fieldtype": "Int",
		},
	]


def get_data() -> list[list]:
	"""Return data for the report.

	The report data is a list of rows, with each row being a list of cell values.
	"""
	return [
		["Row 1", 1],
		["Row 2", 2],
	]


def execute(filters=None):
    columns, data = [], []

    columns = [
        {"label": _("Campaign Name"), "fieldname": "campaign_name", "fieldtype": "Link", "options": "Campaign", "width": 200},
        {"label": _("Completion Rate"), "fieldname": "completion_rate", "fieldtype": "Percent", "width": 150},
        {"label": _("Overdue Milestones"), "fieldname": "overdue_milestones", "fieldtype": "Int", "width": 150}
    ]

    if filters is None:
        filters = {}

    filters.setdefault("campaign_manager", "")
    filters.setdefault("from_date", "2000-01-01")  
    filters.setdefault("to_date", "2100-01-01")   

    conditions = ""
    if filters["campaign_manager"]:
        conditions += " AND t.campaign_manager = %(campaign_manager)s"
    
    conditions += """
        AND (
            (t.start_date BETWEEN %(from_date)s AND %(to_date)s) OR
            (t.end_date BETWEEN %(from_date)s AND %(to_date)s) OR
            (%(from_date)s BETWEEN t.start_date AND t.end_date) OR
            (%(to_date)s BETWEEN t.start_date AND t.end_date)
        )
    """

    campaigns = frappe.db.sql(f"""
        SELECT
            t.name as campaign_name,
            (SELECT COUNT(*) FROM `tabReformiqo Milestone` WHERE campaign = t.name AND status = 'Closed') * 100 / 
            (SELECT COUNT(*) FROM `tabReformiqo Milestone` WHERE campaign = t.name) AS completion_rate,
            (SELECT COUNT(*) FROM `tabReformiqo Milestone` WHERE campaign = t.name AND status = 'Open' AND due_date < CURDATE()) AS overdue_milestones
        FROM `tabCampaign` t
        WHERE 1=1 {conditions}
    """, filters, as_dict=1)

    for campaign in campaigns:
        data.append(campaign)

    return columns, data
