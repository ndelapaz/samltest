from flask import Flask, url_for
from flask_saml2.sp import ServiceProvider
from flask_saml2.utils import certificate_from_file, private_key_from_file

class ExampleServiceProvider(ServiceProvider):
    def get_logout_return_url(self):
        return url_for('index', _external=True)

    def get_default_login_return_url(self):
        return url_for('index', _external=True)

sp = ExampleServiceProvider()
app = Flask(__name__)
app.debug = True
app.secret_key = 'not a secret'
app.config['SERVER_NAME'] = 'localhost:8082'
app.config['SAML2_SP'] = {
    'certificate': certificate_from_file('cert1.pem'),
    'private_key': private_key_from_file('key1.pem'),
}

app.config['SAML2_IDENTITY_PROVIDERS'] = [
    {
        'CLASS': 'flask_saml2.sp.idphandler.IdPHandler',
        'OPTIONS': {
            'display_name': 'KeyCloak',
            'entity_id': 'http://sso1test.gnc.mx:81/auth/realms/Axera-Internal',
            'sso_url': 'http://sso1test.gnc.mx:81/auth/realms/Axera-Internal/protocol/saml',
            'slo_url': 'http://sso1test.gnc.mx:81/auth/realms/Axera-Internal/protocol/saml',
            'certificate': certificate_from_file('cert2.pem')
        },
    },
]

# index
@app.route('/')
def index():
    if sp.is_user_logged_in():
        auth_data = sp.get_auth_data_in_session()

        message = f'''
        <p>You are logged in as <strong>{auth_data.nameid}</strong>.
        The IdP sent back the following attributes:<p>
        '''

        attrs = '<dl>{}</dl>'.format(''.join(
            f'<dt>{attr}</dt><dd>{value}</dd>'
            for attr, value in auth_data.attributes.items()))

        logout_url = url_for('flask_saml2_sp.logout')
        logout = f'<form action="{logout_url}" method="POST"><input type="submit" value="Log out"></form>'

        return message + attrs + logout
    else:
        message = '<p>You are logged out.</p>'

        login_url = url_for('flask_saml2_sp.login')
        link = f'<p><a href="{login_url}">Log in to continue</a></p>'

        return message + link

# Blueprint
app.register_blueprint(sp.create_blueprint(), url_prefix='/saml/')

# Setup
if __name__ == '__main__':
    app.run(port=8082)
