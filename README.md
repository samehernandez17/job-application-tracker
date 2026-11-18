# Job Application Tracker
A web application to help track job applications during the job
search process.
## Features 
- Track companies and job listings
- Record application submissions
- Manage interview schedules
- Store contact information
## Technologies
- MySQL Database
- Python with Flask
- HTML/CSS for the web interface
## Requirements
- Python 3.9 or newer
- MYSQL Server 8.0 or newer, running on your system
- MYSQL Workbench (Easiest way to run the schema.sql file)
- Git


## Setup

### 1.Clone the repository
Run these commands by navigating to the target directory in your system terminal and pasting:

```
git clone https://github.com/samehernandez17/job-application-tracker.git
cd job-application-tracker
```

### 2. Install the required Python libraries

```
python -m pip install -r requirements.txt
```

(Optional) If you want to keep the libraries separate from the rest of your system, you can create a virtual environment first:

```
python -m venv venv
venv\Scripts\activate
python -m pip install -r requirements.txt
```
If on macOS or Linux, activate it using `source venv/bin/activate`

### 3.Create SQL database

The file which creates the SQL database is 'schema.sql'

*Important: if you already have a database named `job_tracker` back it up as running the 'schema.sql' file drops it and recreates a new database with the same name

Open the MYSQL workbench, connect to your own server, click on File then open SQL Script, select 'schema.sql', and then run the script by clicking on the lightning bolt button.

if you want use the command line instead use:

```
mysql -u root -p < schema.sql
```

### 4. Set your MySQL password

Since the app connects as the MySQL user 'root' on 'localhost' and reads the password from an environment variable and is not stored in the code. You must set 'DB_PASSWORD' in the same 
terminal you use to run the site 

Windows Command Prompt:
```
set DB_PASSWORD=your_mysql_password
```

Windows PowerShell:
```
$env:DB_PASSWORD="your_mysql_password"
```

macOS or Linux:
```
export DB_PASSWORD=your_mysql_password
```

If your MySQL 'root' user does not have a password, you can skip this step entirely

Other settings regarding the Database can be changed as well if neccessary:

| Variable | Default | Purpose |
|---|---|---|
| `DB_HOST` | `localhost` | MySQL server address |
| `DB_USER` | `root` | MySQL user |
| `DB_PASSWORD` | (empty) | MySQL password |
| `DB_NAME` | `job_tracker` | Database name |

### 5. Run the app 

```
python app.py
```

*Important: Use the same terminal you used for the previous step if you did so

Now that you have the app running  open **http://127.0.0.1:5000** in your desired web browser, and leave the terminal open while you use the app. 

The Job tracker should now be up and running.

### 6. Exit/ Stop the app

Press CTRL+C in the terminal to stop the app.


## Database
 
| Table | Main columns |
|---|---|
| `companies` | company_name, industry, website, city, state, notes |
| `jobs` | company_id (FK), job_title, job_type, salary_min, salary_max, job_url, date_posted, requirements (JSON) |
| `applications` | job_id (FK), application_date, status, resume_version, cover_letter_sent, interview_data (JSON) |
| `contacts` | company_id (FK), contact_name, title, email, phone, linkedin_url, notes |
 
Foreign keys use `ON DELETE CASCADE`: So deleting a company would also delete all of its corresponding jobs, applications, and contacts. Deleting a job would delete its applications


## Troubleshooting

- **`Access denied for user 'root'`:** the password you set is wrong or was not set in this terminal. Repeat step 4.
- **`Can't connect to MySQL server`:** MySQL is not running. Make sure to start the MySQL service and have it running.
- **`Unknown database 'job_tracker'`:** run `schema.sql` (step 3).
- **`ModuleNotFoundError: No module named 'flask'`:** Repeat step 2 again.





