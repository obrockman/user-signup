#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import webapp2
import re 

content = """
<head>
<h1>Signup</h1>
<style type= "text/css">
    .error {
        color:red;
    }
</style>
</head>
    <form method='post'> 
        <table>
            <tbody>
                <tr>
                    <td>
                        <label for="username">Username</label>
                    </td>
                    <td>
                        <input name="username" type="text" value="%(username)s" required>
                        <span class="error">%(error_username)s</span>
                    </td>
                </tr>
                <tr>
                    <td> 
                        <label for="password">Password</label>
                    </td>
                    <td>
                        <input name="password" type="password" required>
                        <span class="error">%(error_password)s</span>
                    </td>
                </tr>
                <tr> 
                    <td>
                        <label for="verify">Verify Password</label>
                    </td>
                    <td>
                        <input name="verify" type="password" required>
                        <span class="error">%(error_verify)s</span>
                    </td>
                </tr>
                <tr>
                    <td>
                        <label for="email">Email(optional)</label>
                    </td>
                    <td>
                        <input name="email" type="email" value="%(email)s">
                        <span class="error">%(error_email)s</span>
                    </td>
                </tr>
            </tbody>
        </table>
        <br>
        <br>
        <input type="submit">
         
    </form>"""  

USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
def valid_username(username):
    return username and USER_RE.match(username) 

PASS_RE = re.compile(r"^.{3,20}$")
def valid_password(password):
    return password and PASS_RE.match(password)

EMAIL_RE = re.compile(r"^[\S]+@[\5]+\.[\S]+$")
def valid_email(email):
    return EMAIL_RE.match(email)


class MainHandler(webapp2.RequestHandler):
    def writePage(self, username="", email="", error_username="", error_password="", error_verify="", error_email=""):
        self.response.write(content % {"username":username, "email":email, "error_username":error_username, "error_password":error_password,
                                "error_verify":error_verify, "error_email":error_email})


    def get(self):
        self.writePage()

    def post(self):
        have_error = False 
        username = self.request.get('username')
        password = self.request.get('password')
        verify = self.request.get('verify')
        email = self.request.get('email')

        params = {"username": username,
                    "email": email}

        if not valid_username(username):
            params['error_username'] = "That's not a valid username."
            have_error = True 

        if not valid_password(password):
            params['error_password'] = "That wasn't a valid password."
            have_error = True 
        elif password != verify: 
            params['error_verify'] = "Your passwords didn't match."
            have_error = True 

        if valid_email(email):
            params['error_email'] = "That's not a valid email."
            have_error = True 

        if not have_error:
            self.redirect('/welcome?username='+ username)
        else:
            self.writePage(**params)
            

class WelcomeHandler(webapp2.RequestHandler):
    def get(self):
        username = self.request.get('username')
        self.response.write("<h2>Welcome, " + username + "</h2>")



app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/welcome', WelcomeHandler)
], debug=True)
