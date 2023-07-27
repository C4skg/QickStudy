loginResponse = {
    '1000': {
        'status': 'success',
        'message': '登录成功',
        'route': ''
    },
    '1001': {
        'status': 'error',
        'message': '用户名或密码错误',
        'route': ''
    },
    '1002': {
        'status': 'error',
        'message': '验证码错误',
        'route': ''
    },
    '1003': {
        'status': 'error',
        'message': '你已登录',
        'route': ''
    },
    '1004': {
        'status': 'error',
        'message': '参数错误',
        'route': ''
    }
}

registerResponse = {
    '2000': {
        'status': 'success',
        'message': '已发送验证邮箱,注意接收',
        'route': '/'
    },
    '2001': {
        'status': 'error',
        'message': '注册用户已存在',
        'route': ''
    },
    '2002': {
        'status': 'error',
        'message': '账户名或密码格式错误',
        'route': ''
    },
    '2003': {
        'status': 'error',
        'message': '验证码错误',
        'route': ''
    },
    '2004': {
        'status': 'error',
        'message': '参数错误',
        'route': '/'
    }
}

resetResponse = {
    '3000': {
        'status': 'success',
        'message': '已发送重置邮件,注意接收',
        'route': ''
    },
    '3001': {
        'status': 'error',
        'message': '重置邮件已发送,请2分钟后再试',
        'route': ''
    },
    '3002': {
        'status': 'success',
        'message': '重置成功',
        'route': '/'
    },
    '3003': {
        'status': 'error',
        'message': '重置失败',
        'route': ''
    },
    '3004': {
        'status': 'error',
        'message': '用户不存在',
        'route': ''
    },
    '3005': {
        'status': 'error',
        'message': '新密码格式错误',
        'route': ''
    },
    '3006': {
        'status': 'error',
        'message': '距上次重置时间小于一天',
        'route': ''
    },
    '3007': {
        'status': 'error',
        'message': '验证码错误',
        'route': ''
    },
    '3008': {
        'status': 'error',
        'message': '参数错误',
        'route': ''
    }
}

activateResponse = {
    '4000': {
        'status': 'success',
        'message': '激活成功',
        'route': '/'
    },
    '4001': {
        'status': 'error',
        'message': '激活失败',
        'route': '/'
    },
    '4002': {
        'status': 'error',
        'message': '请不要重复激活',
        'route': '/'
    },
    '4003': {
        'status': 'error',
        'message': '参数错误',
        'route': '/'
    }
}

logoutResponse = {
    '5000': {
        'status': 'success',
        'message': '你已退出登录',
        'route': '/'
    },
    '5001': {
        'status': 'error',
        'message': '退出失败',
        'route': '/'
    }
}

uploadResponse = {
    '6000':{
        'status': 'success',
        'message': '上传成功',
        'files': [],
    },
    '6001':{
        'status': 'error',
        'message': '上传失败',
        'files': []
    },
    '6002': {
        'status': 'error',
        'message': '上传文件过大',
        'files': []
    },
    '6003':{
        'status': 'error',
        'message': '权限不足',
        'files': []
    }
}

articleResponse = {
    "7000":{
        "status": 'success',
        'message': '操作成功',
        'route': ''
    },
    "7001":{
        "status": 'error',
        'message': '操作失败',
        'route': ''
    },
    "7002":{
        "status": 'error',
        'message': '参数异常',
        'route': ''
    },
    "7003":{
        "status": 'error',
        'message': '权限不足',
        'route': ''
    }
}
