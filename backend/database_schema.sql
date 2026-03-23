-- =====================================================
-- 绝缘材料参数工具小程序 - 数据库表结构设计
-- Database: shujiao
-- Version: 1.0
-- Date: 2026-02-01
-- =====================================================

-- 1. 用户表 (users)
-- 存储用户基本信息和微信登录凭证
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY COMMENT '用户ID',
    wechat_openid VARCHAR(64) UNIQUE NOT NULL COMMENT '微信OpenID',
    wechat_unionid VARCHAR(64) COMMENT '微信UnionID（可选）',
    nickname VARCHAR(100) DEFAULT '微信用户' COMMENT '用户昵称',
    avatar_url VARCHAR(512) COMMENT '用户头像URL',
    phone VARCHAR(20) COMMENT '手机号',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '注册时间',
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    last_login_at TIMESTAMP NULL COMMENT '最后登录时间',
    is_active BOOLEAN DEFAULT TRUE COMMENT '是否激活',
    is_vip BOOLEAN DEFAULT FALSE COMMENT '是否全库会员',
    vip_expire_at TIMESTAMP NULL COMMENT 'VIP到期时间',
    INDEX idx_wechat_openid (wechat_openid),
    INDEX idx_created_at (created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='用户表';

-- 2. 参数标准表 (parameters)
-- 存储材料参数标准信息
CREATE TABLE IF NOT EXISTS parameters (
    id INT AUTO_INCREMENT PRIMARY KEY COMMENT '参数ID',
    material_category VARCHAR(50) NOT NULL COMMENT '材料分类：玻纤板(FR-4/G11)|PI板|特种塑胶通用(PEEK/PPS/PEI/电木)',
    param_name VARCHAR(200) NOT NULL COMMENT '参数名称',
    param_definition TEXT COMMENT '参数定义',
    test_standard VARCHAR(200) COMMENT '测试标准（如：IPC-TM-650）',
    standard_unit VARCHAR(50) COMMENT '标准单位',
    user_focus VARCHAR(500) COMMENT '用户关注点',
    marking_spec TEXT COMMENT '标注规范',
    remark TEXT COMMENT '备注',
    is_core BOOLEAN DEFAULT FALSE COMMENT '是否核心参数',
    standard_value VARCHAR(200) COMMENT '标准值/参考值',
    view_count INT DEFAULT 0 COMMENT '查看次数',
    favorite_count INT DEFAULT 0 COMMENT '收藏次数',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    INDEX idx_material_category (material_category),
    INDEX idx_param_name (param_name),
    FULLTEXT INDEX ft_param_name_definition (param_name, param_definition)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='参数标准表';

-- 3. 模板库表 (templates)
-- 存储行业模板信息
CREATE TABLE IF NOT EXISTS templates (
    id INT AUTO_INCREMENT PRIMARY KEY COMMENT '模板ID',
    template_category VARCHAR(50) NOT NULL COMMENT '模板分类：参数表模板|店铺架构模板|实拍SOP模板|FAQ话术模板',
    template_name VARCHAR(200) NOT NULL COMMENT '模板名称',
    cover_image_url VARCHAR(512) COMMENT '封面图片URL',
    description TEXT COMMENT '模板描述',
    price DECIMAL(10,2) DEFAULT 0.00 COMMENT '价格（元）：0.00免费，9.9/19.9/29.9付费',
    is_free BOOLEAN DEFAULT TRUE COMMENT '是否免费',
    download_url VARCHAR(512) COMMENT '下载链接（阿里云盘/腾讯微云）',
    download_count INT DEFAULT 0 COMMENT '下载次数',
    purchase_count INT DEFAULT 0 COMMENT '购买次数',
    view_count INT DEFAULT 0 COMMENT '查看次数',
    is_active BOOLEAN DEFAULT TRUE COMMENT '是否上架',
    sort_order INT DEFAULT 0 COMMENT '排序权重（越大越靠前）',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    INDEX idx_template_category (template_category),
    INDEX idx_is_free (is_free),
    INDEX idx_sort_order (sort_order DESC),
    INDEX idx_created_at (created_at DESC)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='模板库表';

-- 4. 轻咨询预约表 (consultations)
-- 存储用户咨询预约记录
CREATE TABLE IF NOT EXISTS consultations (
    id INT AUTO_INCREMENT PRIMARY KEY COMMENT '咨询ID',
    user_id INT NOT NULL COMMENT '用户ID',
    name VARCHAR(100) NOT NULL COMMENT '姓名/称呼',
    company VARCHAR(200) COMMENT '公司/店铺名称（可选）',
    consult_type VARCHAR(100) NOT NULL COMMENT '咨询类型：产品参数梳理与合规标注|1688/淘宝店铺信息架构优化|工厂实拍素材规范指导',
    problem TEXT NOT NULL COMMENT '问题描述（至少50字）',
    contact VARCHAR(100) NOT NULL COMMENT '联系方式（微信/电话）',
    status VARCHAR(20) DEFAULT '待沟通' COMMENT '状态：待沟通|已完成|已取消',
    price DECIMAL(10,2) DEFAULT 99.00 COMMENT '咨询费用（元）',
    consultation_time TIMESTAMP NULL COMMENT '咨询时间',
    summary TEXT COMMENT '咨询总结',
    actions TEXT COMMENT '可执行动作（JSON格式）',
    admin_notes TEXT COMMENT '管理员备注',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '预约时间',
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_user_id (user_id),
    INDEX idx_status (status),
    INDEX idx_created_at (created_at DESC)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='轻咨询预约表';

-- 5. 用户收藏表 (user_favorites)
-- 存储用户收藏的参数和模板
CREATE TABLE IF NOT EXISTS user_favorites (
    id INT AUTO_INCREMENT PRIMARY KEY COMMENT '收藏ID',
    user_id INT NOT NULL COMMENT '用户ID',
    favorite_type VARCHAR(20) NOT NULL COMMENT '收藏类型：parameter|template',
    item_id INT NOT NULL COMMENT '项目ID（参数ID或模板ID）',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '收藏时间',
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    UNIQUE KEY uk_user_favorite (user_id, favorite_type, item_id),
    INDEX idx_user_type (user_id, favorite_type),
    INDEX idx_created_at (created_at DESC)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='用户收藏表';

-- 6. 订单表 (orders)
-- 存储模板购买和咨询预约的订单
CREATE TABLE IF NOT EXISTS orders (
    id INT AUTO_INCREMENT PRIMARY KEY COMMENT '订单ID',
    order_no VARCHAR(32) UNIQUE NOT NULL COMMENT '订单号',
    user_id INT NOT NULL COMMENT '用户ID',
    order_type VARCHAR(20) NOT NULL COMMENT '订单类型：template|consultation|vip_membership',
    item_id INT COMMENT '关联项目ID（模板ID或咨询ID）',
    item_name VARCHAR(200) NOT NULL COMMENT '项目名称',
    amount DECIMAL(10,2) NOT NULL COMMENT '订单金额（元）',
    status VARCHAR(20) DEFAULT 'pending' COMMENT '订单状态：pending|paid|cancelled|refunded',
    payment_method VARCHAR(20) COMMENT '支付方式：wechat',
    transaction_id VARCHAR(64) COMMENT '微信支付交易号',
    paid_at TIMESTAMP NULL COMMENT '支付时间',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_order_no (order_no),
    INDEX idx_user_id (user_id),
    INDEX idx_status (status),
    INDEX idx_created_at (created_at DESC)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='订单表';

-- 7. 下载记录表 (downloads)
-- 记录用户下载模板的历史
CREATE TABLE IF NOT EXISTS downloads (
    id INT AUTO_INCREMENT PRIMARY KEY COMMENT '下载ID',
    user_id INT NOT NULL COMMENT '用户ID',
    template_id INT NOT NULL COMMENT '模板ID',
    order_id INT COMMENT '关联订单ID（付费模板）',
    download_url VARCHAR(512) NOT NULL COMMENT '下载链接',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '下载时间',
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (template_id) REFERENCES templates(id) ON DELETE CASCADE,
    FOREIGN KEY (order_id) REFERENCES orders(id) ON DELETE SET NULL,
    INDEX idx_user_template (user_id, template_id),
    INDEX idx_created_at (created_at DESC)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='下载记录表';

-- 8. 意见反馈表 (feedbacks)
-- 存储用户反馈
CREATE TABLE IF NOT EXISTS feedbacks (
    id INT AUTO_INCREMENT PRIMARY KEY COMMENT '反馈ID',
    user_id INT COMMENT '用户ID（可选，支持匿名反馈）',
    feedback_type VARCHAR(50) NOT NULL COMMENT '反馈类型：功能建议|问题反馈|内容纠错|其他',
    content TEXT NOT NULL COMMENT '反馈内容',
    contact VARCHAR(100) COMMENT '联系方式（可选）',
    images TEXT COMMENT '截图URL（JSON数组）',
    status VARCHAR(20) DEFAULT 'pending' COMMENT '处理状态：pending|processing|resolved|closed',
    admin_reply TEXT COMMENT '管理员回复',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '反馈时间',
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE SET NULL,
    INDEX idx_user_id (user_id),
    INDEX idx_status (status),
    INDEX idx_created_at (created_at DESC)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='意见反馈表';

-- =====================================================
-- 初始化数据示例
-- =====================================================

-- 插入示例参数数据（玻纤板类别）
INSERT INTO parameters (material_category, param_name, param_definition, test_standard, standard_unit, user_focus, is_core) VALUES
('玻纤板(FR-4/G11)', '玻璃化温度Tg', '材料从玻璃态到高弹态的转变温度', 'IPC-TM-650 2.4.25', '℃', '影响耐热性和可靠性', TRUE),
('玻纤板(FR-4/G11)', '击穿电压', '材料被击穿时的电压强度', 'IPC-TM-650 2.5.6', 'kV/mm', '绝缘性能核心指标', TRUE),
('玻纤板(FR-4/G11)', '热膨胀系数CTE', '温度变化时材料的膨胀率', 'IPC-TM-650 2.4.24', 'ppm/℃', '影响焊接可靠性', TRUE);

-- 插入示例模板数据
INSERT INTO templates (template_category, template_name, cover_image_url, description, price, is_free, download_url, sort_order) VALUES
('参数表模板', 'FR-4玻纤板参数表标准模板', 'https://example.com/covers/fr4-template.jpg', '符合IPC标准的FR-4参数表模板，包含所有核心参数', 0.00, TRUE, 'https://aliyundrive.com/s/xxx', 100),
('参数表模板', 'PEEK特种塑胶全参数表模板', 'https://example.com/covers/peek-template.jpg', 'PEEK材料完整参数表，含热性能、力学性能、电性能', 19.90, FALSE, 'https://aliyundrive.com/s/yyy', 90),
('店铺架构模板', '1688店铺信息架构优化模板', 'https://example.com/covers/1688-template.jpg', '1688店铺信息架构方案，提升转化率', 29.90, FALSE, 'https://aliyundrive.com/s/zzz', 80);

-- 创建索引优化查询性能
-- 用于参数搜索的复合索引
CREATE INDEX idx_param_search ON parameters(material_category, is_core, view_count DESC);

-- 用于模板筛选的复合索引
CREATE INDEX idx_template_filter ON templates(template_category, is_free, is_active, sort_order DESC);

-- 用于订单查询的复合索引
CREATE INDEX idx_order_user_status ON orders(user_id, status, created_at DESC);
