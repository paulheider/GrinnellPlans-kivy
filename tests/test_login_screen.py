import pytest

from main import LoginScreen

import mock

import requests

@mock.patch( 'requests.Session' )
def test_session_is_called( mock_requests_Session ):
    session = None
    login_screen = LoginScreen()
    login_url = \
        'https://www.grinnellplans.com/api/1/index.php?task=login'
    username = 'gspelvin'
    password = 'SuperSecure'
    data_packet = { 'username' : username ,
                    'password' : password }
    with mock.patch( 'requests.Session' ):
        login_screen.logInTask( 'gspelvin' , 'SuperSecure' )
        requests.Session.assert_called_once_with()


@mock.patch( 'requests.Session' )
def test_session_no_username( mock_requests_Session ):
    session = None
    login_screen = LoginScreen()
    login_url = \
        'https://www.grinnellplans.com/api/1/index.php?task=login'
    username = ''
    password = 'SuperSecure'
    with mock.patch( 'requests.Session' ):
        login_screen.logInTask( username , password )
        requests.Session.assert_not_called()


@mock.patch( 'requests.Session' )
def test_session_no_password( mock_requests_Session ):
    session = None
    login_screen = LoginScreen()
    login_url = \
        'https://www.grinnellplans.com/api/1/index.php?task=login'
    username = 'gspelvin'
    password = ''
    with mock.patch( 'requests.Session' ):
        login_screen.logInTask( username , password )
        requests.Session.assert_not_called()


@mock.patch( 'requests.Session' )
def test_session_connection( mock_requests_Session ):
    session = None
    login_screen = LoginScreen()
    login_url = \
        'https://www.grinnellplans.com/api/1/index.php?task=login'
    username = 'gspelvin'
    password = 'SuperSecure'
    with mock.patch( 'requests.Session' ):
        login_screen.logInTask( username , password )
        requests.Session.assert_called_once_with()


@mock.patch( 'requests.Session.post' )
@mock.patch( 'main.LLOOGG' )
def test_post_exception( mock_requests_Session_post ,
                         mock_main_LLOOGG ):
    session = None
    login_screen = LoginScreen()
    login_url = \
        'https://www.grinnellplans.com/api/1/index.php?task=login'
    username = 'gspelvin'
    password = 'SuperSecure'
    with mock.patch( 'requests.Session.post' ,
                     side_effect = Exception( 'Caught post() exception' ) ):
        with mock.patch( 'main.LLOOGG' ) as log_calls:
            login_screen.logInTask( username , password )
            log_calls.assert_called_with( 'Error:  Caught post() exception\n' )
            requests.Session.post.assert_called_once()


@mock.patch( 'requests.Session' )
@mock.patch( 'main.LLOOGG' )
def test_session_connection_exception( mock_requests_Session ,
                                      mock_main_LLOOGG ):
    session = None
    login_screen = LoginScreen()
    login_url = \
        'https://www.grinnellplans.com/api/1/index.php?task=login'
    username = 'gspelvin'
    password = 'SuperSecure'
    with mock.patch( 'requests.Session' ,
                     side_effect = Exception( 'Caught Session() instantiation exception' ) ):
        with mock.patch( 'main.LLOOGG' ) as log_calls:
            login_screen.logInTask( username , password )
            log_calls.assert_called_with( 'Error:  Caught Session() instantiation exception\n' )
            requests.Session.post.assert_not_called()


@mock.patch( 'requests.Session.post' )
def test_post_called( mock_requests_Session_post ):
    session = None
    login_screen = LoginScreen()
    login_url = \
        'https://www.grinnellplans.com/api/1/index.php?task=login'
    username = 'gspelvin'
    password = 'SuperSecure'
    packet = { 'username' : username ,
               'password' : password }
    with mock.patch( 'requests.Session.post' ):
        login_screen.logInTask( username , password )
        requests.Session.post.assert_called_once_with( login_url ,
                                                       data = packet )


@mock.patch( 'requests.Session.post' )
@mock.patch( 'main.LLOOGG' )
def test_bad_status_code( mock_requests_Session_post ,
                          mock_main_LLOOGG ):
    session = None
    login_screen = LoginScreen()
    login_url = \
        'https://www.grinnellplans.com/api/1/index.php?task=login'
    username = 'gspelvin'
    password = 'SuperSecure'
    packet = { 'username' : username ,
               'password' : password }
    with mock.patch( 'requests.Session.post' ,
                     return_value = mock.Mock( status_code = 500 ) ):
        with mock.patch( 'main.LLOOGG' ) as log_calls:
            login_screen.logInTask( username , password )
            log_calls.assert_called_with( 'Failed to log in:  500' )


## TODO - make response.json() callable
## 249 - <Mock name='mock.json()' id='140198941780112'>
## Error:  'Mock' object has no attribute '__getitem__'
@mock.patch( 'requests.Session.post' )
def TODO_good_status_code( mock_requests_Session_post , capsys ):
    session = None
    login_screen = LoginScreen()
    login_url = \
        'https://www.grinnellplans.com/api/1/index.php?task=login'
    username = 'gspelvin'
    password = 'SuperSecure'
    packet = { 'username' : username ,
               'password' : password }
    mock_response = mock.Mock( status_code = 200 )
    with mock.patch( 'requests.Session.post' ,
                     return_value = mock_response ):
        login_screen.logInTask( username , password )
        out , err = capsys.readouterr()
        with open( '/tmp/stdout.log' , 'w' ) as fp:
            fp.write( '{}\n'.format( out ) )
