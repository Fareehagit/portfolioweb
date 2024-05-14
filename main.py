from flask import Flask, render_template, redirect, url_for, request, session, flash
from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField, RadioField
from wtforms.validators import DataRequired, Email, ValidationError
from flask_mysqldb import MySQL
from werkzeug.utils import secure_filename
import os
import re


app = Flask(__name__)

app.config['MYSQL_HOST'] =  'localhost'
app.config['MYSQL_USER'] = 'admin'
app.config['MYSQL_PASSWORD'] = 'Admin.51214'
app.config['MYSQL_DB'] = 'portfolio'
app.config['MYSQL_PORT'] = 3307
app.secret_key = 'your_secret_key_here'


mysql = MySQL(app)

app.config['UPLOAD_FOLDER'] = 'C:/Users/Fari/Desktop/final/static/assets/img'

ALLOWED_extensions = set(['png', 'jpg', 'jpeg', 'gif'])
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_extensions

@app.route("/")
def home():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM home")
    user_data = cur.fetchall()
    cur.close()

    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM skills")
    skills_data = cur.fetchall()
    cur.close()

    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM experience")
    exp_data = cur.fetchall()
    cur.close()

    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM supervision")
    sup_data = cur.fetchall()
    cur.close()

    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM education")
    edu_data = cur.fetchall()
    cur.close()

    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM publications")
    pub_data = cur.fetchall()
    cur.close()

    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM summary")
    sum_data = cur.fetchall()
    cur.close()

    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM res_education")
    res_edu_data = cur.fetchall()
    cur.close()

    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM final")
    fyp_data = cur.fetchall()
    cur.close()

    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM res_projects")
    res_project_data = cur.fetchall()
    cur.close()

    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM projects")
    project_data = cur.fetchall()
    cur.close()

    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM costom")
    cust_data = cur.fetchall()
    
    cur.close()

    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM profile ")
    prof_data = cur.fetchone()
    cur.close()
    
    return render_template('index.html', user_data = user_data, skills_data = skills_data, exp_data = exp_data, sup_data = sup_data, edu_data = edu_data, pub_data = pub_data, sum_data = sum_data, res_edu_data = res_edu_data, fyp_data = fyp_data, res_project_data = res_project_data,project_data = project_data, cust = cust_data, prof = prof_data                   )


    

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    message = ''
    if request.method == 'POST':
        # Check if the form fields are present in the request
        if 'name' in request.form and 'password' in request.form and 'email' in request.form:
            name = request.form['name']
            password = request.form['password']
            email = request.form['email']

            # Check if the email already exists in the database
            cursor = mysql.connection.cursor()
            cursor.execute("SELECT * FROM user WHERE email = %s", (email,))
            existing_user = cursor.fetchone()
            cursor.close()

            if existing_user:
                message = 'Email Already exists!'
                flash(message, 'success')
            elif not name or not password or not email:
                message = "Please fill out the form!"
                flash(message, 'success')
            else:
                # Insert new user data into the database
                cursor = mysql.connection.cursor()
                cursor.execute("INSERT INTO user (name, password, email) VALUES (%s, %s, %s)", (name, password, email))
                mysql.connection.commit()
                cursor.close()
                message = 'You have successfully registered!'
        else:
            message = "Please fill out the form!"
            flash(message, 'success')

    return render_template('admin.html', message=message)

@app.route('/login', methods=['GET', 'POST'])
def login():
    message = ''
    if request.method == 'POST':
        # Check if the form fields are present in the request
        if 'name' in request.form and 'password' in request.form:
            name = request.form['name']
            password = request.form['password']

            # Fetch user data from the database
            cursor = mysql.connection.cursor()
            cursor.execute("SELECT * FROM user WHERE name = %s", (name,))
            user = cursor.fetchone()
            cursor.close()

            if user is None:
                message = 'Please enter correct username/password!'
                flash(message, 'success')
            elif user[3] != password:  # Assuming password is stored in the third column
                message = 'Please enter correct username/password!'
                flash(message, 'success')
            else:
                # Set up session for the user
                session['loggedin'] = True
                session['userid'] = user[0]  # Assuming user ID is stored in the first column
                session['name'] = user[1]  # Assuming username is stored in the second column
                message = 'Logged in successfully!'
                flash(message, 'success')
                return redirect(url_for('dashboard'))

    return render_template('login.html', message=message)
       


@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if 'loggedin' in session:
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM home ")
        user_data = cur.fetchone()
        cur.close()
        

        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM skills ")
        skills_data = cur.fetchone()
        
        cur.close()

        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM experience ")
        exp_data = cur.fetchone()
        cur.close()

        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM education ")
        edu_data = cur.fetchone()
        cur.close()

        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM projects ")
        proj_data = cur.fetchone()
        cur.close()

        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM supervision ")
        sup_data = cur.fetchone()
        cur.close()

        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM publications ")
        pub_data = cur.fetchone()
        cur.close()

        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM summary ")
        sum_data = cur.fetchone()
        cur.close()

        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM costom ")
        cust_data = cur.fetchall()
        # print(cust_data) 
        cur.close()

        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM profile ")
        prof_data = cur.fetchone()
        cur.close()

        message = request.args.get('message')

        return render_template('dashboard.html', entry=user_data, skl = skills_data, exp = exp_data, edu = edu_data, proj = proj_data, sup = sup_data, pub = pub_data, sum = sum_data, cust = cust_data, message = message, prof = prof_data)
    return redirect(url_for('login'))


@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('userid', None)
    session.pop('password', None)
    return redirect(url_for('login'))

@app.route('/profile')
def profile():
    if 'loggedin' in session:
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM profile ")
        prof_data = cur.fetchone()
        cur.close()
        
    return render_template('profile.html', entry = prof_data)

@app.route('/edit_home/<int:id>', methods=['GET', 'POST'])
def edit_home(id):
    if 'loggedin' in session:
        try:
            if request.method == 'GET':
                # Establish connection to MySQL
                cur = mysql.connection.cursor()

                # Execute SQL query to select data for the specific employee
                cur.execute("SELECT * FROM home WHERE id = %s", (id,))
                user_data = cur.fetchone()

                cur.close()

                # Render the edit template with the employee data
                return render_template('edit_home.html', data=user_data)
            elif request.method == 'POST':
                # Get form data
                name = request.form['name']
                title = request.form['title']
               

                # Establish connection to MySQL
                cur = mysql.connection.cursor()

                # Execute SQL query to update the data of the employee
                cur.execute("UPDATE home SET name = %s, title = %s WHERE id = %s", (name, title, id))
                mysql.connection.commit()
                cur.close()

                message = "Data updated successfully !"
                flash(message, 'success')

                # Redirect to dashboard after successful update
                return redirect(url_for('dashboard', message = message))
        except Exception as e:
            # Handle any errors that might occur during database access
            print("An error occurred:", e)
            return render_template('error.html', error_message="An error occurred while processing user data.")
    else:
        return redirect(url_for('login'))

@app.route('/edit_profile/<int:id>', methods=['GET', 'POST'])
def edit_profile(id):
    if 'loggedin' in session:
        try:
            if request.method == 'GET':
                # Establish connection to MySQL
                cur = mysql.connection.cursor()

                # Execute SQL query to select data for the specific employee
                cur.execute("SELECT * FROM profile WHERE id = %s", (id,))
                prof_data = cur.fetchone()
                print(prof_data)

                cur.close()

                # Render the edit template with the employee data
                return render_template('edit_profile.html', data=prof_data)
            elif request.method == 'POST':
                # Get form data
                name = request.form['name']
                email = request.form['email']
                telp = request.form['telp']
                birthday = request.form['birthday']
                location = request.form['location']

                # Check if a new image file is uploaded
                if 'uploadfile' in request.files:
                    file = request.files['uploadfile']
                    if file and allowed_file(file.filename):
                        filename = secure_filename(file.filename)
                        x =os.path.join(app.config['UPLOAD_FOLDER'], filename)
                        file.save(x)
                        filenameimage = "static/assets/img/"+filename
                else:
                    # If no new image uploaded, use the existing image filename from the database
                    filenameimage = request.form['filenameimage']

                # Establish connection to MySQL
                cur = mysql.connection.cursor()

                # Execute SQL query to update the data of the employee
                cur.execute("UPDATE profile SET name = %s, email = %s, telp = %s, birthday = %s, location = %s, img = %s  WHERE id = %s", (name, email, telp, birthday, location, filenameimage, id))
                mysql.connection.commit()
                cur.close()

                message = "Data updated successfully !"
                flash(message, 'success')

                # Redirect to dashboard after successful update
                return redirect(url_for('dashboard', message = message))
        except Exception as e:
            # Handle any errors that might occur during database access
            print("An error occurred:", e)
            return render_template('error.html', error_message="An error occurred while processing profile data.")
    else:
        return redirect(url_for('login')) 
   


@app.route('/edit_skill/<int:id>', methods=['GET', 'POST'])
def edit_skill(id):
    if 'loggedin' in session:
        try:
            if request.method == 'GET':
                # Establish connection to MySQL
                cur = mysql.connection.cursor()

                # Execute SQL query to select data for the specific employee
                cur.execute("SELECT * FROM skills WHERE id = %s", (id,))
                skills_data = cur.fetchone()

                cur.close()

                # Render the edit template with the employee data
                return render_template('edit_skill.html', data=skills_data)
            elif request.method == 'POST':
                # Get form data
                skill_name = request.form['skill_name']
                proficiency = request.form['proficiency']
                

                # Establish connection to MySQL
                cur = mysql.connection.cursor()

                # Execute SQL query to update the data of the employee
                cur.execute("UPDATE skills SET skill_name = %s, proficiency = %s WHERE id = %s", (skill_name, proficiency, id))
                mysql.connection.commit()
                cur.close()

                message = "Data updated successfully !"
                flash(message, 'success')

                # Redirect to dashboard after successful update
                return redirect(url_for('dashboard', message = message))
        except Exception as e:
            # Handle any errors that might occur during database access
            print("An error occurred:", e)
            return render_template('error.html', error_message="An error occurred while processing skills data.")
    else:
        return redirect(url_for('login')) 

@app.route('/edit_exp/<int:id>', methods=['GET', 'POST'])
def edit_experience(id):
    if 'loggedin' in session:
        try:
            if request.method == 'GET':
                # Establish connection to MySQL
                cur = mysql.connection.cursor()

                # Execute SQL query to select data for the specific employee
                cur.execute("SELECT * FROM experience WHERE id = %s", (id,))
                exp_data = cur.fetchone()

                cur.close()

                # Render the edit template with the employee data
                return render_template('edit_exp.html', data=exp_data)
            elif request.method == 'POST':
                # Get form data
                job_title = request.form['job_title']
                company_name = request.form['company']
                description = request.form['description']
                start_date = request.form['start_date']
                end_date = request.form['end_date']
                

                # Establish connection to MySQL
                cur = mysql.connection.cursor()

                # Execute SQL query to update the data of the employee
                cur.execute("UPDATE experience SET job_title = %s, company_name = %s, description = %s, start_date = %s, end_date = %s  WHERE id = %s", (job_title, company_name, description, start_date, end_date, id))
                mysql.connection.commit()
                cur.close()

                message = "Data updated successfully !"
                flash(message, 'success')

                # Redirect to dashboard after successful update
                return redirect(url_for('dashboard', message = message))
        except Exception as e:
            # Handle any errors that might occur during database access
            print("An error occurred:", e)
            return render_template('error.html', error_message="An error occurred while processing experience data.")
    else:
        return redirect(url_for('login'))      

@app.route('/edit_edu/<int:id>', methods=['GET', 'POST'])
def edit_education(id):
    if 'loggedin' in session:
        try:
            if request.method == 'GET':
                # Establish connection to MySQL
                cur = mysql.connection.cursor()

                # Execute SQL query to select data for the specific employee
                cur.execute("SELECT * FROM education WHERE id = %s", (id,))
                edu_data = cur.fetchone()

                cur.close()

                # Render the edit template with the employee data
                return render_template('edit_edu.html', data=edu_data)
            elif request.method == 'POST':
                # Get form data
                inst_name = request.form['inst_name']
                degree = request.form['degree']
                stdy_field = request.form['stdy_field']
                gpa_grade = request.form['gpa_grade']
                start_date = request.form['start_date']
                end_date = request.form['end_date']
                

                # Establish connection to MySQL
                cur = mysql.connection.cursor()

                # Execute SQL query to update the data of the employee
                cur.execute("UPDATE education SET inst_name = %s, degree = %s, stdy_field = %s, gpa_grade = %s, start_date = %s, end_date = %s  WHERE id = %s", (inst_name, degree, stdy_field, gpa_grade, start_date, end_date, id))
                mysql.connection.commit()
                cur.close()

                message = "Data updated successfully !"
                flash(message, 'success')

                # Redirect to dashboard after successful update
                return redirect(url_for('dashboard', message = message))
        except Exception as e:
            # Handle any errors that might occur during database access
            print("An error occurred:", e)
            return render_template('error.html', error_message="An error occurred while processing education data.")
    else:
        return redirect(url_for('login'))    

         
@app.route('/edit_project/<int:id>', methods=['GET', 'POST'])
def edit_project(id):
    if 'loggedin' in session:
        try:
            if request.method == 'GET':
                # Establish connection to MySQL
                cur = mysql.connection.cursor()

                # Execute SQL query to select data for the specific employee
                cur.execute("SELECT * FROM projects WHERE id = %s", (id,))
                proj_data = cur.fetchone()

                cur.close()

                # Render the edit template with the employee data
                return render_template('edit_project.html', data=proj_data)
            elif request.method == 'POST':
                # Get form data
                project_name = request.form['project_name']
                description = request.form['description']
            
                

                # Establish connection to MySQL
                cur = mysql.connection.cursor()

                # Execute SQL query to update the data of the employee
                cur.execute("UPDATE projects SET project_name = %s,  description = %s  WHERE id = %s", (project_name, description, id))
                mysql.connection.commit()
                cur.close()

                message = "Data updated successfully !"
                flash(message, 'success')

                # Redirect to dashboard after successful update
                return redirect(url_for('dashboard', message = message))
        except Exception as e:
            # Handle any errors that might occur during database access
            print("An error occurred:", e)
            return render_template('error.html', error_message="An error occurred while processing projects data.")
    else:
        return redirect(url_for('login'))
    
@app.route('/edit_sup/<int:id>', methods=['GET', 'POST'])
def edit_supervision(id):
    if 'loggedin' in session:
        try:
            if request.method == 'GET':
                # Establish connection to MySQL
                cur = mysql.connection.cursor()

                # Execute SQL query to select data for the specific employee
                cur.execute("SELECT * FROM supervision WHERE id = %s", (id,))
                sup_data = cur.fetchone()

                cur.close()

                # Render the edit template with the employee data
                return render_template('edit_sup.html', data=sup_data)
            elif request.method == 'POST':
                # Get form data
                sup_title = request.form['sup_title']
                description = request.form['description']
            
                

                # Establish connection to MySQL
                cur = mysql.connection.cursor()

                # Execute SQL query to update the data of the employee
                cur.execute("UPDATE supervision SET sup_title = %s,  description = %s  WHERE id = %s", (sup_title, description, id))
                mysql.connection.commit()
                cur.close()

                message = "Data updated successfully !"
                flash(message, 'success')

                # Redirect to dashboard after successful update
                return redirect(url_for('dashboard', message = message))
        except Exception as e:
            # Handle any errors that might occur during database access
            print("An error occurred:", e)
            return render_template('error.html', error_message="An error occurred while processing supervision data.")
    else:
        return redirect(url_for('login'))  


@app.route('/edit_publication/<int:id>', methods=['GET', 'POST'])
def edit_publication(id):
    if 'loggedin' in session:
        try:
            if request.method == 'GET':
                # Establish connection to MySQL
                cur = mysql.connection.cursor()

                # Execute SQL query to select data for the specific employee
                cur.execute("SELECT * FROM publications WHERE id = %s", (id,))
                edu_data = cur.fetchone()

                cur.close()

                # Render the edit template with the employee data
                return render_template('edit_publication.html', data=edu_data)
            elif request.method == 'POST':
                # Get form data
                author = request.form['author']
                auth_profession = request.form['auth_profession']
                description = request.form['description']
           
                

                # Establish connection to MySQL
                cur = mysql.connection.cursor()

                # Execute SQL query to update the data of the employee
                cur.execute("UPDATE publications SET author = %s, auth_profession = %s, description = %s  WHERE id = %s", (author, auth_profession,  description, id))
                mysql.connection.commit()
                cur.close()

                message = "Data updated successfully !"
                flash(message, 'success')

                # Redirect to dashboard after successful update
                return redirect(url_for('dashboard', message = message))
        except Exception as e:
            # Handle any errors that might occur during database access
            print("An error occurred:", e)
            return render_template('error.html', error_message="An error occurred while processing publications data.")
    else:
        return redirect(url_for('login'))


@app.route('/edit_res')
def edit_resume():

    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM summary ")
    sum_data = cur.fetchone()
    cur.close()

    
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM res_education ")
    redu_data = cur.fetchone()
    cur.close()

    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM final ")
    fyp_data = cur.fetchone()
    cur.close()
    print(fyp_data)

    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM res_projects ")
    res_proj_data = cur.fetchone()
    cur.close()
    

    return render_template('edit_res.html', redu = redu_data, sum = sum_data, fyp = fyp_data, rproj = res_proj_data)

@app.route('/del_res')
def del_resume():

    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM summary ")
    sum_data = cur.fetchone()
    cur.close()

    
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM res_education ")
    redu_data = cur.fetchone()
    cur.close()

    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM final ")
    fyp_data = cur.fetchone()
    cur.close()
    print(fyp_data)

    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM res_projects ")
    res_proj_data = cur.fetchone()
    cur.close()
    

    return render_template('del_res.html', redu = redu_data, sum = sum_data, fyp = fyp_data, rproj = res_proj_data)

@app.route('/edit_sumry/<int:id>', methods=['GET', 'POST'])
def edit_sumry(id):
    if 'loggedin' in session:
        try:
            if request.method == 'GET':
                # Establish connection to MySQL
                cur = mysql.connection.cursor()

                # Execute SQL query to select data for the specific employee
                cur.execute("SELECT * FROM summary WHERE id = %s", (id,))
                sum_data = cur.fetchone()

                cur.close()

                # Render the edit template with the employee data
                return render_template('edit_sumry.html', data=sum_data)
            elif request.method == 'POST':
                # Get form data
                name = request.form['name']
                about = request.form['about']
                email = request.form['email']
                address = request.form['address']
                telp = request.form['telp']
                
                

                # Establish connection to MySQL
                cur = mysql.connection.cursor()

                # Execute SQL query to update the data of the employee
                cur.execute("UPDATE summary SET name = %s, about = %s, email = %s, address = %s, telp = %s  WHERE id = %s", (name, about, email, address, telp, id))
                mysql.connection.commit()
                cur.close()

                message = "Data updated successfully !"
                flash(message, 'success')

                # Redirect to dashboard after successful update
                return redirect(url_for('dashboard', message = message))
        except Exception as e:
            # Handle any errors that might occur during database access
            print("An error occurred:", e)
            return render_template('error.html', error_message="An error occurred while processing summary data.")
    else:
        return redirect(url_for('login')) 


@app.route('/edit_redu/<int:id>', methods=['GET', 'POST'])
def edit_res_edu(id):
    if 'loggedin' in session:
        try:
            if request.method == 'GET':
                # Establish connection to MySQL
                cur = mysql.connection.cursor()

                # Execute SQL query to select data for the specific employee
                cur.execute("SELECT * FROM res_education WHERE id = %s", (id,))
                redu_data = cur.fetchone()

                cur.close()

                # Render the edit template with the employee data
                return render_template('edit_redu.html', data=redu_data)
            elif request.method == 'POST':
                # Get form data
                inst_name = request.form['inst_name']
                degree = request.form['degree']
                about = request.form['about']
                start_date = request.form['start_date']
                end_date = request.form['end_date']
                

                # Establish connection to MySQL
                cur = mysql.connection.cursor()

                # Execute SQL query to update the data of the employee
                cur.execute("UPDATE res_education SET inst_name = %s, degree = %s, about = %s, start_date = %s, end_date = %s  WHERE id = %s", (inst_name, degree, about, start_date, end_date, id))
                mysql.connection.commit()
                cur.close()

                message = "Data updated successfully !"
                flash(message, 'success')

                # Redirect to dashboard after successful update
                return redirect(url_for('dashboard', message = message))
        except Exception as e:
            # Handle any errors that might occur during database access
            print("An error occurred:", e)
            return render_template('error.html', error_message="An error occurred while processing resume education data.")
    else:
        return redirect(url_for('login'))
    
@app.route('/edit_fyp/<int:id>', methods=['GET', 'POST'])
def edit_fyp(id):
    if 'loggedin' in session:
        try:
            if request.method == 'GET':
                # Establish connection to MySQL
                cur = mysql.connection.cursor()

                # Execute SQL query to select data for the specific employee
                cur.execute("SELECT * FROM final WHERE id = %s", (id,))
                fyp_data = cur.fetchone()

                cur.close()

                # Render the edit template with the employee data
                return render_template('edit_fyp.html', data=fyp_data)
            elif request.method == 'POST':
                # Get form data
                title = request.form['title']
                description = request.form['description']
                acheivements = request.form['acheivements']
                technologies = request.form['technologies']
                key_title = request.form['key_title']
                achive_title = request.form['achive_title']
                

                # Establish connection to MySQL
                cur = mysql.connection.cursor()

                # Execute SQL query to update the data of the employee
                cur.execute("UPDATE final SET title = %s, description = %s, acheivements = %s, technologies = %s, key_title = %s, achive_title = %s  WHERE id = %s", (title, description, acheivements, technologies, key_title, achive_title, id))
                mysql.connection.commit()
                cur.close()

                message = "Data updated successfully !"
                flash(message, 'success')

                # Redirect to dashboard after successful update
                return redirect(url_for('dashboard', message = message))
        except Exception as e:
            # Handle any errors that might occur during database access
            print("An error occurred:", e)
            return render_template('error.html', error_message="An error occurred while processing resume fyp data.")
    else:
        return redirect(url_for('login'))

@app.route('/edit_rproj/<int:id>', methods=['GET', 'POST'])
def edit_rproj(id):
    if 'loggedin' in session:
        try:
            if request.method == 'GET':
                # Establish connection to MySQL
                cur = mysql.connection.cursor()

                # Execute SQL query to select data for the specific employee
                cur.execute("SELECT * FROM res_projects WHERE id = %s", (id,))
                res_proj_data = cur.fetchone()

                cur.close()

                # Render the edit template with the employee data
                return render_template('edit_rproj.html', data=res_proj_data)
            elif request.method == 'POST':
                # Get form data
                title = request.form['title']
                sub_title = request.form['sub_title']
                description = request.form['description']
               
                
                

                # Establish connection to MySQL
                cur = mysql.connection.cursor()

                # Execute SQL query to update the data of the employee
                cur.execute("UPDATE res_projects SET title = %s, sub_title = %s, description = %s  WHERE id = %s", (title, sub_title, description, id))
                mysql.connection.commit()
                cur.close()

                message = "Data updated successfully !"
                flash(message, 'success')

                # Redirect to dashboard after successful update
                return redirect(url_for('dashboard', message = message))
        except Exception as e:
            # Handle any errors that might occur during database access
            print("An error occurred:", e)
            return render_template('error.html', error_message="An error occurred while processing resume projects data.")
    else:
        return redirect(url_for('login'))        

@app.route('/add', methods=['GET', 'POST'])
def add_data():
    if 'loggedin' in session:
        if request.method == 'POST':
            try:
                # Get form data
                title = request.form['title']
                sub_title = request.form['sub_title']
                description = request.form['description']
            

                # Establish connection to MySQL
                cur = mysql.connection.cursor()
                # Execute SQL query to insert data into employes table
                cur.execute("INSERT INTO costom (title, sub_title, description) VALUES (%s, %s, %s)", (title, sub_title, description))
                mysql.connection.commit()
                cur.close()
                message = "Data added successfully !"
                flash(message, 'success')

                return redirect(url_for('dashboard', message = message))
            except Exception as e:
                # Handle any errors that might occur during database access
                print("An error occurred:", e)
                return render_template('error.html', error_message="An error occurred while inserting data.")
    return render_template('add.html')     
 

@app.route('/delete_cust/<int:id>')
def delete_cust(id):
    if 'loggedin' in session:
        try:
            # Establish connection to MySQL
            cur = mysql.connection.cursor()

            # Execute SQL query to delete the employee record
            cur.execute("DELETE FROM costom WHERE id = %s", (id,))
            mysql.connection.commit()
            cur.close()

            message = "Data deleted successfully !"
            flash(message, 'success')


            # Redirect to dashboard after successful deletion
            return redirect(url_for('dashboard' , message = message))
        except Exception as e:
            # Handle any errors that might occur during database access
            print("An error occurred:", e)
            return render_template('error.html', error_message="An error occurred while deleting  data.")
    else:
        return redirect(url_for('login'))
    


@app.route('/delete_skl')
def delete_skl():
    if 'loggedin' in session:
        try:
            # Establish connection to MySQL
            cur = mysql.connection.cursor()

            # Execute SQL query to truncate the skills table
            cur.execute("TRUNCATE TABLE skills")
            mysql.connection.commit()
            cur.close()

            message = "Table 'skills' truncated successfully !"
            flash(message, 'success')

            # Redirect to dashboard after successful truncation
            return redirect(url_for('dashboard', message=message))
        except Exception as e:
            # Handle any errors that might occur during database access
            print("An error occurred:", e)
            return render_template('error.html', error_message="An error occurred while truncating the 'skills' table.")
    else:
        return redirect(url_for('login'))



@app.route('/delete_exp')
def delete_exp():
    if 'loggedin' in session:
        try:
            # Establish connection to MySQL
            cur = mysql.connection.cursor()

            # Execute SQL query to truncate the skills table
            cur.execute("TRUNCATE TABLE experience")
            mysql.connection.commit()
            cur.close()

            message = "Table 'experience' truncated successfully !"
            flash(message, 'success')

            # Redirect to dashboard after successful truncation
            return redirect(url_for('dashboard', message=message))
        except Exception as e:
            # Handle any errors that might occur during database access
            print("An error occurred:", e)
            return render_template('error.html', error_message="An error occurred while truncating the 'experience' table.")
    else:
        return redirect(url_for('login'))
    
@app.route('/delete_edu')
def delete_edu():
    if 'loggedin' in session:
        try:
            # Establish connection to MySQL
            cur = mysql.connection.cursor()

            # Execute SQL query to truncate the skills table
            cur.execute("TRUNCATE TABLE education")
            mysql.connection.commit()
            cur.close()

            message = "Table 'education' truncated successfully !"
            flash(message, 'success')

            # Redirect to dashboard after successful truncation
            return redirect(url_for('dashboard', message=message))
        except Exception as e:
            # Handle any errors that might occur during database access
            print("An error occurred:", e)
            return render_template('error.html', error_message="An error occurred while truncating the 'education' table.")
    else:
        return redirect(url_for('login')) 

@app.route('/delete_proj')
def delete_proj():
    if 'loggedin' in session:
        try:
            # Establish connection to MySQL
            cur = mysql.connection.cursor()

            # Execute SQL query to truncate the skills table
            cur.execute("TRUNCATE TABLE projects")
            mysql.connection.commit()
            cur.close()

            message = "Table 'projects' truncated successfully !"
            flash(message, 'success')

            # Redirect to dashboard after successful truncation
            return redirect(url_for('dashboard', message=message))
        except Exception as e:
            # Handle any errors that might occur during database access
            print("An error occurred:", e)
            return render_template('error.html', error_message="An error occurred while truncating the 'projects' table.")
    else:
        return redirect(url_for('login'))

@app.route('/delete_sup')
def delete_sup():
    if 'loggedin' in session:
        try:
            # Establish connection to MySQL
            cur = mysql.connection.cursor()

            # Execute SQL query to truncate the skills table
            cur.execute("TRUNCATE TABLE supervision")
            mysql.connection.commit()
            cur.close()

            message = "Table 'supervision' truncated successfully !"
            flash(message, 'success')

            # Redirect to dashboard after successful truncation
            return redirect(url_for('dashboard', message=message))
        except Exception as e:
            # Handle any errors that might occur during database access
            print("An error occurred:", e)
            return render_template('error.html', error_message="An error occurred while truncating the 'supervision' table.")
    else:
        return redirect(url_for('login'))

@app.route('/delete_pub')
def delete_pub():
    if 'loggedin' in session:
        try:
            # Establish connection to MySQL
            cur = mysql.connection.cursor()

            # Execute SQL query to truncate the skills table
            cur.execute("TRUNCATE TABLE publications")
            mysql.connection.commit()
            cur.close()

            message = "Table 'publications' truncated successfully !"
            flash(message, 'success')

            # Redirect to dashboard after successful truncation
            return redirect(url_for('dashboard', message=message))
        except Exception as e:
            # Handle any errors that might occur during database access
            print("An error occurred:", e)
            return render_template('error.html', error_message="An error occurred while truncating the 'publications' table.")
    else:
        return redirect(url_for('login'))                
    
@app.route('/delete_home')
def delete_home():
    if 'loggedin' in session:
        try:
            # Establish connection to MySQL
            cur = mysql.connection.cursor()

            # Execute SQL query to truncate the skills table
            cur.execute("TRUNCATE TABLE home")
            mysql.connection.commit()
            cur.close()

            message = "Table 'home' truncated successfully !"
            flash(message, 'success')

            # Redirect to dashboard after successful truncation
            return redirect(url_for('dashboard', message=message))
        except Exception as e:
            # Handle any errors that might occur during database access
            print("An error occurred:", e)
            return render_template('error.html', error_message="An error occurred while truncating the 'home' table.")
    else:
        return redirect(url_for('login')) 

 



@app.route('/delete_resume')
def delete_resume():
    if 'loggedin' in session:
        try:
            # Establish connection to MySQL
            cur = mysql.connection.cursor()

            # Execute SQL query to truncate the skills table
            tables = ['summary', 'res_education', 'res_projects', 'final']
            for table in tables:
                cur.execute(f"TRUNCATE TABLE {table}")
            mysql.connection.commit()
            cur.close()

            message = "Tables in the 'resume' section truncated successfully !"
            flash(message, 'success')

            # Redirect to dashboard after successful truncation
            return redirect(url_for('dashboard', message=message))
        except Exception as e:
            # Handle any errors that might occur during database access
            print("An error occurred:", e)
            return render_template('error.html', error_message="An error occurred while truncating the 'resume' tables.")
    else:
        return redirect(url_for('login'))
                

     
    
           


app.run(debug=True)