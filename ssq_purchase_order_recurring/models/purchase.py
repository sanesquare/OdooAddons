from odoo import models, fields, api
from datetime import timedelta
import pandas as pd


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    name_recurring = fields.Char("Title")
    number_recurring = fields.Char("Name", default="New")
    is_recurring_master = fields.Boolean(default=False)
    is_recurring_order = fields.Boolean(default=False)
    recurring_stage = fields.Selection(
        [("new", "New"), ("running", "Running"), ("expired", "Expired"), ("cancel", "Cancelled")],
        default="new",
        copy=False,
    )
    start_date = fields.Date("Start Date", default=fields.Date.context_today)
    end_date = fields.Date("Until")
    next_order_date = fields.Date("Next Order Date", store=True)
    interval = fields.Integer("Recurrence", required=True, default=1)
    interval_type = fields.Selection(
        [("day", "Days"), ("week", "Weeks"), ("month", "Months"), ("year", "Years")], default="day"
    )
    order_type = fields.Selection([("draft", "Request for Quotation"), ("purchase", "Purchase Order")], default="draft")
    recurring_order_id = fields.Many2one("purchase.order")
    rec_order_count = fields.Integer(compute="_compute_rec_order_count")

    _sql_constraints = [
        ("check_interval", "CHECK(interval > 0)", "Recurrence must be greater than zero."),
    ]

    def _compute_rec_order_count(self):
        for order in self.filtered(lambda o: o.is_recurring_master):
            order.rec_order_count = len(self.search([("recurring_order_id", "=", order.id)]).ids)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get("is_recurring_master") and not self._context.get("duplicate_recurring_order"):
                vals["number_recurring"] = self.env["ir.sequence"].next_by_code("purchase.order.recurring")
        return super().create(vals_list)

    def rec_order_confirm(self):
        rec_order = self.with_context({"duplicate_recurring_order": True}).copy()
        rec_order.write(
            {
                "is_recurring_master": False,
                "is_recurring_order": True,
                "recurring_order_id": self.id,
                "date_order": self.start_date,
                "date_planned": self.start_date,
            }
        )
        self.recurring_stage = "running"
        self.update_next_order_date(self.start_date)
        self.button_confirm()
        if self.order_type == "purchase":
            rec_order.button_confirm()

    def update_next_order_date(self, date_from):
        if self.interval_type == "day":
            next_order_date = date_from + timedelta(days=self.interval)
        elif self.interval_type == "week":
            next_order_date = date_from + timedelta(weeks=self.interval)
        elif self.interval_type == "month":
            next_order_date = date_from + pd.DateOffset(months=self.interval)
        elif self.interval_type == "year":
            next_order_date = date_from + pd.DateOffset(years=self.interval)
        if (next_order_date and self.end_date and next_order_date <= self.end_date) or (
            next_order_date and not self.end_date
        ):
            self.next_order_date = next_order_date

    def create_recurring_order(self):
        last_order = self.search([("recurring_order_id", "=", self.id)], limit=1, order="id desc")
        next_order = last_order.copy()
        if self.order_type == "purchase":
            next_order.button_confirm()
        next_order.date_order = next_order.recurring_order_id.next_order_date
        next_order.recurring_order_id.update_next_order_date(fields.Date.today())

    def rec_order_cancel(self):
        self.recurring_stage = "cancel"
        self.button_cancel()

    @api.onchange("partner_id")
    def _onchange_rec_partner_id(self):
        if self.partner_id and not self.name_recurring:
            self.name_recurring = self.partner_id.name

    @api.onchange("start_date")
    def _onchange_start_date(self):
        if self.start_date:
            self.date_order = self.start_date

    def action_view_rec_orders(self):
        return {
            "name": "Recurring Orders",
            "type": "ir.actions.act_window",
            "res_model": "purchase.order",
            "view_mode": "tree,form",
            "domain": [("recurring_order_id", "=", self.id)],
            "context": {"default_recurring_order_id": self.id, "default_is_recurring_order": True},
            "res_id": self.env.ref("ssq_purchase_order_recurring.action_purchase_order_recurring").id,
        }

    @api.model
    def _update_recurring_order(self):
        for order in self.env["purchase.order"].search(
            [("recurring_stage", "=", "running"), ("is_recurring_master", "=", True)]
        ):
            if order.end_date and order.end_date < fields.Date.today():
                order.recurring_stage = "expired"
            elif order.next_order_date == fields.Date.today():
                order.create_recurring_order()
