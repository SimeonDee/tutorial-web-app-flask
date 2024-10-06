from flask import (request, make_response, 
                   jsonify, render_template, 
                   url_for, redirect, flash)
from flask_sqlalchemy import SQLAlchemy
from setup import create_app
import random
import sys

sys.setrecursionlimit(2000)

# Defining the application
app = create_app()

# from auth_blueprint import get_auth_blueprint_instance
# # Register auth blueprint with app
# auth_bp = get_auth_blueprint_instance()
# app.register_blueprint(auth_bp, url_prefix='/auth')

from models import Question, User, Subject, Result, create_db_tables
from utils.utilities import ensure_post_fields

# global constants
MAX_QUESTION_LIMIT = 50
MARKS_PER_QUESTION = 5


####################
# SUBJECTS
####################

# Get add subject form
@app.route('/subjects/add')
def add_subject():
    return render_template('admin/add_subject.html')

# Get add user form
@app.route('/add_user')
def add_user():
    return render_template('admin/add_user.html')

# show update user form
@app.route('/show_update_user/<int:id>')
def show_update_user(id):
    user = User.query.get_or_404(id, 
                    f'User with id {id} not found')
    return render_template('admin/update_user.html', user=user.to_json())

# Get all subjects
@app.route('/subjects', methods=['GET','POST'])
def list_subjects():
    user_type = request.args.get('user', '')

    if request.method == 'GET':
        subjects = Subject.query.all()
        subjects = [subject.to_json() for subject in subjects]

        if subjects:
            return render_template('admin/list_subjects.html', 
                                    subjects=subjects)
        else:
            return render_template('admin/list_subjects.html')
        
    elif request.method == 'POST':
        data = request.form if request.form else request.json
        valid_data = ensure_post_fields(data, resource='subject')

        if valid_data:
            # confirm if subject not already added
            existing_subject = Subject.query.filter(
                                Subject.name == data['name'].capitalize()
                                ).first()

            if existing_subject:
                err_msg = f'{data["name"]} already exists'
                return render_template('admin/add_subject.html', 
                                       error_message=err_msg, **data)
            
            # creates new subject
            new_subject = Subject(name=data['name'].capitalize())
            new_subject.insert()

            return render_template('admin/add_subject.html', success=True, subject_name=new_subject.name)

        else:
            err_msg = '"name" is a required post data field.'
            return render_template('admin/add_subject.html', 
                                   error_message=err_msg)
     

# Get a subject
@app.route('/subjects/<int:subject_id>', methods=['GET'])
def get_subject(subject_id):    
    # Find subject
    found_subject = Subject.query.get_or_404(
        subject_id, f'Subject with id {subject_id} not found.')
    
    return jsonify({
        'success':True,
        'data': found_subject.to_json()
    })


# Update a subject
@app.route('/subjects/<int:subject_id>', methods=['PATCH', 'POST'])
def update_subject(subject_id):
    
    # Find subject
    found_subject = Subject.query.get_or_404(subject_id, 
                        f'Subject with id {subject_id} not found.')

    data = request.form if request.form else request.json

    if 'name' in data:
        found_subject.name = data['name']

    found_subject.update()

    return redirect(url_for('list_subjects'))


# show update subject form
@app.route('/show_update_subject/<int:id>')
def show_update_subject(id):
    subject = Subject.query.get_or_404(id, 
                    f'Subject with id {id} not found')
    return render_template('admin/update_subject.html', subject=subject.to_json())


# Delete a subject
@app.route('/subjects/<int:id>/delete', methods=['GET','DELETE'])
def delete_subject(id):
    
    # Find subject
    found_subject = Subject.query.get_or_404(id, f'Subject with id {id} not found.')

    found_subject.delete()

    return redirect(url_for('list_subjects'))
    
    # return jsonify({
    #     'success': True,
    #     'message': f'Subject with id {subject_id} for "{found_subject.name}" deleted successfully.'
    # })


########################
# QUESTIONS
########################

# Get add question form
@app.route('/subjects/<int:subject_id>/questions/add')
def add_question(subject_id):
    subject = Subject.query.get_or_404(subject_id, 
                                       f'Subject with ID {subject_id} not found')
    return render_template('admin/add_question.html', subject=subject.to_json())


# Get all questions or Add a new question for a given subject
@app.route('/subjects/<int:subject_id>/questions', methods=['GET', 'POST'])
def list_subject_questions(subject_id):
    
    # Find subject
    subject = Subject.query.get(subject_id)

    if not subject:
        err_msg = f'Subject with id {subject_id} not found.'
        return render_template('admin/error_page.html', error_message=err_msg)
    
    #     return jsonify({
    #         'success':False,
    #         'message': f'Subject with id {subject_id} not found.'
    #     })
    
    
    if request.method == 'GET':
        questions = Question.query.filter(Question.subject_id == subject.id).all()
        
        if len(questions) == 0 or questions is None:
            return render_template('admin/list_questions.html', subject=subject.to_json())
            # return jsonify({
            #     'success':False,
            #     'message': f'No questions yet for {subject.name}.'
            # })
            
        questions = [question.to_json() for question in questions]

        return render_template('admin/list_questions.html', subject=subject.to_json(), questions=questions)
        # return jsonify({
        #     'success':True,
        #     'data': questions,
        #     'subject': subject.name,
        #     'total_questions': len(questions)
        # })

    elif request.method == 'POST':
        data = request.form if request.form else request.json
        valid_data = ensure_post_fields(data, resource='question')
        if not valid_data:
            err_msg = f'"question", "option1", "option2", "option3", "answer" are required fields.'
            return render_template('admin/add_question.html', 
                                   subject=subject.to_json(), 
                                   error_message=err_msg)
            # return jsonify({
            #     'success': False,
            #     'message': f'"question", "option1", "option2", "option3", "answer" are required fields.'
            # })

        new_question = Question(
            subject_id=subject.id,
            question=data['question'],
            option1=data['option1'],
            option2=data['option2'],
            option3=data['option3'],
            answer=data['answer'],
            )
        
        new_question.insert()
        # db.session.add(new_question)
        # db.session.commit()

        return render_template('admin/add_question.html', subject=subject.to_json(), success=True)
    
        # return jsonify({
        #     'success': True,
        #     'data': new_question.to_json()
        # })
    

# Get a specific subject's question
@app.route('/subjects/<int:subject_id>/questions/<int:question_id>', methods=['GET'])
def get_subject_question(subject_id, question_id):
    # Confirm subject with id exists
    subject = Subject.query.get_or_404(
        subject_id, f'Subject with id {subject_id} not found.')    
    # find the question for the subject
    found_question = Question.query.filter(
            Question.subject_id == subject.id, Question.id == question_id
        ).first_or_404(f'Question with id {question_id} for {subject.name} not found.')

    return jsonify({
        'success':True,
        'data': found_question.to_json()
    })


# Update a specific subject's question
@app.route('/subjects/<int:subject_id>/questions/<int:question_id>/edit', methods=['GET','PATCH', 'POST'])
def update_subject_question(subject_id, question_id):
    user_type = request.args.get('user', '')

    # Confirm subject with id exists
    subject = Subject.query.get_or_404(
        subject_id, f'Subject with id {subject_id} not found.')
    # find the question for the subject
    found_question = Question.query.filter(
            Question.subject_id == subject.id, Question.id == question_id
        ).first_or_404(f'Question with id {question_id} for {subject.name} not found.')


    if request.method == 'GET':
        if user_type == 'admin':

            return render_template('admin/update_question.html', subject=subject.to_json(), **found_question.to_json())
        
        return render_template('auth/update_question.html', subject=subject.to_json(), **found_question.to_json())
    elif request.method == 'PATCH' or request.method == 'POST':
        # extract request body data
        data = request.form if request.form else request.json
            
        if 'subject_id' in data:
            found_question.subject_id = subject.id
        if 'question' in data:
            found_question.question = data['question']
        if 'option1' in data:
            found_question.option1 = data['option1']
        if 'option2' in data:
            found_question.option2 = data['option2']
        if 'option3' in data:
            found_question.option3 = data['option3']
        if 'answer' in data:
            found_question.answer = data['answer']

        # update the question records
        found_question.update()

        if user_type == 'admin':
            return redirect(url_for('list_subject_questions', subject_id=subject_id) + '?user=admin')
        else:
            return redirect(url_for('admin_index'))
    

# Delete a specific subject's question
@app.route('/subjects/<int:subject_id>/questions/<int:question_id>/delete', methods=['GET'])
def delete_subject_question(subject_id, question_id):
    # Confirm subject with id exists
    subject = Subject.query.get_or_404(
        subject_id, f'Subject with id {subject_id} not found.')
    # find the question for the subject
    found_question = Question.query.filter(
            Question.subject_id == subject.id, Question.id == question_id
        ).first_or_404(f'Question with id {question_id} for {subject.name} not found.')
    # delete the found_question
    found_question.delete()

    user_category = request.args.get('user', '')
    flash(f'Question  {question_id} successfully deleted for "{subject.name}".')
    
    if user_category == 'admin':
        return redirect(url_for('list_subject_questions', subject_id=subject_id))
    else:
        return redirect(url_for('index'))


# Render start a quiz page
@app.route('/quiz/<int:subject_id>')
def quiz(subject_id):
    subject = Subject.query.get_or_404(subject_id, f'Subjet with given id {subject_id} not found')

    return render_template('quiz/quiz_launcher.html', user=session['user'], subject=subject.to_json())


# Get a randomized quiz question for a subject
@app.route('/subjects/<int:subject_id>/next_question', methods=['GET','POST'])
def show_next_subject_question(subject_id):
    subject = Subject.query.get_or_404(subject_id, f'Subject with id {subject_id} not found.')

    submitted_answer = ''
    correct_answer = ''
    total_score = 0
    previous_questions = []
    past_question_id = 0
    question_count = 0

    if request.method == 'GET':
        previous_questions = []
        question_count = 1
        total_score = 0
        
    elif request.method == 'POST': # Submit last and generate new
        # extract request body data
        data = request.form if request.form else request.json

        # if 'previous_questions' not in data:
        #     return jsonify({
        #         'success': False,
        #         'message': '"previous_questions" is a required body data field'
        #     }), 400
        
        if 'previous_questions' not in data:
            err_msg = '"previous_questions" is a required body data field'
            return render_template('quiz/quiz_launcher.html', 
                                subject=subject.to_json(), 
                                error_message=err_msg)

        if 'submitted_answer' not in data:
            err_msg = 'You have not selected any answer yet'
            past_question_id = int(data['question_id'])
            question = Question.query.get_or_404(past_question_id, f'Question with ID {past_question_id} not found')
            
            question = question.to_json()
            question['random_options'] = eval(data['random_options'])

            return render_template('quiz/quiz_launcher.html', 
                                subject=subject.to_json(), 
                                error_message=err_msg,
                                current_question=question,
                                question_count=int(data['question_count']),
                                show=True
                                )
        
        # if type(data['previous_questions']) != list:
        #     return jsonify({
        #         'success': False,
        #         'message': '"previous_questions" body data must be a list.'
        #     }), 400
        
        submitted_answer = data['submitted_answer'].strip().lower()
        correct_answer = data['correct_answer'].strip().lower()
        total_score = int(data['total_score'])
        previous_questions = eval(data['previous_questions'])
        past_question_id = int(data['question_id'])
        question_count = int(data['question_count'])

        if type(previous_questions) != list:
            err_msg = '"previous_questions" body data must be a list.'
            return render_template('quiz/quiz_launcher.html', 
                                subject=subject.to_json(), 
                                error_message=err_msg)
        
        if submitted_answer == correct_answer:
            total_score += MARKS_PER_QUESTION
        
        question_count += 1

        previous_questions.append(past_question_id)

    # find next questions not already sent before (new questions) from db
    new_question_pool = []
    new_question_pool = Question.query.filter(
            Question.subject_id == subject.id, 
            Question.id.notin_(previous_questions)
        ).all()
    
    # if len(new_question_pool) == 0 or new_question_pool is None:
    #     return jsonify({
    #         'success': False,
    #         'message': f'No more questions for "{subject.name}" subject.',
    #         'end': True
    #     }), 404

    if len(new_question_pool) == 0 or new_question_pool is None:
        # TO-DO: Handle result submission
        err_msg = 'No more questions for {{subject.name}}'
        # print(f'Total score: {total_score}')

        # Submit Result
        score_obtainable = (question_count-1) * MARKS_PER_QUESTION
        percentage_score = round(((total_score / score_obtainable) * 100), 0)

        # save result
        new_result = Result(user_id=session['user']['id'], 
                            subject_id=subject.id,
                            score=total_score, 
                            total_score=score_obtainable
                            )

        new_result.insert()

        return redirect(url_for('show_result', result_id=new_result.id))
        
    
    # randomly select a new question
    new_question = random.choice(new_question_pool)
    
    randomized_options = [
        new_question.answer, 
        new_question.option1, 
        new_question.option2, 
        new_question.option3
    ]

    random.shuffle(randomized_options)

    current_question = new_question.to_json()
    current_question['random_options'] = randomized_options

    context_data = {
        'subject': subject.to_json(),
        'current_question': current_question,
        'previous_questions': previous_questions,
        'total_score': total_score,
        'question_count': question_count,
        'show': True
    }

    if request.method == 'GET':
        context_data['start'] = True

    return render_template('quiz/quiz_launcher.html', **context_data)
    # return jsonify({
    #     'success':True,
    #     'question': new_question.to_json(),
    #     'subject': new_question.subject.to_json()

    # })


######################
# RESULTS
######################

# show all results
@app.route('/results', methods=['GET', 'POST'])
def list_results():
    user_type = request.args.get('user', '')

    if request.method == 'GET':
        # Fetch user results
        results = Result.query.all()

        if len(results) == 0 or results is None:     
            if user_type == 'admin':       
                return render_template('admin/list_results.html')
            return render_template('quiz/results.html')
        
        # return results in a much formatted way
        formatted_results = []
        for result in results:
            formatted_results.append({
                'id': result.id,
                'user': result.user,
                'subject': result.subject.name,
                'score': result.score,
                'total': result.total_score,
                'date': result.created_at,
                'percentage': round((result.score / result.total_score * 100), 0)
            })


        if user_type == 'admin':
            return render_template('admin/list_results.html', results=formatted_results)
        return render_template('quiz/results.html', results=formatted_results)

# Submit Results for user
@app.route('/results/users/<int:user_id>', methods=['GET', 'POST'])
def list_user_results(user_id):

    # ensure user_id is valid
    # user = User.query.filter(User.id == user_id
    #             ).get_or_404(f'User with id {user_id} not found.')
    
    if request.method == 'GET':
        # Fetch user results
        results = Result.query.filter(Result.user_id == user_id
                    ).order_by(Result.subject_id, Result.created_at
                        ).all()

        if 'user' in session:
            user=session['user']

        if len(results) == 0 or results is None:            
            return render_template('quiz/results.html', user=user)
        
        # return results in a much formatted way
        formatted_results = []
        for result in results:
            formatted_results.append({
                'id': result.id,
                'subject': result.subject.name,
                'score': result.score,
                'total': result.total_score,
                'date': result.created_at,
                'percentage': round((result.score / result.total_score * 100), 0)
            })
        
        return render_template('quiz/results.html', user=user, results=formatted_results)

    elif request.method == 'POST':
        data = request.form if request.form else request.json
        valid_data = ensure_post_fields(data, resource='result')
        if not valid_data:
            return jsonify({
                'success': False,
                'message': f'"subject_id", "score" and "total_questions" are required body fields.'
            })

        new_result = Result(user_id=user_id, 
                            subject_id=data['subject.id'],
                            score=data['score'], 
                            total_score=data['total_score'])
        
        new_result.insert()
        # db.session.add(new_result)
        # db.session.commit()

        return jsonify({
            'success': True,
            'data': new_result.to_json()
        })


# Show a Quiz Result for user
@app.route('/results/<int:result_id>', methods=['GET', 'POST'])
def show_result(result_id):
    result = Result.query.get_or_404(result_id, f'Result with ID {id} not found')
    percentage_score = round(((result.score / result.total_score) * 100), 0)
    result_data = {
        'result': result.to_json(),
        'percentage_score': percentage_score,
        'subject': result.subject.to_json()
    }

    return render_template('quiz/quiz_score_report.html', **result_data)


################################################################################
# AUTH ROUTES
################################################################################
from flask import ( Blueprint,
    request, render_template, 
    jsonify, url_for, make_response,
    redirect, session
    )
from utils.mail_utils.sendmail import (send_otp_to_mail, 
                            send_reset_link_to_mail)


@app.route('/', methods=['GET'])
def splash():
    if 'user' in session:
        return render_template('splash.html', user=session['user'])

    return render_template('splash.html')



@app.route('/home', methods=['GET'])
def index():
    
    if 'user' in session:
        user = session['user']

        subjects = Subject.query.all()

        subjects = [subject.to_json() for subject in subjects]

        # all_users = User.query.all()
        return render_template('quiz/index.html', user=user, subjects=subjects)
    else:
        return render_template('auth/login.html')

############
# REGISTER
############
@app.route('/auth/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('auth/register.html')
    elif request.method == 'POST':
        # collect user data
        data = request.form if request.form else request.json 
        user_type = request.args.get('user', '')
        
        try:
            if ('email' not in data or 'password' not in data or 
                'fullname' not in data):
                
                raise Exception('"email", "password" and "fullname" fields are required fields.')
            
            existingEmail = User.query.filter(User.email == data['email'].lower()).one_or_none()
            if existingEmail: 
                err_msg = 'Email address is already used'
                if user_type == 'admin':
                    return render_template('admin/add_user.html', error_message=err_msg, **data)
                else:
                    return render_template('auth/register.html', error_message=err_msg, **data)


            # create new user from collected data
            body_data = dict(data)
            body_data['email'] = body_data['email'].lower()
            new_user = User(**body_data) 

            # Add the new user to db
            new_user.insert()

            if user_type and user_type == 'admin':
                return redirect(url_for('admin_index'))


            return render_template('auth/register_success.html', username=new_user.fullname)
        
        except Exception as ex:
            if user_type and user_type == 'admin':
                return render_template('admin/add_user.html', error_message=ex.__str__(), **data)
            return render_template('auth/register.html', error_message=ex.__str__(), **data)


##########
# LOGIN
##########
@app.route('/auth/login', methods=['GET', 'POST'])
def login():
    user_type = request.args.get('user', '')

    if request.method == 'GET':
        if user_type == 'admin': 
            if 'user' not in session:
                return render_template('admin/login.html')
            elif session['user']['email'] == 'admin@admin.com':
                return redirect(url_for('admin_index'))
            else:
                return render_template('admin/login.html')
        
        elif user_type != 'admin' and 'user' in session:
            return redirect(url_for('index'))
        
        return render_template('auth/login.html')
    
    elif request.method == 'POST':
        # collect user data
        data = request.form if request.form else request.json 

        try:
            if 'email' not in data or 'password' not in data:
                raise Exception('"email" and "password" fields are required in post data.')

            email = data['email']
            password = data['password']

            # if user_type == 'admin':
            #     if email.lower() != 'admin@admin.com' and password != 'admin':
            #         return render_template('admin/login.html', error_message='Invalid Admin credentials')
                
                # Authenticate user from collected data
            user = User.query.filter_by(email=email, password=password).first()

            if user:        
                user.password = ''
                session['user'] = user.to_json()
                if user.email == 'admin@admin.com':
                    return redirect(url_for('admin_index'))
                
                return redirect(url_for('index'))
            
            else:
                if user_type == 'admin':
                    return render_template('admin/login.html', error_message="Invalid Admin login credentials", email=email, password=password)
                return render_template('auth/login.html', error_message="Invalid login credentials", email=email, password=password)
        
        except Exception as ex:
            if user_type == 'admin':
                return render_template('admin/login.html', error_message=ex, email=email, password=password)
            
            return render_template('auth/login.html', error_message=ex, email=email, password=password)
            

###################
# FORGOT PASSWORD
###################
@app.route('/auth/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'GET':
        return render_template('auth/forgot_password.html')
    elif request.method == 'POST':
        data = request.form if request.form else request.json

        if 'email' not in data:
            raise Exception('"email" field is required in post data.')

        # TODO: send link for user to change password to email
        user = User.query.filter_by(email=data['email']).first()
        if user:
            id = user.id
            route_link = f'/reset_password/{id}'
            response = send_reset_link_to_mail(
                receiver=user.email, target_route=route_link, type='html')
            
            return render_template('auth/forgot_password_mail_sent_confirm.html',
                                response=response)
        else:
            return render_template('auth/forgot_password.html', email=data['email'], 
                                   error_message='No such email existing in our records.')



@app.route('/update_user/<int:id>', methods=['GET', 'POST'])
def update_user(id):
    user = User.query.get_or_404(id, f'User with id {id}, not found.')

    if request.method == 'GET':
        return render_template('auth/update_user.html', user=user)
    elif request.method == 'POST':
        
        data = request.form if request.form else request.json
        user_type = request.args.get('user', '')

        try:
            user.email = data['email']
            user.fullname = data['fullname']

            # update user
            user.update()

            # Update the user in session
            if 'user' in session:
                session['user'] = user.to_json()

            if user_type == 'admin':
                return redirect(url_for('admin_index'))

            return redirect(url_for('index'))
        
        except Exception as ex:
            if user_type == 'admin':
                return render_template('admin/update_user.html', error_message=ex.__str__(), **data)
            else:
                return render_template('auth/update_user.html', error_message=ex.__str__(), **data)

    
@app.route('/user/<int:id>/delete', methods=['GET', 'DELETE'])
def delete_user(id):
    user_type = request.args.get('user', '')

    if request.method == 'GET':
        user = User.query.get_or_404(id, f'User with id {id}, not found.')
        user.delete()

        if user_type == 'admin':
            return redirect(url_for('show_users'))
        
        return redirect(url_for('index'))
    
    else:
        if user_type == 'admin':
            return render_template('admin/error_page.html', error_message="Invalid method call on delete user")
        return render_template('auth/error_page.html', error_message="Invalid method call on delete user")


@app.route('/auth/reset_password/<int:id>', methods=['GET', 'POST'])
def reset_password(id):
    if request.method == 'GET':
        user = User.query.get_or_404(id, 'User not found, Or link has been tampered with')       
        return render_template('auth/reset_password.html', username=user.fullname, user_id=user.id)
    elif request.method == 'POST':
        data = request.form if request.form else request.json
        if 'new_password' not in data:
            return render_template(
                'auth/reset_password.html', username=user.fullname, 
                user_id=id, error_message='The new-password field is required')
        
        new_password = data['new_password']
        
        user = User.query.get_or_404(id, 'User not found, Or link has been tampered with')
        user.password = new_password

        user.update()
        # db.session.commit()

        return render_template('auth/password_reset_success.html', username=user.fullname)



########################
    # LOGOUT
########################
@app.route('/auth/logout', methods=['GET'])
def logout():
    if 'user' in session:
        session.pop('user')
        return redirect(url_for('login'))
    else:
        return redirect(url_for('login'))
    

@app.route('/users', methods=['GET', 'POST'])
def show_users():
    users = User.query.all()
    users = [user.to_json() for user in users]
    return render_template('admin/list_users.html', users=users)


#############################################################################################
    # ADMIN ROUTES
#############################################################################################
@app.route('/admin', methods=['GET'])
def admin_index():
    if request.method == 'GET':
        if 'user' not in session:
            return render_template('admin/login.html')

        all_users = User.query.all()
        all_subjects = Subject.query.all()
        all_results = Result.query.all()
        all_questions = Question.query.all()

        items = [
            {'resource':'Total Users', 'value':len(all_users)},
            {'resource':'Total Subjects', 'value':len(all_subjects)},
            {'resource':'Total Results', 'value':len(all_results)},
            {'resource':'Total Questions', 'value':len(all_questions)},
        ]

        return render_template('admin/admin_dashboard.html', 
                               username='Super User', users=all_users, 
                               subjects=all_subjects, results=all_results,
                               items=items, user=session['user']
                               )



#######################
# ERROR HANDLERS
#######################
# @app.errorhandler(404)
# def error_404(error):
#     user_type = request.args.get('user', '')
#     if user_type == 'admin':
#         return render_template('admin/error_page.html', error_message=error)
#     return render_template('auth/error_page.html', error_message=error)

# @app.errorhandler(500)
# def error_500(error):
#     user_type = request.args.get('user', '')
#     if user_type == 'admin':
#         return render_template('admin/error_page.html', error_message=error)
#     return render_template('auth/error_page.html', error_message=error)

# # Default exceptions
# @app.errorhandler(Exception)
# def uncaught_exceptions(error):
#     user_type = request.args.get('user', '')
#     if user_type == 'admin':
#         return render_template('admin/error_page.html', error_message=error)
#     return render_template('auth/error_page.html', error_message=error)



#####################
# Start the server
#####################
if __name__ == '__main__':
    # Run the next line only once
    # create_db_tables(app)

    app.run(debug=True, port=8000)
