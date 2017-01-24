"""
In this file we specify default event handlers which are then populated into the handler map using metaprogramming
Copyright Anjishnu Kumar 2015
Happy Hacking!
"""

from ask import alexa

def lambda_handler(request_obj, context=None):
    '''
    This is the main function to enter to enter into this code.
    If you are hosting this code on AWS Lambda, this should be the entry point.
    Otherwise your server can hit this code as long as you remember that the
    input 'request_obj' is JSON request converted into a nested python object.
    '''

    metadata = {'user_name' : 'SomeRandomDude'} # add your own metadata to the request using key value pairs
    
    ''' inject user relevant metadata into the request if you want to, here.    
    e.g. Something like : 
    ... metadata = {'user_name' : some_database.query_user_name(request.get_user_id())}

    Then in the handler function you can do something like -
    ... return alexa.create_response('Hello there {}!'.format(request.metadata['user_name']))
    '''
    return alexa.route_request(request_obj, metadata)


@alexa.default
def default_handler(request):
    """ The default handler gets invoked if no handler is set for a request type """
    return alexa.respond('Just ask').with_card('Hello World')

@alexa.request("LaunchRequest")
def launch_request_handler(request):
    ''' Handler for LaunchRequest '''
    return alexa.create_response(message="Hello Welcome to My Recipes!")


@alexa.request("SessionEndedRequest")
def session_ended_request_handler(request):
    return alexa.create_response(message="Goodbye!")

@alexa.intent('HiIntent')
def get_hi_intent_handler(request):
    """
    You can insert arbitrary business logic code here    
    """
    return alexa.create_response("Hello. What is your name")

@alexa.intent('NameIntent')
def get_name_intent_handler(request):
    """
    You can insert arbitrary business logic code here    
    """
    name = request.slots["name"]  # Gets an Ingredient Slot from the Request object.
    
    if name== None:
        return alexa.create_response("Sorry I did not catch your name!")

    message = "Hello " + name + " nice to meet you."
    return alexa.create_response(message)

@alexa.intent('ProfessorIntent')
def get_prof_intent_handler(request):
	return alexa.create_response("Your professors are Joao Sedoc, Chris Callison Burch, Lyle Ungar")

if __name__ == "__main__":    
    
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--serve','-s', action='store_true', default=False)
    args = parser.parse_args()
    
    if args.serve:        
        ###
        # This will only be run if you try to run the server in local mode 
        ##
        print('Serving ASK functionality locally.')
        import flask
        server = flask.Flask(__name__)
        @server.route('/')
        def alexa_skills_kit_requests():
            request_obj = flask.request.get_json()
            return lambda_handler(request_obj)
        server.run()
    
