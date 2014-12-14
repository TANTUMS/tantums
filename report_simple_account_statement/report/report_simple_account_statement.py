 #-*- coding: utf 8 -*-
import pooler
from report import report_sxw
import calendar
from datetime import datetime, date, time, timedelta 
import math, pdb 

class ReportStatus(report_sxw.rml_parse):
    def __init__(self, cr, uid, name, context=None):
        super(ReportStatus, self).__init__(cr, uid, name, context=context)
        self.localcontext.update({
            'time': time,
            'get_move_lines': self.get_move_lines,
            'get_last_balance': self.get_last_balance,
            'get_total_debit_credit': self.get_total_debit_credit,
        })
       
    def get_move_lines(self,form):
        common_domain =[('date','>=',form['form']['date_start']),('date','<=',form['form']['date_finish']),('product_id','=',False),('quantity','!=',False),('partner_id','=',form['form']['partner_id'][0]),('tax_id','=',False),('tax_id_secondary','=',False)]
        journals = ['|',('type','=','bank'),('type','=','cash'),('type','=','purchase')]
        journals_ids=self.pool.get('account.journal').search(self.cr,self.uid,journals)
        for journal in journals_ids:
            common_domain.append(('journal_id','in',journals_ids))
        account_movements_ids=self.pool.get('account.move.line').search(self.cr,self.uid,common_domain,order="date")
        account_movements_obj=self.pool.get('account.move.line').browse(self.cr,self.uid,account_movements_ids)
        return account_movements_obj

    def get_total_debit_credit(self, line_ids):
        sum_tot_debit = 0.00
        sum_tot_credit = 0.00
        for line in line_ids:
            if line.debit: 
                sum_tot_debit  += line.debit
            if line.credit:
                sum_tot_credit += line.credit
        return {'sum_tot_debit': sum_tot_debit, 'sum_tot_credit': sum_tot_credit}
    
    def get_last_balance(self,form):
        acummulate_balance = 0.00
        credit_sum_tot = 0.00
        debit_sum_tot  = 0.00
        common_domain =[('date','<',form['form']['date_start']),('product_id','=',False),('quantity','!=',False),('partner_id','=',form['form']['partner_id'][0]),('tax_id','=',False),('tax_id_secondary','=',False)]
        journals = ['|',('type','=','bank'),('type','=','cash'),('type','=','purchase')]
        journals_ids=self.pool.get('account.journal').search(self.cr,self.uid,journals)
        for journal in journals_ids:
            common_domain.append(('journal_id','in',journals_ids))
        account_movements_ids=self.pool.get('account.move.line').search(self.cr,self.uid,common_domain,order="date")
        account_movements_obj=self.pool.get('account.move.line').browse(self.cr,self.uid,account_movements_ids)
        for mov in account_movements_obj:
            if mov.credit:
                credit_sum_tot += mov.credit
            if mov.debit:
                debit_sum_tot  += mov.debit
        acummulate_balance = credit_sum_tot - debit_sum_tot
        return acummulate_balance
        
        


report_sxw.report_sxw('report.simple.account.statement' ,'report.simple.account.statement.wizard', 'report_simple_account_statement/report/report_simple_account_statement.mako', parser = ReportStatus)