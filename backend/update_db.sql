-- 添加MCP调用日志表
CREATE TABLE IF NOT EXISTS mcp_call_logs (
    id INT PRIMARY KEY AUTO_INCREMENT COMMENT '主键ID',
    request_params TEXT NOT NULL COMMENT '请求参数字JSON',
    response_result TEXT COMMENT '响应结果JSON',
    status VARCHAR(20) DEFAULT 'pending' COMMENT '调用状态：pending-等待中, running-执行中, completed-完成, failed-失败',
    error_message TEXT COMMENT '错误信息',
    duration_ms INT DEFAULT 0 COMMENT '调用耗时(毫秒)',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='MCP调用日志表 - 记录外部系统调用MCP的请求和响应';
