from lettuce import step, world, before
from nose.tools import assert_equals
from webtest import *
from app import app
#from app import db
import base64
from app.views import *
import json



@before.all
def before_all():
	world.app = app.test_client()



############## SIGN UP #############################3
@step(u'Given I have the following user details:')
def user_details(step):
	world.user = step.hashes[0]


@step(u'When the user clicks the submit button')
def when_the_user_clicks_the_submit_button(step):
	world.browser = TestApp(app)
	world.response = world.app.post('/api/registeruser', data=json.dumps(world.user))


@step(u'Then it should have a \'([^\']*)\' response')
def then_it_should_get_a_group1_response(step, expected_status_code):
	assert_equals(world.response.status_code, int(expected_status_code))



@step(u'Given the user with an id \'([^\']*)\'')
def given_the_user_with_an_id_group1(step, user_id):
	world.user_id = user_id
	world.user = world.app.get
#########################################################