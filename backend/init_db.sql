-- 智能教学系统数据库表结构
-- MySQL 5.6.16 兼容

-- 知识点表
CREATE TABLE IF NOT EXISTS knowledge_points (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL COMMENT '知识点名称',
    parent_id INT DEFAULT NULL COMMENT '父知识点ID',
    level INT NOT NULL DEFAULT 1 COMMENT '层级',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_parent_id (parent_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='知识点表';

-- 标签表
CREATE TABLE IF NOT EXISTS tags (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(50) NOT NULL UNIQUE COMMENT '标签名称',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='标签表';

-- 题目表
CREATE TABLE IF NOT EXISTS questions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    content TEXT NOT NULL COMMENT '题目内容',
    question_type VARCHAR(20) NOT NULL DEFAULT '单选' COMMENT '题型：单选/多选/判断/填空/主观',
    difficulty VARCHAR(10) NOT NULL DEFAULT 'L2' COMMENT '难度：L1-L5',
    status VARCHAR(20) NOT NULL DEFAULT '草稿' COMMENT '状态：草稿/待审核/已审核',
    source VARCHAR(50) DEFAULT '手动录入' COMMENT '来源：手动录入/系统生成/AI生成/导入',
    answer VARCHAR(500) DEFAULT NULL COMMENT '正确答案',
    explanation TEXT DEFAULT NULL COMMENT '解析',
    creator VARCHAR(50) DEFAULT '系统' COMMENT '创建人',
    reviewer VARCHAR(50) DEFAULT NULL COMMENT '审核人',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_question_type (question_type),
    INDEX idx_difficulty (difficulty),
    INDEX idx_status (status),
    INDEX idx_source (source)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='题目表';

-- 选项表
CREATE TABLE IF NOT EXISTS options (
    id INT AUTO_INCREMENT PRIMARY KEY,
    question_id INT NOT NULL COMMENT '题目ID',
    content TEXT NOT NULL COMMENT '选项内容',
    is_correct TINYINT(1) DEFAULT 0 COMMENT '是否正确答案',
    order_index INT NOT NULL DEFAULT 0 COMMENT '排序序号',
    INDEX idx_question_id (question_id),
    FOREIGN KEY (question_id) REFERENCES questions(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='选项表';

-- 题目-知识点关联表
CREATE TABLE IF NOT EXISTS question_knowledge (
    question_id INT NOT NULL,
    knowledge_point_id INT NOT NULL,
    PRIMARY KEY (question_id, knowledge_point_id),
    FOREIGN KEY (question_id) REFERENCES questions(id) ON DELETE CASCADE,
    FOREIGN KEY (knowledge_point_id) REFERENCES knowledge_points(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='题目-知识点关联表';

-- 题目-标签关联表
CREATE TABLE IF NOT EXISTS question_tags (
    question_id INT NOT NULL,
    tag_id INT NOT NULL,
    PRIMARY KEY (question_id, tag_id),
    FOREIGN KEY (question_id) REFERENCES questions(id) ON DELETE CASCADE,
    FOREIGN KEY (tag_id) REFERENCES tags(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='题目-标签关联表';

-- AI生成任务表
CREATE TABLE IF NOT EXISTS generation_tasks (
    id INT AUTO_INCREMENT PRIMARY KEY,
    knowledge_input VARCHAR(500) DEFAULT NULL COMMENT '知识输入',
    knowledge_ids VARCHAR(255) DEFAULT NULL COMMENT '知识点ID列表',
    question_types VARCHAR(255) NOT NULL COMMENT '题型列表',
    type_counts TEXT DEFAULT NULL COMMENT '各题型数量JSON',
    difficulty_config TEXT DEFAULT NULL COMMENT '难度配置JSON',
    distractor_list TEXT DEFAULT NULL COMMENT '干扰项列表JSON',
    preference_list TEXT DEFAULT NULL COMMENT '内容偏好列表JSON',
    custom_requirement TEXT DEFAULT NULL COMMENT '自定义要求',
    question_count INT NOT NULL DEFAULT 0 COMMENT '题目总数',
    status VARCHAR(20) NOT NULL DEFAULT 'pending' COMMENT '状态：pending/running/completed/failed',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    completed_at DATETIME DEFAULT NULL,
    result TEXT DEFAULT NULL COMMENT '生成结果JSON',
    INDEX idx_status (status)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='AI生成任务表';

-- 生成的题目表
CREATE TABLE IF NOT EXISTS generated_questions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    task_id INT NOT NULL COMMENT '任务ID',
    content TEXT NOT NULL COMMENT '题目内容',
    question_type VARCHAR(20) NOT NULL COMMENT '题型',
    difficulty VARCHAR(10) NOT NULL COMMENT '难度',
    answer VARCHAR(500) DEFAULT NULL COMMENT '正确答案',
    explanation TEXT DEFAULT NULL COMMENT '解析',
    design_reason TEXT DEFAULT NULL COMMENT '题目设计原因',
    distractor_reasons TEXT DEFAULT NULL COMMENT '干扰项设计原因JSON',
    knowledge_points VARCHAR(500) DEFAULT NULL COMMENT '知识点列表',
    options_json TEXT DEFAULT NULL COMMENT '选项JSON',
    is_selected TINYINT(1) DEFAULT 0 COMMENT '是否选中采纳',
    is_draft TINYINT(1) DEFAULT 0 COMMENT '是否存为草稿',
    is_discarded TINYINT(1) DEFAULT 0 COMMENT '是否废弃',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_task_id (task_id),
    FOREIGN KEY (task_id) REFERENCES generation_tasks(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='生成的题目表';

-- 插入初始知识点数据
INSERT INTO knowledge_points (name, parent_id, level) VALUES
('Python基础', NULL, 1),
('数据类型', NULL, 1),
('控制流', NULL, 1),
('函数', NULL, 1),
('面向对象', NULL, 1),
('异常处理', NULL, 1),
('文件操作', NULL, 1),
('模块与包', NULL, 1);

-- 插入初始标签数据
INSERT INTO tags (name) VALUES
('基础'),
('重要'),
('考点'),
('进阶'),
('高频');
