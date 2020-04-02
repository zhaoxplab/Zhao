# rule.py
## 获取解析规则
- 获取所有解析规则
http://127.0.0.1:8000/api/rules
response = {
        'msg': 'success',
        'data': {
            'theme': '模板',
            'rules': {
                "page": "页码",
                "goods_link": "商品链接",
                "goods_name": "商品标题",
                "goods_price": "商品价格",
                "goods_norms": "商品属性",
                "goods_value": "商品属性值",
                "img_links": "图片链接"
            },
            'describe': '描述'
        }
    }
- 通过id获取解析规则
http://127.0.0.1:8000/api/rules/\<int:rule_id>
- 通过主题名获取解析规则
http://127.0.0.1:8000/api/rules/\<string:rule_name>
> get(rule_id=None, rule_name=None)

## post()
## delete()
## put()