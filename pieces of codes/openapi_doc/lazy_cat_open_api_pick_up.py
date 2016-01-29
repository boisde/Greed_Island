# coding=utf-8


def auth():
    """
        @apiDefine AuthHeader

        @apiHeaderExample Auth-Header-Example
            {
                "Authorization": "token 5b42e18555c11dbf2c31403ea6b706a6"
            }
        @apiHeader {string} Authorization 验证身份，格式为"token <token>"，注意"token"后面需要一个空格, 请联系我们取得测试token.
    """
    pass


def auth_first():
    """
        @api {method} 在api对接阶段,请联系我们获得测试token.之后在所有接口请求头中传入token,示例如下: 取得测试/线上token
        @apiVersion 0.0.1
        @apiName auth_first
        @apiDescription 在开始之前，您必须联系我们取得风先生平台的服务访问token。该token将会被我们当做您的身份认证。
        @apiGroup Auth

        @apiUse AuthHeader
    """
    pass


def api_create_pick_up_order():
    """
        @api {post} /open_api/pick_up_order 取货单创建
        @apiVersion 0.0.1
        @apiDescription 创建一条取货单,用于调配风先生配送员进行取货.
        @apiName api_create_pick_up_order
        @apiGroup PickUp

        @apiUse AuthHeader
        @apiParam (Request Payload) {object} origin 来源平台信息
        @apiParam (Request Payload) {string} origin.order_id 来源订单id
        @apiParam (Request Payload) {string} [origin.create_time] 来源订单创建时间, UTC+8, 北京时间, 格式为:`"%Y-%m-%d %H:%M:%S"`
        @apiParam (Request Payload) {object} sender 客户信息
        @apiParam (Request Payload) {string(12)} sender.name 客户姓名
        @apiParam (Request Payload) {string(11)} sender.tel 客户电话
        @apiParam (Request Payload) {string(8)} sender.city 客户取货地址所属城市
        @apiParam (Request Payload) {string(8)} sender.district 客户取货地址所属区
        @apiParam (Request Payload) {string(64)} sender.address 客户详细取货地址
        @apiParam (Request Payload) {object} receiver 收货信息
        @apiParam (Request Payload) {string(12)} receiver.name 收货人姓名
        @apiParam (Request Payload) {string(11)} receiver.tel 收货人电话
        @apiParam (Request Payload) {string(8)} receiver.city 收货地址所属城市
        @apiParam (Request Payload) {string(8)} receiver.district 收货地址所属区
        @apiParam (Request Payload) {string(64)} receiver.address 详细收货地址
        @apiParam (Request Payload) {string(64)} remark 配送备注

        @apiParamExample {json} 请求url/body示例:
        Request URL: http://123.57.40.134:5556/open_api/pick_up_order/create
        Request Method: POST
        Request Payload:
            {
                "origin_order_id": "904dcb84-81a0-4f59-bdb8-dab50baba7d2",
                "sender": {
                    "name": "刘先生",
                    "tel": "13012345678",
                    "city": "杭州市",
                    "district": "滨江区",
                    "address": "江陵路2028号星耀城一幢301"
                },
                "receiver": {
                    "name": "杨小姐",
                    "tel": "812345678",
                    "city": "杭州市",
                    "district": "滨江区",
                    "address": "滨盛路1509号天恒大厦204"
                },
                "remark": "咖啡别撒了，沙拉盒不要翻。告诉杨小姐：健康养生的沙拉对身体好哦，么么哒"
            }
        @apiSuccessExample {json} 成功示例:
            HTTP/1.1 200 OK
            {
                "number": "000000050023"
            }
        @apiSuccess {string} number 风先生运单号
        @apiErrorExample {json} 失败示例:
            HTTP/1.1 400 ValueError
            {
              "message": "order_id[904dcb84-81a0-4f59-bdb8-dab50baba7d2] duplicated."
            }
        @apiError (错误码) 401 Token错误
        @apiError (错误码) 400 该来源平台的订单重复或其他逻辑错误.
    """
    pass


def api_pick_up_order_callback():
    """
        @api {post} <callback> 取货单回调
        @apiVersion 0.0.1
        @apiDescription 当订单状态改变时，请求预先设置好的回调地址，将订单状态的改变通知对方。如果来源平台返回失败，暂时不支持重新尝试。
        @apiName api_pick_up_order_callback
        @apiGroup PickUp

        @apiParam {string(12)} number 风先生运单号
        @apiParam {string} status 风先生运单状态
        @apiParam {string} msg 运单状态变更备注
        @apiParam {string} actual_time 运单状态变更时间, UTC+8, 北京时间
        @apiParam {object} info 其他信息

        @apiParam {string(32)} origin_order_id 来源平台原始订单id


        @apiParamExample {json} 请求url/body示例:
        Request URL: http://callback.your_company.com:8888/update_order?from=mrwind
        Request Method: POST
        Request Payload:
           {
               "number": "000000050023",
               "status": "CREATED/ASSIGNED/PICKED_UP/FINISHED/ERROR",
               "msg": "已创建/已联系配送员/配送员已取货/签收/异常",
               "update_time": "2016-01-04 11:22:14",
               "origin_order_id": "904dcb84-81a0-4f59-bdb8-dab50baba7d2",
           }
    """
    pass
