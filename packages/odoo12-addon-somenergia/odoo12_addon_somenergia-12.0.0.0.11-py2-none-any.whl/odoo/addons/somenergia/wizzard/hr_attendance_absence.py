
from odoo import models, fields, _
import logging
import datetime

logger = logging.getLogger(__name__)


class HrAttendanceAbsence(models.TransientModel):
    _name = 'hr.attendance.absence'

    absence_message = fields.Text("Missatge", help="Missatge que s'enviara al grup de laboral",
                                  default="Avui no em trobo amb forces per assistir a la feina.")

    def _getLeaveType(self):
        leave_type_odoo = self.env['hr.leave.type']
        leave_type = leave_type_odoo.name_search("Indisposició")
        if leave_type:
            return leave_type[0][0]
        leave_type = leave_type_odoo.name_search("Other") or leave_type_odoo.name_search("Altres")
        if leave_type:
            return leave_type[0][0]            
        leave_type = leave_type_odoo.name_search("")
        return leave_type[0][0]

    def run(self):
        # Send Email
        mail_pool = self.env['mail.mail']
        mail_html = "<p>" + str(self.env.user.display_name) + \
            " avui no vindrá. Ha escrit el següent missatge: </p><p>" + \
            str(self.absence_message) + "</p>"
        mail_data = {}
        mail_data.update({'subject': 'Avui no vinc ' +
                         str(self.env.user.display_name)})
        mail_data.update({'email_to': 'avuinovinc@somenergia.coop'})
        mail_data.update({'body_html': mail_html})

        msg_id = mail_pool.create(mail_data)
        if msg_id:
            mail_pool.send(msg_id)
        else:
            return {'warning': 'Error sending mail'}

        # Create Leave
        leave_values = {}
        leave_values.update({'holiday_type': 'employee'})
        leave_values.update({'holiday_status_id': self._getLeaveType()})

        today = datetime.datetime.today().strftime("%Y-%m-%d")
        leave_values.update({'date_from': today + " 08:00:00"})
        leave_values.update({'date_to': today + " 17:00:00"})
        leave_values.update({'request_date_from': today})
        leave_values.update({'request_date_to': today})

        leave_values.update({'request_date_from_period': 'am'})
        leave_values.update({'name': False})
        leave_values.update({'employee_id': self.env.user._uid})
        leave_values.update({'number_of_days': 1})
        leave_values.update({'request_unit_half': False})

        leave_values.update({'request_unit_hours': False})
        leave_values.update({'request_unit_custom': False})
        leave_values.update({'request_hour_from': False})
        leave_values.update({'request_hour_to': False})
        leave_values.update({'mode_company_id': False})
        leave_values.update({'category_id': False})
        leave_values.update({'department_id': False})
        leave_values.update({'payslip_status': False})
        leave_values.update({'report_note': False})
        leave_values.update({'message_attachment_count': 0})

        leave_pool = self.env['hr.leave']
        leave = leave_pool.create(leave_values)
        
        return msg_id, leave
