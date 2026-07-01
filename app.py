from flask import Flask, request, jsonify, render_template, send_file, make_response
from flask_cors import CORS
import csv
from datetime import datetime
import os
from io import StringIO

app = Flask(__name__)
CORS(app)

PATH = 'all excels/'
##> ------ Karthik Sarode : karthik.sarode23@gmail.com - UI for excel files ------

@app.route('/')
def home():
    """Displays the dashboard page of the application."""
    return render_template('dashboard.html')

@app.route('/applied-jobs', methods=['GET'])
def get_applied_jobs():
    '''
    Retrieves a list of applied jobs from the applications history CSV file.
    
    Returns a JSON response containing a list of jobs, each with details such as 
    Job ID, Title, Company, HR Name, HR Link, Job Link, External Job link, and Date Applied.
    
    If the CSV file is not found, returns a 404 error with a relevant message.
    If any other exception occurs, returns a 500 error with the exception message.
    '''

    try:
        jobs = []
        with open(PATH + 'all_applied_applications_history.csv', 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                jobs.append({
                    'Job_ID': row['Job ID'],
                    'Title': row['Title'],
                    'Company': row['Company'],
                    'HR_Name': row['HR Name'],
                    'HR_Link': row['HR Link'],
                    'Job_Link': row['Job Link'],
                    'External_Job_link': row['External Job link'],
                    'Date_Applied': row['Date Applied']
                })
        return jsonify(jobs)
    except FileNotFoundError:
        return jsonify({"error": "No applications history found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/dashboard-stats', methods=['GET'])
def get_dashboard_stats():
    """
    Retrieves dashboard statistics including:
    - Total applications
    - Total companies
    - Total job roles
    - Unique locations
    - Failed applications
    """
    try:
        companies = set()
        job_titles = set()
        locations = set()
        total_applied = 0
        
        # Read applied jobs
        with open(PATH + 'all_applied_applications_history.csv', 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                total_applied += 1
                companies.add(row.get('Company', '').strip())
                job_titles.add(row.get('Title', '').strip())
                locations.add(row.get('Work Location', '').strip())
        
        # Read failed jobs
        total_failed = 0
        try:
            with open(PATH + 'all_failed_applications_history.csv', 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    total_failed += 1
        except:
            total_failed = 0
        
        # Remove empty strings
        companies.discard('')
        job_titles.discard('')
        locations.discard('')
        
        return jsonify({
            "total_applied": total_applied,
            "total_failed": total_failed,
            "total_companies": len(companies),
            "total_job_roles": len(job_titles),
            "total_locations": len(locations),
            "total_applications": total_applied + total_failed
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/company-breakdown', methods=['GET'])
def get_company_breakdown():
    """Get breakdown of applications by company"""
    try:
        company_data = {}
        
        with open(PATH + 'all_applied_applications_history.csv', 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                company = row.get('Company', '').strip()
                if company:
                    if company not in company_data:
                        company_data[company] = 0
                    company_data[company] += 1
        
        # Sort by count
        sorted_companies = sorted(company_data.items(), key=lambda x: x[1], reverse=True)[:10]
        
        return jsonify({
            "companies": [{"name": c[0], "count": c[1]} for c in sorted_companies]
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/download-csv', methods=['GET'])
def download_csv():
    """
    Downloads a CSV file with the following columns:
    Job Role, Company, Location, Skills Required, Date Applied, Status
    """
    try:
        output = StringIO()
        writer = csv.writer(output)
        
        # Write header
        writer.writerow(['Job Role', 'Company', 'Location', 'Skills Required', 'Date Applied', 'Status'])
        
        # Write applied jobs
        try:
            with open(PATH + 'all_applied_applications_history.csv', 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    writer.writerow([
                        row.get('Title', ''),
                        row.get('Company', ''),
                        row.get('Work Location', ''),
                        row.get('Skills required', ''),
                        row.get('Date Applied', ''),
                        'Applied'
                    ])
        except:
            pass
        
        # Write failed jobs
        try:
            with open(PATH + 'all_failed_applications_history.csv', 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    writer.writerow([
                        row.get('Title', ''),
                        row.get('Company', ''),
                        row.get('Work Location', ''),
                        row.get('Skills required', ''),
                        row.get('Date Applied', ''),
                        'Failed/Skipped'
                    ])
        except:
            pass
        
        # Get the CSV content
        csv_content = output.getvalue()
        output.close()
        
        # Return as response
        response = make_response(csv_content)
        response.headers['Content-Disposition'] = f'attachment; filename=job_applications_{datetime.now().strftime("%Y%m%d")}.csv'
        response.headers['Content-Type'] = 'text/csv'
        return response
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/applied-jobs/<job_id>', methods=['PUT'])
def update_applied_date(job_id):
    """
    Updates the 'Date Applied' field of a job in the applications history CSV file.

    Args:
        job_id (str): The Job ID of the job to be updated.

    Returns:
        A JSON response with a message indicating success or failure of the update
        operation. If the job is not found, returns a 404 error with a relevant
        message. If any other exception occurs, returns a 500 error with the
        exception message.
    """
    try:
        data = []
        csvPath = PATH + 'all_applied_applications_history.csv'
        
        if not os.path.exists(csvPath):
            return jsonify({"error": f"CSV file not found at {csvPath}"}), 404
            
        # Read current CSV content
        with open(csvPath, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            fieldNames = reader.fieldnames
            found = False
            for row in reader:
                if row['Job ID'] == job_id:
                    row['Date Applied'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    found = True
                data.append(row)
        
        if not found:
            return jsonify({"error": f"Job ID {job_id} not found"}), 404

        with open(csvPath, 'w', encoding='utf-8', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=fieldNames)
            writer.writeheader()
            writer.writerows(data)
        
        return jsonify({"message": "Date Applied updated successfully"}), 200
    except Exception as e:
        print(f"Error updating applied date: {str(e)}")  # Debug log
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)

##<