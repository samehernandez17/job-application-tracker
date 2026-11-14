DROP DATABASE IF EXISTS job_tracker;
CREATE DATABASE job_tracker;
USE job_tracker;

#tables

#companies 
CREATE TABLE companies (
    company_id   INT PRIMARY KEY AUTO_INCREMENT,
    company_name VARCHAR(100) NOT NULL,
    industry     VARCHAR(50),
    website      VARCHAR(200),
    city         VARCHAR(50),
    state        VARCHAR(50),
    notes        TEXT
);

#jobs
CREATE TABLE jobs (
    job_id       INT PRIMARY KEY AUTO_INCREMENT,
    company_id   INT NOT NULL,
    job_title    VARCHAR(100) NOT NULL,
    job_type     ENUM('Full-time','Part-time','Contract','Internship'),
    salary_min   INT,
    salary_max   INT,
    job_url      VARCHAR(300),
    date_posted  DATE,
    requirements JSON,
    FOREIGN KEY (company_id) REFERENCES companies(company_id) ON DELETE CASCADE
);

#applications
CREATE TABLE applications (
    application_id    INT PRIMARY KEY AUTO_INCREMENT,
    job_id            INT NOT NULL,
    application_date  DATE NOT NULL,
    status            ENUM('Applied','Screening','Interview','Offer','Rejected','Withdrawn')
                      NOT NULL DEFAULT 'Applied',
    resume_version    VARCHAR(50),
    cover_letter_sent BOOLEAN DEFAULT FALSE,
    interview_data    JSON,
    FOREIGN KEY (job_id) REFERENCES jobs(job_id) ON DELETE CASCADE
);

#contacts
CREATE TABLE contacts (
    contact_id   INT PRIMARY KEY AUTO_INCREMENT,
    company_id   INT NOT NULL,
    contact_name VARCHAR(100) NOT NULL,
    title        VARCHAR(100),
    email        VARCHAR(100),
    phone        VARCHAR(20),
    linkedin_url VARCHAR(200),
    notes        TEXT,
    FOREIGN KEY (company_id) REFERENCES companies(company_id) ON DELETE CASCADE
);


 #Sample data
 INSERT INTO companies (company_name, industry, website, city, state, notes) VALUES
('Tech Solutions Inc', 'Technology', 'www.techsolutions.com', 'Miami', 'Florida', 'Referred by a classmate'),
('Data Analytics Corp', 'Data Science', 'www.dataanalytics.com', 'Austin', 'Texas', NULL),
('Cloud Systems LLC', 'Cloud Computing', 'www.cloudsystems.com', 'Seattle', 'Washington', 'Remote friendly'),
('Digital Innovations', 'Software', 'www.digitalinnovations.com', 'San Francisco', 'California', NULL),
('Smart Tech Group', 'AI/ML', 'www.smarttech.com', 'Boston', 'Massachusetts', 'Career fair contact');

INSERT INTO jobs (company_id, job_title, job_type, salary_min, salary_max, job_url, date_posted, requirements) VALUES
(1, 'Software Developer', 'Full-time', 70000, 90000, 'https://techsolutions.com/jobs/1', '2025-01-15', '["Python","SQL","Flask"]'),
(1, 'Software Engineering Intern', 'Internship', 25000, 35000, 'https://techsolutions.com/jobs/2', '2025-01-18', '["Python","Git","SQL"]'),
(2, 'Data Analyst', 'Full-time', 65000, 85000, 'https://dataanalytics.com/jobs/1', '2025-01-12', '["Python","SQL","Tableau"]'),
(2, 'Data Scientist', 'Full-time', 85000, 110000, 'https://dataanalytics.com/jobs/2', '2025-01-07', '["Python","SQL","Machine Learning","Statistics"]'),
(3, 'Cloud Engineer', 'Full-time', 80000, 100000, 'https://cloudsystems.com/jobs/1', '2025-01-08', '["AWS","Python","Linux","Docker"]'),
(3, 'Database Administrator', 'Full-time', 75000, 95000, 'https://cloudsystems.com/jobs/2', '2025-01-10', '["SQL","MySQL","Linux","Performance Tuning"]'),
(4, 'Full Stack Developer', 'Full-time', 75000, 98000, 'https://digitalinnovations.com/jobs/1', '2025-01-14', '["JavaScript","HTML","CSS","Python","Flask"]'),
(5, 'ML Engineer', 'Full-time', 90000, 115000, 'https://smarttech.com/jobs/1', '2025-01-11', '["Python","TensorFlow","Machine Learning","SQL"]');

INSERT INTO applications (job_id, application_date, status, resume_version, cover_letter_sent, interview_data) VALUES
(1, '2025-01-16', 'Applied', 'v2.1', TRUE, NULL),
(3, '2025-01-13', 'Interview', 'v2.1', TRUE, '{"interviewer": "Michael Chen", "format": "Video call", "date": "2025-01-22", "notes": "Prepare SQL window function examples"}'),
(5, '2025-01-09', 'Rejected', 'v2.0', FALSE, NULL),
(7, '2025-01-15', 'Screening', 'v2.1', TRUE,  '{"interviewer": "HR screen", "format": "Phone", "date": "2025-01-20", "notes": "15 minute intro call"}'),
(8, '2025-01-12', 'Offer', 'v2.1', TRUE, '{"interviewer": "Lisa Garcia", "format": "On-site", "date": "2025-01-25", "notes": "Offer expected within a week"}'),
(2, '2025-01-19', 'Applied', 'v3.0', TRUE, NULL);

INSERT INTO contacts (company_id, contact_name, title, email, phone, linkedin_url, notes) VALUES
(1, 'Sarah Johnson', 'HR Manager', 'sjohnson@techsolutions.com', '305-555-0101', 'linkedin.com/in/sarahjohnson', 'Met at career fair'),
(2, 'Michael Chen', 'Technical Recruiter', 'mchen@dataanalytics.com', '512-555-0102', 'linkedin.com/in/michaelchen', NULL),
(3, 'Emily Williams', 'Hiring Manager', 'ewilliams@cloudsystems.com', '206-555-0103', NULL, 'Prefers email'),
(4, 'David Brown', 'Senior Developer', NULL, '415-555-0104', 'linkedin.com/in/davidbrown', 'No email on file'),
(5, 'Lisa Garcia', 'Talent Acquisition', 'lgarcia@smarttech.com', '617-555-0105', 'linkedin.com/in/lisagarcia', NULL),
(1, 'Robert Kim', 'Engineering Manager', 'rkim@techsolutions.com', NULL, NULL, NULL);