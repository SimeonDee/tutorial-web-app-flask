from flask import ( Blueprint,
    request, render_template, 
    jsonify, url_for, make_response,
    redirect, session
    )
from utils.mail_utils.sendmail import (send_otp_to_mail, 
                            send_reset_link_to_mail)
from models import User #, create_db_tables

auth_bp = Blueprint('auth_bp', __name__)

@auth_bp.route('/', methods=['GET'])
def index():
    if request.method == 'GET':
        if 'user' in session:
            user = session['user']
            username = user['fullname']

            # all_users = User.query.all()
            return render_template('quiz/index.html', username=username, user=user)
        else:
            return redirect(url_for('login'))

    else:
        err_msg = 'Invalid Method Call'
        return render_template('auth/error_page.html', error_message=err_msg)


############
# REGISTER
############
@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('auth/register.html')
    elif request.method == 'POST':
        # collect user data
        data = request.form if request.form else request.json 

        try:
            if ('email' not in data or 'password' not in data or 
                'fullname' not in data):
                
                raise Exception('"email", "password" and "fullname" fields are required fields.')
           
            # create new user from collected data
            new_user = User(**data) 

            # Add the new user to db
            new_user.insert()


            # return jsonify({
            #     "success": True,
            #     'user': new_user.to_json()
            # })

            return render_template('auth/register_success.html', username=new_user.fullname)
        
        except Exception as ex:
            return render_template('auth/register.html', error_message=ex.__str__(), form_data=data)


##########
# LOGIN
##########
@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        if 'user' in session:
            return render_template('quiz/index.html', user=session['user'])
        
        return render_template('auth/login.html')
    
    elif request.method == 'POST':
        # collect user data
        data = request.form if request.form else request.json 

        try:
            if 'email' not in data or 'password' not in data:
                raise Exception('"email" and "password" fields are required in post data.')

            email = data['email']
            password = data['password']

            # Authenticate user from collected data
            user = User.query.filter_by(email=email, password=password).first()

            if user:
                user.password = ''
                session['user'] = user.to_json()
                return redirect(url_for('index'))
            else:
                return render_template('auth/login.html', error_message="Invalid login credentials", email=email, password=password)
        
        except Exception as ex:
            return render_template('auth/login.html', error_message=ex, email=email, password=password)
            

###################
# FORGOT PASSWORD
###################
@auth_bp.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'GET':
        return render_template('auth/forgot_password.html')
    elif request.method == 'POST':
        data = request.form if request.form else request.json

        if 'email' not in data:
            raise Exception('"email" field is required in post data.')

        # TODO: send link for user to change password to email
        user = User.query.filter_by(email=data['email']).first_or_404()
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



@auth_bp.route('/update_user/<int:id>', methods=['GET', 'POST'])
def update_user(id):
    user = User.query.get_or_404(id, f'User with id {id}, not found.')

    if request.method == 'GET':
        return render_template('auth/update_user.html', user=user)
    elif request.method == 'POST':
        data = request.form if request.form else request.json

        user.matric = data['matric']
        user.email = data['email']
        user.fullname = data['fullname']

        # update user
        user.update()

        return redirect(url_for('index'))
    
@auth_bp.route('/delete_user/<int:id>', methods=['GET'])
def delete_user(id):
    
    if request.method == 'GET':
        user = User.query.get_or_404(id, f'User with id {id}, not found.')
        user.delete()
        # db.session.delete(user)
        # db.session.commit()

        return redirect(url_for('index'))
    else:
        return render_template('auth/error_page.html', error_message="Invalid method call on delete user")


@auth_bp.route('/reset_password/<int:id>', methods=['GET', 'POST'])
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
    # ADMIN
########################
@auth_bp.route('/admin', methods=['GET'])
def admin_index():
    if request.method == 'GET':
        all_users = User.query.all()
        return render_template('admin/admin_dashboard.html', username='Super User', users=all_users)
    else:
        err_msg = 'Invalid Method Call'
        return render_template('auth/error_page.html', error_message=err_msg)


########################
    # LOGOUT
########################
@auth_bp.route('/logout', methods=['GET'])
def logout():
    if 'user' in session:
        session.pop('user')
        return redirect(url_for('login'))
    else:
        return redirect(url_for('login'))


#######################
# ERROR HANDLERS
#######################
@auth_bp.errorhandler(404)
def error_404(error):
    return render_template('error_page.html', error_message=error)

@auth_bp.errorhandler(500)
def error_500(error):
    return render_template('error_page.html', error_message=error)

# Default exceptions
@auth_bp.errorhandler(Exception)
def uncaught_exceptions(error):
    return render_template('error_page.html', error_message=error)


def get_auth_blueprint_instance():
    return auth_bp