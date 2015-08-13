# -*- coding: utf-8 -*-
# Python source code encoding : https://www.python.org/dev/peps/pep-0263/
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    This module copyright :
#        (c) 2015 Antiun Ingenieria, SL (Madrid, Spain, http://www.antiun.com)
#                 Antonio Espinosa <antonioea@antiun.com>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from openerp import models, fields, api


class ProjectTask(models.Model):
    _inherit = 'project.task'

    leads = fields.One2many(comodel_name='crm.lead', inverse_name='task')
    leads_count = fields.Integer(string='Leads number', compute='_count_leads',
                                 store=True)
    opportunities_count = fields.Integer(string='Opportunities number',
                                         compute='_count_leads',
                                         store=True)

    @api.one
    @api.depends('leads')
    def _count_leads(self):
        opportunities = 0
        leads = 0
        for crm_lead in self.leads:
            if crm_lead.type == 'opportunity':
                leads += 1
            else:
                opportunities += 1
        self.leads_count = leads
        self.opportunities_count = opportunities

    @api.multi
    def write(self, vals):
        result = super(ProjectTask, self).write(vals)
        if 'project_id' in vals:
            leads = self.env['crm.lead'].search([('task', 'in', self.ids)])
            if leads:
                leads.write({'project': vals['project_id']})
        return result
