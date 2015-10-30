#!/usr/bin/env python
# coding:utf-8

"""
Models for router
"""

from tools_lib.transwarp.orm import Model, StringField, IntegerField, DateTimeField, DateField

DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"


class HotOrder(Model):
    """订单Model, 存储带有时效性的订单信息"""
    __table__ = 'hot_order'

    order_id = IntegerField(ddl='int(11)', primary_key=True)
    gen_from = StringField(default=None, nullable=False, ddl='varchar(16)', comment=u'订单生成来源', key=True)
    # need_route = IntegerField(ddl='tinyint(1)', comment=u'该单是否需要分配', key=True)
    state = StringField(default=None, nullable=True, ddl='varchar(16)',
                        comment=u'订单状态 INIT:待分配 CANCELED:已取消 STARTED:待取件 PICKED:待收件'
                                u'DELIVERED:待评价 FIN:已完成 REFUND:退款中 REFUNDED:已退款', key=True)

    create_time = DateTimeField(auto_now_add=True, key=True)  # UTC+8:00
    update_time = DateTimeField(auto_now=True, key=True)  # UTC+8:00

    def __hash__(self):
        return hash("%d" % self.order_id)

    def __eq__(self, other):
        return self.order_id == other.order_id


class OrderState(Model):
    """订单状态变化Model, 存储订单状态相关的事件"""
    __table__ = 'order_state'

    id = IntegerField(ddl='int(11)', primary_key=True)
    hot_order_id = IntegerField(ddl='int(11)', key=True)
    gen_by = StringField(default=None, nullable=False, ddl='varchar(16)', comment=u'订单生成来源')
    state_change_time = DateTimeField(auto_now=True)  # UTC+8:00
    state = StringField(default=None, nullable=True, ddl='varchar(16)',
                        comment=u'订单状态 INIT:待分配 CANCELED:已取消 STARTED:待取件 PICKED:待收件'
                                u'DELIVERED:待评价 FIN:已完成 REFUND:退款中 REFUNDED:已退款', key=True)
    state_info = StringField(default=None, nullable=True, ddl='varchar(32)', comment=u'状态变更详细信息')


if __name__ == "__main__":
    print HotOrder().__sql__()
    print OrderState().__sql__()
