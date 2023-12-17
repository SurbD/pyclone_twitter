from flask import Blueprint, request, session

from app.models import User
from app.auth.forms import RegistrationForm
from app.utils import send_email, confirm_vcode, get_vcode

api = Blueprint('api', __name__)


# Routes API call from Axios

@api.route("/validate-email", methods=['POST'])
def validate_email():
    # For Javascript email validation, 
    # this will later become on with the validate inputs 
    # when it starts returning a message there will be no need for this

    if request.method == 'POST':
        email = request.get_json()['email'].lower()
        user = User.query.filter_by(email=email).first() # SetUp DB
        if user:
            return {'user_exists': True}
        else:
            return {'user_exists': False}
    return

@api.route("/validate-username", methods=["POST"])
def validate_username():

    # Just for testing think of ways to make this part of the overall 
    # validate function thats the validate-inputs   endpoint

    if request.method == 'POST':
        username = request.get_json()['username'].lower()
        user = User.query.filter_by(username=username).first()

        if user:
            message = "This username is taken. Please choose a different one."
            taken = True
        else:
            message = ""
            taken = False
        return {'taken': taken, 'message': message}
        
            

@api.route("/validate-inputs", methods=["POST"])
def validate_inputs():
    form = RegistrationForm()

    if request.method == "POST":
        form_data = request.get_json()
        # print(form_data)
        form.username.data = form_data['username'].lower()
        form.email.data = form_data['email'].lower()
        form.date_of_birth.data = form_data['date_of_birth']

        email_validate = form.email.validate(form) and form.validate_email(form.email)
        username_validate = form.username.validate(form) and form.validate_username(form.username)
        dob_validate = form.date_of_birth.validate(form)
        isAllValid = email_validate and username_validate and dob_validate

        return {
            'isValid': isAllValid,
            'data': {
                'email': {
                    'isvalid': email_validate,
                    'message': None
                },
                'username': {
                    'isValid': username_validate,
                    'message': None
                },
                'date_of_birth': {
                    'isValid': dob_validate,
                    'message': None
                }
            }
        }

    return


@api.route('/get-verification-code', methods=['POST'])
def get_verification_code():
    
    if request.method == 'POST':
        user_data = request.get_json()
        email = user_data['email'].lower()
        username = user_data['username'].lower()

        token, code = get_vcode().values()
        session['verification_token'] = token

        try:
            send_email(email, 'Confirm Email Address',
                        'email/confirm_new_user', code=code, username=username)
        except Exception as e:
            print(e)
            success = False
        else:
            success = True
        return {
            'success': success,
            'token': token
        }

@api.route('/confirm-verification-code', methods=['POST'])
def confirm_verification_code():
    # I don't know if i should pass token as a parameter from the request 
    # or send as json or to even just store the token in session and 
    # retrive and clear it once it has been confirmed
    
    token = session['verification_token']

    if request.method == 'POST':
        code = request.get_json()['code']

        if confirm_vcode(token, code):
            session.pop('verification_token')
            message = ''
            verified = True
        else: 
            message = 'Check email for the verification code or try requesting a new code'
            verified = False

        return {'verified': verified, 'message': message} 
