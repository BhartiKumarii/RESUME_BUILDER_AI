-- database/schema.sql

-- Users table
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    mobile VARCHAR(15) UNIQUE NOT NULL,
    full_name VARCHAR(100),
    email VARCHAR(100),
    gender VARCHAR(20),
    address TEXT,
    profession VARCHAR(100),
    verification_data JSON,
    id_verified BOOLEAN DEFAULT FALSE,
    id_data JSON,
    resume_path VARCHAR(255),
    language VARCHAR(10) DEFAULT 'en',
    passkey_hash VARCHAR(255),
    remember_device BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Job tracking table
CREATE TABLE IF NOT EXISTS job_tracking (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_mobile VARCHAR(15) NOT NULL,
    job_id VARCHAR(50) NOT NULL,
    action ENUM('viewed', 'saved', 'applied') NOT NULL,
    job_data JSON,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_mobile) REFERENCES users(mobile) ON DELETE CASCADE
);

-- User sessions table
CREATE TABLE IF NOT EXISTS user_sessions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_mobile VARCHAR(15) NOT NULL,
    session_token VARCHAR(255) UNIQUE NOT NULL,
    expires_at TIMESTAMP NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_mobile) REFERENCES users(mobile) ON DELETE CASCADE
);

-- OTP verification table
CREATE TABLE IF NOT EXISTS otp_verifications (
    id INT AUTO_INCREMENT PRIMARY KEY,
    mobile VARCHAR(15) NOT NULL,
    otp_code VARCHAR(6) NOT NULL,
    verified BOOLEAN DEFAULT FALSE,
    expires_at TIMESTAMP NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Resume version history table
CREATE TABLE IF NOT EXISTS resume_history (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_mobile VARCHAR(15) NOT NULL,
    template VARCHAR(50) NOT NULL DEFAULT 'modern',
    file_path VARCHAR(255) NOT NULL,
    file_name VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_mobile) REFERENCES users(mobile) ON DELETE CASCADE
);

create table if not exists professions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) UNIQUE NOT NULL,
    description TEXT,
    icon_class VARCHAR(100)
);
-- Insert sample professions data (optional)
INSERT IGNORE INTO professions (name, description, icon_class) VALUES
('Driver', 'Professional driving services', 'fas fa-truck'),
('Electrician', 'Electrical installation and repair', 'fas fa-bolt'),
('Plumber', 'Plumbing and pipe fitting services', 'fas fa-faucet'),
('Carpenter', 'Woodworking and furniture making', 'fas fa-hammer'),
('Mechanic', 'Vehicle repair and maintenance', 'fas fa-tools'),
('Welder', 'Metal welding and fabrication', 'fas fa-fire'),
('Construction Worker', 'Construction and labor services', 'fas fa-hard-hat'),
('Painter', 'Painting and surface coating', 'fas fa-paint-roller'),
('Mason', 'Brick and stone work', 'fas fa-ruler-combined'),
('Gardener', 'Gardening and landscaping', 'fas fa-seedling'),
('Security Guard', 'Security and protection services', 'fas fa-shield-alt'),
('Cleaner', 'Cleaning and sanitation services', 'fas fa-broom');