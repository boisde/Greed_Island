# coding=utf-8
# __author__ = 'mio'


def auth_mixin():
    """
    @apiDefine AuthHeaderMixin
    @apiHeaderExample Auth-Header-Example:
        {
            "Authorization": "token 78323lj4l32l3l23j2n2l22jl"
        }
    @apiHeader {String} Authorization 验证身份,注意格式中"token {token}"token后面有一个空格
    """
    pass


def error_mixin():
    """
        @apiDefine ErrorMixin

        @apiError content 错误信息
        @apiError message 错误消息
        @apiErrorExample 400 Bad Request
            参数错误
            {
                content="missed keys set(['city'])",
                message="ArgsParseFailed"
            }
            查询获取单个数据时，找到不止一个(通过id查找)
            {
                content=null,
                message="MultipleResultsFound"
            }
            查询没有结果(通过id查找)
            {
                content=null,
                message="NoResultFound"
            }
        @apiErrorExample 403 Forbidden
            非可操作用户
            {
                content=null,
                message="Forbidden"
            }
            未知错误
            {
                content=null,
                message="UnknownError"
            }
        @apiErrorExample 422 Unprocessable Entity
            逻辑层错误
            {
                content=null,
                message="LogicResponseFailed"
            }
            插入时重复键值
            {
                content=null,
                message="DuplicateEntry"
            }
            退款失败
            {
                content=null,
                message="RefundMoneyFailed"
            }
            扣款失败
            {
                content=null,
                message="CostMoneyFailed"
            }
    """
    pass


def express_details():
    """
    @apiDefine ExpressDetails
    @apiSuccessExample 成功返回示例
    {
        "content": {
          "status": "FINISHED",
          "transfer_status": 1,
          "shop": {
            "tel": "17808881022",
            "name": "测试产品商家001",
            "is_test": true,
            "avatar": "http://7qnajq.com2.z0.glb.qiniucdn.com/8AD3A76D2D2071E1ECB0A0B21E393573",
            "address": "浙江省杭州市滨江区江陵路",
            "lat": 30.219866,
            "lng": 120.22077,
            "id": 1471,
            "owner_id": 7750900
          },
          "remark": "",
          "errors": [],
          "node": {
            "city": "杭州市",
            "name": "HA3022",
            "distance": 1132,
            "mt_num": 1,
            "mt_list": [
              "0000000000000000000000000000000000000000000020020010060000000000"
            ],
            "couriers": [
              7756082,
              7759069,
              7771381,
              7797998,
              7756818,
              7768146,
              7791237,
              7814415
            ],
            "node_type": "561a875b421aa9b84017ba91",
            "node_type_name": "D3",
            "address": "滨江区江陵路与滨盛路交叉口星耀城",
            "lat": 30.218993,
            "lng": 120.221169,
            "id": "561a987b421aa9cf16f453f6"
          },
          "image": "http://7qnajq.com2.z0.glb.qiniucdn.com/56456465a46s456aaa",
          "receiver": {
            "lat": "30.210268",
            "lng": "120.215111",
            "tel": "13920201113",
            "name": "杨某某",
            "address": "武警医院"
          },
          "number": "000000000005",
          "pick_up_time": null,
          "source": "PHH",
          "fee": {
            "cost": 10,
            "order": 15
          },
          "create_time": "2015-12-28T07:34:53Z",
          "pkg_id": null,
          "vehicle": {},
          "from_courier": 0,
          "path": {},
          "source_order_id": "ibenben-2121"
          "courier": {
            "tel": "17705717701",
            "id": 7792622,
            "avatar": "http://7qnajq.com2.z0.glb.qiniucdn.com/DCE5352E18844B9FC2B6412B3DACD0BD",
            "name": "测试黄忠"
          },
          "trace": [
            {
              "status": "CREATED",
              "loc": {
                "lat": 30.219866,
                "lng": 120.22077
              },
              "remark": "",
              "estimated_time": "2015-12-28T07:34:53Z",
              "msg": "下单成功",
              "operator": {
                "tel": "17808881022",
                "name": "测试产品商家001",
                "is_test": true,
                "avatar": "http://7qnajq.com2.z0.glb.qiniucdn.com/8AD3A76D2D2071E1ECB0A0B21E393573",
                "address": "浙江省杭州市滨江区江陵路",
                "lat": 30.219866,
                "lng": 120.22077,
                "id": 1471,
                "owner_id": 7750900
              },
              "actual_time": "2015-12-28T07:34:53Z"
            },
            {
              "status": "SORTED",
              "loc": {
                "lat": 30.219866,
                "lng": 120.22077
              },
              "estimated_time": null,
              "msg": "城际司机已揽件",
              "operator": {
                "name": "测试城际司机"
              },
              "actual_time": "2015-12-28T07:35:07Z"
            },
            {
              "status": "ADOPTED",
              "loc": {
                "lat": 30.219866,
                "lng": 120.22077
              },
              "estimated_time": null,
              "msg": "城内司机已揽件",
              "operator": {
                "tel": "17705717701",
                "id": 7792622,
                "avatar": "http://7qnajq.com2.z0.glb.qiniucdn.com/DCE5352E18844B9FC2B6412B3DACD0BD",
                "name": "测试城内司机"
              },
              "actual_time": null
            },
            {
              "status": "SENDING",
              "loc": {
                "lat": 30.218993,
                "lng": 120.221169
              },
              "estimated_time": null,
              "msg": "到达中转站, 配送员已取货",
              "operator": {
                "tel": "17705717701",
                "id": 7792622,
                "avatar": "http://7qnajq.com2.z0.glb.qiniucdn.com/DCE5352E18844B9FC2B6412B3DACD0BD",
                "name": "测试黄忠"
              },
              "actual_time": "2015-12-28T07:36:32Z"
            },
            {
              "status": "WAIT_EVIDENCE",
              "loc": {
                "lat": "30.210268",
                "lng": "120.215111"
              },
              "estimated_time": null,
              "msg": "已送达, 等待上传凭证",
              "operator": {
                "tel": "17705717701",
                "id": 7792622,
                "avatar": "http://7qnajq.com2.z0.glb.qiniucdn.com/DCE5352E18844B9FC2B6412B3DACD0BD",
                "name": "测试黄忠"
              },
              "actual_time": "2015-12-28T07:36:52Z"
            },
            {
                "status": "ERROR",
                "type": "收方联系不到",
                "reason": "电话打不通",
                "actual_time": "2015-12-28T07:36:52Z",
                "operator": {
                    "tel": "17705717701",
                    "id": 7792622,
                    "avatar": "http://7qnajq.com2.z0.glb.qiniucdn.com/DCE5352E18844B9FC2B6412B3DACD0BD",
                    "name": "测试黄忠"
                },
                "msg": "标记异常"
            },
            {
              "status": "FINISHED",
              "loc": {
                "lat": "30.210268",
                "lng": "120.215111"
              },
              "estimated_time": null,
              "msg": "已上传凭证, 妥投",
              "operator": {
                "tel": "17705717701",
                "id": 7792622,
                "name": "测试黄忠",
                "avatar": "http://7qnajq.com2.z0.glb.qiniucdn.com/DCE5352E18844B9FC2B6412B3DACD0BD"
              },
              "actual_time": "2015-12-28T07:37:08Z",
              "image": "http://qiniu.com/testhash"
            }
          ]
        },
        "message": ""
    }

    @apiSuccess {Object} content.status CREATED待取货, SENDING配送中已取货, FINISHED已完成, CLOSED商户取消
    @apiSuccess {Object} content.transfer_status 1:可转单,2:转单中-转出,3:转单中-转入,4:不可转单,0:其他
    """
    pass


class OpenApiExpressHandler(object):
    def get(self):
        """
        @api {get} /open_api/send_order 送货单列表查询
        @apiVersion 0.0.1
        @apiName api_get_order_list
        @apiGroup BulkSend

        @apiUse AuthHeaderMixin

        @apiParamExample 请求示例:
            Request URL: http://api.123feng.com:6666/open_api/send_order
            Request Method: GET

        @apiSuccessExample 成功返回示例
            HTTP/1.1 200 OK
            {
                "content": [
                    {
                        "number": "171443407746747445",
                        "status": "ADOPTED",
                        "origin_order_id": "904dcb84-81a0-4f59-bdb8-dab50baba7d2",
                    },
                    ......
                ]
            }
        @apiSuccess (OK 200) {String} message 消息
        @apiSuccess (OK 200) {List} content 数据内容

        @apiSuccess (OK 200) {String} content.List.number 快递单号
        @apiSuccess (OK 200) {String} content.List.status 快递状态, 详细请看『状态回调』接口
        @apiSuccess (OK 200) {String} content.List.origin_order_id 来源订单id

        @apiUse ErrorMixin
        """
        pass

    def post(self):
        """
        @api {post} /open_api/send_order 送货单创建
        @apiVersion 0.0.1
        @apiName api_create_order
        @apiGroup BulkSend

        @apiUse AuthHeaderMixin

        @apiParamExample 请求示例:
            Request URL: http://api.123feng.com:6666/open_api/send_order
            Request Method: POST
            Request Payload:
                {
                    "origin": {
                        "order_id": "904dcb84-81a0-4f59-bdb8-dab50baba7d2",
                        "create_time": "2016-01-12 10:11:23"
                    },
                    "cargo": {
                        "name": "美味好吃的什锦沙拉一份+清爽有回味的冰咖啡一杯",
                        "weight": 350,
                        "price": 1500
                    },
                    "sender": {
                        "name": "懒猫洗衣滨江店",
                        "tel": "13012345678",
                        "city": "杭州市",
                        "district": "滨江区",
                        "address": "江陵路2028号星耀城一幢301",
                        "lng": 120.11,
                        "lat": 30.23
                    },
                    "receiver": {
                        "name": "杨小姐",
                        "tel": "0571-812345678",
                        "city": "杭州市",
                        "district": "滨江区",
                        "address": "滨盛路1509号天恒大厦204",
                        "lng": 120.11,
                        "lat": 30.23
                    },

                    "expected_fetch_time": "2016-01-12 10:11:23",
                    "expected_finish_time": "2016-01-12 10:11:23",
                    "remark": "咖啡别撒了，沙拉盒不要翻。告诉杨小姐：健康养生的风先生沙拉对身体好哦，么么哒"
                }

        @apiParam (Request Payload) {Object} content.origin 来源平台信息
        @apiParam (Request Payload) {String} content.origin.order_id 来源订单id
        @apiParam (Request Payload) {String} content.origin.create_time=null 来源订单创建时间，北京时间。

        @apiParam (Request Payload) {Object} content.cargo 货物信息
        @apiParam (Request Payload) {String} content.cargo.name 货物名字
        @apiParam (Request Payload) {Integer} content.cargo.weight=null 货物总重（单位:克）
        @apiParam (Request Payload) {Integer} content.cargo.price=null 货物总价（单位:人民币 分）。注：price=100 指人民币1元

        @apiParam (Request Payload) {Object} content.sender=注册商户信息 发货信息
        @apiParam (Request Payload) {String} content.sender.name 发货人名字
        @apiParam (Request Payload) {String} content.sender.tel 发货电话
        @apiParam (Request Payload) {String} content.sender.city 发货城市
        @apiParam (Request Payload) {String} content.sender.district 发货行政区
        @apiParam (Request Payload) {String} content.sender.address 发货地址
        @apiParam (Request Payload) {Float} content.sender.lng=null 发货位置经度
        @apiParam (Request Payload) {Float} content.sender.lat=null 发货位置纬度

        @apiParam (Request Payload) {Object} content.receiver 收货信息
        @apiParam (Request Payload) {String} content.receiver.name 收货人名字
        @apiParam (Request Payload) {String} content.receiver.tel收货电话
        @apiParam (Request Payload) {String} content.sender.city 收货城市
        @apiParam (Request Payload) {String} content.sender.district 收货行政区
        @apiParam (Request Payload) {String} content.receiver.address 收货地址
        @apiParam (Request Payload) {Float} content.receiver.lng=null 收货位置经度
        @apiParam (Request Payload) {Float} content.receiver.lat=null 收货位置纬度

        @apiParam (Request Payload) {String} content.expected_fetch_time=null 期望取货时间，北京时间。
        @apiParam (Request Payload) {String} content.expected_finish_time=null 期望送达时间，北京时间。
        @apiParam (Request Payload) {Integer} content.remark=null 配送备注

        @apiSuccessExample 成功返回示例
            HTTP/1.1 201 Created
            {
                "number": "000000089281"
            }

        @apiSuccess (Created 201) {String} number 风先生运单号

        @apiUse ErrorMixin
        """
        pass


class OpenApiOneExpressHandler(object):
    def get(self):
        """
        @api {get} /open_api/send_order/{order_id} 送货单详情查询
        @apiVersion 0.0.1
        @apiName api_get_order_details
        @apiGroup BulkSend

        @apiUse AuthHeaderMixin

        @apiParamExample 请求示例:
            Request URL: http://api.123feng.com:6666/open_api/send_order/000000054526
            Request Method: GET

        @apiSuccessExample 成功返回示例
        {
            "status": "FINISHED",
            "number": "000000000005",
            "remark": "咖啡别撒了，沙拉盒不要翻。告诉杨小姐：健康养生的风先生沙拉对身体好哦，么么哒",
            "create_time": "2016-01-12 10:11:23",
            "image": "http://7qnajq.com2.z0.glb.qiniucdn.com/56456465a46s456aaa",
            "node": {
                "name": "D3",
                "id": "561a987b421aa9cf16f453f6"
            },
            "origin": {
                "order_id": "lanmao-2121",
                "create_time": "2016-01-12 10:11:23",
            },
            "cargo":{
                "name": "一盒沙拉",
                "weight": 120,
                "price": 1500
            },
            "sender": {
                "tel": "17808881022",
                "name": "测试产品商家001",
                "city": "杭州市",
                "district": "滨江区",
                "address": "江陵路1509号天恒大厦",
                "lat": 30.219866,
                "lng": 120.22077,
            },
            "receiver": {
                "lat": "30.210268",
                "lng": "120.215111",
                "tel": "13920201113",
                "name": "杨某某",
                "city": "杭州市",
                "district": "滨江区"
                "address": "武警医院住院部201室"
            },
            "trace": [
                {
                    "status": "FINISHED",
                    "loc": {
                        "lat": "30.210268",
                        "lng": "120.215111"
                    },
                    "msg": "已上传凭证, 妥投",
                    "operator": {
                        "tel": "17705717701",
                        "id": 7792622,
                        "name": "测试黄忠",
                        "avatar": "http://7qnajq.com2.z0.glb.qiniucdn.com/DCE5352E18844B9FC2B6412B3DACD0BD"
                    },
                    "actual_time": "2016-01-12 10:11:23",
                    "image": "http://qiniu.com/testhash"
                },
                {
                    "status": "WAIT_EVIDENCE",
                    "loc": {
                        "lat": "30.210268",
                        "lng": "120.215111"
                    },
                    "msg": "已送达, 等待上传凭证",
                    "operator": {
                        "tel": "17705717701",
                        "id": 7792622,
                        "avatar": "http://7qnajq.com2.z0.glb.qiniucdn.com/DCE5352E18844B9FC2B6412B3DACD0BD",
                        "name": "测试黄忠"
                    },
                    "actual_time": "2016-01-12 10:11:23"
                },
                {
                    "status": "ERROR",
                    "type": "收方联系不到",
                    "reason": "电话打不通",
                    "operator": {
                        "tel": "17705717701",
                        "id": 7792622,
                        "avatar": "http://7qnajq.com2.z0.glb.qiniucdn.com/DCE5352E18844B9FC2B6412B3DACD0BD",
                        "name": "测试黄忠"
                    },
                    "msg": "异常",
                    "actual_time": "2016-01-12 10:11:23",
                },
                {
                    "status": "SENDING",
                    "loc": {
                        "lat": 30.218993,
                        "lng": 120.221169
                    },
                    "msg": "到达中转站, 配送员已取货",
                    "operator": {
                        "tel": "17705717701",
                        "id": 7792622,
                        "avatar": "http://7qnajq.com2.z0.glb.qiniucdn.com/DCE5352E18844B9FC2B6412B3DACD0BD",
                        "name": "测试黄忠"
                    },
                    "actual_time": "2016-01-12 10:11:23"
                },
                {
                    "status": "ADOPTED",
                    "loc": {
                        "lat": 30.219866,
                        "lng": 120.22077
                    },
                    "msg": "城内司机已揽件",
                    "operator": {
                        "tel": "17705717701",
                        "id": 7792622,
                        "avatar": "http://7qnajq.com2.z0.glb.qiniucdn.com/DCE5352E18844B9FC2B6412B3DACD0BD",
                        "name": "测试城内司机"
                    },
                    "actual_time": "2016-01-12 10:11:23"
                },
                {
                    "status": "SORTED",
                    "loc": {
                        "lat": 30.219866,
                        "lng": 120.22077
                    },
                    "msg": "城际司机已揽件",
                    "operator": {
                        "name": "测试城际司机"
                    },
                    "actual_time": "2016-01-12 10:11:23"
                },
                {
                    "status": "CREATED",
                    "loc": {
                        "lat": 30.219866,
                        "lng": 120.22077
                    },
                    "remark": "",
                    "msg": "下单成功",
                    "operator": {
                        "tel": "17808881022",
                        "name": "测试产品商家001",
                        "avatar": "http://7qnajq.com2.z0.glb.qiniucdn.com/DCE5352E18844B9FC2B6412B3DACD0BD",
                        "id": 1471,
                    },
                    "actual_time": "2016-01-12 10:11:23"
                },
            ]
        }   
        @apiUse ErrorMixin
        """
        pass


class OpenApiCallbackHandler(object):
    def post(self):
        """
        @api {post} <callback> 送货单回调
        @apiVersion 0.0.1
        @apiName api_order_callback
        @apiGroup BulkSend
        @apiDescription
        当运单状态改变时，请求预先设置好的回调地址，将订单状态的改变通知对方。如果来源平台返回失败，暂时不支持重新尝试。

        @apiParam (BODY PARAMETERS) {String} number 风先生运单号
        @apiParam (BODY PARAMETERS) {String} status 风先生运单状态
        @apiParam (BODY PARAMETERS) {String} update_time 运单更新时间，北京时间
        @apiParam (BODY PARAMETERS) {String} origin_order_id 对接平台原始订单号

        @apiParamExample 请求示例:
             Request URL: http://callback.your_company.com:8888/update_order?from=mrwind
             Request Method: POST
             Request Payload:
                {
                    "number": "201442301916525112",
                    "status": "CREATED/ADOPTED/PICKED_UP/FINISHED/ERROR",
                    "msg":    "已创建/司机已揽件/配送员已取货/签收/异常"
                    "update_time": "2016-01-12 10:11:23",
                    "origin_order_id": "904dcb84-81a0-4f59-bdb8-dab50baba7d2",
                }
        """
        pass
