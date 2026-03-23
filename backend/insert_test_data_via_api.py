"""通过API插入测试数据"""
import requests
import json

API_BASE = "http://localhost:8000/api/v1"

# 测试参数数据
parameters = [
    {
        "material_category": "玻纤板(FR-4/G11)",
        "param_name": "玻璃化温度Tg",
        "param_definition": "材料从玻璃态到高弹态的转变温度，是衡量材料耐热性的重要指标",
        "test_standard": "IPC-TM-650 2.4.25 (DSC法)",
        "standard_unit": "℃",
        "user_focus": "影响焊接耐热性、尺寸稳定性和可靠性，高Tg板材适用于多层板和高可靠性产品",
        "marking_spec": "标注格式：Tg ≥ 170℃（高Tg）或 Tg ≥ 150℃（中Tg）",
        "remark": "FR-4标准Tg为130-140℃，高Tg板材≥170℃",
        "is_core": True,
        "standard_value": "130-170℃",
        "view_count": 1250,
        "favorite_count": 85
    },
    {
        "material_category": "玻纤板(FR-4/G11)",
        "param_name": "击穿电压",
        "param_definition": "材料被击穿时的电压强度，是衡量绝缘性能的核心指标",
        "test_standard": "IPC-TM-650 2.5.6",
        "standard_unit": "kV/mm",
        "user_focus": "绝缘性能核心指标，关系产品安全性",
        "marking_spec": "标注格式：≥ XX kV/mm",
        "is_core": True,
        "standard_value": "≥40 kV/mm",
        "view_count": 1100,
        "favorite_count": 72
    },
    {
        "material_category": "玻纤板(FR-4/G11)",
        "param_name": "热膨胀系数CTE",
        "param_definition": "温度变化时材料的膨胀率，影响焊接可靠性",
        "test_standard": "IPC-TM-650 2.4.24",
        "standard_unit": "ppm/℃",
        "user_focus": "影响焊接可靠性，Z轴CTE尤其重要",
        "marking_spec": "标注X/Y/Z三个方向的CTE值",
        "is_core": True,
        "standard_value": "X/Y: 12-16 ppm/℃, Z: 50-70 ppm/℃",
        "view_count": 980,
        "favorite_count": 65
    },
    {
        "material_category": "PI板",
        "param_name": "介电常数",
        "param_definition": "材料的介电特性，影响信号传输速度",
        "test_standard": "IPC-TM-650 2.5.5.5",
        "standard_unit": "无",
        "is_core": True,
        "standard_value": "3.0-3.5 @ 1MHz",
        "view_count": 450,
        "favorite_count": 30
    },
    {
        "material_category": "特种塑胶通用(PEEK/PPS/PEI/电木)",
        "param_name": "拉伸强度",
        "param_definition": "材料抵抗拉伸破坏的能力",
        "test_standard": "ASTM D638",
        "standard_unit": "MPa",
        "is_core": True,
        "standard_value": "PEEK: 90-100 MPa",
        "view_count": 680,
        "favorite_count": 45
    },
]

# 测试模板数据
templates = [
    {
        "template_category": "参数表模板",
        "template_name": "FR-4玻纤板参数表标准模板",
        "cover_image_url": "https://via.placeholder.com/300x200?text=FR-4",
        "description": "符合IPC标准的FR-4参数表模板，包含所有核心参数",
        "price": 0.00,
        "is_free": True,
        "download_url": "https://example.com/templates/fr4-template.xlsx",
        "download_count": 156,
        "purchase_count": 0,
        "view_count": 890,
        "is_active": True,
        "sort_order": 100
    },
    {
        "template_category": "参数表模板",
        "template_name": "PEEK特种塑胶全参数表模板",
        "cover_image_url": "https://via.placeholder.com/300x200?text=PEEK",
        "description": "PEEK材料完整参数表，含热性能、力学性能、电性能",
        "price": 19.90,
        "is_free": False,
        "download_url": "https://example.com/templates/peek-template.xlsx",
        "download_count": 89,
        "purchase_count": 89,
        "view_count": 560,
        "is_active": True,
        "sort_order": 90
    },
    {
        "template_category": "店铺架构模板",
        "template_name": "1688店铺信息架构优化模板",
        "cover_image_url": "https://via.placeholder.com/300x200?text=1688",
        "description": "1688店铺信息架构方案，提升转化率",
        "price": 29.90,
        "is_free": False,
        "download_url": "https://example.com/templates/1688-template.xlsx",
        "download_count": 45,
        "purchase_count": 45,
        "view_count": 320,
        "is_active": True,
        "sort_order": 80
    },
    {
        "template_category": "实拍SOP模板",
        "template_name": "工厂实拍标准化流程SOP",
        "cover_image_url": "https://via.placeholder.com/300x200?text=SOP",
        "description": "工厂实拍素材规范指导，包含拍摄角度、光线要求等",
        "price": 9.90,
        "is_free": False,
        "download_url": "https://example.com/templates/photo-sop.pdf",
        "download_count": 120,
        "purchase_count": 120,
        "view_count": 450,
        "is_active": True,
        "sort_order": 70
    },
    {
        "template_category": "FAQ话术模板",
        "template_name": "材料参数常见问题FAQ话术库",
        "cover_image_url": "https://via.placeholder.com/300x200?text=FAQ",
        "description": "整理了50+常见客户询问话术及标准回复",
        "price": 0.00,
        "is_free": True,
        "download_url": "https://example.com/templates/faq-template.docx",
        "download_count": 230,
        "purchase_count": 0,
        "view_count": 780,
        "is_active": True,
        "sort_order": 60
    },
]

def insert_parameters():
    """插入参数数据"""
    print("🚀 开始插入参数数据...")
    for i, param in enumerate(parameters, 1):
        try:
            response = requests.post(f"{API_BASE}/parameters/", json=param)
            if response.status_code == 200:
                result = response.json()
                print(f"✅ [{i}/{len(parameters)}] 插入参数: {param['param_name']}")
            else:
                print(f"❌ [{i}/{len(parameters)}] 插入失败: {param['param_name']} - {response.text}")
        except Exception as e:
            print(f"❌ [{i}/{len(parameters)}] 错误: {param['param_name']} - {str(e)}")

def insert_templates():
    """插入模板数据"""
    print("\n🚀 开始插入模板数据...")
    for i, template in enumerate(templates, 1):
        try:
            response = requests.post(f"{API_BASE}/templates/", json=template)
            if response.status_code == 200:
                result = response.json()
                print(f"✅ [{i}/{len(templates)}] 插入模板: {template['template_name']}")
            else:
                print(f"❌ [{i}/{len(templates)}] 插入失败: {template['template_name']} - {response.text}")
        except Exception as e:
            print(f"❌ [{i}/{len(templates)}] 错误: {template['template_name']} - {str(e)}")

if __name__ == "__main__":
    insert_parameters()
    insert_templates()

    print("\n✅ 测试数据插入完成！")
    print("\n可以访问以下URL查看数据：")
    print(f"- 参数列表: {API_BASE}/parameters/")
    print(f"- 模板列表: {API_BASE}/templates/")
