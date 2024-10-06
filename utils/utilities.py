from models import Question, User, Result, Subject
def ensure_post_fields(data:dict, resource:str='question'):
    if not data or not isinstance(data, dict):
        # return {
        #     'success': False,
        #     'message': f'Missing post data in request body.'
        # }

        return False

    if resource.lower() == 'question':
        if 'question' not in data or 'option1' not in data or \
                'option2' not in data or \
                'option3' not in data or 'answer' not in data:
            
            # return {
            #     'success': False,
            #     'message': f'"question", "option1", "option2", "option3", "answer" are required fields.'
            # }

            return False
        
        else:
            return True
        
    elif resource.lower() == 'user':
        if 'fullname' not in data or 'email' not in data or \
                'password' not in data:
            
            # return {
            #     'success': False,
            #     'message': f'"fullname", "email", "password" are required fields.' 
            # }

            return False
        
        else:
            return True
        
    elif resource.lower() == 'subject':
        if 'name' not in data:
            
            # return {
            #     'success': False,
            #     'message': f'"name" of the subject is a required field.' 
            # }

            return False
        
        else:
            return True
        
    elif resource.lower() == 'result':
        if 'subject_id' not in data or 'score' not in data or \
            'total_questions' not in data:
            
            # return {
            #     'success': False,
            #     'message': f'"user_id", "subject_id" and "score" are required fields.' 
            # }

            return False
        
        else:
            return True
    
    else:
        # return {
        #     'success': False,
        #     'message': f'Invalid resource name supplied' 
        # }

        return False


