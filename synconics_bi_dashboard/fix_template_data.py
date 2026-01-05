
import json
from odoo import api, SUPERUSER_ID

def fix_template(env):
    template = env['dashboard.template'].search([('technical_name', '=', 'sales_dashboard_template')], limit=1)
    if not template:
        print("Template not found.")
        return

    # Safe definition with empty lists and correct kpi_view_type
    safe_definition = {
        "json_payload": [
            {
                "name": "Total Sales",
                "model": "sale.order",
                "chart_type": "kpi",
                "layout_type": "layout1",
                "tile_layout_type": "layout1",
                "theme": "animated",
                "kpi_model": "sale.order",
                "kpi_measurement_field_id": "amount_total",
                "kpi_data_type": "sum",
                "kpi_view_type": "standard",
                "chart_position": {
                    "x": 0,
                    "y": 0,
                    "w": 3,
                    "h": 2
                },
                "todo_action_ids": [],
                "chart_multiplier_ids": [],
                "list_measure_ids": [],
                "list_field_ids": []
            },
            {
                "name": "Quotation Count",
                "model": "sale.order",
                "chart_type": "kpi",
                "layout_type": "layout1",
                "tile_layout_type": "layout1",
                "theme": "animated",
                "kpi_model": "sale.order",
                "kpi_measurement_field_id": "id",
                "kpi_data_type": "count",
                "chart_position": {
                    "x": 3,
                    "y": 0,
                    "w": 3,
                    "h": 2
                },
                "todo_action_ids": [],
                "chart_multiplier_ids": [],
                "list_measure_ids": [],
                "list_field_ids": []
            }
        ]
    }
    
    template.write({'definition': json.dumps(safe_definition, indent=4)})
    print("Successfully updated template definition.")
    env.cr.commit()

fix_template(env)
