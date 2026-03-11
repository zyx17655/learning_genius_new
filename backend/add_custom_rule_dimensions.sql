-- 添加自定义规则专属维度字段到question_rules表
-- 执行此脚本前请确保数据库已备份

ALTER TABLE question_rules ADD COLUMN notation_convention TEXT COMMENT '学科表达与符号习惯';
ALTER TABLE question_rules ADD COLUMN assessment_focus TEXT COMMENT '考察偏好与方法论';
ALTER TABLE question_rules ADD COLUMN subject_traps TEXT COMMENT '干扰项逻辑陷阱';
ALTER TABLE question_rules ADD COLUMN stem_style TEXT COMMENT '语言风格与题干结构';
ALTER TABLE question_rules ADD COLUMN solution_blueprint TEXT COMMENT '解析深度与标准';
