from app import app, db

with app.app_context():
    # 创建所有表
    db.create_all()
    print('数据库表结构创建成功！')
    
    # 初始化知识点数据
    from app.models import KnowledgePoint, Tag
    
    # 检查是否已有数据
    if KnowledgePoint.query.count() == 0:
        # 创建根知识点
        root = KnowledgePoint(name='课程总览', parent_id=None, level=1)
        db.session.add(root)
        
        # 创建一级知识点
        kp1 = KnowledgePoint(name='基础知识', parent_id=1, level=2)
        kp2 = KnowledgePoint(name='核心概念', parent_id=1, level=2)
        kp3 = KnowledgePoint(name='实践应用', parent_id=1, level=2)
        db.session.add_all([kp1, kp2, kp3])
        
        # 创建二级知识点
        kp1_1 = KnowledgePoint(name='基本定义', parent_id=2, level=3)
        kp1_2 = KnowledgePoint(name='发展历史', parent_id=2, level=3)
        kp2_1 = KnowledgePoint(name='核心原理', parent_id=3, level=3)
        kp2_2 = KnowledgePoint(name='关键技术', parent_id=3, level=3)
        kp3_1 = KnowledgePoint(name='实际操作', parent_id=4, level=3)
        kp3_2 = KnowledgePoint(name='故障处理', parent_id=4, level=3)
        db.session.add_all([kp1_1, kp1_2, kp2_1, kp2_2, kp3_1, kp3_2])
        
        db.session.commit()
        print('知识点数据初始化成功！')
    
    # 初始化标签数据
    if Tag.query.count() == 0:
        tags = ['重要', '难点', '常考', '基础', '进阶']
        for tag_name in tags:
            tag = Tag(name=tag_name)
            db.session.add(tag)
        db.session.commit()
        print('标签数据初始化成功！')