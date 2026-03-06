-- 添加 difficulty_reason 字段到 generated_questions 表
ALTER TABLE generated_questions ADD COLUMN difficulty_reason TEXT AFTER design_reason;
