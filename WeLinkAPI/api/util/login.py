import requests
import datetime
import json
from datetime import timedelta
import secrets

from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.urls import reverse
from django.utils import timezone
# from django.db import models
from django.shortcuts import redirect

from WeLinkAPI.settings import CLIENT_ID, REDIRECT_URI, CLIENT_SECRET,\
     GOOGLE_ENDPOINT, DEFAULT_INIT_URI, AUTHORIZE_URL, ACCESS_TOKEN_URL, SCOPES

from ..models import User
from django.contrib.auth.models import User as AuthUser
from django.contrib.auth import authenticate, login, logout

'''
Step 1:
After user clicks login, front end call $request_auth api, and redirect to the back result;

Step 2:
After user successfully login via google, the website redirect back to our a backend page(api page, and store token),
then back end page ===> front end page
'''

def strToDatatime(date_time_str):
    return datetime.datetime.strptime(date_time_str, '%Y-%m-%d %H:%M:%S.%f')

def request_auth(request):
    '''
    use this method to get google auth link, i.e. request authorization code;

    '''
    request.session['init_uri'] = request.GET.get("init_uri", '')
    while request.user.is_authenticated:
        try:
            userLogin = User.objects.filter(user = request.user)[0]
        except:
            break;
        if userLogin.expires_within(datetime.timedelta()):
            # refresh token
            userLogin.access_token, userLogin.expires = refresh_oauth_token(request, userLogin.refresh_token)
        userLogin.save()
        login(request, request.user)
        return HttpResponse('OK')
    return HttpResponse(get_oauth_login_url(client_id=CLIENT_ID,
                        redirect_uri=REDIRECT_URI,
                        state=''))


def redirect_back(request):
    '''
    users automatically redirected to this uri;
    the returned uri carries the authorization code
    '''
    error = request.GET.get('error')
    if error:
        return HttpResponse(status=404)
    code = request.GET.get('code')
    state = request.GET.get('state')
    # if state != request.session['stt']:
    #     return HttpResponse(status=400)

    access_token, expires, refresh_token = get_access_token(
        grant_type='authorization_code',
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        redirect_uri=REDIRECT_URI,
        code=code)

    # get info from google
    profile = requests.get(GOOGLE_ENDPOINT+'/oauth2/v1/userinfo?alt=json&access_token='+access_token).json()
    print('profile:', profile)
    print('request.user:', request.user)
    try:
        user = AuthUser.objects.get(username=profile['email'])
    except AuthUser.DoesNotExist:
        user = AuthUser.objects.create_user(profile['email'])
    login(request, user)
    # create or update user using profile
    try:
        u = User.objects.get(user = request.user)
        u.access_token = access_token
        u.refresh_token = refresh_token
        u.expires = expires
        u.created_on = str(timezone.now())
        u.updated_on = str(timezone.now())
        u.save()
    except User.DoesNotExist:
        User.objects.update_or_create(user = request.user,
            access_token = access_token,
            refresh_token = refresh_token,
            expires = expires,
            created_on = str(timezone.now()),
            updated_on = str(timezone.now()))
    
    # TODO: avatar? self intro and other info?

    # set redirect uri after authorization
    init_uri = DEFAULT_INIT_URI
    print("init_uri in call back:", init_uri)
    if 'init_uri' in request.session:
        init_uri = request.session['init_uri']
    
    return redirect(init_uri)

def request_token(request):
    '''
    users get token from with the auth code
    '''
    pass

def refresh_oauth_token(request, refresh_token):

    '''
    Get the new access token and expiration date via
    a refresh token grant
    '''
    try:
        user = AuthUser.objects.get(request.user)
    except AuthUser.DoesNotExist:
        pass
    acs_tk, exp, _ = get_access_token(
        grant_type='refresh_token',
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        redirect_uri=REDIRECT_URI,
        refresh_token=oauth_struct.d['refresh_token'])
    # Update the model with new token and expiration
    request.session['oauth_struct'] = str(oauth_struct)
    return acs_tk, exp

def get_random_string(length=None, allowed_chars=(
    'abcdefghijklmnopqrstuvwxyz'
    'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
)):
    if length is None:
        length = 24
    return ''.join(secrets.choice(allowed_chars) for i in range(length))

def get_oauth_login_url(client_id, redirect_uri, response_type='code',
                        state=None, scopes=SCOPES, purpose=None,
                        force_login=None):
    """Builds an OAuth request url for google.
    """
    authorize_url = AUTHORIZE_URL
    scopes = " ".join(scopes) if scopes else None  

    auth_request_params = {
        'client_id': client_id,
        'redirect_uri': redirect_uri,
        'response_type': response_type,
        'state': state,
        'scope': scopes,
        'purpose': purpose,
        'force_login': force_login,
    }
    auth_request_params = sorted(auth_request_params.items(), key=lambda val: val[0])

    # Use requests library to help build our url
    auth_request = requests.Request('GET', authorize_url,
                                    params=auth_request_params)
    # Prepared request url uses urlencode for encoding and scrubs any None
    # key-value pairs
    print(auth_request.prepare().url)
    return auth_request.prepare().url

def get_access_token(grant_type, client_id, client_secret, redirect_uri, code=None, refresh_token=None):
    """Performs one of the two grant types supported by OAuth endpoint to
    to retrieve an access token.  Expect a `code` kwarg when performing an
    `authorization_code` grant; otherwise, assume we're doing a `refresh_token`
    grant.
    Return a tuple of the access token, expiration date as a timezone aware DateTime,
    and refresh token (returned by `authorization_code` requests only).
    """
    oauth_token_url = ACCESS_TOKEN_URL
    post_params = {
        'grant_type': grant_type,  # Use 'authorization_code' for new tokens
        'client_id': client_id,
        'client_secret': client_secret,
        'redirect_uri': redirect_uri,
    }

    # Need to add in code or refresh_token, depending on the grant_type
    if grant_type == 'authorization_code':
        post_params['code'] = code
    else:
        post_params['refresh_token'] = refresh_token

    r = requests.post(oauth_token_url, post_params)
    if r.status_code != 200:
        return HttpResponse(status=401)

    # Parse the response for the access_token, expiration time, and (possibly)
    # the refresh token
    response_data = r.json()
    access_token = response_data['access_token']
    seconds_to_expire = response_data['expires_in']
    # Convert the expiration time in seconds to a DateTime
    expires = timezone.now() + timedelta(seconds=seconds_to_expire)
    # Whether a refresh token is included in the response depends on the
    # grant_type - it only appears to be returned for 'authorization_code',
    # but to be safe check the response_data for it
    refresh_token = None
    if 'refresh_token' in response_data:
        refresh_token = response_data['refresh_token']

    return (access_token, str(expires), refresh_token)