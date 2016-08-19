import webapp2
import re

USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
def valid_username(username):
    return USER_RE.match(username)

def valid_password(password):
    PASS_RE = re.compile("^.{3,20}$")
    return password and PASS_RE.match(password)


def valid_email(email):
    EMAIL_RE = re.compile("^[\S]+@[\S]+.[\S]+$")
    return email and EMAIL_RE.match(email)

# Sign up page form
user_form = """
<!DOCTYPE html>
<html>
    <head>
        <title>Sign Up Page</title>
    </head>
    <body>
        <h1>Sign Up</h1>
        <form method="post">
        <table>
            <tr>
                <td> Username   </td>
                <td> <input type="text" name="username" value="%(username)s" /> </td>
                <td> %(usr_err)s</td>
                </tr>
                <tr>
                <td> Password </td>
                <td> <input type="password" name="password" /> </td>
                <td> %(pass_err)s</td>
            </tr>
            <tr>
                <td> Verify Password </td>
                <td> <input type="password" name="verify" /> </td>
                <td> %(ver_err)s </td>
            </tr>
            <tr>
                <td> Email (optional) </td>
                <td> <input type="text" name="email" value="%(email)s" /> </td>
                <td> %(email_err)s</td>
            </tr>
            <tr>
                <td> <input type ="submit" value="Submit" /> </td>
            </tr>
        </table>
        </form>
    </body>
</html>
"""

welcome_form = """
    <!DOCTYPE html>
    <html>
        <head>
            <title>Sign in Page</title>
        </head>

        <body>
            <h1>Welcome, %s!</h1>
        </body>
    </html>
"""

class SignUpForm(webapp2.RequestHandler):
    def write_form(self, username="", password="", verify="", email="",
                   usr_err="", pass_err="", ver_err="", email_err=""):
                   self.response.out.write(user_form % {'username': username,
                                               'password': password,
                                               'verify': verify,
                                               'email': email,
                                               'usr_err': usr_err,
                                               'pass_err': pass_err,
                                               'ver_err': ver_err,
                                               'email_err': email_err})

    def get(self):
        self.write_form()

    def post(self):
        username = self.request.get('username')
        password = self.request.get('password')
        verify = self.request.get('verify')
        email = self.request.get('email')
        usr_err = ""
        pass_err = ""
        ver_err = ""
        email_err = ""
        usr_bool = True
        pass_bool = True
        email_bool = True

        if not valid_username(username):
            usr_err = "That's not a valid username."
            usr_bool = False
        if not valid_password(password):
            pass_err = "That's not a valid password."
            pass_bool = False
        elif password != verify:
            ver_err = "Your passwords didn't match."
        if not valid_email(email):
            email_err = "That's not a valid email."
            email_bool = False

        if email == "":
            email_err = ""
            email_bool = True

        if usr_bool and pass_bool and email_bool and (password == verify):
            self.redirect('/welcome?username=%s' % username)
        else:
            self.write_form(username, password, verify, email,
                            usr_err, pass_err, ver_err, email_err)

class WelcomePage(webapp2.RequestHandler):
    def get(self):
        username = self.request.get('username')
        self.response.out.write(welcome_form % username)

app = webapp2.WSGIApplication([
    ('/', SignUpForm),
    ('/welcome', WelcomePage),
], debug=True)
