
from lettuce import step, world, before
from nose.tools import assert_equals
from passlib.hash import sha256_crypt
import hashlib
import json
import random
from app import app



# =======================================================
@before.all
def before_all():
    world.app = app.test_client()
# =======================================================


# User Registration Sunny Case
@step(u'Given the user fills the form with these details:')
def Given_the_user_fills_the_form_with_these_details(step):
    for item in step.hashes:
        world.name = item["name"] + str(random.randrange(0, 10000))
        world.is_translator = item["is_translator"]
        world.email = str(random.randrange(0, 10000)) + item["email"]
        world.password = item["password"]
@step(u'When I submit the registration form')
def When_I_submit_the_registration_form(step):
    name = world.name
    email = world.email
    password = world.password
    is_translator = world.is_translator
    world.response = world.app.post("/api/register", data = dict(name = name, email = email, password = password, is_translator = is_translator ))
    
@step(u'Then I should get a \'(.*)\' response')
def Then_I_should_get_a_group1_response_group2(step, expected_status_code):
    assert_equals(world.response.status_code, int(expected_status_code))
    
@step(u'And it will return these details:')
def And_it_will_return_these_details(step):
    assert_equals(step.hashes[0]["message"], json.loads(world.response.data)["message"])

# User Registration rainy Case email already exists
@step(u'Given the user fills the registration form with these details:')
def Given_the_user_fills_the_registration_form_with_these_details(step):
    for item in step.hashes:
        world.name = item["name"] + str(random.randrange(0, 10000))
        world.is_translator = item["is_translator"]
        world.email = item["email"]
        world.password = item["password"]
 
# User Registration rainy no email 
@step(u'When I submit the signup form')
def When_I_submit_the_signup_form(step):
    name = world.name
    email = ""
    password = world.password
    is_translator = world.is_translator
    world.response = world.app.post("/api/register", data = dict(name = name, email = email, password = password, is_translator = is_translator ))

# User Registration rainy invalid email    

# =======================================================
# =======================================================

# User sign in sunny
@step(u'Given signs in as:')
def given_the_user_signs_in_as(step):
     for item in step.hashes:
        world.email = item["email"]
        world.password = item["password"]
@step(u'When User signs in')
def When_user_signs_in(step):
    world.response = world.app.post('/api/signin', data = dict(email = world.email, password = world.password))
  

# =======================================================
# =======================================================
  
#log out sunny
@step(u'Given User is logged in as')
def Given_user_is_logged_in_as_group1(step):
    for item in step.hashes:
        world.email = item["email"]
        world.password = item["password"]
    world.response = world.app.post('/api/signin', data = dict(email = world.email, password = world.password))
@step(u'When User logs out')
def user_logs_out(step):
    world.response = world.app.get('/api/signout')
    
#log out rainy (logging out without login)
@step(u'Given User is not logged in as')
def Given_user_is_not_logged_in_as_group1(step):
    for item in step.hashes:
        world.email = item["email"]
        world.password = item["password"]


