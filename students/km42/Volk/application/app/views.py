from django.shortcuts import render, redirect, render_to_response
from app.db.model import Meeting, User, Invitation
from app.db.meeting_dao import MeetingDao
from app.db.invitation_dao import InvitationDao
from app.db.user_dao import UserDao
import google_auth_oauthlib.flow
import os
import hashlib


os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
dir_path = os.path.dirname(os.path.realpath(__file__))
client_json_path = os.path.join(dir_path, 'client_secret.json')


def index(request):
    return render(request, 'index.html')


def auth(request):
    return render(request, 'login.html')


def auth_begin(request):
    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
        client_json_path,
        scopes=['email']
    )
    flow.redirect_uri = 'http://cursdb.com:8000/redirect'
    authorization_url, state = flow.authorization_url(
        access_type='offline',
    )
    return redirect(authorization_url)


def auth_redirect(request):
    state = request.GET['state']
    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
        client_json_path,
        scopes=['profile'],
        state=state,
    )
    flow.redirect_uri = 'http://cursdb.com:8000/redirect'
    authorization_response = request.build_absolute_uri()
    flow.fetch_token(authorization_response=authorization_response)
    session = flow.authorized_session()
    data = session.get('https://www.googleapis.com/userinfo/v2/me').json()
    with UserDao() as dao:
        user = User(data['name'], data['email'])
        dao.create(user)
    response = redirect('/')
    response.set_cookie('useremail', user.email)
    response.set_cookie('username', user.name)
    response.set_cookie('token', hashlib.md5((user.name + user.email).encode()).hexdigest())
    return response


def create_meeting(request):
    if request.method == 'GET':
        with UserDao() as dao:
            autocomplete = dao.get_autocomplete(User(email=request.COOKIES.get('useremail')))
        return render(request, 'create.html', {
            'meeting': Meeting(
                '', '', '', '', [], '', '',
            ),
            'action': 'create',
            'autocomplete': autocomplete
        })
    elif request.method == 'POST':
        emails = {x for x in request.POST['invited'].split(',') if x}
        meeting = Meeting(
            User(email=request.COOKIES.get('useremail')),
            request.POST['title'],
            request.POST['address'],
            request.POST['date'],
            [Invitation(user=User(email=email)) for email in emails],
            request.POST['description'],
        )
        with MeetingDao() as dao:
            dao.create(meeting)

        return render(request, 'created.html', {
            'meeting': meeting,
        })


def view_invitations(request):
    with InvitationDao() as dao:
        meetings = dao.get(User(email=request.COOKIES.get('useremail')))
    return render(request, 'invitations.html', {
        'meetings': meetings,
    })


def view_meetings(request):
    with MeetingDao() as dao:
        meetings = dao.get(User(email=request.COOKIES.get('useremail')))
    return render(request, 'meetings.html', {
        'meetings': meetings,
    })


def edit(request, id):
    if request.method == 'GET':
        with MeetingDao() as dao:
            meeting = dao.get_single(id)
            if meeting is None or meeting.user.email != request.COOKIES.get('useremail'):
                return redirect('/access_denied')
            meeting.date = meeting.date.strftime('%m/%d/%Y')
        with UserDao() as dao:
            autocomplete = dao.get_autocomplete(User(email=request.COOKIES.get('useremail')))

        return render(request, 'create.html', {
            'meeting': meeting,
            'action': 'update/{}/'.format(id),
            'autocomplete': autocomplete,
        })


def update(request, id):
    if request.method == 'POST':
        emails = {x for x in request.POST['invited'].split(',') if x}
        meeting = Meeting(
            User(email=request.COOKIES.get('useremail')),
            request.POST['title'],
            request.POST['address'],
            request.POST['date'],
            [Invitation(user=User(email=email)) for email in emails],
            request.POST['description'],
            id,
        )
        if meeting.user.email != request.COOKIES.get('useremail'):
            return redirect('/access_denied')
        with MeetingDao() as dao:
            dao.update(meeting)

        return redirect('/meetings')


def logout(request):
    response = render_to_response('login.html')
    response.delete_cookie('username')
    response.delete_cookie('useremail')
    return response


def accept(request, id):
    with InvitationDao() as dao:
        dao.accept(id, User(email=request.COOKIES.get('useremail')))
    return redirect('/invitations')


def discard(request, id):
    with InvitationDao() as dao:
        dao.discard(id, User(email=request.COOKIES.get('useremail')))
    return redirect('/invitations')


def access_denied(request):
    return render(request, 'access_denied.html')

