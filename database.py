# ====================================================================================================================
#Imports
# ====================================================================================================================
import os
import mysql.connector
import json



# ====================================================================================================================
#Constants: for dropdowns
# ====================================================================================================================
JOB_TYPES = ['Full-time', 'Part-time', 'Contract', 'Internship']
APPLICATION_STATUSES = ['Applied', 'Screening', 'Interview', 'Offer', 'Rejected', 'Withdrawn']




# ====================================================================================================================
#Database Helper Functions
# ====================================================================================================================
def get_db_connection():
    return mysql.connector.connect(
        host = os.environ.get('DB_HOST', 'localhost'),
        user = os.environ.get('DB_USER', 'root'),
        password = os.environ.get('DB_PASSWORD', ''),
        database = os.environ.get('DB_NAME', 'job_tracker')
    )


def list_all(sql, params=None):
    connection = get_db_connection()
    cursor = None

    try:
        cursor = connection.cursor(dictionary = True)
        cursor.execute(sql, params or ())
        return cursor.fetchall()
    finally:
        if cursor:
            cursor.close()
        connection.close()

def query_one(sql, params=None):
    connection = get_db_connection()
    cursor = None 

    try:
        cursor = connection.cursor(dictionary = True)
        cursor.execute(sql, params or ())
        return cursor.fetchone()
    finally:
        if cursor:
            cursor.close()
        connection.close()

def execute(sql, params =None):
    connection = get_db_connection()
    cursor = None

    try:
        cursor = connection.cursor()
        cursor.execute(sql, params or ())
        connection.commit()
        return cursor.lastrowid
    except mysql.connector.Error:
        connection.rollback()
        raise
    finally:
        if cursor:
            cursor.close()
        
        connection.close()
        

# ====================================================================================================================
#json helper functions
# ====================================================================================================================
def to_json(value):
    if value is None:
        return None
    
    return json.dumps(value) 

def from_json(value):
    if value is None:
        return None
    
    if isinstance(value, (bytes, bytearray)):
        value = value.decode('utf-8')

    if isinstance(value, (list, dict)):
        return value

    return json.loads(value)






# ====================================================================================================================
#Dropdown helpers
# ====================================================================================================================
def company_choices():
    return list_all('SELECT company_id, company_name FROM companies ORDER BY company_name')

def job_choices():
    return list_all('''
        SELECT j.job_id, j.job_title, c.company_name
        FROM jobs j
        JOIN companies c ON j.company_id = c.company_id
        ORDER BY c.company_name, j.job_title
    ''')





# ====================================================================================================================
#Company Functions
# ====================================================================================================================
def get_all_companies():
    return list_all('SELECT * FROM companies ORDER BY company_name')

def get_company(company_id):
    return query_one('SELECT * FROM companies WHERE company_id = %s', (company_id,))

def create_company(data):
    sql = '''
        INSERT INTO companies (company_name, industry, website, city, state, notes)
        VALUES(%s, %s, %s, %s, %s, %s)'''
    
    params =(data['company_name'], data['industry'], data['website'], data['city'], data['state'], data['notes'])
    
    return execute(sql, params)

def update_company(company_id, data):
    sql = '''UPDATE companies
             SET company_name = %s, industry = %s, website = %s, city = %s, state = %s, notes = %s
             WHERE company_id = %s'''

    params = (data['company_name'], data['industry'], data['website'], data['city'], data['state'], data['notes'], company_id,)
    
    execute(sql, params)

def delete_company(company_id):
     execute('DELETE FROM companies WHERE company_id = %s', (company_id,))



# ====================================================================================================================
#jobs functions
# ====================================================================================================================
def get_all_jobs():
    rows = list_all('''SELECT j.*, c.company_name
                        FROM jobs j
                        JOIN companies c ON j.company_id = c.company_id
                        ORDER BY j.date_posted DESC, j.job_title
                    ''')
    for row in rows:
        row['requirements'] = from_json(row['requirements']) or []
    return rows

def get_job(job_id):
    row = query_one('''
        SELECT j.*, c.company_name
        FROM jobs j
        JOIN companies c ON j.company_id = c.company_id
        WHERE j.job_id = %s
        ''', (job_id,))
    if row:
        row['requirements'] = from_json(row['requirements']) or []
    return row

def create_job(data):
    sql = '''INSERT INTO jobs (company_id, job_title, job_type, salary_min, salary_max,
                               job_url, date_posted, requirements)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)'''
    
    params = (data['company_id'], data['job_title'], data['job_type'],
                         data['salary_min'], data['salary_max'], data['job_url'],
                         data['date_posted'], to_json(data['requirements']))
    
    return execute(sql, params)


def update_job(job_id, data):
    sql = '''UPDATE jobs
             SET company_id = %s, job_title = %s, job_type = %s, salary_min = %s,
                 salary_max = %s, job_url = %s, date_posted = %s, requirements = %s
             WHERE job_id = %s'''

    params = (data['company_id'], data['job_title'], data['job_type'],
                  data['salary_min'], data['salary_max'], data['job_url'],
                  data['date_posted'], to_json(data['requirements']), job_id)
    
    execute(sql, params)


def delete_job(job_id):
    execute('DELETE FROM jobs WHERE job_id = %s', (job_id,))




# ====================================================================================================================
#Application functions 
# ====================================================================================================================
def get_all_applications():
    rows = list_all('''
        SELECT a.*, j.job_title, c.company_name
        FROM applications a
        JOIN jobs j ON a.job_id = j.job_id
        JOIN companies c ON j.company_id = c.company_id
        ORDER BY a.application_date DESC, a.application_id DESC
    ''')
    for row in rows:
        row['interview_data'] = from_json(row['interview_data'])
    return rows


def get_application(application_id):
    row = query_one('''
        SELECT a.*, j.job_title, c.company_name
        FROM applications a
        JOIN jobs j ON a.job_id = j.job_id
        JOIN companies c ON j.company_id = c.company_id
        WHERE a.application_id = %s
    ''', (application_id,))
    if row:
        row['interview_data'] = from_json(row['interview_data'])
    return row


def create_application(data):
    sql = '''INSERT INTO applications (job_id, application_date, status, resume_version,
               cover_letter_sent, interview_data)
             VALUES (%s, %s, %s, %s, %s, %s)'''

    params = (data['job_id'], data['application_date'], data['status'],
                         data['resume_version'], data['cover_letter_sent'],
                         to_json(data['interview_data']))
    return execute(sql, params)


def update_application(application_id, data):
    sql = '''UPDATE applications
             SET job_id = %s, application_date = %s, status = %s, resume_version = %s,
                 cover_letter_sent = %s, interview_data = %s
             WHERE application_id = %s'''

    params = (data['job_id'], data['application_date'], data['status'],
                  data['resume_version'], data['cover_letter_sent'],
                  to_json(data['interview_data']), application_id)
    
    execute(sql, params)


def delete_application(application_id):
    execute('DELETE FROM applications WHERE application_id = %s', (application_id,))




# ====================================================================================================================
#contacts functions
# ====================================================================================================================
def get_all_contacts():
    return list_all('''
        SELECT ct.*, c.company_name
        FROM contacts ct
        JOIN companies c ON ct.company_id = c.company_id
        ORDER BY ct.contact_name
    ''')


def get_contact(contact_id):
    return query_one('''
        SELECT ct.*, c.company_name
        FROM contacts ct
        JOIN companies c ON ct.company_id = c.company_id
        WHERE ct.contact_id = %s
    ''', (contact_id,))


def create_contact(data):
    sql = '''INSERT INTO contacts (company_id, contact_name, title, email, phone,
                                   linkedin_url, notes)
             VALUES (%s, %s, %s, %s, %s, %s, %s)'''

    params = (data['company_id'], data['contact_name'], data['title'],
                         data['email'], data['phone'], data['linkedin_url'],
                         data['notes'])
    
    return execute(sql, params)


def update_contact(contact_id, data):
    sql = '''UPDATE contacts
             SET company_id = %s, contact_name = %s, title = %s, email = %s,
                 phone = %s, linkedin_url = %s, notes = %s
             WHERE contact_id = %s'''

    params = (data['company_id'], data['contact_name'], data['title'],
                  data['email'], data['phone'], data['linkedin_url'],
                  data['notes'], contact_id)

    execute(sql, params)


def delete_contact(contact_id):
    execute('DELETE FROM contacts WHERE contact_id = %s', (contact_id,))





# ====================================================================================================================
#Dashboard function
# ====================================================================================================================

def get_counts():
    return query_one('''
        SELECT (SELECT COUNT(*) FROM companies)    AS companies,
               (SELECT COUNT(*) FROM jobs)         AS jobs,
               (SELECT COUNT(*) FROM applications) AS applications,
               (SELECT COUNT(*) FROM contacts)     AS contacts
    ''')

def get_status_counts():
    return list_all('''
        SELECT status, COUNT(*) AS count
        FROM applications
        GROUP BY status
        ORDER BY count DESC, status
    ''')





    



