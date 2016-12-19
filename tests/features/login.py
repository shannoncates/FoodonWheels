from lettuce import step, world, before
from nose.tools import assert_equals
from webtest import *
from app import app
from app.views import *
import json
import base64

@before.all
def before_all():
    world.app = app.test_client()


""" Common steps for jsonify response """


@step(u'Then  it should have a \'([^\']*)\' response')
def then_it_should_get_a_group1_response(step, expected_status_code):
    assert_equals(world.response.status_code, int(expected_status_code))


@step(u'And   it should have a field \'([^\']*)\' containing \'([^\']*)\'')
def and_it_should_get_a_field_group1_containing_group2(step, field, expected_value):
    world.response_json = json.loads(world.response.data)
    assert_equals(str(world.response_json[field]), expected_value)


@step(u'And   the following details will be returned')
def and_the_following_details_will_be_returned(step):
    response_json = json.loads(world.response.data)
assert_equals(world.response_json['entries'], response_json['entries'])

"""Log In"""

@step(u'Given I have the following login details:')
def given_login_details(step):
    world.login = step.hashes[0]


@step(u'When I click login button')
def when_i_click_login_button(step):
    world.browser = TestApp(app)
    world.response = world.app.post('/api/login', data = json.dumps(world.login))

@step(u'Then I get a \'(.*)\' response')
def then_i_should_get_a_200_response(step, expected_status_code):
    assert_equals(world.response.status_code, int(expected_status_code))


@step(u'And a message "Successfully Logged In" is returned')
def message_res(step):
    world.respn = json.loads(world.response.data)
    assert_equals(world.respn['message'], "Successfully Logged In")


@step(u'And a message "Invalid email or password" is returned')
def message_res(step):
    world.respn = json.loads(world.response.data)
assert_equals(world.respn['message'], "Invalid email or password")