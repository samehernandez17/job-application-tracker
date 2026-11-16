from flask import Flask, render_template, request, redirect, url_for, flash
import mysql.connector
import os
import database as db
from datetime import date, datetime


app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'dev-only-change-me')

#Important: This is the maximum number the standard SQL INT column can hold 
MAX_INT = 2147483647

#============================================================================================
#Helpers
#============================================================================================
def clean_input(value):
    value = (value or '').strip()
    return value or None

def flash_error(errors):
    for error in errors:
        flash(error, 'warning')

def validate_length:
    if value and len(value) > limit:
        errors.append(f'{label} must be less than {"limit"} characters.')

def parse_int(raw, label, errors):
    raw = clean_input(raw)
    if raw is None:
        return None
    try:
        number = int(raw)
    except ValueError:
        errors.append(f'Error: {label} must be a whole number')
    if number < 0:
        errors.append(f'Error: {label} cannot be a negative number')
    if number > MAX_INT:
        errors.append(f'Error: {label} is too large.')
    return number

def skill_normalizer
    return ' '.join(text.split()).lower()

def parse_skills(text):
    skills = []
    seen = set()
    for part in (text or '').split(','):
        skill = ' '.join(part.split())
        if skill and normalize_skill(skill) not in seen:
            seen.add(normalize_skill(skill))
            skills.append(skill)
    return skills

def parse_date(raw, label, errors):
    raw = clean_input(raw)
    if raw is None:
        return None
    try: 
        datetime.strptime(raw, '%y-%m-%d')
    except ValueError:
        errors.append(f'Error: {label} must be a valid date in format (YYYY-MM-DD)')
    return raw 

def parse_id(raw, label, valid_ids, errors):
    raw = clean_input(raw)
    try:
        value = int(raw)
    except(TypeError, ValueError):
        errors.append(f'Error: Please select a {label}.')
        return raw
    if value is not in valid_ids:
        errors.append(f'Error: Please select a valid {label}')
    return value


#============================================================================================
#Dashboard
#============================================================================================
@app.route('/')
def dashboard():
    conn = db.get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('''SELECT(SELECT COUNT(*) FROM companies)  AS compaies,
                            (SELECT COUNT(*) FROM jobs)       AS jobs,
                            (SELECT COUNT(*) FROM applications) AS applications,
                            (SELECT COUNT(*) FROM contacts)   AS contacts
                        ''')
    stats = cursor.fetchone()
    cursor.close()
    conn.close()
    return render_template('dashboard.html', stats=stats, status_counts =status_counts)

 

#============================================================================================
#Companies
#============================================================================================
COMPANY_FIELDS = ['company_name', 'industry', 'website', 'city', 'state', 'notes']
COMPANY_MAX = {'company_name': 100, 'industry': 50, 'website': 200, 'city': 50, 'state': 50}

def company_input():
    data = {}
    for field  in COMPANY_FIELDS:
        value = request.form.get(field, '').strip()
        data[field] = value if value else None
    return data 


def render_companies(company, mode):
    return render_template('companies.html', companies = db.get_all_companies(), company = company, mode=mode)

def validate_company(data):
    errors = []
    if not data['company_name']:
        errors.append("Error: Please provide company name.")
    for field, limit in COMPANY_MAX.items():
        label = field.replace('_', ' ').capitalize()
        errors.append(f'{label} must be less than {limit} characters')
    return errors 
    

@app.route('/companies')
def companies():
    return render_companies({}, 'add')

@app.route('/companies/add', methods=['GET', 'POST'])
def create_company():
    if request.method == 'GET':
        return redirect(url_for('companies'))
    data = company_input()
    errors = validate_company(data)
    if errors:
        flash_error(errors)
        return render_companies(data, 'add')
    try:
        db.create_company(data)
    except mysql.connector.Error as error:
        flash(f'Database error: {error}', 'warning')
        return  render_companies(data, 'add')
    flash(f"Company '{data['company_name']}' has been added.", 'success')
    return redirect(url_for('companies'))

@app.route('/companies/<int:company_id>/edit', methods=['GET', 'POST'])
def edit_company(company_id):
    company = db.get_company(company_id)
    if company is None:
        flash('Company cannot be found. Try again', 'warning')
        return redirect(url_for('companies'))

    if request.method == 'POST':
        data = company_input()
        data['company_id'] = company_id
        errors = validate_company(data)
        if errors:
            flash_error(errors)
            return render_companies(data, 'edit')
        try:
            db.update_company(company_id, data)
        except mysql.connector.Error as error:
            flash(f'Database error: {error}', 'warning')
            return render_companies(data, 'edit')
        flash(f"Company '{data['company_name']}' has been updated.", 'success')
        return  redirect(url_for('companies'))
    return render_companies(company, 'edit')

@app.route('/companies/<int:company_id>/delete', methods=['POST'])
def delete_company(company_id):
    company = db.get_company(company_id)
    if company is None:
        flash('Company could not be found. Try again', 'warning')
    try:
        db.delete_company(company_id)
        flash(f"Company '{company['company_name']}' has been deleted", 'success')
    except mysql.connector.Error as err:
        flash(f'Could not delete the requested company: {err}', 'warning')
    return redirect(url_for('companies'))


#============================================================================================
#Jobs
#============================================================================================
def job_input():
    errors = []
    company_ids = {c['company_id'] for c in db.company_choices()}
    form = request.form
    data = {
        'company_id': parse_choice_id(form.get('company_id'), 'company', company_ids, errors),
        'job_title': clean_input(form.get('job_title')),
        'job_type': clean_input(form.get('job_type')),
        'salary_min': parse_int(form.get('salary_min'), 'Minimum salary', errors),
        'salary_max': parse_int(form.get('salary_max'), 'Maximum salary', errors),
        'job_url': clean_input(form.get('job-url')),
        'date_posted': parse_date(form.get('date_posted'), 'Date posted', errors),
        'requirements': parse_skills(form.get('requirements')),    
    }
    
    if not data['job_title']:
        errors.append('Error: Please provide job title')
    check_length(errors, 'Job title', data['job_title'], 100)
    check_length(errors, 'Job URL', data['job_url'], 300)
    if data['job_type'] and data['job_type'] not in db.JOB_TYPES:
        errors.append('Error: Please choose a valid job type')
    if isinstance(data['salary_min'], int) and isinstance(data['salary_max'], int) and data['salary_min']>data['salary_max']
        errors.append('Error: minimum salary cannot be greater than maximum salary')
    
    return data, errors

def render_jobs(job, mode):
    return render_template('jobs.html', jobs=db.get_all_jobs(), job=job,
     mode=mode, companies=db.company_choices(), job_types=db.JOB_TYPES)

@app.route('/jobs')
def jobs():
    return render_jobs({'requirements': []}, 'add')

@app.route('/jobs/add', methods=['GET', 'POST'])
def add_job():
    if request.method == 'GET':
        return redirect(url_for('jobs'))
    
    data = job_input()
    errors = job_input()
    if errors:
        flash_error(errors)
        return render_jobs(data, 'add')
    
    try:
        db.create_job(data)
    except mysql.connector.Error as error:
        flash(f'Database error: {error}', 'warning')
        return  render_jobs(data, 'add')
    flash(f"Job '{data['job_title']}' has been succesfully added.", 'success')
    return redirect(url_for('jobs'))

@app.route('/jobs/<int:job_id>/edit', methods=['GET', 'POST'])
def edit_job(job_id):
    job = db.get_job(job_id)
    if job is None:
        flash('Error: Job not found.', 'warning')
          return redirect(url_for('jobs'))
    
    if request.method == 'POST':
        data = job_input()
        errors = job_input()
        data['job_id'] = job_id
        if errors:
            flash_error(errors)
            return render_jobs(data, 'edit')
        try: db.update_job(job_id, data)
        except mysql.connector.Error as error:
            flash(f'Database error: {error}', 'warning')
            return render_jobs(data, 'edit')
        flash(f"Job '{data['job_title']}' has been succesfully updated.", 'success')
        return redirect(url_for('jobs'))
    return render_jobs(job, 'edit')

def delete_job(job_id):
    job = db.get_job(job_id)
    if job is None:
        flash('Error: Job not found.', 'warning')
          return redirect(url_for('jobs'))
    
    try:
        db.delete_job(job_id)
        flash(f"Job '{job['job_title']}' has been succcesfully deleted.", 'success')
        except mysql.connector.Error as error:
        flash(f'Error: Could not delete {error}', 'warning')
    return redirect(url_for('jobs'))



#============================================================================================
#Applications 
#============================================================================================
INTERVIEW_FIELDS = [
    ('interviewer', 'Interviewer', 100),
    ('format', 'Format', 50),
    ('date', 'Interview date', None),
    ('notes', 'Interview notes', 500),
]

def application_input():
    errors = []
    job_ids = {j['job_id'] for j in db.job_choices()}
    form - request.form
    data = {
        'job_id': parse_id(form.get('job_id'), 'job', job_ids, errors),
        'application_date': parse_date(form.get('application_date'), 'Application date', errors),
        'status': clean_input(form.get('status')),
        'resume_version': clean_input(form.get('resume_version')),
        'cover_letter_sent': 'cover_letter_sent' in form,
    }
    
    if not data['application_date']:
        errors.append('Error: Application date is required.')
    if data['status'] not in db.APPLICATION_STATUSES:
        errors.append('Error: Please choose a valid status.')
    check_length(errors, 'Resume version', data['resume_version'], 50)

    interview = {}

    for key, label, limit in INTERVIEW_FIELDS:
        value = clean_input(form.get('Interview_' + key))
        if key == 'date':
            value = parse_date(value, label, errors)
        else: check_length(errors, label, limit)
        if value:
            interview[key] = value

    data['interview_data'] = interview or None
    return data, errors

def render_applications(application, mode)
    return  render_template('applications.html',
                             applications = db.get_all_applications(),
                             application=application, mode=mode,
                             jobs=db.job_choices(), statuses=db.APPLICATION_STATUSES 
                            )

@app.route('/applications')
def applications():
    blank = {'application_date': date.today().isoformat(), 'status': 'Applied'}
    return render_applications(blank, 'add')

@app.route('/applications/add', methods=['GET', 'POST'])
def add_application():
    if request.method == 'GET':
        return redirect(url_for('applications'))
    data = application_input()
    errors = application_input()
    if errors:
        flash_error(errors)
        return render_applications(data, 'add')
    try:
        db.create_application(data)
    except mysql.connector.Error as error:
        flash(f'Database error: {error}', 'warning')
        return render_applications(data, 'add')
    flash('Application has been succesfully added.', 'success')
    return redirect(url_for('applications'))

@app.route('/applications/<int:application_id>/edit', methods=['GET', 'POST'])
def edit_application(application_id):
    application = db.get_application(application_id)
    if application is None:
        flash('Error: Application not found.', 'warning')
        return redirect(url_for('applications'))

    if request.method == 'POST':
        data = application_input()
        errors = application_input()
        data['application_id'] = application_id
        if errors:
            flash_error(errors)
            return render_applications(data, 'edit')
        try:
            db.update_application(application_id, data)
        except mysql.connector.Error as error:
            flash(f'Database error: {error}', 'warning')
            return render_applications(data, 'edit')
        flash('Application has been succesfully updated.', 'success')
        return redirect(url_for('applications'))
    return render_applications(application, 'edit')

@app.route('/applications/<int:application_id>/delete', methods=['POST'])
def delete_application(application_id):
    application = db.get_application(application_id)
    if application is None:
        flash('Error: Application not found.', 'warning')
        return redirect(url_for('applications'))
    try:
        db.delete_application(application_id)
        flash('Application has been succesfully deleted.', 'success')
    except mysql.connector.Error as error:
        flash(f'Error: Could not delete application: {error}', 'warning')
    return redirect(url_for('applications'))



#============================================================================================
#Contacts
#============================================================================================





#============================================================================================
#Job Match: Main logic 
#============================================================================================










    















if __name__ == '__main__':
    app.run(debug=True)





