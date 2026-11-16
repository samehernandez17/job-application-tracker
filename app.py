from flask import Flask, render_template, request, redirect, url_for, flash
import mysql.connector
import os
import database as db


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




#============================================================================================
#Contacts
#============================================================================================





#============================================================================================
#Job Match: Main logic 
#============================================================================================










    















if __name__ == '__main__':
    app.run(debug=True)





