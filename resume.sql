-- ============================================================================
-- UNIFIED RESUME PLATFORM - DATABASE SCHEMA & DATA
-- ============================================================================
-- This file contains:
-- 1. Database creation
-- 2. Table definitions
-- 3. INSERT statements for dummy data
--
-- Related files:
-- - insert_data.sql: Reference file for INSERT statements (linked to this file)
-- - init_database.py: Python script to initialize database
--
-- Usage:
-- Run in MySQL Workbench: SOURCE resume.sql;
-- Or use: python init_database.py
-- ============================================================================

-- Create Database
CREATE DATABASE IF NOT EXISTS unified_resume_platform;
USE unified_resume_platform;

-- ============================================================================
-- CLEAR ALL DATA (Uncomment below section to delete all existing data)
-- ============================================================================
/*
SET FOREIGN_KEY_CHECKS = 0;
DELETE FROM audit_log;
DELETE FROM match_details;
DELETE FROM resume_matches;
DELETE FROM job_analysis;
DELETE FROM job_skills;
DELETE FROM resume_skills;
DELETE FROM skills;
DELETE FROM job_descriptions;
DELETE FROM resumes;
ALTER TABLE audit_log AUTO_INCREMENT = 1;
ALTER TABLE match_details AUTO_INCREMENT = 1;
ALTER TABLE resume_matches AUTO_INCREMENT = 1;
ALTER TABLE job_analysis AUTO_INCREMENT = 1;
ALTER TABLE job_skills AUTO_INCREMENT = 1;
ALTER TABLE resume_skills AUTO_INCREMENT = 1;
ALTER TABLE skills AUTO_INCREMENT = 1;
ALTER TABLE job_descriptions AUTO_INCREMENT = 1;
ALTER TABLE resumes AUTO_INCREMENT = 1;
SET FOREIGN_KEY_CHECKS = 1;
*/
-- ============================================================================

-- Table: resumes
-- Stores resume information submitted by candidates
CREATE TABLE IF NOT EXISTS resumes (
    resume_id INT AUTO_INCREMENT PRIMARY KEY,
    resume_text LONGTEXT NOT NULL,
    candidate_name VARCHAR(255),
    candidate_email VARCHAR(255),
    uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_candidate_email (candidate_email),
    INDEX idx_uploaded_at (uploaded_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;





-- Table: resume_matches
-- Stores matching analysis results between resumes and job descriptions
CREATE TABLE IF NOT EXISTS resume_matches (
    match_id INT AUTO_INCREMENT PRIMARY KEY,
    resume_id INT NOT NULL,
    job_id INT NOT NULL,
    match_score DECIMAL(5,2) NOT NULL,
    skill_match_percentage DECIMAL(5,2),
    matched_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (resume_id) REFERENCES resumes(resume_id) ON DELETE CASCADE,
    FOREIGN KEY (job_id) REFERENCES job_descriptions(job_id) ON DELETE CASCADE,
    INDEX idx_resume_id (resume_id),
    INDEX idx_job_id (job_id),
    INDEX idx_match_score (match_score),
    INDEX idx_matched_at (matched_at),
    UNIQUE KEY unique_match (resume_id, job_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

 -- Jessica White -> Operations Director (Great match)

-- Table: skills
-- Master table for skills extracted from resumes and job descriptions
CREATE TABLE IF NOT EXISTS skills (
    skill_id INT AUTO_INCREMENT PRIMARY KEY,
    skill_name VARCHAR(255) NOT NULL UNIQUE,
    skill_category VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_skill_name (skill_name),
    INDEX idx_skill_category (skill_category)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;



-- Table: resume_skills
-- Junction table linking resumes to skills
CREATE TABLE IF NOT EXISTS resume_skills (
    resume_skill_id INT AUTO_INCREMENT PRIMARY KEY,
    resume_id INT NOT NULL,
    skill_id INT NOT NULL,
    proficiency_level ENUM('beginner', 'intermediate', 'advanced', 'expert') DEFAULT 'intermediate',
    FOREIGN KEY (resume_id) REFERENCES resumes(resume_id) ON DELETE CASCADE,
    FOREIGN KEY (skill_id) REFERENCES skills(skill_id) ON DELETE CASCADE,
    INDEX idx_resume_id (resume_id),
    INDEX idx_skill_id (skill_id),
    UNIQUE KEY unique_resume_skill (resume_id, skill_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;



-- Table: job_skills
-- Junction table linking job descriptions to required skills
CREATE TABLE IF NOT EXISTS job_skills (
    job_skill_id INT AUTO_INCREMENT PRIMARY KEY,
    job_id INT NOT NULL,
    skill_id INT NOT NULL,
    is_required BOOLEAN DEFAULT TRUE,
    importance_level ENUM('low', 'medium', 'high', 'critical') DEFAULT 'medium',
    FOREIGN KEY (job_id) REFERENCES job_descriptions(job_id) ON DELETE CASCADE,
    FOREIGN KEY (skill_id) REFERENCES skills(skill_id) ON DELETE CASCADE,
    INDEX idx_job_id (job_id),
    INDEX idx_skill_id (skill_id),
    INDEX idx_is_required (is_required),
    UNIQUE KEY unique_job_skill (job_id, skill_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;



-- Table: job_analysis
-- Stores detailed analysis of job descriptions
CREATE TABLE IF NOT EXISTS job_analysis (
    analysis_id INT AUTO_INCREMENT PRIMARY KEY,
    job_description_text LONGTEXT NOT NULL,
    keywords JSON,
    required_skills JSON,
    preferred_skills JSON,
    experience_level VARCHAR(100),
    education_requirements TEXT,
    analyzed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_analyzed_at (analyzed_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Table: match_details
-- Stores detailed breakdown of matching skills for each resume-job match
CREATE TABLE IF NOT EXISTS match_details (
    detail_id INT AUTO_INCREMENT PRIMARY KEY,
    match_id INT NOT NULL,
    matching_skills JSON,
    missing_skills JSON,
    resume_skills JSON,
    job_skills JSON,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (match_id) REFERENCES resume_matches(match_id) ON DELETE CASCADE,
    INDEX idx_match_id (match_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Table: audit_log
-- Tracks all major operations for auditing purposes
CREATE TABLE IF NOT EXISTS audit_log (
    log_id INT AUTO_INCREMENT PRIMARY KEY,
    action_type ENUM('resume_upload', 'job_post', 'match_analysis', 'job_analysis', 'resume_update', 'job_update') NOT NULL,
    entity_type VARCHAR(50),
    entity_id INT,
    performed_by VARCHAR(255),
    action_details JSON,
    performed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_action_type (action_type),
    INDEX idx_entity_type (entity_type),
    INDEX idx_performed_at (performed_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
