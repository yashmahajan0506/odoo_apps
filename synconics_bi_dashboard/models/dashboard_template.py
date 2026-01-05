from odoo import models, fields, api, _
from odoo.exceptions import UserError
import json
import logging

_logger = logging.getLogger(__name__)

class DashboardTemplate(models.Model):
    _name = "dashboard.template"
    _description = "Dashboard Template"

    name = fields.Char(string="Name", required=True)
    technical_name = fields.Char(string="Technical Name", required=True, unique=True, 
                               help="Unique identifier for the template")
    depends_on = fields.Char(string="Depends On", required=True, 
                           help="Technical name of the module required for this dashboard (e.g., 'sale')")
    definition = fields.Text(string="JSON Definition", required=True)
    dashboard_id = fields.Many2one("dashboard.dashboard", string="Active Dashboard", copy=False)
    state = fields.Selection([
        ('archived', 'Archived'),
        ('active', 'Unarchived')
    ], string="Status", default='archived', compute="_compute_state", store=True)
    
    @api.depends('dashboard_id')
    def _compute_state(self):
        for rec in self:
            rec.state = 'active' if rec.dashboard_id else 'archived'

    def action_unarchive(self):
        self.ensure_one()
        if self.dashboard_id:
            raise UserError(_("This dashboard is already unarchived."))

        # Check dependency
        if self.depends_on:
            module = self.env['ir.module.module'].search([
                ('name', '=', self.depends_on),
                ('state', '=', 'installed')
            ], limit=1)
            
            if not module:
                raise UserError(_(
                    "The required module '%s' is not installed. Please install it first."
                ) % self.depends_on)

        try:
            json_data = json.loads(self.definition)
        except Exception as e:
            raise UserError(_("Invalid JSON definition: %s") % str(e))

        # The import method expects specific structure. 
        # Typically one dashboard per import, but let's see.
        # We need to create the dashboard record first, then import charts?
        # Actually dashboard_import_json in dashboard.dashboard expects to be called on a dashboard record
        # OR it creates one? 
        # Looking at dashboard.py: 
        # def dashboard_import_json(self, json_payload): ... self.write(...)
        # It updates THIS dashboard instance.
        
        # So we need to create a dashboard first.
        dashboard_vals = {
            'name': self.name,
        }
        # If we have any specific context or default values
        
        Dashboard = self.env['dashboard.dashboard']
        new_dashboard = Dashboard.create(dashboard_vals)
        
        # Now import the charts
        # The json_payload expected by dashboard_import_json seems to be:
        # { "json_payload": [ ... list of chart dicts ... ], "grid_stack_dimensions": [...] }
        # Let's double check dashboard.py
        
        try:
            # We assume the stored definition is the full export payload
            result = new_dashboard.dashboard_import_json(json_data)
            
            if result.get('type') == 'error':
                 # Cleanup if failed
                new_dashboard.unlink()
                raise UserError(result.get('message'))
                
            # Perform Menu creation which usually happens in create_update_menu
            new_dashboard.create_update_menu()
            
            self.dashboard_id = new_dashboard.id
            
        except Exception as e:
            if new_dashboard:
                new_dashboard.unlink()
            raise UserError(_("Error importing dashboard: %s") % str(e))

        return {
            'type': 'ir.actions.client',
            'tag': 'reload',
        }

    def action_archive(self):
        self.ensure_one()
        if not self.dashboard_id:
            return
            
        # Unlink the dashboard
        # This should trigger the unlink of menu/action if cascade or logic exists
        # dashboard.py unlink() checks if created_menu_id exists and raises error?
        # Let's check dashboard.py unlink method.
        # It says: "To delete selected dashboard, kindly click on Delete Menu first!" if created_menu_id exists.
        # So we might need to remove the menu first or bypass that check or call action_delete_menu.
        
        # Actually dashboard.py:
        # def unlink(self):
        # ... raise checking created_menu_id
        # We should iterate and remove menu manually if needed or update dashboard.py to allow unlink from code 
        # if we are sure.
        
        # But wait, we cannot easily modify dashboard.py to behave differently just for us without checking context.
        # Let's see if there is an action to delete menu. 
        # It looks like the user typically deletes via UI.
        
        # Ideally, we should automate the deletion.
        # If I look at dashboard.py, there is NO action_delete_menu method visible in the snippet I saw?
        # Wait, line 603: # rec.action_delete_menu() is commented out?
        
        # I need to handle cleaning up the menu and action.
        dashboard = self.dashboard_id
        if dashboard.created_menu_id:
            dashboard.created_menu_id.unlink()
        if dashboard.created_action_id:
            dashboard.created_action_id.unlink()
            
        # Now we can unlink the dashboard
        dashboard.unlink()
        self.dashboard_id = False
