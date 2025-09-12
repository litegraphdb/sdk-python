import litegraph

sdk = litegraph.configure(
    endpoint="http://YOUR_SERVER_URL_HERE:PORT",
    tenant_guid="00000000-0000-0000-0000-000000000000",
    access_key="litegraphadmin",
)


def retrieve_tenants_for_email():
    tenants = litegraph.Authentication.retrieve_tenants_for_email(
        email="default@user.com"
    )
    print(tenants)


retrieve_tenants_for_email()


def generate_authentication_token():
    token = litegraph.Authentication.generate_authentication_token(
        email="default@user.com",
        password="password",
        tenant_guid="00000000-0000-0000-0000-000000000000",
    )
    print(token)


generate_authentication_token()


def retrieve_token_details():
    token_details = litegraph.Authentication.retrieve_token_details(
        token="mXCNtMWDsW0/pr+IwRFUjZYDoWLdu5ikKlbZr907gYrfE1YYCDFfFTleuYAW0mY1rkrhpPOgDf3Fbtk0iiy8JBF2WlWMw0MttbH0mDgNf1ZSJHGR5nQDG9oRHFe0q9SaIMCVyRGIdsgewLr7YPM46nsrHcLTA7RPKKOPA/mYZG6/kOGQV3FnT7F3u293+NBgWMXRYzNhmTwqEA021/gc9r1rVXjZcWXgv1apW/xyqCkF4aOriuyThcV55zibCugyDuj7MTSjke7Wp8LyJiBFUxz+745NyEbLACSkJ1wp8nxuRUDD+YhlfgavUHEzFot0mWYuJDU3JeyyDNSHS3VvKOih+51K0H0ucEKhbKUA+zo="
    )
    print(token_details)


retrieve_token_details()
