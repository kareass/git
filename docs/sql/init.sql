-- ============================================
-- 需求开发事项统计 - 数据库初始化脚本
-- MySQL 8.0+
-- ============================================

CREATE DATABASE IF NOT EXISTS `work_statistics`
  DEFAULT CHARACTER SET utf8mb4
  DEFAULT COLLATE utf8mb4_unicode_ci;

USE `work_statistics`;

-- ============================================
-- 用户表
-- ============================================
CREATE TABLE IF NOT EXISTS `sys_user` (
  `id` INT NOT NULL AUTO_INCREMENT COMMENT '主键',
  `username` VARCHAR(50) NOT NULL COMMENT '用户名（唯一）',
  `password_hash` VARCHAR(255) NOT NULL COMMENT '密码哈希（bcrypt）',
  `role` ENUM('admin', 'user') NOT NULL DEFAULT 'user' COMMENT '角色：admin=管理员，user=普通用户',
  `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_username` (`username`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='用户表';

-- ============================================
-- 任务表
-- ============================================
CREATE TABLE IF NOT EXISTS `sys_task` (
  `id` INT NOT NULL AUTO_INCREMENT COMMENT '主键',
  `name` VARCHAR(200) NOT NULL COMMENT '任务名称',
  `register_time` DATETIME NOT NULL COMMENT '登记时间',
  `complete_time` DATETIME NULL COMMENT '完成时间',
  `publisher` VARCHAR(50) NOT NULL COMMENT '发布人',
  `is_completed` TINYINT(1) NOT NULL DEFAULT 0 COMMENT '是否完成：0=未完成，1=已完成',
  `remark` TEXT NULL COMMENT '备注',
  `priority` ENUM('normal', 'medium', 'urgent') NOT NULL DEFAULT 'normal' COMMENT '优先级',
  `user_id` INT NOT NULL COMMENT '所属用户ID',
  `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  KEY `idx_user_id` (`user_id`),
  KEY `idx_is_completed` (`is_completed`),
  KEY `idx_register_time` (`register_time`),
  CONSTRAINT `fk_task_user` FOREIGN KEY (`user_id`) REFERENCES `sys_user` (`id`) ON DELETE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='任务表';

-- ============================================
-- 任务明细表
-- ============================================
CREATE TABLE IF NOT EXISTS `sys_task_detail` (
  `id` INT NOT NULL AUTO_INCREMENT COMMENT '主键',
  `task_id` INT NOT NULL COMMENT '所属任务ID',
  `name` VARCHAR(200) NOT NULL COMMENT '明细任务名称',
  `progress` VARCHAR(50) NULL COMMENT '当前进度',
  `time` DATETIME NULL COMMENT '时间',
  `remark` TEXT NULL COMMENT '备注',
  `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  KEY `idx_task_id` (`task_id`),
  CONSTRAINT `fk_detail_task` FOREIGN KEY (`task_id`) REFERENCES `sys_task` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='任务明细表';

-- ============================================
-- 初始化测试数据
-- ============================================

-- 密码: admin123 (bcrypt hash)
INSERT INTO `sys_user` (`username`, `password_hash`, `role`) VALUES
('admin', '$2b$12$F4cZCKmUURsgi5C7snXvvuhr6i2vKKqAXdIMoWJZkvI6To5QH9gay', 'admin'),
('user1', '$2b$12$F4cZCKmUURsgi5C7snXvvuhr6i2vKKqAXdIMoWJZkvI6To5QH9gay', 'user');

-- 测试任务数据
INSERT INTO `sys_task` (`name`, `register_time`, `publisher`, `is_completed`, `remark`, `priority`, `user_id`) VALUES
('完成用户登录功能开发', '2026-05-28 09:00:00', 'admin', 0, '需要对接前端', 'medium', 1),
('修复任务列表分页问题', '2026-05-28 10:30:00', 'admin', 0, NULL, 'normal', 1),
('完成后台数据库设计', '2026-05-27 14:00:00', 'user1', 1, '已输出ER图', 'urgent', 2);

-- 测试任务明细
INSERT INTO `sys_task_detail` (`task_id`, `name`, `progress`, `time`, `remark`) VALUES
(1, '前端登录页开发', '80%', '2026-05-28 11:00:00', '等待接口联调'),
(1, '后端登录API开发', '100%', '2026-05-28 10:00:00', '已完成'),
(3, '输出ER图', '100%', '2026-05-27 18:00:00', NULL);

-- ============================================
-- Oracle 兼容说明
-- ============================================
-- 如果需要兼容 Oracle，可将：
--   TINYINT(1) -> NUMBER(1)
--   DATETIME -> TIMESTAMP
--   TEXT -> CLOB
--   VARCHAR -> VARCHAR2
--   AUTO_INCREMENT -> 序列 + 触发器