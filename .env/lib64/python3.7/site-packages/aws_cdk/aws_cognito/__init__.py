"""
## Amazon Cognito Construct Library

<!--BEGIN STABILITY BANNER-->---


![cfn-resources: Stable](https://img.shields.io/badge/cfn--resources-stable-success.svg?style=for-the-badge)

> All classes with the `Cfn` prefix in this module ([CFN Resources](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_lib)) are always stable and safe to use.

![cdk-constructs: Experimental](https://img.shields.io/badge/cdk--constructs-experimental-important.svg?style=for-the-badge)

> The APIs of higher level constructs in this module are experimental and under active development. They are subject to non-backward compatible changes or removal in any future version. These are not subject to the [Semantic Versioning](https://semver.org/) model and breaking changes will be announced in the release notes. This means that while you may use them, you may need to update your source code when upgrading to a newer version of this package.

---
<!--END STABILITY BANNER-->

[Amazon Cognito](https://docs.aws.amazon.com/cognito/latest/developerguide/what-is-amazon-cognito.html) provides
authentication, authorization, and user management for your web and mobile apps. Your users can sign in directly with a
user name and password, or through a third party such as Facebook, Amazon, Google or Apple.

The two main components of Amazon Cognito are [user
pools](https://docs.aws.amazon.com/cognito/latest/developerguide/cognito-user-identity-pools.html) and [identity
pools](https://docs.aws.amazon.com/cognito/latest/developerguide/cognito-identity.html). User pools are user directories
that provide sign-up and sign-in options for your app users. Identity pools enable you to grant your users access to
other AWS services.

This module is part of the [AWS Cloud Development Kit](https://github.com/aws/aws-cdk) project.

## Table of Contents

* [User Pools](#user-pools)

  * [Sign Up](#sign-up)
  * [Sign In](#sign-in)
  * [Attributes](#attributes)
  * [Security](#security)

    * [Multi-factor Authentication](#multi-factor-authentication-mfa)
  * [Emails](#emails)
  * [Lambda Triggers](#lambda-triggers)
  * [Import](#importing-user-pools)
  * [App Clients](#app-clients)
  * [Domains](#domains)

## User Pools

User pools allow creating and managing your own directory of users that can sign up and sign in. They enable easy
integration with social identity providers such as Facebook, Google, Amazon, Microsoft Active Directory, etc. through
SAML.

Using the CDK, a new user pool can be created as part of the stack using the construct's constructor. You may specify
the `userPoolName` to give your own identifier to the user pool. If not, CloudFormation will generate a name.

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
UserPool(self, "myuserpool",
    user_pool_name="myawesomeapp-userpool"
)
```

### Sign Up

Users can either be signed up by the app's administrators or can sign themselves up. Once a user has signed up, their
account needs to be confirmed. Cognito provides several ways to sign users up and confirm their accounts. Learn more
about [user sign up here](https://docs.aws.amazon.com/cognito/latest/developerguide/signing-up-users-in-your-app.html).

When a user signs up, email and SMS messages are used to verify their account and contact methods. The following code
snippet configures a user pool with properties relevant to these verification messages -

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
UserPool(self, "myuserpool",
    # ...
    self_sign_up_enabled=True,
    user_verification={
        "email_subject": "Verify your email for our awesome app!",
        "email_body": "Hello {username}, Thanks for signing up to our awesome app! Your verification code is {####}",
        "email_style": VerificationEmailStyle.CODE,
        "sms_message": "Hello {username}, Thanks for signing up to our awesome app! Your verification code is {####}"
    }
)
```

By default, self sign up is disabled. Learn more about [email and SMS verification messages
here](https://docs.aws.amazon.com/cognito/latest/developerguide/cognito-user-pool-settings-message-customizations.html).

Besides users signing themselves up, an administrator of any user pool can sign users up. The user then receives an
invitation to join the user pool. The following code snippet configures a user pool with properties relevant to the
invitation messages -

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
UserPool(self, "myuserpool",
    # ...
    user_invitation={
        "email_subject": "Invite to join our awesome app!",
        "email_body": "Hello {username}, you have been invited to join our awesome app! Your temporary password is {####}",
        "sms_message": "Your temporary password for our awesome app is {####}"
    }
)
```

All email subjects, bodies and SMS messages for both invitation and verification support Cognito's message templating.
Learn more about [message templates
here](https://docs.aws.amazon.com/cognito/latest/developerguide/cognito-user-pool-settings-message-templates.html).

### Sign In

Users registering or signing in into your application can do so with multiple identifiers. There are 4 options
available:

* `username`: Allow signing in using the one time immutable user name that the user chose at the time of sign up.
* `email`: Allow signing in using the email address that is associated with the account.
* `phone`: Allow signing in using the phone number that is associated with the account.
* `preferredUsername`: Allow signing in with an alternate user name that the user can change at any time. However, this
  is not available if the `username` option is not chosen.

The following code sets up a user pool so that the user can sign in with either their username or their email address -

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
UserPool(self, "myuserpool",
    # ...
    # ...
    sign_in_aliases={
        "username": True,
        "email": True
    }
)
```

User pools can either be configured so that user name is primary sign in form, but also allows for the other three to be
used additionally; or it can be configured so that email and/or phone numbers are the only ways a user can register and
sign in. Read more about this
[here](https://docs.aws.amazon.com/cognito/latest/developerguide/user-pool-settings-attributes.html#user-pool-settings-aliases-settings).

To match with 'Option 1' in the above link, with a verified email, `signInAliases` should be set to
`{ username: true, email: true }`. To match with 'Option 2' in the above link with both a verified
email and phone number, this property should be set to `{ email: true, phone: true }`.

Cognito recommends that email and phone number be automatically verified, if they are one of the sign in methods for
the user pool. Read more about that
[here](https://docs.aws.amazon.com/cognito/latest/developerguide/user-pool-settings-attributes.html#user-pool-settings-aliases).
The CDK does this by default, when email and/or phone number are specified as part of `signInAliases`. This can be
overridden by specifying the `autoVerify` property.

The following code snippet sets up only email as a sign in alias, but both email and phone number to be auto-verified.

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
UserPool(self, "myuserpool",
    # ...
    # ...
    sign_in_aliases={"username": True, "email": True},
    auto_verify={"email": True, "phone": True}
)
```

A user pool can optionally ignore case when evaluating sign-ins. When `signInCaseSensitive` is false, Cognito will not
check the capitalization of the alias when signing in. Default is true.

### Attributes

Attributes represent the various properties of each user that's collected and stored in the user pool. Cognito
provides a set of standard attributes that are available for all user pools. Users are allowed to select any of these
standard attributes to be required. Users will not be able to sign up to the user pool without providing the required
attributes. Besides these, additional attributes can be further defined, and are known as custom attributes.

Learn more on [attributes in Cognito's
documentation](https://docs.aws.amazon.com/cognito/latest/developerguide/user-pool-settings-attributes.html).

The following code sample configures a user pool with two standard attributes (name and address) as required, and adds
four optional attributes.

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
UserPool(self, "myuserpool",
    # ...
    required_attributes={
        "fullname": True,
        "address": True
    },
    custom_attributes={
        "myappid": StringAttribute(min_len=5, max_len=15, mutable=False),
        "callingcode": NumberAttribute(min=1, max=3, mutable=True),
        "is_employee": BooleanAttribute(mutable=True),
        "joined_on": DateTimeAttribute()
    }
)
```

As shown in the code snippet, there are data types that are available for custom attributes. The 'String' and 'Number'
data types allow for further constraints on their length and values, respectively.

Custom attributes cannot be marked as required.

All custom attributes share the property `mutable` that specifies whether the value of the attribute can be changed.
The default value is `false`.

### Security

Cognito sends various messages to its users via SMS, for different actions, ranging from account verification to
marketing. In order to send SMS messages, Cognito needs an IAM role that it can assume, with permissions that allow it
to send SMS messages. By default, CDK will create this IAM role but can also be explicily specified to an existing IAM
role using the `smsRole` property.

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
from aws_cdk.aws_iam import Role

pool_sms_role = Role(self, "userpoolsmsrole")

UserPool(self, "myuserpool",
    # ...
    sms_role=pool_sms_role,
    sms_role_external_id="c87467be-4f34-11ea-b77f-2e728ce88125"
)
```

When the `smsRole` property is specified, the `smsRoleExternalId` may also be specified. The value of
`smsRoleExternalId` will be used as the `sts:ExternalId` when the Cognito service assumes the role. In turn, the role's
assume role policy should be configured to accept this value as the ExternalId. Learn more about [ExternalId
here](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_create_for-user_externalid.html).

#### Multi-factor Authentication (MFA)

User pools can be configured to enable multi-factor authentication (MFA). It can either be turned off, set to optional
or made required. Setting MFA to optional means that individual users can choose to enable it.
Additionally, the MFA code can be sent either via SMS text message or via a time-based software token.
See the [documentation on MFA](https://docs.aws.amazon.com/cognito/latest/developerguide/user-pool-settings-mfa.html) to
learn more.

The following code snippet marks MFA for the user pool as required. This means that all users are required to
configure an MFA token and use it for sign in. It also allows for the users to use both SMS based MFA, as well,
[time-based one time password
(TOTP)](https://docs.aws.amazon.com/cognito/latest/developerguide/user-pool-settings-mfa-totp.html).

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
UserPool(self, "myuserpool",
    # ...
    mfa=Mfa.REQUIRED,
    mfa_second_factor={
        "sms": True,
        "otp": True
    }
)
```

User pools can be configured with policies around a user's password. This includes the password length and the
character sets that they must contain.

Further to this, it can also be configured with the validity of the auto-generated temporary password. A temporary
password is generated by the user pool either when an admin signs up a user or when a password reset is requested.
The validity of this password dictates how long to give the user to use this password before expiring it.

The following code snippet configures these properties -

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
UserPool(self, "myuserpool",
    # ...
    password_policy={
        "min_length": 12,
        "require_lowercase": True,
        "require_uppercase": True,
        "require_digits": True,
        "require_symbols": True,
        "temp_password_validity": Duration.days(3)
    }
)
```

Note that, `tempPasswordValidity` can be specified only in whole days. Specifying fractional days would throw an error.

### Emails

Cognito sends emails to users in the user pool, when particular actions take place, such as welcome emails, invitation
emails, password resets, etc. The address from which these emails are sent can be configured on the user pool.
Read more about [email settings here](https://docs.aws.amazon.com/cognito/latest/developerguide/user-pool-email.html).

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
UserPool(self, "myuserpool",
    # ...
    email_transmission={
        "from": "noreply@myawesomeapp.com",
        "reply_to": "support@myawesomeapp.com"
    }
)
```

By default, user pools are configured to use Cognito's built-in email capability, but it can also be configured to use
Amazon SES, however, support for Amazon SES is not available in the CDK yet. If you would like this to be implemented,
give [this issue](https://github.com/aws/aws-cdk/issues/6768) a +1. Until then, you can use the [cfn
layer](https://docs.aws.amazon.com/cdk/latest/guide/cfn_layer.html) to configure this.

### Lambda Triggers

User pools can be configured such that AWS Lambda functions can be triggered when certain user operations or actions
occur, such as, sign up, user confirmation, sign in, etc. They can also be used to add custom authentication
challenges, user migrations and custom verification messages. Learn more about triggers at [User Pool Workflows with
Triggers](https://docs.aws.amazon.com/cognito/latest/developerguide/cognito-user-identity-pools-working-with-aws-lambda-triggers.html).

Lambda triggers can either be specified as part of the `UserPool` initialization, or it can be added later, via methods
on the construct, as so -

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
auth_challenge_fn = lambda.Function(self, "authChallengeFn")

userpool = UserPool(self, "myuserpool",
    # ...
    triggers={
        "create_auth_challenge": auth_challenge_fn
    }
)

userpool.add_trigger(UserPoolOperation.USER_MIGRATION, lambda.Function(self, "userMigrationFn"))
```

The following table lists the set of triggers available, and their corresponding method to add it to the user pool.
For more information on the function of these triggers and how to configure them, read [User Pool Workflows with
Triggers](https://docs.aws.amazon.com/cognito/latest/developerguide/cognito-user-identity-pools-working-with-aws-lambda-triggers.html).

### Importing User Pools

Any user pool that has been created outside of this stack, can be imported into the CDK app. Importing a user pool
allows for it to be used in other parts of the CDK app that reference an `IUserPool`. However, imported user pools have
limited configurability. As a rule of thumb, none of the properties that is are part of the
[`AWS::Cognito::UserPool`](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpool.html)
CloudFormation resource can be configured.

User pools can be imported either using their id via the `UserPool.fromUserPoolId()`, or by using their ARN, via the
`UserPool.fromUserPoolArn()` API.

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
stack = Stack(app, "my-stack")

awesome_pool = UserPool.from_user_pool_id(stack, "awesome-user-pool", "us-east-1_oiuR12Abd")

other_awesome_pool = UserPool.from_user_pool_arn(stack, "other-awesome-user-pool", "arn:aws:cognito-idp:eu-west-1:123456789012:userpool/us-east-1_mtRyYQ14D")
```

### App Clients

An app is an entity within a user pool that has permission to call unauthenticated APIs (APIs that do not have an
authenticated user), such as APIs to register, sign in, and handle forgotten passwords. To call these APIs, you need an
app client ID and an optional client secret. Read [Configuring a User Pool App
Client](https://docs.aws.amazon.com/cognito/latest/developerguide/user-pool-settings-client-apps.html) to learn more.

The following code creates an app client and retrieves the client id -

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
pool = UserPool(self, "pool")
client = pool.add_client("customer-app-client")
client_id = client.user_pool_client_id
```

Existing app clients can be imported into the CDK app using the `UserPoolClient.fromUserPoolClientId()` API. For new
and imported user pools, clients can also be created via the `UserPoolClient` constructor, as so -

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
imported_pool = UserPool.from_user_pool_id(self, "imported-pool", "us-east-1_oiuR12Abd")
UserPoolClient(self, "customer-app-client",
    user_pool=imported_pool
)
```

Clients can be configured with authentication flows. Authentication flows allow users on a client to be authenticated
with a user pool. Cognito user pools provide several several different types of authentication, such as, SRP (Secure
Remote Password) authentication, username-and-password authentication, etc. Learn more about this at [UserPool Authentication
Flow](https://docs.aws.amazon.com/cognito/latest/developerguide/amazon-cognito-user-pools-authentication-flow.html).

The following code configures a client to use both SRP and username-and-password authentication -

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
pool = UserPool(self, "pool")
pool.add_client("app-client",
    auth_flows={
        "user_password": True,
        "user_srp": True
    }
)
```

Custom authentication protocols can be configured by setting the `custom` property under `authFlow` and defining lambda
functions for the corresponding user pool [triggers](#lambda-triggers). Learn more at [Custom Authentication
Flow](https://docs.aws.amazon.com/cognito/latest/developerguide/amazon-cognito-user-pools-authentication-flow.html#amazon-cognito-user-pools-custom-authentication-flow).

In addition to these authentication mechanisms, Cognito user pools also support using OAuth 2.0 framework for
authenticating users. User pool clients can be configured with OAuth 2.0 authorization flows and scopes. Learn more
about the [OAuth 2.0 authorization framework](https://tools.ietf.org/html/rfc6749) and [Cognito user pool's
implementation of
OAuth2.0](https://aws.amazon.com/blogs/mobile/understanding-amazon-cognito-user-pool-oauth-2-0-grants/).

The following code configures an app client with the authorization code grant flow and registers the the app's welcome
page as a callback (or redirect) URL. It also configures the access token scope to 'openid'. All of these concepts can
be found in the [OAuth 2.0 RFC](https://tools.ietf.org/html/rfc6749).

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
pool = UserPool(self, "Pool")
pool.add_client("app-client",
    o_auth={
        "flows": {
            "authorization_code_grant": True
        },
        "scopes": [OAuthScope.OPENID],
        "callback_urls": ["https://my-app-domain.com/welcome"]
    }
)
```

An app client can be configured to prevent user existence errors. This
instructs the Cognito authentication API to return generic authentication
failure responses instead of an UserNotFoundException. By default, the flag
is not set, which means different things for existing and new stacks. See the
[documentation](https://docs.aws.amazon.com/cognito/latest/developerguide/cognito-user-pool-managing-errors.html)
for the full details on the behavior of this flag.

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
pool = UserPool(self, "Pool")
pool.add_client("app-client",
    prevent_user_existence_errors=True
)
```

### Domains

After setting up an [app client](#app-clients), the address for the user pool's sign-up and sign-in webpages can be
configured using domains. There are two ways to set up a domain - either the Amazon Cognito hosted domain can be chosen
with an available domain prefix, or a custom domain name can be chosen. The custom domain must be one that is already
owned, and whose certificate is registered in AWS Certificate Manager.

The following code sets up a user pool domain in Amazon Cognito hosted domain with the prefix 'my-awesome-app', and another domain with the custom domain 'user.myapp.com' -

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
pool = UserPool(self, "Pool")

pool.add_domain("CognitoDomain",
    cognito_domain={
        "domain_prefix": "my-awesome-app"
    }
)

domain_cert = acm.Certificate.from_certificate_arn(self, "domainCert", certificate_arn)
pool.add_domain("CustomDomain",
    custom_domain={
        "domain_name": "user.myapp.com",
        "certificate": domain_cert
    }
)
```

Read more about [Using the Amazon Cognito
Domain](https://docs.aws.amazon.com/cognito/latest/developerguide/cognito-user-pools-assign-domain-prefix.html) and [Using Your Own
Domain](https://docs.aws.amazon.com/cognito/latest/developerguide/cognito-user-pools-add-custom-domain.html).
"""
import abc
import builtins
import datetime
import enum
import typing

import jsii
import jsii.compat
import publication

import aws_cdk.aws_certificatemanager
import aws_cdk.aws_iam
import aws_cdk.aws_lambda
import aws_cdk.core
import aws_cdk.custom_resources
import constructs

from ._jsii import *


@jsii.data_type(jsii_type="@aws-cdk/aws-cognito.AuthFlow", jsii_struct_bases=[], name_mapping={'admin_user_password': 'adminUserPassword', 'custom': 'custom', 'refresh_token': 'refreshToken', 'user_password': 'userPassword', 'user_srp': 'userSrp'})
class AuthFlow():
    def __init__(self, *, admin_user_password: typing.Optional[bool]=None, custom: typing.Optional[bool]=None, refresh_token: typing.Optional[bool]=None, user_password: typing.Optional[bool]=None, user_srp: typing.Optional[bool]=None) -> None:
        """Types of authentication flow.

        :param admin_user_password: Enable admin based user password authentication flow. Default: false
        :param custom: Enable custom authentication flow. Default: false
        :param refresh_token: Enable authflow to refresh tokens. Default: false
        :param user_password: Enable auth using username & password. Default: false
        :param user_srp: Enable SRP based authentication. Default: false

        see
        :see: https://docs.aws.amazon.com/cognito/latest/developerguide/amazon-cognito-user-pools-authentication-flow.html
        stability
        :stability: experimental
        """
        self._values = {
        }
        if admin_user_password is not None: self._values["admin_user_password"] = admin_user_password
        if custom is not None: self._values["custom"] = custom
        if refresh_token is not None: self._values["refresh_token"] = refresh_token
        if user_password is not None: self._values["user_password"] = user_password
        if user_srp is not None: self._values["user_srp"] = user_srp

    @builtins.property
    def admin_user_password(self) -> typing.Optional[bool]:
        """Enable admin based user password authentication flow.

        default
        :default: false

        stability
        :stability: experimental
        """
        return self._values.get('admin_user_password')

    @builtins.property
    def custom(self) -> typing.Optional[bool]:
        """Enable custom authentication flow.

        default
        :default: false

        stability
        :stability: experimental
        """
        return self._values.get('custom')

    @builtins.property
    def refresh_token(self) -> typing.Optional[bool]:
        """Enable authflow to refresh tokens.

        default
        :default: false

        stability
        :stability: experimental
        """
        return self._values.get('refresh_token')

    @builtins.property
    def user_password(self) -> typing.Optional[bool]:
        """Enable auth using username & password.

        default
        :default: false

        stability
        :stability: experimental
        """
        return self._values.get('user_password')

    @builtins.property
    def user_srp(self) -> typing.Optional[bool]:
        """Enable SRP based authentication.

        default
        :default: false

        stability
        :stability: experimental
        """
        return self._values.get('user_srp')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'AuthFlow(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="@aws-cdk/aws-cognito.AutoVerifiedAttrs", jsii_struct_bases=[], name_mapping={'email': 'email', 'phone': 'phone'})
class AutoVerifiedAttrs():
    def __init__(self, *, email: typing.Optional[bool]=None, phone: typing.Optional[bool]=None) -> None:
        """Attributes that can be automatically verified for users in a user pool.

        :param email: Whether the email address of the user should be auto verified at sign up. Note: If both ``email`` and ``phone`` is set, Cognito only verifies the phone number. To also verify email, see here - https://docs.aws.amazon.com/cognito/latest/developerguide/user-pool-settings-email-phone-verification.html Default: - true, if email is turned on for ``signIn``. false, otherwise.
        :param phone: Whether the phone number of the user should be auto verified at sign up. Default: - true, if phone is turned on for ``signIn``. false, otherwise.

        stability
        :stability: experimental
        """
        self._values = {
        }
        if email is not None: self._values["email"] = email
        if phone is not None: self._values["phone"] = phone

    @builtins.property
    def email(self) -> typing.Optional[bool]:
        """Whether the email address of the user should be auto verified at sign up.

        Note: If both ``email`` and ``phone`` is set, Cognito only verifies the phone number. To also verify email, see here -
        https://docs.aws.amazon.com/cognito/latest/developerguide/user-pool-settings-email-phone-verification.html

        default
        :default: - true, if email is turned on for ``signIn``. false, otherwise.

        stability
        :stability: experimental
        """
        return self._values.get('email')

    @builtins.property
    def phone(self) -> typing.Optional[bool]:
        """Whether the phone number of the user should be auto verified at sign up.

        default
        :default: - true, if phone is turned on for ``signIn``. false, otherwise.

        stability
        :stability: experimental
        """
        return self._values.get('phone')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'AutoVerifiedAttrs(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.implements(aws_cdk.core.IInspectable)
class CfnIdentityPool(aws_cdk.core.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-cognito.CfnIdentityPool"):
    """A CloudFormation ``AWS::Cognito::IdentityPool``.

    see
    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-identitypool.html
    cloudformationResource:
    :cloudformationResource:: AWS::Cognito::IdentityPool
    """
    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, allow_unauthenticated_identities: typing.Union[bool, aws_cdk.core.IResolvable], allow_classic_flow: typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.core.IResolvable]]]=None, cognito_events: typing.Any=None, cognito_identity_providers: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union[aws_cdk.core.IResolvable, "CognitoIdentityProviderProperty"]]]]]=None, cognito_streams: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["CognitoStreamsProperty"]]]=None, developer_provider_name: typing.Optional[str]=None, identity_pool_name: typing.Optional[str]=None, open_id_connect_provider_arns: typing.Optional[typing.List[str]]=None, push_sync: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["PushSyncProperty"]]]=None, saml_provider_arns: typing.Optional[typing.List[str]]=None, supported_login_providers: typing.Any=None) -> None:
        """Create a new ``AWS::Cognito::IdentityPool``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param allow_unauthenticated_identities: ``AWS::Cognito::IdentityPool.AllowUnauthenticatedIdentities``.
        :param allow_classic_flow: ``AWS::Cognito::IdentityPool.AllowClassicFlow``.
        :param cognito_events: ``AWS::Cognito::IdentityPool.CognitoEvents``.
        :param cognito_identity_providers: ``AWS::Cognito::IdentityPool.CognitoIdentityProviders``.
        :param cognito_streams: ``AWS::Cognito::IdentityPool.CognitoStreams``.
        :param developer_provider_name: ``AWS::Cognito::IdentityPool.DeveloperProviderName``.
        :param identity_pool_name: ``AWS::Cognito::IdentityPool.IdentityPoolName``.
        :param open_id_connect_provider_arns: ``AWS::Cognito::IdentityPool.OpenIdConnectProviderARNs``.
        :param push_sync: ``AWS::Cognito::IdentityPool.PushSync``.
        :param saml_provider_arns: ``AWS::Cognito::IdentityPool.SamlProviderARNs``.
        :param supported_login_providers: ``AWS::Cognito::IdentityPool.SupportedLoginProviders``.
        """
        props = CfnIdentityPoolProps(allow_unauthenticated_identities=allow_unauthenticated_identities, allow_classic_flow=allow_classic_flow, cognito_events=cognito_events, cognito_identity_providers=cognito_identity_providers, cognito_streams=cognito_streams, developer_provider_name=developer_provider_name, identity_pool_name=identity_pool_name, open_id_connect_provider_arns=open_id_connect_provider_arns, push_sync=push_sync, saml_provider_arns=saml_provider_arns, supported_login_providers=supported_login_providers)

        jsii.create(CfnIdentityPool, self, [scope, id, props])

    @jsii.member(jsii_name="fromCloudFormation")
    @builtins.classmethod
    def from_cloud_formation(cls, scope: aws_cdk.core.Construct, id: str, resource_attributes: typing.Any, *, finder: aws_cdk.core.ICfnFinder) -> "CfnIdentityPool":
        """A factory method that creates a new instance of this class from an object containing the CloudFormation properties of this resource.

        Used in the @aws-cdk/cloudformation-include module.

        :param scope: -
        :param id: -
        :param resource_attributes: -
        :param finder: The finder interface used to resolve references across the template.

        stability
        :stability: experimental
        """
        options = aws_cdk.core.FromCloudFormationOptions(finder=finder)

        return jsii.sinvoke(cls, "fromCloudFormation", [scope, id, resource_attributes, options])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: aws_cdk.core.TreeInspector) -> None:
        """Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "inspect", [inspector])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, props: typing.Mapping[str, typing.Any]) -> typing.Mapping[str, typing.Any]:
        """
        :param props: -
        """
        return jsii.invoke(self, "renderProperties", [props])

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> str:
        """The CloudFormation resource type name for this resource class."""
        return jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME")

    @builtins.property
    @jsii.member(jsii_name="attrName")
    def attr_name(self) -> str:
        """
        cloudformationAttribute:
        :cloudformationAttribute:: Name
        """
        return jsii.get(self, "attrName")

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[str, typing.Any]:
        return jsii.get(self, "cfnProperties")

    @builtins.property
    @jsii.member(jsii_name="allowUnauthenticatedIdentities")
    def allow_unauthenticated_identities(self) -> typing.Union[bool, aws_cdk.core.IResolvable]:
        """``AWS::Cognito::IdentityPool.AllowUnauthenticatedIdentities``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-identitypool.html#cfn-cognito-identitypool-allowunauthenticatedidentities
        """
        return jsii.get(self, "allowUnauthenticatedIdentities")

    @allow_unauthenticated_identities.setter
    def allow_unauthenticated_identities(self, value: typing.Union[bool, aws_cdk.core.IResolvable]):
        jsii.set(self, "allowUnauthenticatedIdentities", value)

    @builtins.property
    @jsii.member(jsii_name="cognitoEvents")
    def cognito_events(self) -> typing.Any:
        """``AWS::Cognito::IdentityPool.CognitoEvents``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-identitypool.html#cfn-cognito-identitypool-cognitoevents
        """
        return jsii.get(self, "cognitoEvents")

    @cognito_events.setter
    def cognito_events(self, value: typing.Any):
        jsii.set(self, "cognitoEvents", value)

    @builtins.property
    @jsii.member(jsii_name="supportedLoginProviders")
    def supported_login_providers(self) -> typing.Any:
        """``AWS::Cognito::IdentityPool.SupportedLoginProviders``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-identitypool.html#cfn-cognito-identitypool-supportedloginproviders
        """
        return jsii.get(self, "supportedLoginProviders")

    @supported_login_providers.setter
    def supported_login_providers(self, value: typing.Any):
        jsii.set(self, "supportedLoginProviders", value)

    @builtins.property
    @jsii.member(jsii_name="allowClassicFlow")
    def allow_classic_flow(self) -> typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.core.IResolvable]]]:
        """``AWS::Cognito::IdentityPool.AllowClassicFlow``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-identitypool.html#cfn-cognito-identitypool-allowclassicflow
        """
        return jsii.get(self, "allowClassicFlow")

    @allow_classic_flow.setter
    def allow_classic_flow(self, value: typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.core.IResolvable]]]):
        jsii.set(self, "allowClassicFlow", value)

    @builtins.property
    @jsii.member(jsii_name="cognitoIdentityProviders")
    def cognito_identity_providers(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union[aws_cdk.core.IResolvable, "CognitoIdentityProviderProperty"]]]]]:
        """``AWS::Cognito::IdentityPool.CognitoIdentityProviders``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-identitypool.html#cfn-cognito-identitypool-cognitoidentityproviders
        """
        return jsii.get(self, "cognitoIdentityProviders")

    @cognito_identity_providers.setter
    def cognito_identity_providers(self, value: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union[aws_cdk.core.IResolvable, "CognitoIdentityProviderProperty"]]]]]):
        jsii.set(self, "cognitoIdentityProviders", value)

    @builtins.property
    @jsii.member(jsii_name="cognitoStreams")
    def cognito_streams(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["CognitoStreamsProperty"]]]:
        """``AWS::Cognito::IdentityPool.CognitoStreams``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-identitypool.html#cfn-cognito-identitypool-cognitostreams
        """
        return jsii.get(self, "cognitoStreams")

    @cognito_streams.setter
    def cognito_streams(self, value: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["CognitoStreamsProperty"]]]):
        jsii.set(self, "cognitoStreams", value)

    @builtins.property
    @jsii.member(jsii_name="developerProviderName")
    def developer_provider_name(self) -> typing.Optional[str]:
        """``AWS::Cognito::IdentityPool.DeveloperProviderName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-identitypool.html#cfn-cognito-identitypool-developerprovidername
        """
        return jsii.get(self, "developerProviderName")

    @developer_provider_name.setter
    def developer_provider_name(self, value: typing.Optional[str]):
        jsii.set(self, "developerProviderName", value)

    @builtins.property
    @jsii.member(jsii_name="identityPoolName")
    def identity_pool_name(self) -> typing.Optional[str]:
        """``AWS::Cognito::IdentityPool.IdentityPoolName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-identitypool.html#cfn-cognito-identitypool-identitypoolname
        """
        return jsii.get(self, "identityPoolName")

    @identity_pool_name.setter
    def identity_pool_name(self, value: typing.Optional[str]):
        jsii.set(self, "identityPoolName", value)

    @builtins.property
    @jsii.member(jsii_name="openIdConnectProviderArns")
    def open_id_connect_provider_arns(self) -> typing.Optional[typing.List[str]]:
        """``AWS::Cognito::IdentityPool.OpenIdConnectProviderARNs``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-identitypool.html#cfn-cognito-identitypool-openidconnectproviderarns
        """
        return jsii.get(self, "openIdConnectProviderArns")

    @open_id_connect_provider_arns.setter
    def open_id_connect_provider_arns(self, value: typing.Optional[typing.List[str]]):
        jsii.set(self, "openIdConnectProviderArns", value)

    @builtins.property
    @jsii.member(jsii_name="pushSync")
    def push_sync(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["PushSyncProperty"]]]:
        """``AWS::Cognito::IdentityPool.PushSync``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-identitypool.html#cfn-cognito-identitypool-pushsync
        """
        return jsii.get(self, "pushSync")

    @push_sync.setter
    def push_sync(self, value: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["PushSyncProperty"]]]):
        jsii.set(self, "pushSync", value)

    @builtins.property
    @jsii.member(jsii_name="samlProviderArns")
    def saml_provider_arns(self) -> typing.Optional[typing.List[str]]:
        """``AWS::Cognito::IdentityPool.SamlProviderARNs``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-identitypool.html#cfn-cognito-identitypool-samlproviderarns
        """
        return jsii.get(self, "samlProviderArns")

    @saml_provider_arns.setter
    def saml_provider_arns(self, value: typing.Optional[typing.List[str]]):
        jsii.set(self, "samlProviderArns", value)

    @jsii.data_type(jsii_type="@aws-cdk/aws-cognito.CfnIdentityPool.CognitoIdentityProviderProperty", jsii_struct_bases=[], name_mapping={'client_id': 'clientId', 'provider_name': 'providerName', 'server_side_token_check': 'serverSideTokenCheck'})
    class CognitoIdentityProviderProperty():
        def __init__(self, *, client_id: typing.Optional[str]=None, provider_name: typing.Optional[str]=None, server_side_token_check: typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.core.IResolvable]]]=None) -> None:
            """
            :param client_id: ``CfnIdentityPool.CognitoIdentityProviderProperty.ClientId``.
            :param provider_name: ``CfnIdentityPool.CognitoIdentityProviderProperty.ProviderName``.
            :param server_side_token_check: ``CfnIdentityPool.CognitoIdentityProviderProperty.ServerSideTokenCheck``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-identitypool-cognitoidentityprovider.html
            """
            self._values = {
            }
            if client_id is not None: self._values["client_id"] = client_id
            if provider_name is not None: self._values["provider_name"] = provider_name
            if server_side_token_check is not None: self._values["server_side_token_check"] = server_side_token_check

        @builtins.property
        def client_id(self) -> typing.Optional[str]:
            """``CfnIdentityPool.CognitoIdentityProviderProperty.ClientId``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-identitypool-cognitoidentityprovider.html#cfn-cognito-identitypool-cognitoidentityprovider-clientid
            """
            return self._values.get('client_id')

        @builtins.property
        def provider_name(self) -> typing.Optional[str]:
            """``CfnIdentityPool.CognitoIdentityProviderProperty.ProviderName``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-identitypool-cognitoidentityprovider.html#cfn-cognito-identitypool-cognitoidentityprovider-providername
            """
            return self._values.get('provider_name')

        @builtins.property
        def server_side_token_check(self) -> typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.core.IResolvable]]]:
            """``CfnIdentityPool.CognitoIdentityProviderProperty.ServerSideTokenCheck``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-identitypool-cognitoidentityprovider.html#cfn-cognito-identitypool-cognitoidentityprovider-serversidetokencheck
            """
            return self._values.get('server_side_token_check')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'CognitoIdentityProviderProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="@aws-cdk/aws-cognito.CfnIdentityPool.CognitoStreamsProperty", jsii_struct_bases=[], name_mapping={'role_arn': 'roleArn', 'streaming_status': 'streamingStatus', 'stream_name': 'streamName'})
    class CognitoStreamsProperty():
        def __init__(self, *, role_arn: typing.Optional[str]=None, streaming_status: typing.Optional[str]=None, stream_name: typing.Optional[str]=None) -> None:
            """
            :param role_arn: ``CfnIdentityPool.CognitoStreamsProperty.RoleArn``.
            :param streaming_status: ``CfnIdentityPool.CognitoStreamsProperty.StreamingStatus``.
            :param stream_name: ``CfnIdentityPool.CognitoStreamsProperty.StreamName``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-identitypool-cognitostreams.html
            """
            self._values = {
            }
            if role_arn is not None: self._values["role_arn"] = role_arn
            if streaming_status is not None: self._values["streaming_status"] = streaming_status
            if stream_name is not None: self._values["stream_name"] = stream_name

        @builtins.property
        def role_arn(self) -> typing.Optional[str]:
            """``CfnIdentityPool.CognitoStreamsProperty.RoleArn``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-identitypool-cognitostreams.html#cfn-cognito-identitypool-cognitostreams-rolearn
            """
            return self._values.get('role_arn')

        @builtins.property
        def streaming_status(self) -> typing.Optional[str]:
            """``CfnIdentityPool.CognitoStreamsProperty.StreamingStatus``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-identitypool-cognitostreams.html#cfn-cognito-identitypool-cognitostreams-streamingstatus
            """
            return self._values.get('streaming_status')

        @builtins.property
        def stream_name(self) -> typing.Optional[str]:
            """``CfnIdentityPool.CognitoStreamsProperty.StreamName``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-identitypool-cognitostreams.html#cfn-cognito-identitypool-cognitostreams-streamname
            """
            return self._values.get('stream_name')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'CognitoStreamsProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="@aws-cdk/aws-cognito.CfnIdentityPool.PushSyncProperty", jsii_struct_bases=[], name_mapping={'application_arns': 'applicationArns', 'role_arn': 'roleArn'})
    class PushSyncProperty():
        def __init__(self, *, application_arns: typing.Optional[typing.List[str]]=None, role_arn: typing.Optional[str]=None) -> None:
            """
            :param application_arns: ``CfnIdentityPool.PushSyncProperty.ApplicationArns``.
            :param role_arn: ``CfnIdentityPool.PushSyncProperty.RoleArn``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-identitypool-pushsync.html
            """
            self._values = {
            }
            if application_arns is not None: self._values["application_arns"] = application_arns
            if role_arn is not None: self._values["role_arn"] = role_arn

        @builtins.property
        def application_arns(self) -> typing.Optional[typing.List[str]]:
            """``CfnIdentityPool.PushSyncProperty.ApplicationArns``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-identitypool-pushsync.html#cfn-cognito-identitypool-pushsync-applicationarns
            """
            return self._values.get('application_arns')

        @builtins.property
        def role_arn(self) -> typing.Optional[str]:
            """``CfnIdentityPool.PushSyncProperty.RoleArn``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-identitypool-pushsync.html#cfn-cognito-identitypool-pushsync-rolearn
            """
            return self._values.get('role_arn')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'PushSyncProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())



@jsii.data_type(jsii_type="@aws-cdk/aws-cognito.CfnIdentityPoolProps", jsii_struct_bases=[], name_mapping={'allow_unauthenticated_identities': 'allowUnauthenticatedIdentities', 'allow_classic_flow': 'allowClassicFlow', 'cognito_events': 'cognitoEvents', 'cognito_identity_providers': 'cognitoIdentityProviders', 'cognito_streams': 'cognitoStreams', 'developer_provider_name': 'developerProviderName', 'identity_pool_name': 'identityPoolName', 'open_id_connect_provider_arns': 'openIdConnectProviderArns', 'push_sync': 'pushSync', 'saml_provider_arns': 'samlProviderArns', 'supported_login_providers': 'supportedLoginProviders'})
class CfnIdentityPoolProps():
    def __init__(self, *, allow_unauthenticated_identities: typing.Union[bool, aws_cdk.core.IResolvable], allow_classic_flow: typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.core.IResolvable]]]=None, cognito_events: typing.Any=None, cognito_identity_providers: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnIdentityPool.CognitoIdentityProviderProperty"]]]]]=None, cognito_streams: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["CfnIdentityPool.CognitoStreamsProperty"]]]=None, developer_provider_name: typing.Optional[str]=None, identity_pool_name: typing.Optional[str]=None, open_id_connect_provider_arns: typing.Optional[typing.List[str]]=None, push_sync: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["CfnIdentityPool.PushSyncProperty"]]]=None, saml_provider_arns: typing.Optional[typing.List[str]]=None, supported_login_providers: typing.Any=None) -> None:
        """Properties for defining a ``AWS::Cognito::IdentityPool``.

        :param allow_unauthenticated_identities: ``AWS::Cognito::IdentityPool.AllowUnauthenticatedIdentities``.
        :param allow_classic_flow: ``AWS::Cognito::IdentityPool.AllowClassicFlow``.
        :param cognito_events: ``AWS::Cognito::IdentityPool.CognitoEvents``.
        :param cognito_identity_providers: ``AWS::Cognito::IdentityPool.CognitoIdentityProviders``.
        :param cognito_streams: ``AWS::Cognito::IdentityPool.CognitoStreams``.
        :param developer_provider_name: ``AWS::Cognito::IdentityPool.DeveloperProviderName``.
        :param identity_pool_name: ``AWS::Cognito::IdentityPool.IdentityPoolName``.
        :param open_id_connect_provider_arns: ``AWS::Cognito::IdentityPool.OpenIdConnectProviderARNs``.
        :param push_sync: ``AWS::Cognito::IdentityPool.PushSync``.
        :param saml_provider_arns: ``AWS::Cognito::IdentityPool.SamlProviderARNs``.
        :param supported_login_providers: ``AWS::Cognito::IdentityPool.SupportedLoginProviders``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-identitypool.html
        """
        self._values = {
            'allow_unauthenticated_identities': allow_unauthenticated_identities,
        }
        if allow_classic_flow is not None: self._values["allow_classic_flow"] = allow_classic_flow
        if cognito_events is not None: self._values["cognito_events"] = cognito_events
        if cognito_identity_providers is not None: self._values["cognito_identity_providers"] = cognito_identity_providers
        if cognito_streams is not None: self._values["cognito_streams"] = cognito_streams
        if developer_provider_name is not None: self._values["developer_provider_name"] = developer_provider_name
        if identity_pool_name is not None: self._values["identity_pool_name"] = identity_pool_name
        if open_id_connect_provider_arns is not None: self._values["open_id_connect_provider_arns"] = open_id_connect_provider_arns
        if push_sync is not None: self._values["push_sync"] = push_sync
        if saml_provider_arns is not None: self._values["saml_provider_arns"] = saml_provider_arns
        if supported_login_providers is not None: self._values["supported_login_providers"] = supported_login_providers

    @builtins.property
    def allow_unauthenticated_identities(self) -> typing.Union[bool, aws_cdk.core.IResolvable]:
        """``AWS::Cognito::IdentityPool.AllowUnauthenticatedIdentities``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-identitypool.html#cfn-cognito-identitypool-allowunauthenticatedidentities
        """
        return self._values.get('allow_unauthenticated_identities')

    @builtins.property
    def allow_classic_flow(self) -> typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.core.IResolvable]]]:
        """``AWS::Cognito::IdentityPool.AllowClassicFlow``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-identitypool.html#cfn-cognito-identitypool-allowclassicflow
        """
        return self._values.get('allow_classic_flow')

    @builtins.property
    def cognito_events(self) -> typing.Any:
        """``AWS::Cognito::IdentityPool.CognitoEvents``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-identitypool.html#cfn-cognito-identitypool-cognitoevents
        """
        return self._values.get('cognito_events')

    @builtins.property
    def cognito_identity_providers(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnIdentityPool.CognitoIdentityProviderProperty"]]]]]:
        """``AWS::Cognito::IdentityPool.CognitoIdentityProviders``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-identitypool.html#cfn-cognito-identitypool-cognitoidentityproviders
        """
        return self._values.get('cognito_identity_providers')

    @builtins.property
    def cognito_streams(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["CfnIdentityPool.CognitoStreamsProperty"]]]:
        """``AWS::Cognito::IdentityPool.CognitoStreams``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-identitypool.html#cfn-cognito-identitypool-cognitostreams
        """
        return self._values.get('cognito_streams')

    @builtins.property
    def developer_provider_name(self) -> typing.Optional[str]:
        """``AWS::Cognito::IdentityPool.DeveloperProviderName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-identitypool.html#cfn-cognito-identitypool-developerprovidername
        """
        return self._values.get('developer_provider_name')

    @builtins.property
    def identity_pool_name(self) -> typing.Optional[str]:
        """``AWS::Cognito::IdentityPool.IdentityPoolName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-identitypool.html#cfn-cognito-identitypool-identitypoolname
        """
        return self._values.get('identity_pool_name')

    @builtins.property
    def open_id_connect_provider_arns(self) -> typing.Optional[typing.List[str]]:
        """``AWS::Cognito::IdentityPool.OpenIdConnectProviderARNs``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-identitypool.html#cfn-cognito-identitypool-openidconnectproviderarns
        """
        return self._values.get('open_id_connect_provider_arns')

    @builtins.property
    def push_sync(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["CfnIdentityPool.PushSyncProperty"]]]:
        """``AWS::Cognito::IdentityPool.PushSync``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-identitypool.html#cfn-cognito-identitypool-pushsync
        """
        return self._values.get('push_sync')

    @builtins.property
    def saml_provider_arns(self) -> typing.Optional[typing.List[str]]:
        """``AWS::Cognito::IdentityPool.SamlProviderARNs``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-identitypool.html#cfn-cognito-identitypool-samlproviderarns
        """
        return self._values.get('saml_provider_arns')

    @builtins.property
    def supported_login_providers(self) -> typing.Any:
        """``AWS::Cognito::IdentityPool.SupportedLoginProviders``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-identitypool.html#cfn-cognito-identitypool-supportedloginproviders
        """
        return self._values.get('supported_login_providers')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'CfnIdentityPoolProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.implements(aws_cdk.core.IInspectable)
class CfnIdentityPoolRoleAttachment(aws_cdk.core.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-cognito.CfnIdentityPoolRoleAttachment"):
    """A CloudFormation ``AWS::Cognito::IdentityPoolRoleAttachment``.

    see
    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-identitypoolroleattachment.html
    cloudformationResource:
    :cloudformationResource:: AWS::Cognito::IdentityPoolRoleAttachment
    """
    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, identity_pool_id: str, role_mappings: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.Mapping[str, typing.Union[aws_cdk.core.IResolvable, "RoleMappingProperty"]]]]]=None, roles: typing.Any=None) -> None:
        """Create a new ``AWS::Cognito::IdentityPoolRoleAttachment``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param identity_pool_id: ``AWS::Cognito::IdentityPoolRoleAttachment.IdentityPoolId``.
        :param role_mappings: ``AWS::Cognito::IdentityPoolRoleAttachment.RoleMappings``.
        :param roles: ``AWS::Cognito::IdentityPoolRoleAttachment.Roles``.
        """
        props = CfnIdentityPoolRoleAttachmentProps(identity_pool_id=identity_pool_id, role_mappings=role_mappings, roles=roles)

        jsii.create(CfnIdentityPoolRoleAttachment, self, [scope, id, props])

    @jsii.member(jsii_name="fromCloudFormation")
    @builtins.classmethod
    def from_cloud_formation(cls, scope: aws_cdk.core.Construct, id: str, resource_attributes: typing.Any, *, finder: aws_cdk.core.ICfnFinder) -> "CfnIdentityPoolRoleAttachment":
        """A factory method that creates a new instance of this class from an object containing the CloudFormation properties of this resource.

        Used in the @aws-cdk/cloudformation-include module.

        :param scope: -
        :param id: -
        :param resource_attributes: -
        :param finder: The finder interface used to resolve references across the template.

        stability
        :stability: experimental
        """
        options = aws_cdk.core.FromCloudFormationOptions(finder=finder)

        return jsii.sinvoke(cls, "fromCloudFormation", [scope, id, resource_attributes, options])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: aws_cdk.core.TreeInspector) -> None:
        """Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "inspect", [inspector])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, props: typing.Mapping[str, typing.Any]) -> typing.Mapping[str, typing.Any]:
        """
        :param props: -
        """
        return jsii.invoke(self, "renderProperties", [props])

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> str:
        """The CloudFormation resource type name for this resource class."""
        return jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME")

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[str, typing.Any]:
        return jsii.get(self, "cfnProperties")

    @builtins.property
    @jsii.member(jsii_name="identityPoolId")
    def identity_pool_id(self) -> str:
        """``AWS::Cognito::IdentityPoolRoleAttachment.IdentityPoolId``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-identitypoolroleattachment.html#cfn-cognito-identitypoolroleattachment-identitypoolid
        """
        return jsii.get(self, "identityPoolId")

    @identity_pool_id.setter
    def identity_pool_id(self, value: str):
        jsii.set(self, "identityPoolId", value)

    @builtins.property
    @jsii.member(jsii_name="roles")
    def roles(self) -> typing.Any:
        """``AWS::Cognito::IdentityPoolRoleAttachment.Roles``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-identitypoolroleattachment.html#cfn-cognito-identitypoolroleattachment-roles
        """
        return jsii.get(self, "roles")

    @roles.setter
    def roles(self, value: typing.Any):
        jsii.set(self, "roles", value)

    @builtins.property
    @jsii.member(jsii_name="roleMappings")
    def role_mappings(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.Mapping[str, typing.Union[aws_cdk.core.IResolvable, "RoleMappingProperty"]]]]]:
        """``AWS::Cognito::IdentityPoolRoleAttachment.RoleMappings``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-identitypoolroleattachment.html#cfn-cognito-identitypoolroleattachment-rolemappings
        """
        return jsii.get(self, "roleMappings")

    @role_mappings.setter
    def role_mappings(self, value: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.Mapping[str, typing.Union[aws_cdk.core.IResolvable, "RoleMappingProperty"]]]]]):
        jsii.set(self, "roleMappings", value)

    @jsii.data_type(jsii_type="@aws-cdk/aws-cognito.CfnIdentityPoolRoleAttachment.MappingRuleProperty", jsii_struct_bases=[], name_mapping={'claim': 'claim', 'match_type': 'matchType', 'role_arn': 'roleArn', 'value': 'value'})
    class MappingRuleProperty():
        def __init__(self, *, claim: str, match_type: str, role_arn: str, value: str) -> None:
            """
            :param claim: ``CfnIdentityPoolRoleAttachment.MappingRuleProperty.Claim``.
            :param match_type: ``CfnIdentityPoolRoleAttachment.MappingRuleProperty.MatchType``.
            :param role_arn: ``CfnIdentityPoolRoleAttachment.MappingRuleProperty.RoleARN``.
            :param value: ``CfnIdentityPoolRoleAttachment.MappingRuleProperty.Value``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-identitypoolroleattachment-mappingrule.html
            """
            self._values = {
                'claim': claim,
                'match_type': match_type,
                'role_arn': role_arn,
                'value': value,
            }

        @builtins.property
        def claim(self) -> str:
            """``CfnIdentityPoolRoleAttachment.MappingRuleProperty.Claim``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-identitypoolroleattachment-mappingrule.html#cfn-cognito-identitypoolroleattachment-mappingrule-claim
            """
            return self._values.get('claim')

        @builtins.property
        def match_type(self) -> str:
            """``CfnIdentityPoolRoleAttachment.MappingRuleProperty.MatchType``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-identitypoolroleattachment-mappingrule.html#cfn-cognito-identitypoolroleattachment-mappingrule-matchtype
            """
            return self._values.get('match_type')

        @builtins.property
        def role_arn(self) -> str:
            """``CfnIdentityPoolRoleAttachment.MappingRuleProperty.RoleARN``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-identitypoolroleattachment-mappingrule.html#cfn-cognito-identitypoolroleattachment-mappingrule-rolearn
            """
            return self._values.get('role_arn')

        @builtins.property
        def value(self) -> str:
            """``CfnIdentityPoolRoleAttachment.MappingRuleProperty.Value``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-identitypoolroleattachment-mappingrule.html#cfn-cognito-identitypoolroleattachment-mappingrule-value
            """
            return self._values.get('value')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'MappingRuleProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="@aws-cdk/aws-cognito.CfnIdentityPoolRoleAttachment.RoleMappingProperty", jsii_struct_bases=[], name_mapping={'type': 'type', 'ambiguous_role_resolution': 'ambiguousRoleResolution', 'identity_provider': 'identityProvider', 'rules_configuration': 'rulesConfiguration'})
    class RoleMappingProperty():
        def __init__(self, *, type: str, ambiguous_role_resolution: typing.Optional[str]=None, identity_provider: typing.Optional[str]=None, rules_configuration: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["CfnIdentityPoolRoleAttachment.RulesConfigurationTypeProperty"]]]=None) -> None:
            """
            :param type: ``CfnIdentityPoolRoleAttachment.RoleMappingProperty.Type``.
            :param ambiguous_role_resolution: ``CfnIdentityPoolRoleAttachment.RoleMappingProperty.AmbiguousRoleResolution``.
            :param identity_provider: ``CfnIdentityPoolRoleAttachment.RoleMappingProperty.IdentityProvider``.
            :param rules_configuration: ``CfnIdentityPoolRoleAttachment.RoleMappingProperty.RulesConfiguration``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-identitypoolroleattachment-rolemapping.html
            """
            self._values = {
                'type': type,
            }
            if ambiguous_role_resolution is not None: self._values["ambiguous_role_resolution"] = ambiguous_role_resolution
            if identity_provider is not None: self._values["identity_provider"] = identity_provider
            if rules_configuration is not None: self._values["rules_configuration"] = rules_configuration

        @builtins.property
        def type(self) -> str:
            """``CfnIdentityPoolRoleAttachment.RoleMappingProperty.Type``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-identitypoolroleattachment-rolemapping.html#cfn-cognito-identitypoolroleattachment-rolemapping-type
            """
            return self._values.get('type')

        @builtins.property
        def ambiguous_role_resolution(self) -> typing.Optional[str]:
            """``CfnIdentityPoolRoleAttachment.RoleMappingProperty.AmbiguousRoleResolution``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-identitypoolroleattachment-rolemapping.html#cfn-cognito-identitypoolroleattachment-rolemapping-ambiguousroleresolution
            """
            return self._values.get('ambiguous_role_resolution')

        @builtins.property
        def identity_provider(self) -> typing.Optional[str]:
            """``CfnIdentityPoolRoleAttachment.RoleMappingProperty.IdentityProvider``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-identitypoolroleattachment-rolemapping.html#cfn-cognito-identitypoolroleattachment-rolemapping-identityprovider
            """
            return self._values.get('identity_provider')

        @builtins.property
        def rules_configuration(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["CfnIdentityPoolRoleAttachment.RulesConfigurationTypeProperty"]]]:
            """``CfnIdentityPoolRoleAttachment.RoleMappingProperty.RulesConfiguration``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-identitypoolroleattachment-rolemapping.html#cfn-cognito-identitypoolroleattachment-rolemapping-rulesconfiguration
            """
            return self._values.get('rules_configuration')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'RoleMappingProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="@aws-cdk/aws-cognito.CfnIdentityPoolRoleAttachment.RulesConfigurationTypeProperty", jsii_struct_bases=[], name_mapping={'rules': 'rules'})
    class RulesConfigurationTypeProperty():
        def __init__(self, *, rules: typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnIdentityPoolRoleAttachment.MappingRuleProperty"]]]) -> None:
            """
            :param rules: ``CfnIdentityPoolRoleAttachment.RulesConfigurationTypeProperty.Rules``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-identitypoolroleattachment-rulesconfigurationtype.html
            """
            self._values = {
                'rules': rules,
            }

        @builtins.property
        def rules(self) -> typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnIdentityPoolRoleAttachment.MappingRuleProperty"]]]:
            """``CfnIdentityPoolRoleAttachment.RulesConfigurationTypeProperty.Rules``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-identitypoolroleattachment-rulesconfigurationtype.html#cfn-cognito-identitypoolroleattachment-rulesconfigurationtype-rules
            """
            return self._values.get('rules')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'RulesConfigurationTypeProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())



@jsii.data_type(jsii_type="@aws-cdk/aws-cognito.CfnIdentityPoolRoleAttachmentProps", jsii_struct_bases=[], name_mapping={'identity_pool_id': 'identityPoolId', 'role_mappings': 'roleMappings', 'roles': 'roles'})
class CfnIdentityPoolRoleAttachmentProps():
    def __init__(self, *, identity_pool_id: str, role_mappings: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.Mapping[str, typing.Union[aws_cdk.core.IResolvable, "CfnIdentityPoolRoleAttachment.RoleMappingProperty"]]]]]=None, roles: typing.Any=None) -> None:
        """Properties for defining a ``AWS::Cognito::IdentityPoolRoleAttachment``.

        :param identity_pool_id: ``AWS::Cognito::IdentityPoolRoleAttachment.IdentityPoolId``.
        :param role_mappings: ``AWS::Cognito::IdentityPoolRoleAttachment.RoleMappings``.
        :param roles: ``AWS::Cognito::IdentityPoolRoleAttachment.Roles``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-identitypoolroleattachment.html
        """
        self._values = {
            'identity_pool_id': identity_pool_id,
        }
        if role_mappings is not None: self._values["role_mappings"] = role_mappings
        if roles is not None: self._values["roles"] = roles

    @builtins.property
    def identity_pool_id(self) -> str:
        """``AWS::Cognito::IdentityPoolRoleAttachment.IdentityPoolId``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-identitypoolroleattachment.html#cfn-cognito-identitypoolroleattachment-identitypoolid
        """
        return self._values.get('identity_pool_id')

    @builtins.property
    def role_mappings(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.Mapping[str, typing.Union[aws_cdk.core.IResolvable, "CfnIdentityPoolRoleAttachment.RoleMappingProperty"]]]]]:
        """``AWS::Cognito::IdentityPoolRoleAttachment.RoleMappings``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-identitypoolroleattachment.html#cfn-cognito-identitypoolroleattachment-rolemappings
        """
        return self._values.get('role_mappings')

    @builtins.property
    def roles(self) -> typing.Any:
        """``AWS::Cognito::IdentityPoolRoleAttachment.Roles``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-identitypoolroleattachment.html#cfn-cognito-identitypoolroleattachment-roles
        """
        return self._values.get('roles')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'CfnIdentityPoolRoleAttachmentProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.implements(aws_cdk.core.IInspectable)
class CfnUserPool(aws_cdk.core.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-cognito.CfnUserPool"):
    """A CloudFormation ``AWS::Cognito::UserPool``.

    see
    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpool.html
    cloudformationResource:
    :cloudformationResource:: AWS::Cognito::UserPool
    """
    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, account_recovery_setting: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["AccountRecoverySettingProperty"]]]=None, admin_create_user_config: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["AdminCreateUserConfigProperty"]]]=None, alias_attributes: typing.Optional[typing.List[str]]=None, auto_verified_attributes: typing.Optional[typing.List[str]]=None, device_configuration: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["DeviceConfigurationProperty"]]]=None, email_configuration: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["EmailConfigurationProperty"]]]=None, email_verification_message: typing.Optional[str]=None, email_verification_subject: typing.Optional[str]=None, enabled_mfas: typing.Optional[typing.List[str]]=None, lambda_config: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["LambdaConfigProperty"]]]=None, mfa_configuration: typing.Optional[str]=None, policies: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["PoliciesProperty"]]]=None, schema: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union[aws_cdk.core.IResolvable, "SchemaAttributeProperty"]]]]]=None, sms_authentication_message: typing.Optional[str]=None, sms_configuration: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["SmsConfigurationProperty"]]]=None, sms_verification_message: typing.Optional[str]=None, username_attributes: typing.Optional[typing.List[str]]=None, username_configuration: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["UsernameConfigurationProperty"]]]=None, user_pool_add_ons: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["UserPoolAddOnsProperty"]]]=None, user_pool_name: typing.Optional[str]=None, user_pool_tags: typing.Any=None, verification_message_template: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["VerificationMessageTemplateProperty"]]]=None) -> None:
        """Create a new ``AWS::Cognito::UserPool``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param account_recovery_setting: ``AWS::Cognito::UserPool.AccountRecoverySetting``.
        :param admin_create_user_config: ``AWS::Cognito::UserPool.AdminCreateUserConfig``.
        :param alias_attributes: ``AWS::Cognito::UserPool.AliasAttributes``.
        :param auto_verified_attributes: ``AWS::Cognito::UserPool.AutoVerifiedAttributes``.
        :param device_configuration: ``AWS::Cognito::UserPool.DeviceConfiguration``.
        :param email_configuration: ``AWS::Cognito::UserPool.EmailConfiguration``.
        :param email_verification_message: ``AWS::Cognito::UserPool.EmailVerificationMessage``.
        :param email_verification_subject: ``AWS::Cognito::UserPool.EmailVerificationSubject``.
        :param enabled_mfas: ``AWS::Cognito::UserPool.EnabledMfas``.
        :param lambda_config: ``AWS::Cognito::UserPool.LambdaConfig``.
        :param mfa_configuration: ``AWS::Cognito::UserPool.MfaConfiguration``.
        :param policies: ``AWS::Cognito::UserPool.Policies``.
        :param schema: ``AWS::Cognito::UserPool.Schema``.
        :param sms_authentication_message: ``AWS::Cognito::UserPool.SmsAuthenticationMessage``.
        :param sms_configuration: ``AWS::Cognito::UserPool.SmsConfiguration``.
        :param sms_verification_message: ``AWS::Cognito::UserPool.SmsVerificationMessage``.
        :param username_attributes: ``AWS::Cognito::UserPool.UsernameAttributes``.
        :param username_configuration: ``AWS::Cognito::UserPool.UsernameConfiguration``.
        :param user_pool_add_ons: ``AWS::Cognito::UserPool.UserPoolAddOns``.
        :param user_pool_name: ``AWS::Cognito::UserPool.UserPoolName``.
        :param user_pool_tags: ``AWS::Cognito::UserPool.UserPoolTags``.
        :param verification_message_template: ``AWS::Cognito::UserPool.VerificationMessageTemplate``.
        """
        props = CfnUserPoolProps(account_recovery_setting=account_recovery_setting, admin_create_user_config=admin_create_user_config, alias_attributes=alias_attributes, auto_verified_attributes=auto_verified_attributes, device_configuration=device_configuration, email_configuration=email_configuration, email_verification_message=email_verification_message, email_verification_subject=email_verification_subject, enabled_mfas=enabled_mfas, lambda_config=lambda_config, mfa_configuration=mfa_configuration, policies=policies, schema=schema, sms_authentication_message=sms_authentication_message, sms_configuration=sms_configuration, sms_verification_message=sms_verification_message, username_attributes=username_attributes, username_configuration=username_configuration, user_pool_add_ons=user_pool_add_ons, user_pool_name=user_pool_name, user_pool_tags=user_pool_tags, verification_message_template=verification_message_template)

        jsii.create(CfnUserPool, self, [scope, id, props])

    @jsii.member(jsii_name="fromCloudFormation")
    @builtins.classmethod
    def from_cloud_formation(cls, scope: aws_cdk.core.Construct, id: str, resource_attributes: typing.Any, *, finder: aws_cdk.core.ICfnFinder) -> "CfnUserPool":
        """A factory method that creates a new instance of this class from an object containing the CloudFormation properties of this resource.

        Used in the @aws-cdk/cloudformation-include module.

        :param scope: -
        :param id: -
        :param resource_attributes: -
        :param finder: The finder interface used to resolve references across the template.

        stability
        :stability: experimental
        """
        options = aws_cdk.core.FromCloudFormationOptions(finder=finder)

        return jsii.sinvoke(cls, "fromCloudFormation", [scope, id, resource_attributes, options])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: aws_cdk.core.TreeInspector) -> None:
        """Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "inspect", [inspector])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, props: typing.Mapping[str, typing.Any]) -> typing.Mapping[str, typing.Any]:
        """
        :param props: -
        """
        return jsii.invoke(self, "renderProperties", [props])

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> str:
        """The CloudFormation resource type name for this resource class."""
        return jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME")

    @builtins.property
    @jsii.member(jsii_name="attrArn")
    def attr_arn(self) -> str:
        """
        cloudformationAttribute:
        :cloudformationAttribute:: Arn
        """
        return jsii.get(self, "attrArn")

    @builtins.property
    @jsii.member(jsii_name="attrProviderName")
    def attr_provider_name(self) -> str:
        """
        cloudformationAttribute:
        :cloudformationAttribute:: ProviderName
        """
        return jsii.get(self, "attrProviderName")

    @builtins.property
    @jsii.member(jsii_name="attrProviderUrl")
    def attr_provider_url(self) -> str:
        """
        cloudformationAttribute:
        :cloudformationAttribute:: ProviderURL
        """
        return jsii.get(self, "attrProviderUrl")

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[str, typing.Any]:
        return jsii.get(self, "cfnProperties")

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> aws_cdk.core.TagManager:
        """``AWS::Cognito::UserPool.UserPoolTags``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpool.html#cfn-cognito-userpool-userpooltags
        """
        return jsii.get(self, "tags")

    @builtins.property
    @jsii.member(jsii_name="accountRecoverySetting")
    def account_recovery_setting(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["AccountRecoverySettingProperty"]]]:
        """``AWS::Cognito::UserPool.AccountRecoverySetting``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpool.html#cfn-cognito-userpool-accountrecoverysetting
        """
        return jsii.get(self, "accountRecoverySetting")

    @account_recovery_setting.setter
    def account_recovery_setting(self, value: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["AccountRecoverySettingProperty"]]]):
        jsii.set(self, "accountRecoverySetting", value)

    @builtins.property
    @jsii.member(jsii_name="adminCreateUserConfig")
    def admin_create_user_config(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["AdminCreateUserConfigProperty"]]]:
        """``AWS::Cognito::UserPool.AdminCreateUserConfig``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpool.html#cfn-cognito-userpool-admincreateuserconfig
        """
        return jsii.get(self, "adminCreateUserConfig")

    @admin_create_user_config.setter
    def admin_create_user_config(self, value: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["AdminCreateUserConfigProperty"]]]):
        jsii.set(self, "adminCreateUserConfig", value)

    @builtins.property
    @jsii.member(jsii_name="aliasAttributes")
    def alias_attributes(self) -> typing.Optional[typing.List[str]]:
        """``AWS::Cognito::UserPool.AliasAttributes``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpool.html#cfn-cognito-userpool-aliasattributes
        """
        return jsii.get(self, "aliasAttributes")

    @alias_attributes.setter
    def alias_attributes(self, value: typing.Optional[typing.List[str]]):
        jsii.set(self, "aliasAttributes", value)

    @builtins.property
    @jsii.member(jsii_name="autoVerifiedAttributes")
    def auto_verified_attributes(self) -> typing.Optional[typing.List[str]]:
        """``AWS::Cognito::UserPool.AutoVerifiedAttributes``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpool.html#cfn-cognito-userpool-autoverifiedattributes
        """
        return jsii.get(self, "autoVerifiedAttributes")

    @auto_verified_attributes.setter
    def auto_verified_attributes(self, value: typing.Optional[typing.List[str]]):
        jsii.set(self, "autoVerifiedAttributes", value)

    @builtins.property
    @jsii.member(jsii_name="deviceConfiguration")
    def device_configuration(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["DeviceConfigurationProperty"]]]:
        """``AWS::Cognito::UserPool.DeviceConfiguration``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpool.html#cfn-cognito-userpool-deviceconfiguration
        """
        return jsii.get(self, "deviceConfiguration")

    @device_configuration.setter
    def device_configuration(self, value: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["DeviceConfigurationProperty"]]]):
        jsii.set(self, "deviceConfiguration", value)

    @builtins.property
    @jsii.member(jsii_name="emailConfiguration")
    def email_configuration(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["EmailConfigurationProperty"]]]:
        """``AWS::Cognito::UserPool.EmailConfiguration``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpool.html#cfn-cognito-userpool-emailconfiguration
        """
        return jsii.get(self, "emailConfiguration")

    @email_configuration.setter
    def email_configuration(self, value: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["EmailConfigurationProperty"]]]):
        jsii.set(self, "emailConfiguration", value)

    @builtins.property
    @jsii.member(jsii_name="emailVerificationMessage")
    def email_verification_message(self) -> typing.Optional[str]:
        """``AWS::Cognito::UserPool.EmailVerificationMessage``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpool.html#cfn-cognito-userpool-emailverificationmessage
        """
        return jsii.get(self, "emailVerificationMessage")

    @email_verification_message.setter
    def email_verification_message(self, value: typing.Optional[str]):
        jsii.set(self, "emailVerificationMessage", value)

    @builtins.property
    @jsii.member(jsii_name="emailVerificationSubject")
    def email_verification_subject(self) -> typing.Optional[str]:
        """``AWS::Cognito::UserPool.EmailVerificationSubject``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpool.html#cfn-cognito-userpool-emailverificationsubject
        """
        return jsii.get(self, "emailVerificationSubject")

    @email_verification_subject.setter
    def email_verification_subject(self, value: typing.Optional[str]):
        jsii.set(self, "emailVerificationSubject", value)

    @builtins.property
    @jsii.member(jsii_name="enabledMfas")
    def enabled_mfas(self) -> typing.Optional[typing.List[str]]:
        """``AWS::Cognito::UserPool.EnabledMfas``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpool.html#cfn-cognito-userpool-enabledmfas
        """
        return jsii.get(self, "enabledMfas")

    @enabled_mfas.setter
    def enabled_mfas(self, value: typing.Optional[typing.List[str]]):
        jsii.set(self, "enabledMfas", value)

    @builtins.property
    @jsii.member(jsii_name="lambdaConfig")
    def lambda_config(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["LambdaConfigProperty"]]]:
        """``AWS::Cognito::UserPool.LambdaConfig``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpool.html#cfn-cognito-userpool-lambdaconfig
        """
        return jsii.get(self, "lambdaConfig")

    @lambda_config.setter
    def lambda_config(self, value: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["LambdaConfigProperty"]]]):
        jsii.set(self, "lambdaConfig", value)

    @builtins.property
    @jsii.member(jsii_name="mfaConfiguration")
    def mfa_configuration(self) -> typing.Optional[str]:
        """``AWS::Cognito::UserPool.MfaConfiguration``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpool.html#cfn-cognito-userpool-mfaconfiguration
        """
        return jsii.get(self, "mfaConfiguration")

    @mfa_configuration.setter
    def mfa_configuration(self, value: typing.Optional[str]):
        jsii.set(self, "mfaConfiguration", value)

    @builtins.property
    @jsii.member(jsii_name="policies")
    def policies(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["PoliciesProperty"]]]:
        """``AWS::Cognito::UserPool.Policies``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpool.html#cfn-cognito-userpool-policies
        """
        return jsii.get(self, "policies")

    @policies.setter
    def policies(self, value: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["PoliciesProperty"]]]):
        jsii.set(self, "policies", value)

    @builtins.property
    @jsii.member(jsii_name="schema")
    def schema(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union[aws_cdk.core.IResolvable, "SchemaAttributeProperty"]]]]]:
        """``AWS::Cognito::UserPool.Schema``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpool.html#cfn-cognito-userpool-schema
        """
        return jsii.get(self, "schema")

    @schema.setter
    def schema(self, value: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union[aws_cdk.core.IResolvable, "SchemaAttributeProperty"]]]]]):
        jsii.set(self, "schema", value)

    @builtins.property
    @jsii.member(jsii_name="smsAuthenticationMessage")
    def sms_authentication_message(self) -> typing.Optional[str]:
        """``AWS::Cognito::UserPool.SmsAuthenticationMessage``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpool.html#cfn-cognito-userpool-smsauthenticationmessage
        """
        return jsii.get(self, "smsAuthenticationMessage")

    @sms_authentication_message.setter
    def sms_authentication_message(self, value: typing.Optional[str]):
        jsii.set(self, "smsAuthenticationMessage", value)

    @builtins.property
    @jsii.member(jsii_name="smsConfiguration")
    def sms_configuration(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["SmsConfigurationProperty"]]]:
        """``AWS::Cognito::UserPool.SmsConfiguration``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpool.html#cfn-cognito-userpool-smsconfiguration
        """
        return jsii.get(self, "smsConfiguration")

    @sms_configuration.setter
    def sms_configuration(self, value: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["SmsConfigurationProperty"]]]):
        jsii.set(self, "smsConfiguration", value)

    @builtins.property
    @jsii.member(jsii_name="smsVerificationMessage")
    def sms_verification_message(self) -> typing.Optional[str]:
        """``AWS::Cognito::UserPool.SmsVerificationMessage``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpool.html#cfn-cognito-userpool-smsverificationmessage
        """
        return jsii.get(self, "smsVerificationMessage")

    @sms_verification_message.setter
    def sms_verification_message(self, value: typing.Optional[str]):
        jsii.set(self, "smsVerificationMessage", value)

    @builtins.property
    @jsii.member(jsii_name="usernameAttributes")
    def username_attributes(self) -> typing.Optional[typing.List[str]]:
        """``AWS::Cognito::UserPool.UsernameAttributes``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpool.html#cfn-cognito-userpool-usernameattributes
        """
        return jsii.get(self, "usernameAttributes")

    @username_attributes.setter
    def username_attributes(self, value: typing.Optional[typing.List[str]]):
        jsii.set(self, "usernameAttributes", value)

    @builtins.property
    @jsii.member(jsii_name="usernameConfiguration")
    def username_configuration(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["UsernameConfigurationProperty"]]]:
        """``AWS::Cognito::UserPool.UsernameConfiguration``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpool.html#cfn-cognito-userpool-usernameconfiguration
        """
        return jsii.get(self, "usernameConfiguration")

    @username_configuration.setter
    def username_configuration(self, value: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["UsernameConfigurationProperty"]]]):
        jsii.set(self, "usernameConfiguration", value)

    @builtins.property
    @jsii.member(jsii_name="userPoolAddOns")
    def user_pool_add_ons(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["UserPoolAddOnsProperty"]]]:
        """``AWS::Cognito::UserPool.UserPoolAddOns``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpool.html#cfn-cognito-userpool-userpooladdons
        """
        return jsii.get(self, "userPoolAddOns")

    @user_pool_add_ons.setter
    def user_pool_add_ons(self, value: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["UserPoolAddOnsProperty"]]]):
        jsii.set(self, "userPoolAddOns", value)

    @builtins.property
    @jsii.member(jsii_name="userPoolName")
    def user_pool_name(self) -> typing.Optional[str]:
        """``AWS::Cognito::UserPool.UserPoolName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpool.html#cfn-cognito-userpool-userpoolname
        """
        return jsii.get(self, "userPoolName")

    @user_pool_name.setter
    def user_pool_name(self, value: typing.Optional[str]):
        jsii.set(self, "userPoolName", value)

    @builtins.property
    @jsii.member(jsii_name="verificationMessageTemplate")
    def verification_message_template(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["VerificationMessageTemplateProperty"]]]:
        """``AWS::Cognito::UserPool.VerificationMessageTemplate``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpool.html#cfn-cognito-userpool-verificationmessagetemplate
        """
        return jsii.get(self, "verificationMessageTemplate")

    @verification_message_template.setter
    def verification_message_template(self, value: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["VerificationMessageTemplateProperty"]]]):
        jsii.set(self, "verificationMessageTemplate", value)

    @jsii.data_type(jsii_type="@aws-cdk/aws-cognito.CfnUserPool.AccountRecoverySettingProperty", jsii_struct_bases=[], name_mapping={'recovery_mechanisms': 'recoveryMechanisms'})
    class AccountRecoverySettingProperty():
        def __init__(self, *, recovery_mechanisms: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnUserPool.RecoveryOptionProperty"]]]]]=None) -> None:
            """
            :param recovery_mechanisms: ``CfnUserPool.AccountRecoverySettingProperty.RecoveryMechanisms``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-userpool-accountrecoverysetting.html
            """
            self._values = {
            }
            if recovery_mechanisms is not None: self._values["recovery_mechanisms"] = recovery_mechanisms

        @builtins.property
        def recovery_mechanisms(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnUserPool.RecoveryOptionProperty"]]]]]:
            """``CfnUserPool.AccountRecoverySettingProperty.RecoveryMechanisms``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-userpool-accountrecoverysetting.html#cfn-cognito-userpool-accountrecoverysetting-recoverymechanisms
            """
            return self._values.get('recovery_mechanisms')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'AccountRecoverySettingProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="@aws-cdk/aws-cognito.CfnUserPool.AdminCreateUserConfigProperty", jsii_struct_bases=[], name_mapping={'allow_admin_create_user_only': 'allowAdminCreateUserOnly', 'invite_message_template': 'inviteMessageTemplate', 'unused_account_validity_days': 'unusedAccountValidityDays'})
    class AdminCreateUserConfigProperty():
        def __init__(self, *, allow_admin_create_user_only: typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.core.IResolvable]]]=None, invite_message_template: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["CfnUserPool.InviteMessageTemplateProperty"]]]=None, unused_account_validity_days: typing.Optional[jsii.Number]=None) -> None:
            """
            :param allow_admin_create_user_only: ``CfnUserPool.AdminCreateUserConfigProperty.AllowAdminCreateUserOnly``.
            :param invite_message_template: ``CfnUserPool.AdminCreateUserConfigProperty.InviteMessageTemplate``.
            :param unused_account_validity_days: ``CfnUserPool.AdminCreateUserConfigProperty.UnusedAccountValidityDays``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-userpool-admincreateuserconfig.html
            """
            self._values = {
            }
            if allow_admin_create_user_only is not None: self._values["allow_admin_create_user_only"] = allow_admin_create_user_only
            if invite_message_template is not None: self._values["invite_message_template"] = invite_message_template
            if unused_account_validity_days is not None: self._values["unused_account_validity_days"] = unused_account_validity_days

        @builtins.property
        def allow_admin_create_user_only(self) -> typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.core.IResolvable]]]:
            """``CfnUserPool.AdminCreateUserConfigProperty.AllowAdminCreateUserOnly``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-userpool-admincreateuserconfig.html#cfn-cognito-userpool-admincreateuserconfig-allowadmincreateuseronly
            """
            return self._values.get('allow_admin_create_user_only')

        @builtins.property
        def invite_message_template(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["CfnUserPool.InviteMessageTemplateProperty"]]]:
            """``CfnUserPool.AdminCreateUserConfigProperty.InviteMessageTemplate``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-userpool-admincreateuserconfig.html#cfn-cognito-userpool-admincreateuserconfig-invitemessagetemplate
            """
            return self._values.get('invite_message_template')

        @builtins.property
        def unused_account_validity_days(self) -> typing.Optional[jsii.Number]:
            """``CfnUserPool.AdminCreateUserConfigProperty.UnusedAccountValidityDays``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-userpool-admincreateuserconfig.html#cfn-cognito-userpool-admincreateuserconfig-unusedaccountvaliditydays
            """
            return self._values.get('unused_account_validity_days')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'AdminCreateUserConfigProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="@aws-cdk/aws-cognito.CfnUserPool.DeviceConfigurationProperty", jsii_struct_bases=[], name_mapping={'challenge_required_on_new_device': 'challengeRequiredOnNewDevice', 'device_only_remembered_on_user_prompt': 'deviceOnlyRememberedOnUserPrompt'})
    class DeviceConfigurationProperty():
        def __init__(self, *, challenge_required_on_new_device: typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.core.IResolvable]]]=None, device_only_remembered_on_user_prompt: typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.core.IResolvable]]]=None) -> None:
            """
            :param challenge_required_on_new_device: ``CfnUserPool.DeviceConfigurationProperty.ChallengeRequiredOnNewDevice``.
            :param device_only_remembered_on_user_prompt: ``CfnUserPool.DeviceConfigurationProperty.DeviceOnlyRememberedOnUserPrompt``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-userpool-deviceconfiguration.html
            """
            self._values = {
            }
            if challenge_required_on_new_device is not None: self._values["challenge_required_on_new_device"] = challenge_required_on_new_device
            if device_only_remembered_on_user_prompt is not None: self._values["device_only_remembered_on_user_prompt"] = device_only_remembered_on_user_prompt

        @builtins.property
        def challenge_required_on_new_device(self) -> typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.core.IResolvable]]]:
            """``CfnUserPool.DeviceConfigurationProperty.ChallengeRequiredOnNewDevice``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-userpool-deviceconfiguration.html#cfn-cognito-userpool-deviceconfiguration-challengerequiredonnewdevice
            """
            return self._values.get('challenge_required_on_new_device')

        @builtins.property
        def device_only_remembered_on_user_prompt(self) -> typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.core.IResolvable]]]:
            """``CfnUserPool.DeviceConfigurationProperty.DeviceOnlyRememberedOnUserPrompt``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-userpool-deviceconfiguration.html#cfn-cognito-userpool-deviceconfiguration-deviceonlyrememberedonuserprompt
            """
            return self._values.get('device_only_remembered_on_user_prompt')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'DeviceConfigurationProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="@aws-cdk/aws-cognito.CfnUserPool.EmailConfigurationProperty", jsii_struct_bases=[], name_mapping={'configuration_set': 'configurationSet', 'email_sending_account': 'emailSendingAccount', 'from_': 'from', 'reply_to_email_address': 'replyToEmailAddress', 'source_arn': 'sourceArn'})
    class EmailConfigurationProperty():
        def __init__(self, *, configuration_set: typing.Optional[str]=None, email_sending_account: typing.Optional[str]=None, from_: typing.Optional[str]=None, reply_to_email_address: typing.Optional[str]=None, source_arn: typing.Optional[str]=None) -> None:
            """
            :param configuration_set: ``CfnUserPool.EmailConfigurationProperty.ConfigurationSet``.
            :param email_sending_account: ``CfnUserPool.EmailConfigurationProperty.EmailSendingAccount``.
            :param from_: ``CfnUserPool.EmailConfigurationProperty.From``.
            :param reply_to_email_address: ``CfnUserPool.EmailConfigurationProperty.ReplyToEmailAddress``.
            :param source_arn: ``CfnUserPool.EmailConfigurationProperty.SourceArn``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-userpool-emailconfiguration.html
            """
            self._values = {
            }
            if configuration_set is not None: self._values["configuration_set"] = configuration_set
            if email_sending_account is not None: self._values["email_sending_account"] = email_sending_account
            if from_ is not None: self._values["from_"] = from_
            if reply_to_email_address is not None: self._values["reply_to_email_address"] = reply_to_email_address
            if source_arn is not None: self._values["source_arn"] = source_arn

        @builtins.property
        def configuration_set(self) -> typing.Optional[str]:
            """``CfnUserPool.EmailConfigurationProperty.ConfigurationSet``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-userpool-emailconfiguration.html#cfn-cognito-userpool-emailconfiguration-configurationset
            """
            return self._values.get('configuration_set')

        @builtins.property
        def email_sending_account(self) -> typing.Optional[str]:
            """``CfnUserPool.EmailConfigurationProperty.EmailSendingAccount``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-userpool-emailconfiguration.html#cfn-cognito-userpool-emailconfiguration-emailsendingaccount
            """
            return self._values.get('email_sending_account')

        @builtins.property
        def from_(self) -> typing.Optional[str]:
            """``CfnUserPool.EmailConfigurationProperty.From``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-userpool-emailconfiguration.html#cfn-cognito-userpool-emailconfiguration-from
            """
            return self._values.get('from_')

        @builtins.property
        def reply_to_email_address(self) -> typing.Optional[str]:
            """``CfnUserPool.EmailConfigurationProperty.ReplyToEmailAddress``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-userpool-emailconfiguration.html#cfn-cognito-userpool-emailconfiguration-replytoemailaddress
            """
            return self._values.get('reply_to_email_address')

        @builtins.property
        def source_arn(self) -> typing.Optional[str]:
            """``CfnUserPool.EmailConfigurationProperty.SourceArn``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-userpool-emailconfiguration.html#cfn-cognito-userpool-emailconfiguration-sourcearn
            """
            return self._values.get('source_arn')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'EmailConfigurationProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="@aws-cdk/aws-cognito.CfnUserPool.InviteMessageTemplateProperty", jsii_struct_bases=[], name_mapping={'email_message': 'emailMessage', 'email_subject': 'emailSubject', 'sms_message': 'smsMessage'})
    class InviteMessageTemplateProperty():
        def __init__(self, *, email_message: typing.Optional[str]=None, email_subject: typing.Optional[str]=None, sms_message: typing.Optional[str]=None) -> None:
            """
            :param email_message: ``CfnUserPool.InviteMessageTemplateProperty.EmailMessage``.
            :param email_subject: ``CfnUserPool.InviteMessageTemplateProperty.EmailSubject``.
            :param sms_message: ``CfnUserPool.InviteMessageTemplateProperty.SMSMessage``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-userpool-invitemessagetemplate.html
            """
            self._values = {
            }
            if email_message is not None: self._values["email_message"] = email_message
            if email_subject is not None: self._values["email_subject"] = email_subject
            if sms_message is not None: self._values["sms_message"] = sms_message

        @builtins.property
        def email_message(self) -> typing.Optional[str]:
            """``CfnUserPool.InviteMessageTemplateProperty.EmailMessage``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-userpool-invitemessagetemplate.html#cfn-cognito-userpool-invitemessagetemplate-emailmessage
            """
            return self._values.get('email_message')

        @builtins.property
        def email_subject(self) -> typing.Optional[str]:
            """``CfnUserPool.InviteMessageTemplateProperty.EmailSubject``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-userpool-invitemessagetemplate.html#cfn-cognito-userpool-invitemessagetemplate-emailsubject
            """
            return self._values.get('email_subject')

        @builtins.property
        def sms_message(self) -> typing.Optional[str]:
            """``CfnUserPool.InviteMessageTemplateProperty.SMSMessage``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-userpool-invitemessagetemplate.html#cfn-cognito-userpool-invitemessagetemplate-smsmessage
            """
            return self._values.get('sms_message')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'InviteMessageTemplateProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="@aws-cdk/aws-cognito.CfnUserPool.LambdaConfigProperty", jsii_struct_bases=[], name_mapping={'create_auth_challenge': 'createAuthChallenge', 'custom_message': 'customMessage', 'define_auth_challenge': 'defineAuthChallenge', 'post_authentication': 'postAuthentication', 'post_confirmation': 'postConfirmation', 'pre_authentication': 'preAuthentication', 'pre_sign_up': 'preSignUp', 'pre_token_generation': 'preTokenGeneration', 'user_migration': 'userMigration', 'verify_auth_challenge_response': 'verifyAuthChallengeResponse'})
    class LambdaConfigProperty():
        def __init__(self, *, create_auth_challenge: typing.Optional[str]=None, custom_message: typing.Optional[str]=None, define_auth_challenge: typing.Optional[str]=None, post_authentication: typing.Optional[str]=None, post_confirmation: typing.Optional[str]=None, pre_authentication: typing.Optional[str]=None, pre_sign_up: typing.Optional[str]=None, pre_token_generation: typing.Optional[str]=None, user_migration: typing.Optional[str]=None, verify_auth_challenge_response: typing.Optional[str]=None) -> None:
            """
            :param create_auth_challenge: ``CfnUserPool.LambdaConfigProperty.CreateAuthChallenge``.
            :param custom_message: ``CfnUserPool.LambdaConfigProperty.CustomMessage``.
            :param define_auth_challenge: ``CfnUserPool.LambdaConfigProperty.DefineAuthChallenge``.
            :param post_authentication: ``CfnUserPool.LambdaConfigProperty.PostAuthentication``.
            :param post_confirmation: ``CfnUserPool.LambdaConfigProperty.PostConfirmation``.
            :param pre_authentication: ``CfnUserPool.LambdaConfigProperty.PreAuthentication``.
            :param pre_sign_up: ``CfnUserPool.LambdaConfigProperty.PreSignUp``.
            :param pre_token_generation: ``CfnUserPool.LambdaConfigProperty.PreTokenGeneration``.
            :param user_migration: ``CfnUserPool.LambdaConfigProperty.UserMigration``.
            :param verify_auth_challenge_response: ``CfnUserPool.LambdaConfigProperty.VerifyAuthChallengeResponse``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-userpool-lambdaconfig.html
            """
            self._values = {
            }
            if create_auth_challenge is not None: self._values["create_auth_challenge"] = create_auth_challenge
            if custom_message is not None: self._values["custom_message"] = custom_message
            if define_auth_challenge is not None: self._values["define_auth_challenge"] = define_auth_challenge
            if post_authentication is not None: self._values["post_authentication"] = post_authentication
            if post_confirmation is not None: self._values["post_confirmation"] = post_confirmation
            if pre_authentication is not None: self._values["pre_authentication"] = pre_authentication
            if pre_sign_up is not None: self._values["pre_sign_up"] = pre_sign_up
            if pre_token_generation is not None: self._values["pre_token_generation"] = pre_token_generation
            if user_migration is not None: self._values["user_migration"] = user_migration
            if verify_auth_challenge_response is not None: self._values["verify_auth_challenge_response"] = verify_auth_challenge_response

        @builtins.property
        def create_auth_challenge(self) -> typing.Optional[str]:
            """``CfnUserPool.LambdaConfigProperty.CreateAuthChallenge``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-userpool-lambdaconfig.html#cfn-cognito-userpool-lambdaconfig-createauthchallenge
            """
            return self._values.get('create_auth_challenge')

        @builtins.property
        def custom_message(self) -> typing.Optional[str]:
            """``CfnUserPool.LambdaConfigProperty.CustomMessage``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-userpool-lambdaconfig.html#cfn-cognito-userpool-lambdaconfig-custommessage
            """
            return self._values.get('custom_message')

        @builtins.property
        def define_auth_challenge(self) -> typing.Optional[str]:
            """``CfnUserPool.LambdaConfigProperty.DefineAuthChallenge``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-userpool-lambdaconfig.html#cfn-cognito-userpool-lambdaconfig-defineauthchallenge
            """
            return self._values.get('define_auth_challenge')

        @builtins.property
        def post_authentication(self) -> typing.Optional[str]:
            """``CfnUserPool.LambdaConfigProperty.PostAuthentication``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-userpool-lambdaconfig.html#cfn-cognito-userpool-lambdaconfig-postauthentication
            """
            return self._values.get('post_authentication')

        @builtins.property
        def post_confirmation(self) -> typing.Optional[str]:
            """``CfnUserPool.LambdaConfigProperty.PostConfirmation``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-userpool-lambdaconfig.html#cfn-cognito-userpool-lambdaconfig-postconfirmation
            """
            return self._values.get('post_confirmation')

        @builtins.property
        def pre_authentication(self) -> typing.Optional[str]:
            """``CfnUserPool.LambdaConfigProperty.PreAuthentication``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-userpool-lambdaconfig.html#cfn-cognito-userpool-lambdaconfig-preauthentication
            """
            return self._values.get('pre_authentication')

        @builtins.property
        def pre_sign_up(self) -> typing.Optional[str]:
            """``CfnUserPool.LambdaConfigProperty.PreSignUp``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-userpool-lambdaconfig.html#cfn-cognito-userpool-lambdaconfig-presignup
            """
            return self._values.get('pre_sign_up')

        @builtins.property
        def pre_token_generation(self) -> typing.Optional[str]:
            """``CfnUserPool.LambdaConfigProperty.PreTokenGeneration``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-userpool-lambdaconfig.html#cfn-cognito-userpool-lambdaconfig-pretokengeneration
            """
            return self._values.get('pre_token_generation')

        @builtins.property
        def user_migration(self) -> typing.Optional[str]:
            """``CfnUserPool.LambdaConfigProperty.UserMigration``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-userpool-lambdaconfig.html#cfn-cognito-userpool-lambdaconfig-usermigration
            """
            return self._values.get('user_migration')

        @builtins.property
        def verify_auth_challenge_response(self) -> typing.Optional[str]:
            """``CfnUserPool.LambdaConfigProperty.VerifyAuthChallengeResponse``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-userpool-lambdaconfig.html#cfn-cognito-userpool-lambdaconfig-verifyauthchallengeresponse
            """
            return self._values.get('verify_auth_challenge_response')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'LambdaConfigProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="@aws-cdk/aws-cognito.CfnUserPool.NumberAttributeConstraintsProperty", jsii_struct_bases=[], name_mapping={'max_value': 'maxValue', 'min_value': 'minValue'})
    class NumberAttributeConstraintsProperty():
        def __init__(self, *, max_value: typing.Optional[str]=None, min_value: typing.Optional[str]=None) -> None:
            """
            :param max_value: ``CfnUserPool.NumberAttributeConstraintsProperty.MaxValue``.
            :param min_value: ``CfnUserPool.NumberAttributeConstraintsProperty.MinValue``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-userpool-numberattributeconstraints.html
            """
            self._values = {
            }
            if max_value is not None: self._values["max_value"] = max_value
            if min_value is not None: self._values["min_value"] = min_value

        @builtins.property
        def max_value(self) -> typing.Optional[str]:
            """``CfnUserPool.NumberAttributeConstraintsProperty.MaxValue``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-userpool-numberattributeconstraints.html#cfn-cognito-userpool-numberattributeconstraints-maxvalue
            """
            return self._values.get('max_value')

        @builtins.property
        def min_value(self) -> typing.Optional[str]:
            """``CfnUserPool.NumberAttributeConstraintsProperty.MinValue``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-userpool-numberattributeconstraints.html#cfn-cognito-userpool-numberattributeconstraints-minvalue
            """
            return self._values.get('min_value')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'NumberAttributeConstraintsProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="@aws-cdk/aws-cognito.CfnUserPool.PasswordPolicyProperty", jsii_struct_bases=[], name_mapping={'minimum_length': 'minimumLength', 'require_lowercase': 'requireLowercase', 'require_numbers': 'requireNumbers', 'require_symbols': 'requireSymbols', 'require_uppercase': 'requireUppercase', 'temporary_password_validity_days': 'temporaryPasswordValidityDays'})
    class PasswordPolicyProperty():
        def __init__(self, *, minimum_length: typing.Optional[jsii.Number]=None, require_lowercase: typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.core.IResolvable]]]=None, require_numbers: typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.core.IResolvable]]]=None, require_symbols: typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.core.IResolvable]]]=None, require_uppercase: typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.core.IResolvable]]]=None, temporary_password_validity_days: typing.Optional[jsii.Number]=None) -> None:
            """
            :param minimum_length: ``CfnUserPool.PasswordPolicyProperty.MinimumLength``.
            :param require_lowercase: ``CfnUserPool.PasswordPolicyProperty.RequireLowercase``.
            :param require_numbers: ``CfnUserPool.PasswordPolicyProperty.RequireNumbers``.
            :param require_symbols: ``CfnUserPool.PasswordPolicyProperty.RequireSymbols``.
            :param require_uppercase: ``CfnUserPool.PasswordPolicyProperty.RequireUppercase``.
            :param temporary_password_validity_days: ``CfnUserPool.PasswordPolicyProperty.TemporaryPasswordValidityDays``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-userpool-passwordpolicy.html
            """
            self._values = {
            }
            if minimum_length is not None: self._values["minimum_length"] = minimum_length
            if require_lowercase is not None: self._values["require_lowercase"] = require_lowercase
            if require_numbers is not None: self._values["require_numbers"] = require_numbers
            if require_symbols is not None: self._values["require_symbols"] = require_symbols
            if require_uppercase is not None: self._values["require_uppercase"] = require_uppercase
            if temporary_password_validity_days is not None: self._values["temporary_password_validity_days"] = temporary_password_validity_days

        @builtins.property
        def minimum_length(self) -> typing.Optional[jsii.Number]:
            """``CfnUserPool.PasswordPolicyProperty.MinimumLength``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-userpool-passwordpolicy.html#cfn-cognito-userpool-passwordpolicy-minimumlength
            """
            return self._values.get('minimum_length')

        @builtins.property
        def require_lowercase(self) -> typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.core.IResolvable]]]:
            """``CfnUserPool.PasswordPolicyProperty.RequireLowercase``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-userpool-passwordpolicy.html#cfn-cognito-userpool-passwordpolicy-requirelowercase
            """
            return self._values.get('require_lowercase')

        @builtins.property
        def require_numbers(self) -> typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.core.IResolvable]]]:
            """``CfnUserPool.PasswordPolicyProperty.RequireNumbers``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-userpool-passwordpolicy.html#cfn-cognito-userpool-passwordpolicy-requirenumbers
            """
            return self._values.get('require_numbers')

        @builtins.property
        def require_symbols(self) -> typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.core.IResolvable]]]:
            """``CfnUserPool.PasswordPolicyProperty.RequireSymbols``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-userpool-passwordpolicy.html#cfn-cognito-userpool-passwordpolicy-requiresymbols
            """
            return self._values.get('require_symbols')

        @builtins.property
        def require_uppercase(self) -> typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.core.IResolvable]]]:
            """``CfnUserPool.PasswordPolicyProperty.RequireUppercase``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-userpool-passwordpolicy.html#cfn-cognito-userpool-passwordpolicy-requireuppercase
            """
            return self._values.get('require_uppercase')

        @builtins.property
        def temporary_password_validity_days(self) -> typing.Optional[jsii.Number]:
            """``CfnUserPool.PasswordPolicyProperty.TemporaryPasswordValidityDays``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-userpool-passwordpolicy.html#cfn-cognito-userpool-passwordpolicy-temporarypasswordvaliditydays
            """
            return self._values.get('temporary_password_validity_days')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'PasswordPolicyProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="@aws-cdk/aws-cognito.CfnUserPool.PoliciesProperty", jsii_struct_bases=[], name_mapping={'password_policy': 'passwordPolicy'})
    class PoliciesProperty():
        def __init__(self, *, password_policy: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["CfnUserPool.PasswordPolicyProperty"]]]=None) -> None:
            """
            :param password_policy: ``CfnUserPool.PoliciesProperty.PasswordPolicy``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-userpool-policies.html
            """
            self._values = {
            }
            if password_policy is not None: self._values["password_policy"] = password_policy

        @builtins.property
        def password_policy(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["CfnUserPool.PasswordPolicyProperty"]]]:
            """``CfnUserPool.PoliciesProperty.PasswordPolicy``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-userpool-policies.html#cfn-cognito-userpool-policies-passwordpolicy
            """
            return self._values.get('password_policy')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'PoliciesProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="@aws-cdk/aws-cognito.CfnUserPool.RecoveryOptionProperty", jsii_struct_bases=[], name_mapping={'name': 'name', 'priority': 'priority'})
    class RecoveryOptionProperty():
        def __init__(self, *, name: typing.Optional[str]=None, priority: typing.Optional[jsii.Number]=None) -> None:
            """
            :param name: ``CfnUserPool.RecoveryOptionProperty.Name``.
            :param priority: ``CfnUserPool.RecoveryOptionProperty.Priority``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-userpool-recoveryoption.html
            """
            self._values = {
            }
            if name is not None: self._values["name"] = name
            if priority is not None: self._values["priority"] = priority

        @builtins.property
        def name(self) -> typing.Optional[str]:
            """``CfnUserPool.RecoveryOptionProperty.Name``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-userpool-recoveryoption.html#cfn-cognito-userpool-recoveryoption-name
            """
            return self._values.get('name')

        @builtins.property
        def priority(self) -> typing.Optional[jsii.Number]:
            """``CfnUserPool.RecoveryOptionProperty.Priority``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-userpool-recoveryoption.html#cfn-cognito-userpool-recoveryoption-priority
            """
            return self._values.get('priority')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'RecoveryOptionProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="@aws-cdk/aws-cognito.CfnUserPool.SchemaAttributeProperty", jsii_struct_bases=[], name_mapping={'attribute_data_type': 'attributeDataType', 'developer_only_attribute': 'developerOnlyAttribute', 'mutable': 'mutable', 'name': 'name', 'number_attribute_constraints': 'numberAttributeConstraints', 'required': 'required', 'string_attribute_constraints': 'stringAttributeConstraints'})
    class SchemaAttributeProperty():
        def __init__(self, *, attribute_data_type: typing.Optional[str]=None, developer_only_attribute: typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.core.IResolvable]]]=None, mutable: typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.core.IResolvable]]]=None, name: typing.Optional[str]=None, number_attribute_constraints: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["CfnUserPool.NumberAttributeConstraintsProperty"]]]=None, required: typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.core.IResolvable]]]=None, string_attribute_constraints: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["CfnUserPool.StringAttributeConstraintsProperty"]]]=None) -> None:
            """
            :param attribute_data_type: ``CfnUserPool.SchemaAttributeProperty.AttributeDataType``.
            :param developer_only_attribute: ``CfnUserPool.SchemaAttributeProperty.DeveloperOnlyAttribute``.
            :param mutable: ``CfnUserPool.SchemaAttributeProperty.Mutable``.
            :param name: ``CfnUserPool.SchemaAttributeProperty.Name``.
            :param number_attribute_constraints: ``CfnUserPool.SchemaAttributeProperty.NumberAttributeConstraints``.
            :param required: ``CfnUserPool.SchemaAttributeProperty.Required``.
            :param string_attribute_constraints: ``CfnUserPool.SchemaAttributeProperty.StringAttributeConstraints``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-userpool-schemaattribute.html
            """
            self._values = {
            }
            if attribute_data_type is not None: self._values["attribute_data_type"] = attribute_data_type
            if developer_only_attribute is not None: self._values["developer_only_attribute"] = developer_only_attribute
            if mutable is not None: self._values["mutable"] = mutable
            if name is not None: self._values["name"] = name
            if number_attribute_constraints is not None: self._values["number_attribute_constraints"] = number_attribute_constraints
            if required is not None: self._values["required"] = required
            if string_attribute_constraints is not None: self._values["string_attribute_constraints"] = string_attribute_constraints

        @builtins.property
        def attribute_data_type(self) -> typing.Optional[str]:
            """``CfnUserPool.SchemaAttributeProperty.AttributeDataType``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-userpool-schemaattribute.html#cfn-cognito-userpool-schemaattribute-attributedatatype
            """
            return self._values.get('attribute_data_type')

        @builtins.property
        def developer_only_attribute(self) -> typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.core.IResolvable]]]:
            """``CfnUserPool.SchemaAttributeProperty.DeveloperOnlyAttribute``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-userpool-schemaattribute.html#cfn-cognito-userpool-schemaattribute-developeronlyattribute
            """
            return self._values.get('developer_only_attribute')

        @builtins.property
        def mutable(self) -> typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.core.IResolvable]]]:
            """``CfnUserPool.SchemaAttributeProperty.Mutable``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-userpool-schemaattribute.html#cfn-cognito-userpool-schemaattribute-mutable
            """
            return self._values.get('mutable')

        @builtins.property
        def name(self) -> typing.Optional[str]:
            """``CfnUserPool.SchemaAttributeProperty.Name``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-userpool-schemaattribute.html#cfn-cognito-userpool-schemaattribute-name
            """
            return self._values.get('name')

        @builtins.property
        def number_attribute_constraints(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["CfnUserPool.NumberAttributeConstraintsProperty"]]]:
            """``CfnUserPool.SchemaAttributeProperty.NumberAttributeConstraints``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-userpool-schemaattribute.html#cfn-cognito-userpool-schemaattribute-numberattributeconstraints
            """
            return self._values.get('number_attribute_constraints')

        @builtins.property
        def required(self) -> typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.core.IResolvable]]]:
            """``CfnUserPool.SchemaAttributeProperty.Required``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-userpool-schemaattribute.html#cfn-cognito-userpool-schemaattribute-required
            """
            return self._values.get('required')

        @builtins.property
        def string_attribute_constraints(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["CfnUserPool.StringAttributeConstraintsProperty"]]]:
            """``CfnUserPool.SchemaAttributeProperty.StringAttributeConstraints``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-userpool-schemaattribute.html#cfn-cognito-userpool-schemaattribute-stringattributeconstraints
            """
            return self._values.get('string_attribute_constraints')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'SchemaAttributeProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="@aws-cdk/aws-cognito.CfnUserPool.SmsConfigurationProperty", jsii_struct_bases=[], name_mapping={'external_id': 'externalId', 'sns_caller_arn': 'snsCallerArn'})
    class SmsConfigurationProperty():
        def __init__(self, *, external_id: typing.Optional[str]=None, sns_caller_arn: typing.Optional[str]=None) -> None:
            """
            :param external_id: ``CfnUserPool.SmsConfigurationProperty.ExternalId``.
            :param sns_caller_arn: ``CfnUserPool.SmsConfigurationProperty.SnsCallerArn``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-userpool-smsconfiguration.html
            """
            self._values = {
            }
            if external_id is not None: self._values["external_id"] = external_id
            if sns_caller_arn is not None: self._values["sns_caller_arn"] = sns_caller_arn

        @builtins.property
        def external_id(self) -> typing.Optional[str]:
            """``CfnUserPool.SmsConfigurationProperty.ExternalId``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-userpool-smsconfiguration.html#cfn-cognito-userpool-smsconfiguration-externalid
            """
            return self._values.get('external_id')

        @builtins.property
        def sns_caller_arn(self) -> typing.Optional[str]:
            """``CfnUserPool.SmsConfigurationProperty.SnsCallerArn``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-userpool-smsconfiguration.html#cfn-cognito-userpool-smsconfiguration-snscallerarn
            """
            return self._values.get('sns_caller_arn')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'SmsConfigurationProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="@aws-cdk/aws-cognito.CfnUserPool.StringAttributeConstraintsProperty", jsii_struct_bases=[], name_mapping={'max_length': 'maxLength', 'min_length': 'minLength'})
    class StringAttributeConstraintsProperty():
        def __init__(self, *, max_length: typing.Optional[str]=None, min_length: typing.Optional[str]=None) -> None:
            """
            :param max_length: ``CfnUserPool.StringAttributeConstraintsProperty.MaxLength``.
            :param min_length: ``CfnUserPool.StringAttributeConstraintsProperty.MinLength``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-userpool-stringattributeconstraints.html
            """
            self._values = {
            }
            if max_length is not None: self._values["max_length"] = max_length
            if min_length is not None: self._values["min_length"] = min_length

        @builtins.property
        def max_length(self) -> typing.Optional[str]:
            """``CfnUserPool.StringAttributeConstraintsProperty.MaxLength``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-userpool-stringattributeconstraints.html#cfn-cognito-userpool-stringattributeconstraints-maxlength
            """
            return self._values.get('max_length')

        @builtins.property
        def min_length(self) -> typing.Optional[str]:
            """``CfnUserPool.StringAttributeConstraintsProperty.MinLength``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-userpool-stringattributeconstraints.html#cfn-cognito-userpool-stringattributeconstraints-minlength
            """
            return self._values.get('min_length')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'StringAttributeConstraintsProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="@aws-cdk/aws-cognito.CfnUserPool.UserPoolAddOnsProperty", jsii_struct_bases=[], name_mapping={'advanced_security_mode': 'advancedSecurityMode'})
    class UserPoolAddOnsProperty():
        def __init__(self, *, advanced_security_mode: typing.Optional[str]=None) -> None:
            """
            :param advanced_security_mode: ``CfnUserPool.UserPoolAddOnsProperty.AdvancedSecurityMode``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-userpool-userpooladdons.html
            """
            self._values = {
            }
            if advanced_security_mode is not None: self._values["advanced_security_mode"] = advanced_security_mode

        @builtins.property
        def advanced_security_mode(self) -> typing.Optional[str]:
            """``CfnUserPool.UserPoolAddOnsProperty.AdvancedSecurityMode``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-userpool-userpooladdons.html#cfn-cognito-userpool-userpooladdons-advancedsecuritymode
            """
            return self._values.get('advanced_security_mode')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'UserPoolAddOnsProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="@aws-cdk/aws-cognito.CfnUserPool.UsernameConfigurationProperty", jsii_struct_bases=[], name_mapping={'case_sensitive': 'caseSensitive'})
    class UsernameConfigurationProperty():
        def __init__(self, *, case_sensitive: typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.core.IResolvable]]]=None) -> None:
            """
            :param case_sensitive: ``CfnUserPool.UsernameConfigurationProperty.CaseSensitive``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-userpool-usernameconfiguration.html
            """
            self._values = {
            }
            if case_sensitive is not None: self._values["case_sensitive"] = case_sensitive

        @builtins.property
        def case_sensitive(self) -> typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.core.IResolvable]]]:
            """``CfnUserPool.UsernameConfigurationProperty.CaseSensitive``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-userpool-usernameconfiguration.html#cfn-cognito-userpool-usernameconfiguration-casesensitive
            """
            return self._values.get('case_sensitive')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'UsernameConfigurationProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="@aws-cdk/aws-cognito.CfnUserPool.VerificationMessageTemplateProperty", jsii_struct_bases=[], name_mapping={'default_email_option': 'defaultEmailOption', 'email_message': 'emailMessage', 'email_message_by_link': 'emailMessageByLink', 'email_subject': 'emailSubject', 'email_subject_by_link': 'emailSubjectByLink', 'sms_message': 'smsMessage'})
    class VerificationMessageTemplateProperty():
        def __init__(self, *, default_email_option: typing.Optional[str]=None, email_message: typing.Optional[str]=None, email_message_by_link: typing.Optional[str]=None, email_subject: typing.Optional[str]=None, email_subject_by_link: typing.Optional[str]=None, sms_message: typing.Optional[str]=None) -> None:
            """
            :param default_email_option: ``CfnUserPool.VerificationMessageTemplateProperty.DefaultEmailOption``.
            :param email_message: ``CfnUserPool.VerificationMessageTemplateProperty.EmailMessage``.
            :param email_message_by_link: ``CfnUserPool.VerificationMessageTemplateProperty.EmailMessageByLink``.
            :param email_subject: ``CfnUserPool.VerificationMessageTemplateProperty.EmailSubject``.
            :param email_subject_by_link: ``CfnUserPool.VerificationMessageTemplateProperty.EmailSubjectByLink``.
            :param sms_message: ``CfnUserPool.VerificationMessageTemplateProperty.SmsMessage``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-userpool-verificationmessagetemplate.html
            """
            self._values = {
            }
            if default_email_option is not None: self._values["default_email_option"] = default_email_option
            if email_message is not None: self._values["email_message"] = email_message
            if email_message_by_link is not None: self._values["email_message_by_link"] = email_message_by_link
            if email_subject is not None: self._values["email_subject"] = email_subject
            if email_subject_by_link is not None: self._values["email_subject_by_link"] = email_subject_by_link
            if sms_message is not None: self._values["sms_message"] = sms_message

        @builtins.property
        def default_email_option(self) -> typing.Optional[str]:
            """``CfnUserPool.VerificationMessageTemplateProperty.DefaultEmailOption``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-userpool-verificationmessagetemplate.html#cfn-cognito-userpool-verificationmessagetemplate-defaultemailoption
            """
            return self._values.get('default_email_option')

        @builtins.property
        def email_message(self) -> typing.Optional[str]:
            """``CfnUserPool.VerificationMessageTemplateProperty.EmailMessage``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-userpool-verificationmessagetemplate.html#cfn-cognito-userpool-verificationmessagetemplate-emailmessage
            """
            return self._values.get('email_message')

        @builtins.property
        def email_message_by_link(self) -> typing.Optional[str]:
            """``CfnUserPool.VerificationMessageTemplateProperty.EmailMessageByLink``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-userpool-verificationmessagetemplate.html#cfn-cognito-userpool-verificationmessagetemplate-emailmessagebylink
            """
            return self._values.get('email_message_by_link')

        @builtins.property
        def email_subject(self) -> typing.Optional[str]:
            """``CfnUserPool.VerificationMessageTemplateProperty.EmailSubject``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-userpool-verificationmessagetemplate.html#cfn-cognito-userpool-verificationmessagetemplate-emailsubject
            """
            return self._values.get('email_subject')

        @builtins.property
        def email_subject_by_link(self) -> typing.Optional[str]:
            """``CfnUserPool.VerificationMessageTemplateProperty.EmailSubjectByLink``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-userpool-verificationmessagetemplate.html#cfn-cognito-userpool-verificationmessagetemplate-emailsubjectbylink
            """
            return self._values.get('email_subject_by_link')

        @builtins.property
        def sms_message(self) -> typing.Optional[str]:
            """``CfnUserPool.VerificationMessageTemplateProperty.SmsMessage``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-userpool-verificationmessagetemplate.html#cfn-cognito-userpool-verificationmessagetemplate-smsmessage
            """
            return self._values.get('sms_message')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'VerificationMessageTemplateProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())



@jsii.implements(aws_cdk.core.IInspectable)
class CfnUserPoolClient(aws_cdk.core.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-cognito.CfnUserPoolClient"):
    """A CloudFormation ``AWS::Cognito::UserPoolClient``.

    see
    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpoolclient.html
    cloudformationResource:
    :cloudformationResource:: AWS::Cognito::UserPoolClient
    """
    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, user_pool_id: str, allowed_o_auth_flows: typing.Optional[typing.List[str]]=None, allowed_o_auth_flows_user_pool_client: typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.core.IResolvable]]]=None, allowed_o_auth_scopes: typing.Optional[typing.List[str]]=None, analytics_configuration: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["AnalyticsConfigurationProperty"]]]=None, callback_ur_ls: typing.Optional[typing.List[str]]=None, client_name: typing.Optional[str]=None, default_redirect_uri: typing.Optional[str]=None, explicit_auth_flows: typing.Optional[typing.List[str]]=None, generate_secret: typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.core.IResolvable]]]=None, logout_ur_ls: typing.Optional[typing.List[str]]=None, prevent_user_existence_errors: typing.Optional[str]=None, read_attributes: typing.Optional[typing.List[str]]=None, refresh_token_validity: typing.Optional[jsii.Number]=None, supported_identity_providers: typing.Optional[typing.List[str]]=None, write_attributes: typing.Optional[typing.List[str]]=None) -> None:
        """Create a new ``AWS::Cognito::UserPoolClient``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param user_pool_id: ``AWS::Cognito::UserPoolClient.UserPoolId``.
        :param allowed_o_auth_flows: ``AWS::Cognito::UserPoolClient.AllowedOAuthFlows``.
        :param allowed_o_auth_flows_user_pool_client: ``AWS::Cognito::UserPoolClient.AllowedOAuthFlowsUserPoolClient``.
        :param allowed_o_auth_scopes: ``AWS::Cognito::UserPoolClient.AllowedOAuthScopes``.
        :param analytics_configuration: ``AWS::Cognito::UserPoolClient.AnalyticsConfiguration``.
        :param callback_ur_ls: ``AWS::Cognito::UserPoolClient.CallbackURLs``.
        :param client_name: ``AWS::Cognito::UserPoolClient.ClientName``.
        :param default_redirect_uri: ``AWS::Cognito::UserPoolClient.DefaultRedirectURI``.
        :param explicit_auth_flows: ``AWS::Cognito::UserPoolClient.ExplicitAuthFlows``.
        :param generate_secret: ``AWS::Cognito::UserPoolClient.GenerateSecret``.
        :param logout_ur_ls: ``AWS::Cognito::UserPoolClient.LogoutURLs``.
        :param prevent_user_existence_errors: ``AWS::Cognito::UserPoolClient.PreventUserExistenceErrors``.
        :param read_attributes: ``AWS::Cognito::UserPoolClient.ReadAttributes``.
        :param refresh_token_validity: ``AWS::Cognito::UserPoolClient.RefreshTokenValidity``.
        :param supported_identity_providers: ``AWS::Cognito::UserPoolClient.SupportedIdentityProviders``.
        :param write_attributes: ``AWS::Cognito::UserPoolClient.WriteAttributes``.
        """
        props = CfnUserPoolClientProps(user_pool_id=user_pool_id, allowed_o_auth_flows=allowed_o_auth_flows, allowed_o_auth_flows_user_pool_client=allowed_o_auth_flows_user_pool_client, allowed_o_auth_scopes=allowed_o_auth_scopes, analytics_configuration=analytics_configuration, callback_ur_ls=callback_ur_ls, client_name=client_name, default_redirect_uri=default_redirect_uri, explicit_auth_flows=explicit_auth_flows, generate_secret=generate_secret, logout_ur_ls=logout_ur_ls, prevent_user_existence_errors=prevent_user_existence_errors, read_attributes=read_attributes, refresh_token_validity=refresh_token_validity, supported_identity_providers=supported_identity_providers, write_attributes=write_attributes)

        jsii.create(CfnUserPoolClient, self, [scope, id, props])

    @jsii.member(jsii_name="fromCloudFormation")
    @builtins.classmethod
    def from_cloud_formation(cls, scope: aws_cdk.core.Construct, id: str, resource_attributes: typing.Any, *, finder: aws_cdk.core.ICfnFinder) -> "CfnUserPoolClient":
        """A factory method that creates a new instance of this class from an object containing the CloudFormation properties of this resource.

        Used in the @aws-cdk/cloudformation-include module.

        :param scope: -
        :param id: -
        :param resource_attributes: -
        :param finder: The finder interface used to resolve references across the template.

        stability
        :stability: experimental
        """
        options = aws_cdk.core.FromCloudFormationOptions(finder=finder)

        return jsii.sinvoke(cls, "fromCloudFormation", [scope, id, resource_attributes, options])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: aws_cdk.core.TreeInspector) -> None:
        """Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "inspect", [inspector])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, props: typing.Mapping[str, typing.Any]) -> typing.Mapping[str, typing.Any]:
        """
        :param props: -
        """
        return jsii.invoke(self, "renderProperties", [props])

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> str:
        """The CloudFormation resource type name for this resource class."""
        return jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME")

    @builtins.property
    @jsii.member(jsii_name="attrClientSecret")
    def attr_client_secret(self) -> str:
        """
        cloudformationAttribute:
        :cloudformationAttribute:: ClientSecret
        """
        return jsii.get(self, "attrClientSecret")

    @builtins.property
    @jsii.member(jsii_name="attrName")
    def attr_name(self) -> str:
        """
        cloudformationAttribute:
        :cloudformationAttribute:: Name
        """
        return jsii.get(self, "attrName")

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[str, typing.Any]:
        return jsii.get(self, "cfnProperties")

    @builtins.property
    @jsii.member(jsii_name="userPoolId")
    def user_pool_id(self) -> str:
        """``AWS::Cognito::UserPoolClient.UserPoolId``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpoolclient.html#cfn-cognito-userpoolclient-userpoolid
        """
        return jsii.get(self, "userPoolId")

    @user_pool_id.setter
    def user_pool_id(self, value: str):
        jsii.set(self, "userPoolId", value)

    @builtins.property
    @jsii.member(jsii_name="allowedOAuthFlows")
    def allowed_o_auth_flows(self) -> typing.Optional[typing.List[str]]:
        """``AWS::Cognito::UserPoolClient.AllowedOAuthFlows``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpoolclient.html#cfn-cognito-userpoolclient-allowedoauthflows
        """
        return jsii.get(self, "allowedOAuthFlows")

    @allowed_o_auth_flows.setter
    def allowed_o_auth_flows(self, value: typing.Optional[typing.List[str]]):
        jsii.set(self, "allowedOAuthFlows", value)

    @builtins.property
    @jsii.member(jsii_name="allowedOAuthFlowsUserPoolClient")
    def allowed_o_auth_flows_user_pool_client(self) -> typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.core.IResolvable]]]:
        """``AWS::Cognito::UserPoolClient.AllowedOAuthFlowsUserPoolClient``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpoolclient.html#cfn-cognito-userpoolclient-allowedoauthflowsuserpoolclient
        """
        return jsii.get(self, "allowedOAuthFlowsUserPoolClient")

    @allowed_o_auth_flows_user_pool_client.setter
    def allowed_o_auth_flows_user_pool_client(self, value: typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.core.IResolvable]]]):
        jsii.set(self, "allowedOAuthFlowsUserPoolClient", value)

    @builtins.property
    @jsii.member(jsii_name="allowedOAuthScopes")
    def allowed_o_auth_scopes(self) -> typing.Optional[typing.List[str]]:
        """``AWS::Cognito::UserPoolClient.AllowedOAuthScopes``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpoolclient.html#cfn-cognito-userpoolclient-allowedoauthscopes
        """
        return jsii.get(self, "allowedOAuthScopes")

    @allowed_o_auth_scopes.setter
    def allowed_o_auth_scopes(self, value: typing.Optional[typing.List[str]]):
        jsii.set(self, "allowedOAuthScopes", value)

    @builtins.property
    @jsii.member(jsii_name="analyticsConfiguration")
    def analytics_configuration(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["AnalyticsConfigurationProperty"]]]:
        """``AWS::Cognito::UserPoolClient.AnalyticsConfiguration``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpoolclient.html#cfn-cognito-userpoolclient-analyticsconfiguration
        """
        return jsii.get(self, "analyticsConfiguration")

    @analytics_configuration.setter
    def analytics_configuration(self, value: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["AnalyticsConfigurationProperty"]]]):
        jsii.set(self, "analyticsConfiguration", value)

    @builtins.property
    @jsii.member(jsii_name="callbackUrLs")
    def callback_ur_ls(self) -> typing.Optional[typing.List[str]]:
        """``AWS::Cognito::UserPoolClient.CallbackURLs``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpoolclient.html#cfn-cognito-userpoolclient-callbackurls
        """
        return jsii.get(self, "callbackUrLs")

    @callback_ur_ls.setter
    def callback_ur_ls(self, value: typing.Optional[typing.List[str]]):
        jsii.set(self, "callbackUrLs", value)

    @builtins.property
    @jsii.member(jsii_name="clientName")
    def client_name(self) -> typing.Optional[str]:
        """``AWS::Cognito::UserPoolClient.ClientName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpoolclient.html#cfn-cognito-userpoolclient-clientname
        """
        return jsii.get(self, "clientName")

    @client_name.setter
    def client_name(self, value: typing.Optional[str]):
        jsii.set(self, "clientName", value)

    @builtins.property
    @jsii.member(jsii_name="defaultRedirectUri")
    def default_redirect_uri(self) -> typing.Optional[str]:
        """``AWS::Cognito::UserPoolClient.DefaultRedirectURI``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpoolclient.html#cfn-cognito-userpoolclient-defaultredirecturi
        """
        return jsii.get(self, "defaultRedirectUri")

    @default_redirect_uri.setter
    def default_redirect_uri(self, value: typing.Optional[str]):
        jsii.set(self, "defaultRedirectUri", value)

    @builtins.property
    @jsii.member(jsii_name="explicitAuthFlows")
    def explicit_auth_flows(self) -> typing.Optional[typing.List[str]]:
        """``AWS::Cognito::UserPoolClient.ExplicitAuthFlows``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpoolclient.html#cfn-cognito-userpoolclient-explicitauthflows
        """
        return jsii.get(self, "explicitAuthFlows")

    @explicit_auth_flows.setter
    def explicit_auth_flows(self, value: typing.Optional[typing.List[str]]):
        jsii.set(self, "explicitAuthFlows", value)

    @builtins.property
    @jsii.member(jsii_name="generateSecret")
    def generate_secret(self) -> typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.core.IResolvable]]]:
        """``AWS::Cognito::UserPoolClient.GenerateSecret``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpoolclient.html#cfn-cognito-userpoolclient-generatesecret
        """
        return jsii.get(self, "generateSecret")

    @generate_secret.setter
    def generate_secret(self, value: typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.core.IResolvable]]]):
        jsii.set(self, "generateSecret", value)

    @builtins.property
    @jsii.member(jsii_name="logoutUrLs")
    def logout_ur_ls(self) -> typing.Optional[typing.List[str]]:
        """``AWS::Cognito::UserPoolClient.LogoutURLs``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpoolclient.html#cfn-cognito-userpoolclient-logouturls
        """
        return jsii.get(self, "logoutUrLs")

    @logout_ur_ls.setter
    def logout_ur_ls(self, value: typing.Optional[typing.List[str]]):
        jsii.set(self, "logoutUrLs", value)

    @builtins.property
    @jsii.member(jsii_name="preventUserExistenceErrors")
    def prevent_user_existence_errors(self) -> typing.Optional[str]:
        """``AWS::Cognito::UserPoolClient.PreventUserExistenceErrors``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpoolclient.html#cfn-cognito-userpoolclient-preventuserexistenceerrors
        """
        return jsii.get(self, "preventUserExistenceErrors")

    @prevent_user_existence_errors.setter
    def prevent_user_existence_errors(self, value: typing.Optional[str]):
        jsii.set(self, "preventUserExistenceErrors", value)

    @builtins.property
    @jsii.member(jsii_name="readAttributes")
    def read_attributes(self) -> typing.Optional[typing.List[str]]:
        """``AWS::Cognito::UserPoolClient.ReadAttributes``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpoolclient.html#cfn-cognito-userpoolclient-readattributes
        """
        return jsii.get(self, "readAttributes")

    @read_attributes.setter
    def read_attributes(self, value: typing.Optional[typing.List[str]]):
        jsii.set(self, "readAttributes", value)

    @builtins.property
    @jsii.member(jsii_name="refreshTokenValidity")
    def refresh_token_validity(self) -> typing.Optional[jsii.Number]:
        """``AWS::Cognito::UserPoolClient.RefreshTokenValidity``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpoolclient.html#cfn-cognito-userpoolclient-refreshtokenvalidity
        """
        return jsii.get(self, "refreshTokenValidity")

    @refresh_token_validity.setter
    def refresh_token_validity(self, value: typing.Optional[jsii.Number]):
        jsii.set(self, "refreshTokenValidity", value)

    @builtins.property
    @jsii.member(jsii_name="supportedIdentityProviders")
    def supported_identity_providers(self) -> typing.Optional[typing.List[str]]:
        """``AWS::Cognito::UserPoolClient.SupportedIdentityProviders``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpoolclient.html#cfn-cognito-userpoolclient-supportedidentityproviders
        """
        return jsii.get(self, "supportedIdentityProviders")

    @supported_identity_providers.setter
    def supported_identity_providers(self, value: typing.Optional[typing.List[str]]):
        jsii.set(self, "supportedIdentityProviders", value)

    @builtins.property
    @jsii.member(jsii_name="writeAttributes")
    def write_attributes(self) -> typing.Optional[typing.List[str]]:
        """``AWS::Cognito::UserPoolClient.WriteAttributes``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpoolclient.html#cfn-cognito-userpoolclient-writeattributes
        """
        return jsii.get(self, "writeAttributes")

    @write_attributes.setter
    def write_attributes(self, value: typing.Optional[typing.List[str]]):
        jsii.set(self, "writeAttributes", value)

    @jsii.data_type(jsii_type="@aws-cdk/aws-cognito.CfnUserPoolClient.AnalyticsConfigurationProperty", jsii_struct_bases=[], name_mapping={'application_id': 'applicationId', 'external_id': 'externalId', 'role_arn': 'roleArn', 'user_data_shared': 'userDataShared'})
    class AnalyticsConfigurationProperty():
        def __init__(self, *, application_id: typing.Optional[str]=None, external_id: typing.Optional[str]=None, role_arn: typing.Optional[str]=None, user_data_shared: typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.core.IResolvable]]]=None) -> None:
            """
            :param application_id: ``CfnUserPoolClient.AnalyticsConfigurationProperty.ApplicationId``.
            :param external_id: ``CfnUserPoolClient.AnalyticsConfigurationProperty.ExternalId``.
            :param role_arn: ``CfnUserPoolClient.AnalyticsConfigurationProperty.RoleArn``.
            :param user_data_shared: ``CfnUserPoolClient.AnalyticsConfigurationProperty.UserDataShared``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-userpoolclient-analyticsconfiguration.html
            """
            self._values = {
            }
            if application_id is not None: self._values["application_id"] = application_id
            if external_id is not None: self._values["external_id"] = external_id
            if role_arn is not None: self._values["role_arn"] = role_arn
            if user_data_shared is not None: self._values["user_data_shared"] = user_data_shared

        @builtins.property
        def application_id(self) -> typing.Optional[str]:
            """``CfnUserPoolClient.AnalyticsConfigurationProperty.ApplicationId``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-userpoolclient-analyticsconfiguration.html#cfn-cognito-userpoolclient-analyticsconfiguration-applicationid
            """
            return self._values.get('application_id')

        @builtins.property
        def external_id(self) -> typing.Optional[str]:
            """``CfnUserPoolClient.AnalyticsConfigurationProperty.ExternalId``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-userpoolclient-analyticsconfiguration.html#cfn-cognito-userpoolclient-analyticsconfiguration-externalid
            """
            return self._values.get('external_id')

        @builtins.property
        def role_arn(self) -> typing.Optional[str]:
            """``CfnUserPoolClient.AnalyticsConfigurationProperty.RoleArn``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-userpoolclient-analyticsconfiguration.html#cfn-cognito-userpoolclient-analyticsconfiguration-rolearn
            """
            return self._values.get('role_arn')

        @builtins.property
        def user_data_shared(self) -> typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.core.IResolvable]]]:
            """``CfnUserPoolClient.AnalyticsConfigurationProperty.UserDataShared``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-userpoolclient-analyticsconfiguration.html#cfn-cognito-userpoolclient-analyticsconfiguration-userdatashared
            """
            return self._values.get('user_data_shared')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'AnalyticsConfigurationProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())



@jsii.data_type(jsii_type="@aws-cdk/aws-cognito.CfnUserPoolClientProps", jsii_struct_bases=[], name_mapping={'user_pool_id': 'userPoolId', 'allowed_o_auth_flows': 'allowedOAuthFlows', 'allowed_o_auth_flows_user_pool_client': 'allowedOAuthFlowsUserPoolClient', 'allowed_o_auth_scopes': 'allowedOAuthScopes', 'analytics_configuration': 'analyticsConfiguration', 'callback_ur_ls': 'callbackUrLs', 'client_name': 'clientName', 'default_redirect_uri': 'defaultRedirectUri', 'explicit_auth_flows': 'explicitAuthFlows', 'generate_secret': 'generateSecret', 'logout_ur_ls': 'logoutUrLs', 'prevent_user_existence_errors': 'preventUserExistenceErrors', 'read_attributes': 'readAttributes', 'refresh_token_validity': 'refreshTokenValidity', 'supported_identity_providers': 'supportedIdentityProviders', 'write_attributes': 'writeAttributes'})
class CfnUserPoolClientProps():
    def __init__(self, *, user_pool_id: str, allowed_o_auth_flows: typing.Optional[typing.List[str]]=None, allowed_o_auth_flows_user_pool_client: typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.core.IResolvable]]]=None, allowed_o_auth_scopes: typing.Optional[typing.List[str]]=None, analytics_configuration: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["CfnUserPoolClient.AnalyticsConfigurationProperty"]]]=None, callback_ur_ls: typing.Optional[typing.List[str]]=None, client_name: typing.Optional[str]=None, default_redirect_uri: typing.Optional[str]=None, explicit_auth_flows: typing.Optional[typing.List[str]]=None, generate_secret: typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.core.IResolvable]]]=None, logout_ur_ls: typing.Optional[typing.List[str]]=None, prevent_user_existence_errors: typing.Optional[str]=None, read_attributes: typing.Optional[typing.List[str]]=None, refresh_token_validity: typing.Optional[jsii.Number]=None, supported_identity_providers: typing.Optional[typing.List[str]]=None, write_attributes: typing.Optional[typing.List[str]]=None) -> None:
        """Properties for defining a ``AWS::Cognito::UserPoolClient``.

        :param user_pool_id: ``AWS::Cognito::UserPoolClient.UserPoolId``.
        :param allowed_o_auth_flows: ``AWS::Cognito::UserPoolClient.AllowedOAuthFlows``.
        :param allowed_o_auth_flows_user_pool_client: ``AWS::Cognito::UserPoolClient.AllowedOAuthFlowsUserPoolClient``.
        :param allowed_o_auth_scopes: ``AWS::Cognito::UserPoolClient.AllowedOAuthScopes``.
        :param analytics_configuration: ``AWS::Cognito::UserPoolClient.AnalyticsConfiguration``.
        :param callback_ur_ls: ``AWS::Cognito::UserPoolClient.CallbackURLs``.
        :param client_name: ``AWS::Cognito::UserPoolClient.ClientName``.
        :param default_redirect_uri: ``AWS::Cognito::UserPoolClient.DefaultRedirectURI``.
        :param explicit_auth_flows: ``AWS::Cognito::UserPoolClient.ExplicitAuthFlows``.
        :param generate_secret: ``AWS::Cognito::UserPoolClient.GenerateSecret``.
        :param logout_ur_ls: ``AWS::Cognito::UserPoolClient.LogoutURLs``.
        :param prevent_user_existence_errors: ``AWS::Cognito::UserPoolClient.PreventUserExistenceErrors``.
        :param read_attributes: ``AWS::Cognito::UserPoolClient.ReadAttributes``.
        :param refresh_token_validity: ``AWS::Cognito::UserPoolClient.RefreshTokenValidity``.
        :param supported_identity_providers: ``AWS::Cognito::UserPoolClient.SupportedIdentityProviders``.
        :param write_attributes: ``AWS::Cognito::UserPoolClient.WriteAttributes``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpoolclient.html
        """
        self._values = {
            'user_pool_id': user_pool_id,
        }
        if allowed_o_auth_flows is not None: self._values["allowed_o_auth_flows"] = allowed_o_auth_flows
        if allowed_o_auth_flows_user_pool_client is not None: self._values["allowed_o_auth_flows_user_pool_client"] = allowed_o_auth_flows_user_pool_client
        if allowed_o_auth_scopes is not None: self._values["allowed_o_auth_scopes"] = allowed_o_auth_scopes
        if analytics_configuration is not None: self._values["analytics_configuration"] = analytics_configuration
        if callback_ur_ls is not None: self._values["callback_ur_ls"] = callback_ur_ls
        if client_name is not None: self._values["client_name"] = client_name
        if default_redirect_uri is not None: self._values["default_redirect_uri"] = default_redirect_uri
        if explicit_auth_flows is not None: self._values["explicit_auth_flows"] = explicit_auth_flows
        if generate_secret is not None: self._values["generate_secret"] = generate_secret
        if logout_ur_ls is not None: self._values["logout_ur_ls"] = logout_ur_ls
        if prevent_user_existence_errors is not None: self._values["prevent_user_existence_errors"] = prevent_user_existence_errors
        if read_attributes is not None: self._values["read_attributes"] = read_attributes
        if refresh_token_validity is not None: self._values["refresh_token_validity"] = refresh_token_validity
        if supported_identity_providers is not None: self._values["supported_identity_providers"] = supported_identity_providers
        if write_attributes is not None: self._values["write_attributes"] = write_attributes

    @builtins.property
    def user_pool_id(self) -> str:
        """``AWS::Cognito::UserPoolClient.UserPoolId``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpoolclient.html#cfn-cognito-userpoolclient-userpoolid
        """
        return self._values.get('user_pool_id')

    @builtins.property
    def allowed_o_auth_flows(self) -> typing.Optional[typing.List[str]]:
        """``AWS::Cognito::UserPoolClient.AllowedOAuthFlows``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpoolclient.html#cfn-cognito-userpoolclient-allowedoauthflows
        """
        return self._values.get('allowed_o_auth_flows')

    @builtins.property
    def allowed_o_auth_flows_user_pool_client(self) -> typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.core.IResolvable]]]:
        """``AWS::Cognito::UserPoolClient.AllowedOAuthFlowsUserPoolClient``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpoolclient.html#cfn-cognito-userpoolclient-allowedoauthflowsuserpoolclient
        """
        return self._values.get('allowed_o_auth_flows_user_pool_client')

    @builtins.property
    def allowed_o_auth_scopes(self) -> typing.Optional[typing.List[str]]:
        """``AWS::Cognito::UserPoolClient.AllowedOAuthScopes``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpoolclient.html#cfn-cognito-userpoolclient-allowedoauthscopes
        """
        return self._values.get('allowed_o_auth_scopes')

    @builtins.property
    def analytics_configuration(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["CfnUserPoolClient.AnalyticsConfigurationProperty"]]]:
        """``AWS::Cognito::UserPoolClient.AnalyticsConfiguration``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpoolclient.html#cfn-cognito-userpoolclient-analyticsconfiguration
        """
        return self._values.get('analytics_configuration')

    @builtins.property
    def callback_ur_ls(self) -> typing.Optional[typing.List[str]]:
        """``AWS::Cognito::UserPoolClient.CallbackURLs``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpoolclient.html#cfn-cognito-userpoolclient-callbackurls
        """
        return self._values.get('callback_ur_ls')

    @builtins.property
    def client_name(self) -> typing.Optional[str]:
        """``AWS::Cognito::UserPoolClient.ClientName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpoolclient.html#cfn-cognito-userpoolclient-clientname
        """
        return self._values.get('client_name')

    @builtins.property
    def default_redirect_uri(self) -> typing.Optional[str]:
        """``AWS::Cognito::UserPoolClient.DefaultRedirectURI``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpoolclient.html#cfn-cognito-userpoolclient-defaultredirecturi
        """
        return self._values.get('default_redirect_uri')

    @builtins.property
    def explicit_auth_flows(self) -> typing.Optional[typing.List[str]]:
        """``AWS::Cognito::UserPoolClient.ExplicitAuthFlows``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpoolclient.html#cfn-cognito-userpoolclient-explicitauthflows
        """
        return self._values.get('explicit_auth_flows')

    @builtins.property
    def generate_secret(self) -> typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.core.IResolvable]]]:
        """``AWS::Cognito::UserPoolClient.GenerateSecret``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpoolclient.html#cfn-cognito-userpoolclient-generatesecret
        """
        return self._values.get('generate_secret')

    @builtins.property
    def logout_ur_ls(self) -> typing.Optional[typing.List[str]]:
        """``AWS::Cognito::UserPoolClient.LogoutURLs``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpoolclient.html#cfn-cognito-userpoolclient-logouturls
        """
        return self._values.get('logout_ur_ls')

    @builtins.property
    def prevent_user_existence_errors(self) -> typing.Optional[str]:
        """``AWS::Cognito::UserPoolClient.PreventUserExistenceErrors``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpoolclient.html#cfn-cognito-userpoolclient-preventuserexistenceerrors
        """
        return self._values.get('prevent_user_existence_errors')

    @builtins.property
    def read_attributes(self) -> typing.Optional[typing.List[str]]:
        """``AWS::Cognito::UserPoolClient.ReadAttributes``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpoolclient.html#cfn-cognito-userpoolclient-readattributes
        """
        return self._values.get('read_attributes')

    @builtins.property
    def refresh_token_validity(self) -> typing.Optional[jsii.Number]:
        """``AWS::Cognito::UserPoolClient.RefreshTokenValidity``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpoolclient.html#cfn-cognito-userpoolclient-refreshtokenvalidity
        """
        return self._values.get('refresh_token_validity')

    @builtins.property
    def supported_identity_providers(self) -> typing.Optional[typing.List[str]]:
        """``AWS::Cognito::UserPoolClient.SupportedIdentityProviders``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpoolclient.html#cfn-cognito-userpoolclient-supportedidentityproviders
        """
        return self._values.get('supported_identity_providers')

    @builtins.property
    def write_attributes(self) -> typing.Optional[typing.List[str]]:
        """``AWS::Cognito::UserPoolClient.WriteAttributes``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpoolclient.html#cfn-cognito-userpoolclient-writeattributes
        """
        return self._values.get('write_attributes')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'CfnUserPoolClientProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.implements(aws_cdk.core.IInspectable)
class CfnUserPoolDomain(aws_cdk.core.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-cognito.CfnUserPoolDomain"):
    """A CloudFormation ``AWS::Cognito::UserPoolDomain``.

    see
    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpooldomain.html
    cloudformationResource:
    :cloudformationResource:: AWS::Cognito::UserPoolDomain
    """
    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, domain: str, user_pool_id: str, custom_domain_config: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["CustomDomainConfigTypeProperty"]]]=None) -> None:
        """Create a new ``AWS::Cognito::UserPoolDomain``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param domain: ``AWS::Cognito::UserPoolDomain.Domain``.
        :param user_pool_id: ``AWS::Cognito::UserPoolDomain.UserPoolId``.
        :param custom_domain_config: ``AWS::Cognito::UserPoolDomain.CustomDomainConfig``.
        """
        props = CfnUserPoolDomainProps(domain=domain, user_pool_id=user_pool_id, custom_domain_config=custom_domain_config)

        jsii.create(CfnUserPoolDomain, self, [scope, id, props])

    @jsii.member(jsii_name="fromCloudFormation")
    @builtins.classmethod
    def from_cloud_formation(cls, scope: aws_cdk.core.Construct, id: str, resource_attributes: typing.Any, *, finder: aws_cdk.core.ICfnFinder) -> "CfnUserPoolDomain":
        """A factory method that creates a new instance of this class from an object containing the CloudFormation properties of this resource.

        Used in the @aws-cdk/cloudformation-include module.

        :param scope: -
        :param id: -
        :param resource_attributes: -
        :param finder: The finder interface used to resolve references across the template.

        stability
        :stability: experimental
        """
        options = aws_cdk.core.FromCloudFormationOptions(finder=finder)

        return jsii.sinvoke(cls, "fromCloudFormation", [scope, id, resource_attributes, options])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: aws_cdk.core.TreeInspector) -> None:
        """Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "inspect", [inspector])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, props: typing.Mapping[str, typing.Any]) -> typing.Mapping[str, typing.Any]:
        """
        :param props: -
        """
        return jsii.invoke(self, "renderProperties", [props])

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> str:
        """The CloudFormation resource type name for this resource class."""
        return jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME")

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[str, typing.Any]:
        return jsii.get(self, "cfnProperties")

    @builtins.property
    @jsii.member(jsii_name="domain")
    def domain(self) -> str:
        """``AWS::Cognito::UserPoolDomain.Domain``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpooldomain.html#cfn-cognito-userpooldomain-domain
        """
        return jsii.get(self, "domain")

    @domain.setter
    def domain(self, value: str):
        jsii.set(self, "domain", value)

    @builtins.property
    @jsii.member(jsii_name="userPoolId")
    def user_pool_id(self) -> str:
        """``AWS::Cognito::UserPoolDomain.UserPoolId``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpooldomain.html#cfn-cognito-userpooldomain-userpoolid
        """
        return jsii.get(self, "userPoolId")

    @user_pool_id.setter
    def user_pool_id(self, value: str):
        jsii.set(self, "userPoolId", value)

    @builtins.property
    @jsii.member(jsii_name="customDomainConfig")
    def custom_domain_config(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["CustomDomainConfigTypeProperty"]]]:
        """``AWS::Cognito::UserPoolDomain.CustomDomainConfig``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpooldomain.html#cfn-cognito-userpooldomain-customdomainconfig
        """
        return jsii.get(self, "customDomainConfig")

    @custom_domain_config.setter
    def custom_domain_config(self, value: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["CustomDomainConfigTypeProperty"]]]):
        jsii.set(self, "customDomainConfig", value)

    @jsii.data_type(jsii_type="@aws-cdk/aws-cognito.CfnUserPoolDomain.CustomDomainConfigTypeProperty", jsii_struct_bases=[], name_mapping={'certificate_arn': 'certificateArn'})
    class CustomDomainConfigTypeProperty():
        def __init__(self, *, certificate_arn: typing.Optional[str]=None) -> None:
            """
            :param certificate_arn: ``CfnUserPoolDomain.CustomDomainConfigTypeProperty.CertificateArn``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-userpooldomain-customdomainconfigtype.html
            """
            self._values = {
            }
            if certificate_arn is not None: self._values["certificate_arn"] = certificate_arn

        @builtins.property
        def certificate_arn(self) -> typing.Optional[str]:
            """``CfnUserPoolDomain.CustomDomainConfigTypeProperty.CertificateArn``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-userpooldomain-customdomainconfigtype.html#cfn-cognito-userpooldomain-customdomainconfigtype-certificatearn
            """
            return self._values.get('certificate_arn')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'CustomDomainConfigTypeProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())



@jsii.data_type(jsii_type="@aws-cdk/aws-cognito.CfnUserPoolDomainProps", jsii_struct_bases=[], name_mapping={'domain': 'domain', 'user_pool_id': 'userPoolId', 'custom_domain_config': 'customDomainConfig'})
class CfnUserPoolDomainProps():
    def __init__(self, *, domain: str, user_pool_id: str, custom_domain_config: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["CfnUserPoolDomain.CustomDomainConfigTypeProperty"]]]=None) -> None:
        """Properties for defining a ``AWS::Cognito::UserPoolDomain``.

        :param domain: ``AWS::Cognito::UserPoolDomain.Domain``.
        :param user_pool_id: ``AWS::Cognito::UserPoolDomain.UserPoolId``.
        :param custom_domain_config: ``AWS::Cognito::UserPoolDomain.CustomDomainConfig``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpooldomain.html
        """
        self._values = {
            'domain': domain,
            'user_pool_id': user_pool_id,
        }
        if custom_domain_config is not None: self._values["custom_domain_config"] = custom_domain_config

    @builtins.property
    def domain(self) -> str:
        """``AWS::Cognito::UserPoolDomain.Domain``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpooldomain.html#cfn-cognito-userpooldomain-domain
        """
        return self._values.get('domain')

    @builtins.property
    def user_pool_id(self) -> str:
        """``AWS::Cognito::UserPoolDomain.UserPoolId``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpooldomain.html#cfn-cognito-userpooldomain-userpoolid
        """
        return self._values.get('user_pool_id')

    @builtins.property
    def custom_domain_config(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["CfnUserPoolDomain.CustomDomainConfigTypeProperty"]]]:
        """``AWS::Cognito::UserPoolDomain.CustomDomainConfig``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpooldomain.html#cfn-cognito-userpooldomain-customdomainconfig
        """
        return self._values.get('custom_domain_config')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'CfnUserPoolDomainProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.implements(aws_cdk.core.IInspectable)
class CfnUserPoolGroup(aws_cdk.core.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-cognito.CfnUserPoolGroup"):
    """A CloudFormation ``AWS::Cognito::UserPoolGroup``.

    see
    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpoolgroup.html
    cloudformationResource:
    :cloudformationResource:: AWS::Cognito::UserPoolGroup
    """
    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, user_pool_id: str, description: typing.Optional[str]=None, group_name: typing.Optional[str]=None, precedence: typing.Optional[jsii.Number]=None, role_arn: typing.Optional[str]=None) -> None:
        """Create a new ``AWS::Cognito::UserPoolGroup``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param user_pool_id: ``AWS::Cognito::UserPoolGroup.UserPoolId``.
        :param description: ``AWS::Cognito::UserPoolGroup.Description``.
        :param group_name: ``AWS::Cognito::UserPoolGroup.GroupName``.
        :param precedence: ``AWS::Cognito::UserPoolGroup.Precedence``.
        :param role_arn: ``AWS::Cognito::UserPoolGroup.RoleArn``.
        """
        props = CfnUserPoolGroupProps(user_pool_id=user_pool_id, description=description, group_name=group_name, precedence=precedence, role_arn=role_arn)

        jsii.create(CfnUserPoolGroup, self, [scope, id, props])

    @jsii.member(jsii_name="fromCloudFormation")
    @builtins.classmethod
    def from_cloud_formation(cls, scope: aws_cdk.core.Construct, id: str, resource_attributes: typing.Any, *, finder: aws_cdk.core.ICfnFinder) -> "CfnUserPoolGroup":
        """A factory method that creates a new instance of this class from an object containing the CloudFormation properties of this resource.

        Used in the @aws-cdk/cloudformation-include module.

        :param scope: -
        :param id: -
        :param resource_attributes: -
        :param finder: The finder interface used to resolve references across the template.

        stability
        :stability: experimental
        """
        options = aws_cdk.core.FromCloudFormationOptions(finder=finder)

        return jsii.sinvoke(cls, "fromCloudFormation", [scope, id, resource_attributes, options])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: aws_cdk.core.TreeInspector) -> None:
        """Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "inspect", [inspector])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, props: typing.Mapping[str, typing.Any]) -> typing.Mapping[str, typing.Any]:
        """
        :param props: -
        """
        return jsii.invoke(self, "renderProperties", [props])

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> str:
        """The CloudFormation resource type name for this resource class."""
        return jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME")

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[str, typing.Any]:
        return jsii.get(self, "cfnProperties")

    @builtins.property
    @jsii.member(jsii_name="userPoolId")
    def user_pool_id(self) -> str:
        """``AWS::Cognito::UserPoolGroup.UserPoolId``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpoolgroup.html#cfn-cognito-userpoolgroup-userpoolid
        """
        return jsii.get(self, "userPoolId")

    @user_pool_id.setter
    def user_pool_id(self, value: str):
        jsii.set(self, "userPoolId", value)

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> typing.Optional[str]:
        """``AWS::Cognito::UserPoolGroup.Description``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpoolgroup.html#cfn-cognito-userpoolgroup-description
        """
        return jsii.get(self, "description")

    @description.setter
    def description(self, value: typing.Optional[str]):
        jsii.set(self, "description", value)

    @builtins.property
    @jsii.member(jsii_name="groupName")
    def group_name(self) -> typing.Optional[str]:
        """``AWS::Cognito::UserPoolGroup.GroupName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpoolgroup.html#cfn-cognito-userpoolgroup-groupname
        """
        return jsii.get(self, "groupName")

    @group_name.setter
    def group_name(self, value: typing.Optional[str]):
        jsii.set(self, "groupName", value)

    @builtins.property
    @jsii.member(jsii_name="precedence")
    def precedence(self) -> typing.Optional[jsii.Number]:
        """``AWS::Cognito::UserPoolGroup.Precedence``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpoolgroup.html#cfn-cognito-userpoolgroup-precedence
        """
        return jsii.get(self, "precedence")

    @precedence.setter
    def precedence(self, value: typing.Optional[jsii.Number]):
        jsii.set(self, "precedence", value)

    @builtins.property
    @jsii.member(jsii_name="roleArn")
    def role_arn(self) -> typing.Optional[str]:
        """``AWS::Cognito::UserPoolGroup.RoleArn``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpoolgroup.html#cfn-cognito-userpoolgroup-rolearn
        """
        return jsii.get(self, "roleArn")

    @role_arn.setter
    def role_arn(self, value: typing.Optional[str]):
        jsii.set(self, "roleArn", value)


@jsii.data_type(jsii_type="@aws-cdk/aws-cognito.CfnUserPoolGroupProps", jsii_struct_bases=[], name_mapping={'user_pool_id': 'userPoolId', 'description': 'description', 'group_name': 'groupName', 'precedence': 'precedence', 'role_arn': 'roleArn'})
class CfnUserPoolGroupProps():
    def __init__(self, *, user_pool_id: str, description: typing.Optional[str]=None, group_name: typing.Optional[str]=None, precedence: typing.Optional[jsii.Number]=None, role_arn: typing.Optional[str]=None) -> None:
        """Properties for defining a ``AWS::Cognito::UserPoolGroup``.

        :param user_pool_id: ``AWS::Cognito::UserPoolGroup.UserPoolId``.
        :param description: ``AWS::Cognito::UserPoolGroup.Description``.
        :param group_name: ``AWS::Cognito::UserPoolGroup.GroupName``.
        :param precedence: ``AWS::Cognito::UserPoolGroup.Precedence``.
        :param role_arn: ``AWS::Cognito::UserPoolGroup.RoleArn``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpoolgroup.html
        """
        self._values = {
            'user_pool_id': user_pool_id,
        }
        if description is not None: self._values["description"] = description
        if group_name is not None: self._values["group_name"] = group_name
        if precedence is not None: self._values["precedence"] = precedence
        if role_arn is not None: self._values["role_arn"] = role_arn

    @builtins.property
    def user_pool_id(self) -> str:
        """``AWS::Cognito::UserPoolGroup.UserPoolId``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpoolgroup.html#cfn-cognito-userpoolgroup-userpoolid
        """
        return self._values.get('user_pool_id')

    @builtins.property
    def description(self) -> typing.Optional[str]:
        """``AWS::Cognito::UserPoolGroup.Description``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpoolgroup.html#cfn-cognito-userpoolgroup-description
        """
        return self._values.get('description')

    @builtins.property
    def group_name(self) -> typing.Optional[str]:
        """``AWS::Cognito::UserPoolGroup.GroupName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpoolgroup.html#cfn-cognito-userpoolgroup-groupname
        """
        return self._values.get('group_name')

    @builtins.property
    def precedence(self) -> typing.Optional[jsii.Number]:
        """``AWS::Cognito::UserPoolGroup.Precedence``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpoolgroup.html#cfn-cognito-userpoolgroup-precedence
        """
        return self._values.get('precedence')

    @builtins.property
    def role_arn(self) -> typing.Optional[str]:
        """``AWS::Cognito::UserPoolGroup.RoleArn``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpoolgroup.html#cfn-cognito-userpoolgroup-rolearn
        """
        return self._values.get('role_arn')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'CfnUserPoolGroupProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.implements(aws_cdk.core.IInspectable)
class CfnUserPoolIdentityProvider(aws_cdk.core.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-cognito.CfnUserPoolIdentityProvider"):
    """A CloudFormation ``AWS::Cognito::UserPoolIdentityProvider``.

    see
    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpoolidentityprovider.html
    cloudformationResource:
    :cloudformationResource:: AWS::Cognito::UserPoolIdentityProvider
    """
    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, provider_name: str, provider_type: str, user_pool_id: str, attribute_mapping: typing.Any=None, idp_identifiers: typing.Optional[typing.List[str]]=None, provider_details: typing.Any=None) -> None:
        """Create a new ``AWS::Cognito::UserPoolIdentityProvider``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param provider_name: ``AWS::Cognito::UserPoolIdentityProvider.ProviderName``.
        :param provider_type: ``AWS::Cognito::UserPoolIdentityProvider.ProviderType``.
        :param user_pool_id: ``AWS::Cognito::UserPoolIdentityProvider.UserPoolId``.
        :param attribute_mapping: ``AWS::Cognito::UserPoolIdentityProvider.AttributeMapping``.
        :param idp_identifiers: ``AWS::Cognito::UserPoolIdentityProvider.IdpIdentifiers``.
        :param provider_details: ``AWS::Cognito::UserPoolIdentityProvider.ProviderDetails``.
        """
        props = CfnUserPoolIdentityProviderProps(provider_name=provider_name, provider_type=provider_type, user_pool_id=user_pool_id, attribute_mapping=attribute_mapping, idp_identifiers=idp_identifiers, provider_details=provider_details)

        jsii.create(CfnUserPoolIdentityProvider, self, [scope, id, props])

    @jsii.member(jsii_name="fromCloudFormation")
    @builtins.classmethod
    def from_cloud_formation(cls, scope: aws_cdk.core.Construct, id: str, resource_attributes: typing.Any, *, finder: aws_cdk.core.ICfnFinder) -> "CfnUserPoolIdentityProvider":
        """A factory method that creates a new instance of this class from an object containing the CloudFormation properties of this resource.

        Used in the @aws-cdk/cloudformation-include module.

        :param scope: -
        :param id: -
        :param resource_attributes: -
        :param finder: The finder interface used to resolve references across the template.

        stability
        :stability: experimental
        """
        options = aws_cdk.core.FromCloudFormationOptions(finder=finder)

        return jsii.sinvoke(cls, "fromCloudFormation", [scope, id, resource_attributes, options])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: aws_cdk.core.TreeInspector) -> None:
        """Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "inspect", [inspector])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, props: typing.Mapping[str, typing.Any]) -> typing.Mapping[str, typing.Any]:
        """
        :param props: -
        """
        return jsii.invoke(self, "renderProperties", [props])

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> str:
        """The CloudFormation resource type name for this resource class."""
        return jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME")

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[str, typing.Any]:
        return jsii.get(self, "cfnProperties")

    @builtins.property
    @jsii.member(jsii_name="attributeMapping")
    def attribute_mapping(self) -> typing.Any:
        """``AWS::Cognito::UserPoolIdentityProvider.AttributeMapping``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpoolidentityprovider.html#cfn-cognito-userpoolidentityprovider-attributemapping
        """
        return jsii.get(self, "attributeMapping")

    @attribute_mapping.setter
    def attribute_mapping(self, value: typing.Any):
        jsii.set(self, "attributeMapping", value)

    @builtins.property
    @jsii.member(jsii_name="providerDetails")
    def provider_details(self) -> typing.Any:
        """``AWS::Cognito::UserPoolIdentityProvider.ProviderDetails``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpoolidentityprovider.html#cfn-cognito-userpoolidentityprovider-providerdetails
        """
        return jsii.get(self, "providerDetails")

    @provider_details.setter
    def provider_details(self, value: typing.Any):
        jsii.set(self, "providerDetails", value)

    @builtins.property
    @jsii.member(jsii_name="providerName")
    def provider_name(self) -> str:
        """``AWS::Cognito::UserPoolIdentityProvider.ProviderName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpoolidentityprovider.html#cfn-cognito-userpoolidentityprovider-providername
        """
        return jsii.get(self, "providerName")

    @provider_name.setter
    def provider_name(self, value: str):
        jsii.set(self, "providerName", value)

    @builtins.property
    @jsii.member(jsii_name="providerType")
    def provider_type(self) -> str:
        """``AWS::Cognito::UserPoolIdentityProvider.ProviderType``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpoolidentityprovider.html#cfn-cognito-userpoolidentityprovider-providertype
        """
        return jsii.get(self, "providerType")

    @provider_type.setter
    def provider_type(self, value: str):
        jsii.set(self, "providerType", value)

    @builtins.property
    @jsii.member(jsii_name="userPoolId")
    def user_pool_id(self) -> str:
        """``AWS::Cognito::UserPoolIdentityProvider.UserPoolId``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpoolidentityprovider.html#cfn-cognito-userpoolidentityprovider-userpoolid
        """
        return jsii.get(self, "userPoolId")

    @user_pool_id.setter
    def user_pool_id(self, value: str):
        jsii.set(self, "userPoolId", value)

    @builtins.property
    @jsii.member(jsii_name="idpIdentifiers")
    def idp_identifiers(self) -> typing.Optional[typing.List[str]]:
        """``AWS::Cognito::UserPoolIdentityProvider.IdpIdentifiers``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpoolidentityprovider.html#cfn-cognito-userpoolidentityprovider-idpidentifiers
        """
        return jsii.get(self, "idpIdentifiers")

    @idp_identifiers.setter
    def idp_identifiers(self, value: typing.Optional[typing.List[str]]):
        jsii.set(self, "idpIdentifiers", value)


@jsii.data_type(jsii_type="@aws-cdk/aws-cognito.CfnUserPoolIdentityProviderProps", jsii_struct_bases=[], name_mapping={'provider_name': 'providerName', 'provider_type': 'providerType', 'user_pool_id': 'userPoolId', 'attribute_mapping': 'attributeMapping', 'idp_identifiers': 'idpIdentifiers', 'provider_details': 'providerDetails'})
class CfnUserPoolIdentityProviderProps():
    def __init__(self, *, provider_name: str, provider_type: str, user_pool_id: str, attribute_mapping: typing.Any=None, idp_identifiers: typing.Optional[typing.List[str]]=None, provider_details: typing.Any=None) -> None:
        """Properties for defining a ``AWS::Cognito::UserPoolIdentityProvider``.

        :param provider_name: ``AWS::Cognito::UserPoolIdentityProvider.ProviderName``.
        :param provider_type: ``AWS::Cognito::UserPoolIdentityProvider.ProviderType``.
        :param user_pool_id: ``AWS::Cognito::UserPoolIdentityProvider.UserPoolId``.
        :param attribute_mapping: ``AWS::Cognito::UserPoolIdentityProvider.AttributeMapping``.
        :param idp_identifiers: ``AWS::Cognito::UserPoolIdentityProvider.IdpIdentifiers``.
        :param provider_details: ``AWS::Cognito::UserPoolIdentityProvider.ProviderDetails``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpoolidentityprovider.html
        """
        self._values = {
            'provider_name': provider_name,
            'provider_type': provider_type,
            'user_pool_id': user_pool_id,
        }
        if attribute_mapping is not None: self._values["attribute_mapping"] = attribute_mapping
        if idp_identifiers is not None: self._values["idp_identifiers"] = idp_identifiers
        if provider_details is not None: self._values["provider_details"] = provider_details

    @builtins.property
    def provider_name(self) -> str:
        """``AWS::Cognito::UserPoolIdentityProvider.ProviderName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpoolidentityprovider.html#cfn-cognito-userpoolidentityprovider-providername
        """
        return self._values.get('provider_name')

    @builtins.property
    def provider_type(self) -> str:
        """``AWS::Cognito::UserPoolIdentityProvider.ProviderType``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpoolidentityprovider.html#cfn-cognito-userpoolidentityprovider-providertype
        """
        return self._values.get('provider_type')

    @builtins.property
    def user_pool_id(self) -> str:
        """``AWS::Cognito::UserPoolIdentityProvider.UserPoolId``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpoolidentityprovider.html#cfn-cognito-userpoolidentityprovider-userpoolid
        """
        return self._values.get('user_pool_id')

    @builtins.property
    def attribute_mapping(self) -> typing.Any:
        """``AWS::Cognito::UserPoolIdentityProvider.AttributeMapping``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpoolidentityprovider.html#cfn-cognito-userpoolidentityprovider-attributemapping
        """
        return self._values.get('attribute_mapping')

    @builtins.property
    def idp_identifiers(self) -> typing.Optional[typing.List[str]]:
        """``AWS::Cognito::UserPoolIdentityProvider.IdpIdentifiers``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpoolidentityprovider.html#cfn-cognito-userpoolidentityprovider-idpidentifiers
        """
        return self._values.get('idp_identifiers')

    @builtins.property
    def provider_details(self) -> typing.Any:
        """``AWS::Cognito::UserPoolIdentityProvider.ProviderDetails``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpoolidentityprovider.html#cfn-cognito-userpoolidentityprovider-providerdetails
        """
        return self._values.get('provider_details')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'CfnUserPoolIdentityProviderProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="@aws-cdk/aws-cognito.CfnUserPoolProps", jsii_struct_bases=[], name_mapping={'account_recovery_setting': 'accountRecoverySetting', 'admin_create_user_config': 'adminCreateUserConfig', 'alias_attributes': 'aliasAttributes', 'auto_verified_attributes': 'autoVerifiedAttributes', 'device_configuration': 'deviceConfiguration', 'email_configuration': 'emailConfiguration', 'email_verification_message': 'emailVerificationMessage', 'email_verification_subject': 'emailVerificationSubject', 'enabled_mfas': 'enabledMfas', 'lambda_config': 'lambdaConfig', 'mfa_configuration': 'mfaConfiguration', 'policies': 'policies', 'schema': 'schema', 'sms_authentication_message': 'smsAuthenticationMessage', 'sms_configuration': 'smsConfiguration', 'sms_verification_message': 'smsVerificationMessage', 'username_attributes': 'usernameAttributes', 'username_configuration': 'usernameConfiguration', 'user_pool_add_ons': 'userPoolAddOns', 'user_pool_name': 'userPoolName', 'user_pool_tags': 'userPoolTags', 'verification_message_template': 'verificationMessageTemplate'})
class CfnUserPoolProps():
    def __init__(self, *, account_recovery_setting: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["CfnUserPool.AccountRecoverySettingProperty"]]]=None, admin_create_user_config: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["CfnUserPool.AdminCreateUserConfigProperty"]]]=None, alias_attributes: typing.Optional[typing.List[str]]=None, auto_verified_attributes: typing.Optional[typing.List[str]]=None, device_configuration: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["CfnUserPool.DeviceConfigurationProperty"]]]=None, email_configuration: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["CfnUserPool.EmailConfigurationProperty"]]]=None, email_verification_message: typing.Optional[str]=None, email_verification_subject: typing.Optional[str]=None, enabled_mfas: typing.Optional[typing.List[str]]=None, lambda_config: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["CfnUserPool.LambdaConfigProperty"]]]=None, mfa_configuration: typing.Optional[str]=None, policies: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["CfnUserPool.PoliciesProperty"]]]=None, schema: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnUserPool.SchemaAttributeProperty"]]]]]=None, sms_authentication_message: typing.Optional[str]=None, sms_configuration: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["CfnUserPool.SmsConfigurationProperty"]]]=None, sms_verification_message: typing.Optional[str]=None, username_attributes: typing.Optional[typing.List[str]]=None, username_configuration: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["CfnUserPool.UsernameConfigurationProperty"]]]=None, user_pool_add_ons: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["CfnUserPool.UserPoolAddOnsProperty"]]]=None, user_pool_name: typing.Optional[str]=None, user_pool_tags: typing.Any=None, verification_message_template: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["CfnUserPool.VerificationMessageTemplateProperty"]]]=None) -> None:
        """Properties for defining a ``AWS::Cognito::UserPool``.

        :param account_recovery_setting: ``AWS::Cognito::UserPool.AccountRecoverySetting``.
        :param admin_create_user_config: ``AWS::Cognito::UserPool.AdminCreateUserConfig``.
        :param alias_attributes: ``AWS::Cognito::UserPool.AliasAttributes``.
        :param auto_verified_attributes: ``AWS::Cognito::UserPool.AutoVerifiedAttributes``.
        :param device_configuration: ``AWS::Cognito::UserPool.DeviceConfiguration``.
        :param email_configuration: ``AWS::Cognito::UserPool.EmailConfiguration``.
        :param email_verification_message: ``AWS::Cognito::UserPool.EmailVerificationMessage``.
        :param email_verification_subject: ``AWS::Cognito::UserPool.EmailVerificationSubject``.
        :param enabled_mfas: ``AWS::Cognito::UserPool.EnabledMfas``.
        :param lambda_config: ``AWS::Cognito::UserPool.LambdaConfig``.
        :param mfa_configuration: ``AWS::Cognito::UserPool.MfaConfiguration``.
        :param policies: ``AWS::Cognito::UserPool.Policies``.
        :param schema: ``AWS::Cognito::UserPool.Schema``.
        :param sms_authentication_message: ``AWS::Cognito::UserPool.SmsAuthenticationMessage``.
        :param sms_configuration: ``AWS::Cognito::UserPool.SmsConfiguration``.
        :param sms_verification_message: ``AWS::Cognito::UserPool.SmsVerificationMessage``.
        :param username_attributes: ``AWS::Cognito::UserPool.UsernameAttributes``.
        :param username_configuration: ``AWS::Cognito::UserPool.UsernameConfiguration``.
        :param user_pool_add_ons: ``AWS::Cognito::UserPool.UserPoolAddOns``.
        :param user_pool_name: ``AWS::Cognito::UserPool.UserPoolName``.
        :param user_pool_tags: ``AWS::Cognito::UserPool.UserPoolTags``.
        :param verification_message_template: ``AWS::Cognito::UserPool.VerificationMessageTemplate``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpool.html
        """
        self._values = {
        }
        if account_recovery_setting is not None: self._values["account_recovery_setting"] = account_recovery_setting
        if admin_create_user_config is not None: self._values["admin_create_user_config"] = admin_create_user_config
        if alias_attributes is not None: self._values["alias_attributes"] = alias_attributes
        if auto_verified_attributes is not None: self._values["auto_verified_attributes"] = auto_verified_attributes
        if device_configuration is not None: self._values["device_configuration"] = device_configuration
        if email_configuration is not None: self._values["email_configuration"] = email_configuration
        if email_verification_message is not None: self._values["email_verification_message"] = email_verification_message
        if email_verification_subject is not None: self._values["email_verification_subject"] = email_verification_subject
        if enabled_mfas is not None: self._values["enabled_mfas"] = enabled_mfas
        if lambda_config is not None: self._values["lambda_config"] = lambda_config
        if mfa_configuration is not None: self._values["mfa_configuration"] = mfa_configuration
        if policies is not None: self._values["policies"] = policies
        if schema is not None: self._values["schema"] = schema
        if sms_authentication_message is not None: self._values["sms_authentication_message"] = sms_authentication_message
        if sms_configuration is not None: self._values["sms_configuration"] = sms_configuration
        if sms_verification_message is not None: self._values["sms_verification_message"] = sms_verification_message
        if username_attributes is not None: self._values["username_attributes"] = username_attributes
        if username_configuration is not None: self._values["username_configuration"] = username_configuration
        if user_pool_add_ons is not None: self._values["user_pool_add_ons"] = user_pool_add_ons
        if user_pool_name is not None: self._values["user_pool_name"] = user_pool_name
        if user_pool_tags is not None: self._values["user_pool_tags"] = user_pool_tags
        if verification_message_template is not None: self._values["verification_message_template"] = verification_message_template

    @builtins.property
    def account_recovery_setting(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["CfnUserPool.AccountRecoverySettingProperty"]]]:
        """``AWS::Cognito::UserPool.AccountRecoverySetting``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpool.html#cfn-cognito-userpool-accountrecoverysetting
        """
        return self._values.get('account_recovery_setting')

    @builtins.property
    def admin_create_user_config(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["CfnUserPool.AdminCreateUserConfigProperty"]]]:
        """``AWS::Cognito::UserPool.AdminCreateUserConfig``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpool.html#cfn-cognito-userpool-admincreateuserconfig
        """
        return self._values.get('admin_create_user_config')

    @builtins.property
    def alias_attributes(self) -> typing.Optional[typing.List[str]]:
        """``AWS::Cognito::UserPool.AliasAttributes``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpool.html#cfn-cognito-userpool-aliasattributes
        """
        return self._values.get('alias_attributes')

    @builtins.property
    def auto_verified_attributes(self) -> typing.Optional[typing.List[str]]:
        """``AWS::Cognito::UserPool.AutoVerifiedAttributes``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpool.html#cfn-cognito-userpool-autoverifiedattributes
        """
        return self._values.get('auto_verified_attributes')

    @builtins.property
    def device_configuration(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["CfnUserPool.DeviceConfigurationProperty"]]]:
        """``AWS::Cognito::UserPool.DeviceConfiguration``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpool.html#cfn-cognito-userpool-deviceconfiguration
        """
        return self._values.get('device_configuration')

    @builtins.property
    def email_configuration(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["CfnUserPool.EmailConfigurationProperty"]]]:
        """``AWS::Cognito::UserPool.EmailConfiguration``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpool.html#cfn-cognito-userpool-emailconfiguration
        """
        return self._values.get('email_configuration')

    @builtins.property
    def email_verification_message(self) -> typing.Optional[str]:
        """``AWS::Cognito::UserPool.EmailVerificationMessage``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpool.html#cfn-cognito-userpool-emailverificationmessage
        """
        return self._values.get('email_verification_message')

    @builtins.property
    def email_verification_subject(self) -> typing.Optional[str]:
        """``AWS::Cognito::UserPool.EmailVerificationSubject``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpool.html#cfn-cognito-userpool-emailverificationsubject
        """
        return self._values.get('email_verification_subject')

    @builtins.property
    def enabled_mfas(self) -> typing.Optional[typing.List[str]]:
        """``AWS::Cognito::UserPool.EnabledMfas``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpool.html#cfn-cognito-userpool-enabledmfas
        """
        return self._values.get('enabled_mfas')

    @builtins.property
    def lambda_config(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["CfnUserPool.LambdaConfigProperty"]]]:
        """``AWS::Cognito::UserPool.LambdaConfig``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpool.html#cfn-cognito-userpool-lambdaconfig
        """
        return self._values.get('lambda_config')

    @builtins.property
    def mfa_configuration(self) -> typing.Optional[str]:
        """``AWS::Cognito::UserPool.MfaConfiguration``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpool.html#cfn-cognito-userpool-mfaconfiguration
        """
        return self._values.get('mfa_configuration')

    @builtins.property
    def policies(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["CfnUserPool.PoliciesProperty"]]]:
        """``AWS::Cognito::UserPool.Policies``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpool.html#cfn-cognito-userpool-policies
        """
        return self._values.get('policies')

    @builtins.property
    def schema(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnUserPool.SchemaAttributeProperty"]]]]]:
        """``AWS::Cognito::UserPool.Schema``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpool.html#cfn-cognito-userpool-schema
        """
        return self._values.get('schema')

    @builtins.property
    def sms_authentication_message(self) -> typing.Optional[str]:
        """``AWS::Cognito::UserPool.SmsAuthenticationMessage``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpool.html#cfn-cognito-userpool-smsauthenticationmessage
        """
        return self._values.get('sms_authentication_message')

    @builtins.property
    def sms_configuration(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["CfnUserPool.SmsConfigurationProperty"]]]:
        """``AWS::Cognito::UserPool.SmsConfiguration``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpool.html#cfn-cognito-userpool-smsconfiguration
        """
        return self._values.get('sms_configuration')

    @builtins.property
    def sms_verification_message(self) -> typing.Optional[str]:
        """``AWS::Cognito::UserPool.SmsVerificationMessage``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpool.html#cfn-cognito-userpool-smsverificationmessage
        """
        return self._values.get('sms_verification_message')

    @builtins.property
    def username_attributes(self) -> typing.Optional[typing.List[str]]:
        """``AWS::Cognito::UserPool.UsernameAttributes``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpool.html#cfn-cognito-userpool-usernameattributes
        """
        return self._values.get('username_attributes')

    @builtins.property
    def username_configuration(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["CfnUserPool.UsernameConfigurationProperty"]]]:
        """``AWS::Cognito::UserPool.UsernameConfiguration``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpool.html#cfn-cognito-userpool-usernameconfiguration
        """
        return self._values.get('username_configuration')

    @builtins.property
    def user_pool_add_ons(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["CfnUserPool.UserPoolAddOnsProperty"]]]:
        """``AWS::Cognito::UserPool.UserPoolAddOns``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpool.html#cfn-cognito-userpool-userpooladdons
        """
        return self._values.get('user_pool_add_ons')

    @builtins.property
    def user_pool_name(self) -> typing.Optional[str]:
        """``AWS::Cognito::UserPool.UserPoolName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpool.html#cfn-cognito-userpool-userpoolname
        """
        return self._values.get('user_pool_name')

    @builtins.property
    def user_pool_tags(self) -> typing.Any:
        """``AWS::Cognito::UserPool.UserPoolTags``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpool.html#cfn-cognito-userpool-userpooltags
        """
        return self._values.get('user_pool_tags')

    @builtins.property
    def verification_message_template(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["CfnUserPool.VerificationMessageTemplateProperty"]]]:
        """``AWS::Cognito::UserPool.VerificationMessageTemplate``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpool.html#cfn-cognito-userpool-verificationmessagetemplate
        """
        return self._values.get('verification_message_template')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'CfnUserPoolProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.implements(aws_cdk.core.IInspectable)
class CfnUserPoolResourceServer(aws_cdk.core.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-cognito.CfnUserPoolResourceServer"):
    """A CloudFormation ``AWS::Cognito::UserPoolResourceServer``.

    see
    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpoolresourceserver.html
    cloudformationResource:
    :cloudformationResource:: AWS::Cognito::UserPoolResourceServer
    """
    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, identifier: str, name: str, user_pool_id: str, scopes: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union[aws_cdk.core.IResolvable, "ResourceServerScopeTypeProperty"]]]]]=None) -> None:
        """Create a new ``AWS::Cognito::UserPoolResourceServer``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param identifier: ``AWS::Cognito::UserPoolResourceServer.Identifier``.
        :param name: ``AWS::Cognito::UserPoolResourceServer.Name``.
        :param user_pool_id: ``AWS::Cognito::UserPoolResourceServer.UserPoolId``.
        :param scopes: ``AWS::Cognito::UserPoolResourceServer.Scopes``.
        """
        props = CfnUserPoolResourceServerProps(identifier=identifier, name=name, user_pool_id=user_pool_id, scopes=scopes)

        jsii.create(CfnUserPoolResourceServer, self, [scope, id, props])

    @jsii.member(jsii_name="fromCloudFormation")
    @builtins.classmethod
    def from_cloud_formation(cls, scope: aws_cdk.core.Construct, id: str, resource_attributes: typing.Any, *, finder: aws_cdk.core.ICfnFinder) -> "CfnUserPoolResourceServer":
        """A factory method that creates a new instance of this class from an object containing the CloudFormation properties of this resource.

        Used in the @aws-cdk/cloudformation-include module.

        :param scope: -
        :param id: -
        :param resource_attributes: -
        :param finder: The finder interface used to resolve references across the template.

        stability
        :stability: experimental
        """
        options = aws_cdk.core.FromCloudFormationOptions(finder=finder)

        return jsii.sinvoke(cls, "fromCloudFormation", [scope, id, resource_attributes, options])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: aws_cdk.core.TreeInspector) -> None:
        """Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "inspect", [inspector])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, props: typing.Mapping[str, typing.Any]) -> typing.Mapping[str, typing.Any]:
        """
        :param props: -
        """
        return jsii.invoke(self, "renderProperties", [props])

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> str:
        """The CloudFormation resource type name for this resource class."""
        return jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME")

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[str, typing.Any]:
        return jsii.get(self, "cfnProperties")

    @builtins.property
    @jsii.member(jsii_name="identifier")
    def identifier(self) -> str:
        """``AWS::Cognito::UserPoolResourceServer.Identifier``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpoolresourceserver.html#cfn-cognito-userpoolresourceserver-identifier
        """
        return jsii.get(self, "identifier")

    @identifier.setter
    def identifier(self, value: str):
        jsii.set(self, "identifier", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> str:
        """``AWS::Cognito::UserPoolResourceServer.Name``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpoolresourceserver.html#cfn-cognito-userpoolresourceserver-name
        """
        return jsii.get(self, "name")

    @name.setter
    def name(self, value: str):
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="userPoolId")
    def user_pool_id(self) -> str:
        """``AWS::Cognito::UserPoolResourceServer.UserPoolId``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpoolresourceserver.html#cfn-cognito-userpoolresourceserver-userpoolid
        """
        return jsii.get(self, "userPoolId")

    @user_pool_id.setter
    def user_pool_id(self, value: str):
        jsii.set(self, "userPoolId", value)

    @builtins.property
    @jsii.member(jsii_name="scopes")
    def scopes(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union[aws_cdk.core.IResolvable, "ResourceServerScopeTypeProperty"]]]]]:
        """``AWS::Cognito::UserPoolResourceServer.Scopes``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpoolresourceserver.html#cfn-cognito-userpoolresourceserver-scopes
        """
        return jsii.get(self, "scopes")

    @scopes.setter
    def scopes(self, value: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union[aws_cdk.core.IResolvable, "ResourceServerScopeTypeProperty"]]]]]):
        jsii.set(self, "scopes", value)

    @jsii.data_type(jsii_type="@aws-cdk/aws-cognito.CfnUserPoolResourceServer.ResourceServerScopeTypeProperty", jsii_struct_bases=[], name_mapping={'scope_description': 'scopeDescription', 'scope_name': 'scopeName'})
    class ResourceServerScopeTypeProperty():
        def __init__(self, *, scope_description: str, scope_name: str) -> None:
            """
            :param scope_description: ``CfnUserPoolResourceServer.ResourceServerScopeTypeProperty.ScopeDescription``.
            :param scope_name: ``CfnUserPoolResourceServer.ResourceServerScopeTypeProperty.ScopeName``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-userpoolresourceserver-resourceserverscopetype.html
            """
            self._values = {
                'scope_description': scope_description,
                'scope_name': scope_name,
            }

        @builtins.property
        def scope_description(self) -> str:
            """``CfnUserPoolResourceServer.ResourceServerScopeTypeProperty.ScopeDescription``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-userpoolresourceserver-resourceserverscopetype.html#cfn-cognito-userpoolresourceserver-resourceserverscopetype-scopedescription
            """
            return self._values.get('scope_description')

        @builtins.property
        def scope_name(self) -> str:
            """``CfnUserPoolResourceServer.ResourceServerScopeTypeProperty.ScopeName``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-userpoolresourceserver-resourceserverscopetype.html#cfn-cognito-userpoolresourceserver-resourceserverscopetype-scopename
            """
            return self._values.get('scope_name')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'ResourceServerScopeTypeProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())



@jsii.data_type(jsii_type="@aws-cdk/aws-cognito.CfnUserPoolResourceServerProps", jsii_struct_bases=[], name_mapping={'identifier': 'identifier', 'name': 'name', 'user_pool_id': 'userPoolId', 'scopes': 'scopes'})
class CfnUserPoolResourceServerProps():
    def __init__(self, *, identifier: str, name: str, user_pool_id: str, scopes: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnUserPoolResourceServer.ResourceServerScopeTypeProperty"]]]]]=None) -> None:
        """Properties for defining a ``AWS::Cognito::UserPoolResourceServer``.

        :param identifier: ``AWS::Cognito::UserPoolResourceServer.Identifier``.
        :param name: ``AWS::Cognito::UserPoolResourceServer.Name``.
        :param user_pool_id: ``AWS::Cognito::UserPoolResourceServer.UserPoolId``.
        :param scopes: ``AWS::Cognito::UserPoolResourceServer.Scopes``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpoolresourceserver.html
        """
        self._values = {
            'identifier': identifier,
            'name': name,
            'user_pool_id': user_pool_id,
        }
        if scopes is not None: self._values["scopes"] = scopes

    @builtins.property
    def identifier(self) -> str:
        """``AWS::Cognito::UserPoolResourceServer.Identifier``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpoolresourceserver.html#cfn-cognito-userpoolresourceserver-identifier
        """
        return self._values.get('identifier')

    @builtins.property
    def name(self) -> str:
        """``AWS::Cognito::UserPoolResourceServer.Name``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpoolresourceserver.html#cfn-cognito-userpoolresourceserver-name
        """
        return self._values.get('name')

    @builtins.property
    def user_pool_id(self) -> str:
        """``AWS::Cognito::UserPoolResourceServer.UserPoolId``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpoolresourceserver.html#cfn-cognito-userpoolresourceserver-userpoolid
        """
        return self._values.get('user_pool_id')

    @builtins.property
    def scopes(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnUserPoolResourceServer.ResourceServerScopeTypeProperty"]]]]]:
        """``AWS::Cognito::UserPoolResourceServer.Scopes``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpoolresourceserver.html#cfn-cognito-userpoolresourceserver-scopes
        """
        return self._values.get('scopes')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'CfnUserPoolResourceServerProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.implements(aws_cdk.core.IInspectable)
class CfnUserPoolRiskConfigurationAttachment(aws_cdk.core.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-cognito.CfnUserPoolRiskConfigurationAttachment"):
    """A CloudFormation ``AWS::Cognito::UserPoolRiskConfigurationAttachment``.

    see
    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpoolriskconfigurationattachment.html
    cloudformationResource:
    :cloudformationResource:: AWS::Cognito::UserPoolRiskConfigurationAttachment
    """
    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, client_id: str, user_pool_id: str, account_takeover_risk_configuration: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["AccountTakeoverRiskConfigurationTypeProperty"]]]=None, compromised_credentials_risk_configuration: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["CompromisedCredentialsRiskConfigurationTypeProperty"]]]=None, risk_exception_configuration: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["RiskExceptionConfigurationTypeProperty"]]]=None) -> None:
        """Create a new ``AWS::Cognito::UserPoolRiskConfigurationAttachment``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param client_id: ``AWS::Cognito::UserPoolRiskConfigurationAttachment.ClientId``.
        :param user_pool_id: ``AWS::Cognito::UserPoolRiskConfigurationAttachment.UserPoolId``.
        :param account_takeover_risk_configuration: ``AWS::Cognito::UserPoolRiskConfigurationAttachment.AccountTakeoverRiskConfiguration``.
        :param compromised_credentials_risk_configuration: ``AWS::Cognito::UserPoolRiskConfigurationAttachment.CompromisedCredentialsRiskConfiguration``.
        :param risk_exception_configuration: ``AWS::Cognito::UserPoolRiskConfigurationAttachment.RiskExceptionConfiguration``.
        """
        props = CfnUserPoolRiskConfigurationAttachmentProps(client_id=client_id, user_pool_id=user_pool_id, account_takeover_risk_configuration=account_takeover_risk_configuration, compromised_credentials_risk_configuration=compromised_credentials_risk_configuration, risk_exception_configuration=risk_exception_configuration)

        jsii.create(CfnUserPoolRiskConfigurationAttachment, self, [scope, id, props])

    @jsii.member(jsii_name="fromCloudFormation")
    @builtins.classmethod
    def from_cloud_formation(cls, scope: aws_cdk.core.Construct, id: str, resource_attributes: typing.Any, *, finder: aws_cdk.core.ICfnFinder) -> "CfnUserPoolRiskConfigurationAttachment":
        """A factory method that creates a new instance of this class from an object containing the CloudFormation properties of this resource.

        Used in the @aws-cdk/cloudformation-include module.

        :param scope: -
        :param id: -
        :param resource_attributes: -
        :param finder: The finder interface used to resolve references across the template.

        stability
        :stability: experimental
        """
        options = aws_cdk.core.FromCloudFormationOptions(finder=finder)

        return jsii.sinvoke(cls, "fromCloudFormation", [scope, id, resource_attributes, options])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: aws_cdk.core.TreeInspector) -> None:
        """Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "inspect", [inspector])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, props: typing.Mapping[str, typing.Any]) -> typing.Mapping[str, typing.Any]:
        """
        :param props: -
        """
        return jsii.invoke(self, "renderProperties", [props])

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> str:
        """The CloudFormation resource type name for this resource class."""
        return jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME")

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[str, typing.Any]:
        return jsii.get(self, "cfnProperties")

    @builtins.property
    @jsii.member(jsii_name="clientId")
    def client_id(self) -> str:
        """``AWS::Cognito::UserPoolRiskConfigurationAttachment.ClientId``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpoolriskconfigurationattachment.html#cfn-cognito-userpoolriskconfigurationattachment-clientid
        """
        return jsii.get(self, "clientId")

    @client_id.setter
    def client_id(self, value: str):
        jsii.set(self, "clientId", value)

    @builtins.property
    @jsii.member(jsii_name="userPoolId")
    def user_pool_id(self) -> str:
        """``AWS::Cognito::UserPoolRiskConfigurationAttachment.UserPoolId``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpoolriskconfigurationattachment.html#cfn-cognito-userpoolriskconfigurationattachment-userpoolid
        """
        return jsii.get(self, "userPoolId")

    @user_pool_id.setter
    def user_pool_id(self, value: str):
        jsii.set(self, "userPoolId", value)

    @builtins.property
    @jsii.member(jsii_name="accountTakeoverRiskConfiguration")
    def account_takeover_risk_configuration(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["AccountTakeoverRiskConfigurationTypeProperty"]]]:
        """``AWS::Cognito::UserPoolRiskConfigurationAttachment.AccountTakeoverRiskConfiguration``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpoolriskconfigurationattachment.html#cfn-cognito-userpoolriskconfigurationattachment-accounttakeoverriskconfiguration
        """
        return jsii.get(self, "accountTakeoverRiskConfiguration")

    @account_takeover_risk_configuration.setter
    def account_takeover_risk_configuration(self, value: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["AccountTakeoverRiskConfigurationTypeProperty"]]]):
        jsii.set(self, "accountTakeoverRiskConfiguration", value)

    @builtins.property
    @jsii.member(jsii_name="compromisedCredentialsRiskConfiguration")
    def compromised_credentials_risk_configuration(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["CompromisedCredentialsRiskConfigurationTypeProperty"]]]:
        """``AWS::Cognito::UserPoolRiskConfigurationAttachment.CompromisedCredentialsRiskConfiguration``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpoolriskconfigurationattachment.html#cfn-cognito-userpoolriskconfigurationattachment-compromisedcredentialsriskconfiguration
        """
        return jsii.get(self, "compromisedCredentialsRiskConfiguration")

    @compromised_credentials_risk_configuration.setter
    def compromised_credentials_risk_configuration(self, value: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["CompromisedCredentialsRiskConfigurationTypeProperty"]]]):
        jsii.set(self, "compromisedCredentialsRiskConfiguration", value)

    @builtins.property
    @jsii.member(jsii_name="riskExceptionConfiguration")
    def risk_exception_configuration(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["RiskExceptionConfigurationTypeProperty"]]]:
        """``AWS::Cognito::UserPoolRiskConfigurationAttachment.RiskExceptionConfiguration``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpoolriskconfigurationattachment.html#cfn-cognito-userpoolriskconfigurationattachment-riskexceptionconfiguration
        """
        return jsii.get(self, "riskExceptionConfiguration")

    @risk_exception_configuration.setter
    def risk_exception_configuration(self, value: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["RiskExceptionConfigurationTypeProperty"]]]):
        jsii.set(self, "riskExceptionConfiguration", value)

    @jsii.data_type(jsii_type="@aws-cdk/aws-cognito.CfnUserPoolRiskConfigurationAttachment.AccountTakeoverActionTypeProperty", jsii_struct_bases=[], name_mapping={'event_action': 'eventAction', 'notify': 'notify'})
    class AccountTakeoverActionTypeProperty():
        def __init__(self, *, event_action: str, notify: typing.Union[bool, aws_cdk.core.IResolvable]) -> None:
            """
            :param event_action: ``CfnUserPoolRiskConfigurationAttachment.AccountTakeoverActionTypeProperty.EventAction``.
            :param notify: ``CfnUserPoolRiskConfigurationAttachment.AccountTakeoverActionTypeProperty.Notify``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-userpoolriskconfigurationattachment-accounttakeoveractiontype.html
            """
            self._values = {
                'event_action': event_action,
                'notify': notify,
            }

        @builtins.property
        def event_action(self) -> str:
            """``CfnUserPoolRiskConfigurationAttachment.AccountTakeoverActionTypeProperty.EventAction``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-userpoolriskconfigurationattachment-accounttakeoveractiontype.html#cfn-cognito-userpoolriskconfigurationattachment-accounttakeoveractiontype-eventaction
            """
            return self._values.get('event_action')

        @builtins.property
        def notify(self) -> typing.Union[bool, aws_cdk.core.IResolvable]:
            """``CfnUserPoolRiskConfigurationAttachment.AccountTakeoverActionTypeProperty.Notify``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-userpoolriskconfigurationattachment-accounttakeoveractiontype.html#cfn-cognito-userpoolriskconfigurationattachment-accounttakeoveractiontype-notify
            """
            return self._values.get('notify')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'AccountTakeoverActionTypeProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="@aws-cdk/aws-cognito.CfnUserPoolRiskConfigurationAttachment.AccountTakeoverActionsTypeProperty", jsii_struct_bases=[], name_mapping={'high_action': 'highAction', 'low_action': 'lowAction', 'medium_action': 'mediumAction'})
    class AccountTakeoverActionsTypeProperty():
        def __init__(self, *, high_action: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["CfnUserPoolRiskConfigurationAttachment.AccountTakeoverActionTypeProperty"]]]=None, low_action: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["CfnUserPoolRiskConfigurationAttachment.AccountTakeoverActionTypeProperty"]]]=None, medium_action: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["CfnUserPoolRiskConfigurationAttachment.AccountTakeoverActionTypeProperty"]]]=None) -> None:
            """
            :param high_action: ``CfnUserPoolRiskConfigurationAttachment.AccountTakeoverActionsTypeProperty.HighAction``.
            :param low_action: ``CfnUserPoolRiskConfigurationAttachment.AccountTakeoverActionsTypeProperty.LowAction``.
            :param medium_action: ``CfnUserPoolRiskConfigurationAttachment.AccountTakeoverActionsTypeProperty.MediumAction``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-userpoolriskconfigurationattachment-accounttakeoveractionstype.html
            """
            self._values = {
            }
            if high_action is not None: self._values["high_action"] = high_action
            if low_action is not None: self._values["low_action"] = low_action
            if medium_action is not None: self._values["medium_action"] = medium_action

        @builtins.property
        def high_action(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["CfnUserPoolRiskConfigurationAttachment.AccountTakeoverActionTypeProperty"]]]:
            """``CfnUserPoolRiskConfigurationAttachment.AccountTakeoverActionsTypeProperty.HighAction``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-userpoolriskconfigurationattachment-accounttakeoveractionstype.html#cfn-cognito-userpoolriskconfigurationattachment-accounttakeoveractionstype-highaction
            """
            return self._values.get('high_action')

        @builtins.property
        def low_action(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["CfnUserPoolRiskConfigurationAttachment.AccountTakeoverActionTypeProperty"]]]:
            """``CfnUserPoolRiskConfigurationAttachment.AccountTakeoverActionsTypeProperty.LowAction``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-userpoolriskconfigurationattachment-accounttakeoveractionstype.html#cfn-cognito-userpoolriskconfigurationattachment-accounttakeoveractionstype-lowaction
            """
            return self._values.get('low_action')

        @builtins.property
        def medium_action(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["CfnUserPoolRiskConfigurationAttachment.AccountTakeoverActionTypeProperty"]]]:
            """``CfnUserPoolRiskConfigurationAttachment.AccountTakeoverActionsTypeProperty.MediumAction``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-userpoolriskconfigurationattachment-accounttakeoveractionstype.html#cfn-cognito-userpoolriskconfigurationattachment-accounttakeoveractionstype-mediumaction
            """
            return self._values.get('medium_action')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'AccountTakeoverActionsTypeProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="@aws-cdk/aws-cognito.CfnUserPoolRiskConfigurationAttachment.AccountTakeoverRiskConfigurationTypeProperty", jsii_struct_bases=[], name_mapping={'actions': 'actions', 'notify_configuration': 'notifyConfiguration'})
    class AccountTakeoverRiskConfigurationTypeProperty():
        def __init__(self, *, actions: typing.Union[aws_cdk.core.IResolvable, "CfnUserPoolRiskConfigurationAttachment.AccountTakeoverActionsTypeProperty"], notify_configuration: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["CfnUserPoolRiskConfigurationAttachment.NotifyConfigurationTypeProperty"]]]=None) -> None:
            """
            :param actions: ``CfnUserPoolRiskConfigurationAttachment.AccountTakeoverRiskConfigurationTypeProperty.Actions``.
            :param notify_configuration: ``CfnUserPoolRiskConfigurationAttachment.AccountTakeoverRiskConfigurationTypeProperty.NotifyConfiguration``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-userpoolriskconfigurationattachment-accounttakeoverriskconfigurationtype.html
            """
            self._values = {
                'actions': actions,
            }
            if notify_configuration is not None: self._values["notify_configuration"] = notify_configuration

        @builtins.property
        def actions(self) -> typing.Union[aws_cdk.core.IResolvable, "CfnUserPoolRiskConfigurationAttachment.AccountTakeoverActionsTypeProperty"]:
            """``CfnUserPoolRiskConfigurationAttachment.AccountTakeoverRiskConfigurationTypeProperty.Actions``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-userpoolriskconfigurationattachment-accounttakeoverriskconfigurationtype.html#cfn-cognito-userpoolriskconfigurationattachment-accounttakeoverriskconfigurationtype-actions
            """
            return self._values.get('actions')

        @builtins.property
        def notify_configuration(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["CfnUserPoolRiskConfigurationAttachment.NotifyConfigurationTypeProperty"]]]:
            """``CfnUserPoolRiskConfigurationAttachment.AccountTakeoverRiskConfigurationTypeProperty.NotifyConfiguration``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-userpoolriskconfigurationattachment-accounttakeoverriskconfigurationtype.html#cfn-cognito-userpoolriskconfigurationattachment-accounttakeoverriskconfigurationtype-notifyconfiguration
            """
            return self._values.get('notify_configuration')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'AccountTakeoverRiskConfigurationTypeProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="@aws-cdk/aws-cognito.CfnUserPoolRiskConfigurationAttachment.CompromisedCredentialsActionsTypeProperty", jsii_struct_bases=[], name_mapping={'event_action': 'eventAction'})
    class CompromisedCredentialsActionsTypeProperty():
        def __init__(self, *, event_action: str) -> None:
            """
            :param event_action: ``CfnUserPoolRiskConfigurationAttachment.CompromisedCredentialsActionsTypeProperty.EventAction``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-userpoolriskconfigurationattachment-compromisedcredentialsactionstype.html
            """
            self._values = {
                'event_action': event_action,
            }

        @builtins.property
        def event_action(self) -> str:
            """``CfnUserPoolRiskConfigurationAttachment.CompromisedCredentialsActionsTypeProperty.EventAction``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-userpoolriskconfigurationattachment-compromisedcredentialsactionstype.html#cfn-cognito-userpoolriskconfigurationattachment-compromisedcredentialsactionstype-eventaction
            """
            return self._values.get('event_action')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'CompromisedCredentialsActionsTypeProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="@aws-cdk/aws-cognito.CfnUserPoolRiskConfigurationAttachment.CompromisedCredentialsRiskConfigurationTypeProperty", jsii_struct_bases=[], name_mapping={'actions': 'actions', 'event_filter': 'eventFilter'})
    class CompromisedCredentialsRiskConfigurationTypeProperty():
        def __init__(self, *, actions: typing.Union[aws_cdk.core.IResolvable, "CfnUserPoolRiskConfigurationAttachment.CompromisedCredentialsActionsTypeProperty"], event_filter: typing.Optional[typing.List[str]]=None) -> None:
            """
            :param actions: ``CfnUserPoolRiskConfigurationAttachment.CompromisedCredentialsRiskConfigurationTypeProperty.Actions``.
            :param event_filter: ``CfnUserPoolRiskConfigurationAttachment.CompromisedCredentialsRiskConfigurationTypeProperty.EventFilter``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-userpoolriskconfigurationattachment-compromisedcredentialsriskconfigurationtype.html
            """
            self._values = {
                'actions': actions,
            }
            if event_filter is not None: self._values["event_filter"] = event_filter

        @builtins.property
        def actions(self) -> typing.Union[aws_cdk.core.IResolvable, "CfnUserPoolRiskConfigurationAttachment.CompromisedCredentialsActionsTypeProperty"]:
            """``CfnUserPoolRiskConfigurationAttachment.CompromisedCredentialsRiskConfigurationTypeProperty.Actions``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-userpoolriskconfigurationattachment-compromisedcredentialsriskconfigurationtype.html#cfn-cognito-userpoolriskconfigurationattachment-compromisedcredentialsriskconfigurationtype-actions
            """
            return self._values.get('actions')

        @builtins.property
        def event_filter(self) -> typing.Optional[typing.List[str]]:
            """``CfnUserPoolRiskConfigurationAttachment.CompromisedCredentialsRiskConfigurationTypeProperty.EventFilter``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-userpoolriskconfigurationattachment-compromisedcredentialsriskconfigurationtype.html#cfn-cognito-userpoolriskconfigurationattachment-compromisedcredentialsriskconfigurationtype-eventfilter
            """
            return self._values.get('event_filter')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'CompromisedCredentialsRiskConfigurationTypeProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="@aws-cdk/aws-cognito.CfnUserPoolRiskConfigurationAttachment.NotifyConfigurationTypeProperty", jsii_struct_bases=[], name_mapping={'source_arn': 'sourceArn', 'block_email': 'blockEmail', 'from_': 'from', 'mfa_email': 'mfaEmail', 'no_action_email': 'noActionEmail', 'reply_to': 'replyTo'})
    class NotifyConfigurationTypeProperty():
        def __init__(self, *, source_arn: str, block_email: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["CfnUserPoolRiskConfigurationAttachment.NotifyEmailTypeProperty"]]]=None, from_: typing.Optional[str]=None, mfa_email: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["CfnUserPoolRiskConfigurationAttachment.NotifyEmailTypeProperty"]]]=None, no_action_email: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["CfnUserPoolRiskConfigurationAttachment.NotifyEmailTypeProperty"]]]=None, reply_to: typing.Optional[str]=None) -> None:
            """
            :param source_arn: ``CfnUserPoolRiskConfigurationAttachment.NotifyConfigurationTypeProperty.SourceArn``.
            :param block_email: ``CfnUserPoolRiskConfigurationAttachment.NotifyConfigurationTypeProperty.BlockEmail``.
            :param from_: ``CfnUserPoolRiskConfigurationAttachment.NotifyConfigurationTypeProperty.From``.
            :param mfa_email: ``CfnUserPoolRiskConfigurationAttachment.NotifyConfigurationTypeProperty.MfaEmail``.
            :param no_action_email: ``CfnUserPoolRiskConfigurationAttachment.NotifyConfigurationTypeProperty.NoActionEmail``.
            :param reply_to: ``CfnUserPoolRiskConfigurationAttachment.NotifyConfigurationTypeProperty.ReplyTo``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-userpoolriskconfigurationattachment-notifyconfigurationtype.html
            """
            self._values = {
                'source_arn': source_arn,
            }
            if block_email is not None: self._values["block_email"] = block_email
            if from_ is not None: self._values["from_"] = from_
            if mfa_email is not None: self._values["mfa_email"] = mfa_email
            if no_action_email is not None: self._values["no_action_email"] = no_action_email
            if reply_to is not None: self._values["reply_to"] = reply_to

        @builtins.property
        def source_arn(self) -> str:
            """``CfnUserPoolRiskConfigurationAttachment.NotifyConfigurationTypeProperty.SourceArn``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-userpoolriskconfigurationattachment-notifyconfigurationtype.html#cfn-cognito-userpoolriskconfigurationattachment-notifyconfigurationtype-sourcearn
            """
            return self._values.get('source_arn')

        @builtins.property
        def block_email(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["CfnUserPoolRiskConfigurationAttachment.NotifyEmailTypeProperty"]]]:
            """``CfnUserPoolRiskConfigurationAttachment.NotifyConfigurationTypeProperty.BlockEmail``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-userpoolriskconfigurationattachment-notifyconfigurationtype.html#cfn-cognito-userpoolriskconfigurationattachment-notifyconfigurationtype-blockemail
            """
            return self._values.get('block_email')

        @builtins.property
        def from_(self) -> typing.Optional[str]:
            """``CfnUserPoolRiskConfigurationAttachment.NotifyConfigurationTypeProperty.From``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-userpoolriskconfigurationattachment-notifyconfigurationtype.html#cfn-cognito-userpoolriskconfigurationattachment-notifyconfigurationtype-from
            """
            return self._values.get('from_')

        @builtins.property
        def mfa_email(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["CfnUserPoolRiskConfigurationAttachment.NotifyEmailTypeProperty"]]]:
            """``CfnUserPoolRiskConfigurationAttachment.NotifyConfigurationTypeProperty.MfaEmail``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-userpoolriskconfigurationattachment-notifyconfigurationtype.html#cfn-cognito-userpoolriskconfigurationattachment-notifyconfigurationtype-mfaemail
            """
            return self._values.get('mfa_email')

        @builtins.property
        def no_action_email(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["CfnUserPoolRiskConfigurationAttachment.NotifyEmailTypeProperty"]]]:
            """``CfnUserPoolRiskConfigurationAttachment.NotifyConfigurationTypeProperty.NoActionEmail``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-userpoolriskconfigurationattachment-notifyconfigurationtype.html#cfn-cognito-userpoolriskconfigurationattachment-notifyconfigurationtype-noactionemail
            """
            return self._values.get('no_action_email')

        @builtins.property
        def reply_to(self) -> typing.Optional[str]:
            """``CfnUserPoolRiskConfigurationAttachment.NotifyConfigurationTypeProperty.ReplyTo``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-userpoolriskconfigurationattachment-notifyconfigurationtype.html#cfn-cognito-userpoolriskconfigurationattachment-notifyconfigurationtype-replyto
            """
            return self._values.get('reply_to')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'NotifyConfigurationTypeProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="@aws-cdk/aws-cognito.CfnUserPoolRiskConfigurationAttachment.NotifyEmailTypeProperty", jsii_struct_bases=[], name_mapping={'subject': 'subject', 'html_body': 'htmlBody', 'text_body': 'textBody'})
    class NotifyEmailTypeProperty():
        def __init__(self, *, subject: str, html_body: typing.Optional[str]=None, text_body: typing.Optional[str]=None) -> None:
            """
            :param subject: ``CfnUserPoolRiskConfigurationAttachment.NotifyEmailTypeProperty.Subject``.
            :param html_body: ``CfnUserPoolRiskConfigurationAttachment.NotifyEmailTypeProperty.HtmlBody``.
            :param text_body: ``CfnUserPoolRiskConfigurationAttachment.NotifyEmailTypeProperty.TextBody``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-userpoolriskconfigurationattachment-notifyemailtype.html
            """
            self._values = {
                'subject': subject,
            }
            if html_body is not None: self._values["html_body"] = html_body
            if text_body is not None: self._values["text_body"] = text_body

        @builtins.property
        def subject(self) -> str:
            """``CfnUserPoolRiskConfigurationAttachment.NotifyEmailTypeProperty.Subject``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-userpoolriskconfigurationattachment-notifyemailtype.html#cfn-cognito-userpoolriskconfigurationattachment-notifyemailtype-subject
            """
            return self._values.get('subject')

        @builtins.property
        def html_body(self) -> typing.Optional[str]:
            """``CfnUserPoolRiskConfigurationAttachment.NotifyEmailTypeProperty.HtmlBody``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-userpoolriskconfigurationattachment-notifyemailtype.html#cfn-cognito-userpoolriskconfigurationattachment-notifyemailtype-htmlbody
            """
            return self._values.get('html_body')

        @builtins.property
        def text_body(self) -> typing.Optional[str]:
            """``CfnUserPoolRiskConfigurationAttachment.NotifyEmailTypeProperty.TextBody``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-userpoolriskconfigurationattachment-notifyemailtype.html#cfn-cognito-userpoolriskconfigurationattachment-notifyemailtype-textbody
            """
            return self._values.get('text_body')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'NotifyEmailTypeProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="@aws-cdk/aws-cognito.CfnUserPoolRiskConfigurationAttachment.RiskExceptionConfigurationTypeProperty", jsii_struct_bases=[], name_mapping={'blocked_ip_range_list': 'blockedIpRangeList', 'skipped_ip_range_list': 'skippedIpRangeList'})
    class RiskExceptionConfigurationTypeProperty():
        def __init__(self, *, blocked_ip_range_list: typing.Optional[typing.List[str]]=None, skipped_ip_range_list: typing.Optional[typing.List[str]]=None) -> None:
            """
            :param blocked_ip_range_list: ``CfnUserPoolRiskConfigurationAttachment.RiskExceptionConfigurationTypeProperty.BlockedIPRangeList``.
            :param skipped_ip_range_list: ``CfnUserPoolRiskConfigurationAttachment.RiskExceptionConfigurationTypeProperty.SkippedIPRangeList``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-userpoolriskconfigurationattachment-riskexceptionconfigurationtype.html
            """
            self._values = {
            }
            if blocked_ip_range_list is not None: self._values["blocked_ip_range_list"] = blocked_ip_range_list
            if skipped_ip_range_list is not None: self._values["skipped_ip_range_list"] = skipped_ip_range_list

        @builtins.property
        def blocked_ip_range_list(self) -> typing.Optional[typing.List[str]]:
            """``CfnUserPoolRiskConfigurationAttachment.RiskExceptionConfigurationTypeProperty.BlockedIPRangeList``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-userpoolriskconfigurationattachment-riskexceptionconfigurationtype.html#cfn-cognito-userpoolriskconfigurationattachment-riskexceptionconfigurationtype-blockediprangelist
            """
            return self._values.get('blocked_ip_range_list')

        @builtins.property
        def skipped_ip_range_list(self) -> typing.Optional[typing.List[str]]:
            """``CfnUserPoolRiskConfigurationAttachment.RiskExceptionConfigurationTypeProperty.SkippedIPRangeList``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-userpoolriskconfigurationattachment-riskexceptionconfigurationtype.html#cfn-cognito-userpoolriskconfigurationattachment-riskexceptionconfigurationtype-skippediprangelist
            """
            return self._values.get('skipped_ip_range_list')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'RiskExceptionConfigurationTypeProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())



@jsii.data_type(jsii_type="@aws-cdk/aws-cognito.CfnUserPoolRiskConfigurationAttachmentProps", jsii_struct_bases=[], name_mapping={'client_id': 'clientId', 'user_pool_id': 'userPoolId', 'account_takeover_risk_configuration': 'accountTakeoverRiskConfiguration', 'compromised_credentials_risk_configuration': 'compromisedCredentialsRiskConfiguration', 'risk_exception_configuration': 'riskExceptionConfiguration'})
class CfnUserPoolRiskConfigurationAttachmentProps():
    def __init__(self, *, client_id: str, user_pool_id: str, account_takeover_risk_configuration: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["CfnUserPoolRiskConfigurationAttachment.AccountTakeoverRiskConfigurationTypeProperty"]]]=None, compromised_credentials_risk_configuration: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["CfnUserPoolRiskConfigurationAttachment.CompromisedCredentialsRiskConfigurationTypeProperty"]]]=None, risk_exception_configuration: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["CfnUserPoolRiskConfigurationAttachment.RiskExceptionConfigurationTypeProperty"]]]=None) -> None:
        """Properties for defining a ``AWS::Cognito::UserPoolRiskConfigurationAttachment``.

        :param client_id: ``AWS::Cognito::UserPoolRiskConfigurationAttachment.ClientId``.
        :param user_pool_id: ``AWS::Cognito::UserPoolRiskConfigurationAttachment.UserPoolId``.
        :param account_takeover_risk_configuration: ``AWS::Cognito::UserPoolRiskConfigurationAttachment.AccountTakeoverRiskConfiguration``.
        :param compromised_credentials_risk_configuration: ``AWS::Cognito::UserPoolRiskConfigurationAttachment.CompromisedCredentialsRiskConfiguration``.
        :param risk_exception_configuration: ``AWS::Cognito::UserPoolRiskConfigurationAttachment.RiskExceptionConfiguration``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpoolriskconfigurationattachment.html
        """
        self._values = {
            'client_id': client_id,
            'user_pool_id': user_pool_id,
        }
        if account_takeover_risk_configuration is not None: self._values["account_takeover_risk_configuration"] = account_takeover_risk_configuration
        if compromised_credentials_risk_configuration is not None: self._values["compromised_credentials_risk_configuration"] = compromised_credentials_risk_configuration
        if risk_exception_configuration is not None: self._values["risk_exception_configuration"] = risk_exception_configuration

    @builtins.property
    def client_id(self) -> str:
        """``AWS::Cognito::UserPoolRiskConfigurationAttachment.ClientId``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpoolriskconfigurationattachment.html#cfn-cognito-userpoolriskconfigurationattachment-clientid
        """
        return self._values.get('client_id')

    @builtins.property
    def user_pool_id(self) -> str:
        """``AWS::Cognito::UserPoolRiskConfigurationAttachment.UserPoolId``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpoolriskconfigurationattachment.html#cfn-cognito-userpoolriskconfigurationattachment-userpoolid
        """
        return self._values.get('user_pool_id')

    @builtins.property
    def account_takeover_risk_configuration(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["CfnUserPoolRiskConfigurationAttachment.AccountTakeoverRiskConfigurationTypeProperty"]]]:
        """``AWS::Cognito::UserPoolRiskConfigurationAttachment.AccountTakeoverRiskConfiguration``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpoolriskconfigurationattachment.html#cfn-cognito-userpoolriskconfigurationattachment-accounttakeoverriskconfiguration
        """
        return self._values.get('account_takeover_risk_configuration')

    @builtins.property
    def compromised_credentials_risk_configuration(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["CfnUserPoolRiskConfigurationAttachment.CompromisedCredentialsRiskConfigurationTypeProperty"]]]:
        """``AWS::Cognito::UserPoolRiskConfigurationAttachment.CompromisedCredentialsRiskConfiguration``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpoolriskconfigurationattachment.html#cfn-cognito-userpoolriskconfigurationattachment-compromisedcredentialsriskconfiguration
        """
        return self._values.get('compromised_credentials_risk_configuration')

    @builtins.property
    def risk_exception_configuration(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["CfnUserPoolRiskConfigurationAttachment.RiskExceptionConfigurationTypeProperty"]]]:
        """``AWS::Cognito::UserPoolRiskConfigurationAttachment.RiskExceptionConfiguration``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpoolriskconfigurationattachment.html#cfn-cognito-userpoolriskconfigurationattachment-riskexceptionconfiguration
        """
        return self._values.get('risk_exception_configuration')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'CfnUserPoolRiskConfigurationAttachmentProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.implements(aws_cdk.core.IInspectable)
class CfnUserPoolUICustomizationAttachment(aws_cdk.core.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-cognito.CfnUserPoolUICustomizationAttachment"):
    """A CloudFormation ``AWS::Cognito::UserPoolUICustomizationAttachment``.

    see
    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpooluicustomizationattachment.html
    cloudformationResource:
    :cloudformationResource:: AWS::Cognito::UserPoolUICustomizationAttachment
    """
    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, client_id: str, user_pool_id: str, css: typing.Optional[str]=None) -> None:
        """Create a new ``AWS::Cognito::UserPoolUICustomizationAttachment``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param client_id: ``AWS::Cognito::UserPoolUICustomizationAttachment.ClientId``.
        :param user_pool_id: ``AWS::Cognito::UserPoolUICustomizationAttachment.UserPoolId``.
        :param css: ``AWS::Cognito::UserPoolUICustomizationAttachment.CSS``.
        """
        props = CfnUserPoolUICustomizationAttachmentProps(client_id=client_id, user_pool_id=user_pool_id, css=css)

        jsii.create(CfnUserPoolUICustomizationAttachment, self, [scope, id, props])

    @jsii.member(jsii_name="fromCloudFormation")
    @builtins.classmethod
    def from_cloud_formation(cls, scope: aws_cdk.core.Construct, id: str, resource_attributes: typing.Any, *, finder: aws_cdk.core.ICfnFinder) -> "CfnUserPoolUICustomizationAttachment":
        """A factory method that creates a new instance of this class from an object containing the CloudFormation properties of this resource.

        Used in the @aws-cdk/cloudformation-include module.

        :param scope: -
        :param id: -
        :param resource_attributes: -
        :param finder: The finder interface used to resolve references across the template.

        stability
        :stability: experimental
        """
        options = aws_cdk.core.FromCloudFormationOptions(finder=finder)

        return jsii.sinvoke(cls, "fromCloudFormation", [scope, id, resource_attributes, options])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: aws_cdk.core.TreeInspector) -> None:
        """Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "inspect", [inspector])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, props: typing.Mapping[str, typing.Any]) -> typing.Mapping[str, typing.Any]:
        """
        :param props: -
        """
        return jsii.invoke(self, "renderProperties", [props])

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> str:
        """The CloudFormation resource type name for this resource class."""
        return jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME")

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[str, typing.Any]:
        return jsii.get(self, "cfnProperties")

    @builtins.property
    @jsii.member(jsii_name="clientId")
    def client_id(self) -> str:
        """``AWS::Cognito::UserPoolUICustomizationAttachment.ClientId``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpooluicustomizationattachment.html#cfn-cognito-userpooluicustomizationattachment-clientid
        """
        return jsii.get(self, "clientId")

    @client_id.setter
    def client_id(self, value: str):
        jsii.set(self, "clientId", value)

    @builtins.property
    @jsii.member(jsii_name="userPoolId")
    def user_pool_id(self) -> str:
        """``AWS::Cognito::UserPoolUICustomizationAttachment.UserPoolId``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpooluicustomizationattachment.html#cfn-cognito-userpooluicustomizationattachment-userpoolid
        """
        return jsii.get(self, "userPoolId")

    @user_pool_id.setter
    def user_pool_id(self, value: str):
        jsii.set(self, "userPoolId", value)

    @builtins.property
    @jsii.member(jsii_name="css")
    def css(self) -> typing.Optional[str]:
        """``AWS::Cognito::UserPoolUICustomizationAttachment.CSS``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpooluicustomizationattachment.html#cfn-cognito-userpooluicustomizationattachment-css
        """
        return jsii.get(self, "css")

    @css.setter
    def css(self, value: typing.Optional[str]):
        jsii.set(self, "css", value)


@jsii.data_type(jsii_type="@aws-cdk/aws-cognito.CfnUserPoolUICustomizationAttachmentProps", jsii_struct_bases=[], name_mapping={'client_id': 'clientId', 'user_pool_id': 'userPoolId', 'css': 'css'})
class CfnUserPoolUICustomizationAttachmentProps():
    def __init__(self, *, client_id: str, user_pool_id: str, css: typing.Optional[str]=None) -> None:
        """Properties for defining a ``AWS::Cognito::UserPoolUICustomizationAttachment``.

        :param client_id: ``AWS::Cognito::UserPoolUICustomizationAttachment.ClientId``.
        :param user_pool_id: ``AWS::Cognito::UserPoolUICustomizationAttachment.UserPoolId``.
        :param css: ``AWS::Cognito::UserPoolUICustomizationAttachment.CSS``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpooluicustomizationattachment.html
        """
        self._values = {
            'client_id': client_id,
            'user_pool_id': user_pool_id,
        }
        if css is not None: self._values["css"] = css

    @builtins.property
    def client_id(self) -> str:
        """``AWS::Cognito::UserPoolUICustomizationAttachment.ClientId``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpooluicustomizationattachment.html#cfn-cognito-userpooluicustomizationattachment-clientid
        """
        return self._values.get('client_id')

    @builtins.property
    def user_pool_id(self) -> str:
        """``AWS::Cognito::UserPoolUICustomizationAttachment.UserPoolId``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpooluicustomizationattachment.html#cfn-cognito-userpooluicustomizationattachment-userpoolid
        """
        return self._values.get('user_pool_id')

    @builtins.property
    def css(self) -> typing.Optional[str]:
        """``AWS::Cognito::UserPoolUICustomizationAttachment.CSS``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpooluicustomizationattachment.html#cfn-cognito-userpooluicustomizationattachment-css
        """
        return self._values.get('css')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'CfnUserPoolUICustomizationAttachmentProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.implements(aws_cdk.core.IInspectable)
class CfnUserPoolUser(aws_cdk.core.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-cognito.CfnUserPoolUser"):
    """A CloudFormation ``AWS::Cognito::UserPoolUser``.

    see
    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpooluser.html
    cloudformationResource:
    :cloudformationResource:: AWS::Cognito::UserPoolUser
    """
    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, user_pool_id: str, client_metadata: typing.Any=None, desired_delivery_mediums: typing.Optional[typing.List[str]]=None, force_alias_creation: typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.core.IResolvable]]]=None, message_action: typing.Optional[str]=None, user_attributes: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union[aws_cdk.core.IResolvable, "AttributeTypeProperty"]]]]]=None, username: typing.Optional[str]=None, validation_data: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union[aws_cdk.core.IResolvable, "AttributeTypeProperty"]]]]]=None) -> None:
        """Create a new ``AWS::Cognito::UserPoolUser``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param user_pool_id: ``AWS::Cognito::UserPoolUser.UserPoolId``.
        :param client_metadata: ``AWS::Cognito::UserPoolUser.ClientMetadata``.
        :param desired_delivery_mediums: ``AWS::Cognito::UserPoolUser.DesiredDeliveryMediums``.
        :param force_alias_creation: ``AWS::Cognito::UserPoolUser.ForceAliasCreation``.
        :param message_action: ``AWS::Cognito::UserPoolUser.MessageAction``.
        :param user_attributes: ``AWS::Cognito::UserPoolUser.UserAttributes``.
        :param username: ``AWS::Cognito::UserPoolUser.Username``.
        :param validation_data: ``AWS::Cognito::UserPoolUser.ValidationData``.
        """
        props = CfnUserPoolUserProps(user_pool_id=user_pool_id, client_metadata=client_metadata, desired_delivery_mediums=desired_delivery_mediums, force_alias_creation=force_alias_creation, message_action=message_action, user_attributes=user_attributes, username=username, validation_data=validation_data)

        jsii.create(CfnUserPoolUser, self, [scope, id, props])

    @jsii.member(jsii_name="fromCloudFormation")
    @builtins.classmethod
    def from_cloud_formation(cls, scope: aws_cdk.core.Construct, id: str, resource_attributes: typing.Any, *, finder: aws_cdk.core.ICfnFinder) -> "CfnUserPoolUser":
        """A factory method that creates a new instance of this class from an object containing the CloudFormation properties of this resource.

        Used in the @aws-cdk/cloudformation-include module.

        :param scope: -
        :param id: -
        :param resource_attributes: -
        :param finder: The finder interface used to resolve references across the template.

        stability
        :stability: experimental
        """
        options = aws_cdk.core.FromCloudFormationOptions(finder=finder)

        return jsii.sinvoke(cls, "fromCloudFormation", [scope, id, resource_attributes, options])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: aws_cdk.core.TreeInspector) -> None:
        """Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "inspect", [inspector])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, props: typing.Mapping[str, typing.Any]) -> typing.Mapping[str, typing.Any]:
        """
        :param props: -
        """
        return jsii.invoke(self, "renderProperties", [props])

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> str:
        """The CloudFormation resource type name for this resource class."""
        return jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME")

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[str, typing.Any]:
        return jsii.get(self, "cfnProperties")

    @builtins.property
    @jsii.member(jsii_name="clientMetadata")
    def client_metadata(self) -> typing.Any:
        """``AWS::Cognito::UserPoolUser.ClientMetadata``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpooluser.html#cfn-cognito-userpooluser-clientmetadata
        """
        return jsii.get(self, "clientMetadata")

    @client_metadata.setter
    def client_metadata(self, value: typing.Any):
        jsii.set(self, "clientMetadata", value)

    @builtins.property
    @jsii.member(jsii_name="userPoolId")
    def user_pool_id(self) -> str:
        """``AWS::Cognito::UserPoolUser.UserPoolId``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpooluser.html#cfn-cognito-userpooluser-userpoolid
        """
        return jsii.get(self, "userPoolId")

    @user_pool_id.setter
    def user_pool_id(self, value: str):
        jsii.set(self, "userPoolId", value)

    @builtins.property
    @jsii.member(jsii_name="desiredDeliveryMediums")
    def desired_delivery_mediums(self) -> typing.Optional[typing.List[str]]:
        """``AWS::Cognito::UserPoolUser.DesiredDeliveryMediums``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpooluser.html#cfn-cognito-userpooluser-desireddeliverymediums
        """
        return jsii.get(self, "desiredDeliveryMediums")

    @desired_delivery_mediums.setter
    def desired_delivery_mediums(self, value: typing.Optional[typing.List[str]]):
        jsii.set(self, "desiredDeliveryMediums", value)

    @builtins.property
    @jsii.member(jsii_name="forceAliasCreation")
    def force_alias_creation(self) -> typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.core.IResolvable]]]:
        """``AWS::Cognito::UserPoolUser.ForceAliasCreation``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpooluser.html#cfn-cognito-userpooluser-forcealiascreation
        """
        return jsii.get(self, "forceAliasCreation")

    @force_alias_creation.setter
    def force_alias_creation(self, value: typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.core.IResolvable]]]):
        jsii.set(self, "forceAliasCreation", value)

    @builtins.property
    @jsii.member(jsii_name="messageAction")
    def message_action(self) -> typing.Optional[str]:
        """``AWS::Cognito::UserPoolUser.MessageAction``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpooluser.html#cfn-cognito-userpooluser-messageaction
        """
        return jsii.get(self, "messageAction")

    @message_action.setter
    def message_action(self, value: typing.Optional[str]):
        jsii.set(self, "messageAction", value)

    @builtins.property
    @jsii.member(jsii_name="userAttributes")
    def user_attributes(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union[aws_cdk.core.IResolvable, "AttributeTypeProperty"]]]]]:
        """``AWS::Cognito::UserPoolUser.UserAttributes``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpooluser.html#cfn-cognito-userpooluser-userattributes
        """
        return jsii.get(self, "userAttributes")

    @user_attributes.setter
    def user_attributes(self, value: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union[aws_cdk.core.IResolvable, "AttributeTypeProperty"]]]]]):
        jsii.set(self, "userAttributes", value)

    @builtins.property
    @jsii.member(jsii_name="username")
    def username(self) -> typing.Optional[str]:
        """``AWS::Cognito::UserPoolUser.Username``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpooluser.html#cfn-cognito-userpooluser-username
        """
        return jsii.get(self, "username")

    @username.setter
    def username(self, value: typing.Optional[str]):
        jsii.set(self, "username", value)

    @builtins.property
    @jsii.member(jsii_name="validationData")
    def validation_data(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union[aws_cdk.core.IResolvable, "AttributeTypeProperty"]]]]]:
        """``AWS::Cognito::UserPoolUser.ValidationData``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpooluser.html#cfn-cognito-userpooluser-validationdata
        """
        return jsii.get(self, "validationData")

    @validation_data.setter
    def validation_data(self, value: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union[aws_cdk.core.IResolvable, "AttributeTypeProperty"]]]]]):
        jsii.set(self, "validationData", value)

    @jsii.data_type(jsii_type="@aws-cdk/aws-cognito.CfnUserPoolUser.AttributeTypeProperty", jsii_struct_bases=[], name_mapping={'name': 'name', 'value': 'value'})
    class AttributeTypeProperty():
        def __init__(self, *, name: typing.Optional[str]=None, value: typing.Optional[str]=None) -> None:
            """
            :param name: ``CfnUserPoolUser.AttributeTypeProperty.Name``.
            :param value: ``CfnUserPoolUser.AttributeTypeProperty.Value``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-userpooluser-attributetype.html
            """
            self._values = {
            }
            if name is not None: self._values["name"] = name
            if value is not None: self._values["value"] = value

        @builtins.property
        def name(self) -> typing.Optional[str]:
            """``CfnUserPoolUser.AttributeTypeProperty.Name``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-userpooluser-attributetype.html#cfn-cognito-userpooluser-attributetype-name
            """
            return self._values.get('name')

        @builtins.property
        def value(self) -> typing.Optional[str]:
            """``CfnUserPoolUser.AttributeTypeProperty.Value``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-userpooluser-attributetype.html#cfn-cognito-userpooluser-attributetype-value
            """
            return self._values.get('value')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'AttributeTypeProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())



@jsii.data_type(jsii_type="@aws-cdk/aws-cognito.CfnUserPoolUserProps", jsii_struct_bases=[], name_mapping={'user_pool_id': 'userPoolId', 'client_metadata': 'clientMetadata', 'desired_delivery_mediums': 'desiredDeliveryMediums', 'force_alias_creation': 'forceAliasCreation', 'message_action': 'messageAction', 'user_attributes': 'userAttributes', 'username': 'username', 'validation_data': 'validationData'})
class CfnUserPoolUserProps():
    def __init__(self, *, user_pool_id: str, client_metadata: typing.Any=None, desired_delivery_mediums: typing.Optional[typing.List[str]]=None, force_alias_creation: typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.core.IResolvable]]]=None, message_action: typing.Optional[str]=None, user_attributes: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnUserPoolUser.AttributeTypeProperty"]]]]]=None, username: typing.Optional[str]=None, validation_data: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnUserPoolUser.AttributeTypeProperty"]]]]]=None) -> None:
        """Properties for defining a ``AWS::Cognito::UserPoolUser``.

        :param user_pool_id: ``AWS::Cognito::UserPoolUser.UserPoolId``.
        :param client_metadata: ``AWS::Cognito::UserPoolUser.ClientMetadata``.
        :param desired_delivery_mediums: ``AWS::Cognito::UserPoolUser.DesiredDeliveryMediums``.
        :param force_alias_creation: ``AWS::Cognito::UserPoolUser.ForceAliasCreation``.
        :param message_action: ``AWS::Cognito::UserPoolUser.MessageAction``.
        :param user_attributes: ``AWS::Cognito::UserPoolUser.UserAttributes``.
        :param username: ``AWS::Cognito::UserPoolUser.Username``.
        :param validation_data: ``AWS::Cognito::UserPoolUser.ValidationData``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpooluser.html
        """
        self._values = {
            'user_pool_id': user_pool_id,
        }
        if client_metadata is not None: self._values["client_metadata"] = client_metadata
        if desired_delivery_mediums is not None: self._values["desired_delivery_mediums"] = desired_delivery_mediums
        if force_alias_creation is not None: self._values["force_alias_creation"] = force_alias_creation
        if message_action is not None: self._values["message_action"] = message_action
        if user_attributes is not None: self._values["user_attributes"] = user_attributes
        if username is not None: self._values["username"] = username
        if validation_data is not None: self._values["validation_data"] = validation_data

    @builtins.property
    def user_pool_id(self) -> str:
        """``AWS::Cognito::UserPoolUser.UserPoolId``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpooluser.html#cfn-cognito-userpooluser-userpoolid
        """
        return self._values.get('user_pool_id')

    @builtins.property
    def client_metadata(self) -> typing.Any:
        """``AWS::Cognito::UserPoolUser.ClientMetadata``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpooluser.html#cfn-cognito-userpooluser-clientmetadata
        """
        return self._values.get('client_metadata')

    @builtins.property
    def desired_delivery_mediums(self) -> typing.Optional[typing.List[str]]:
        """``AWS::Cognito::UserPoolUser.DesiredDeliveryMediums``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpooluser.html#cfn-cognito-userpooluser-desireddeliverymediums
        """
        return self._values.get('desired_delivery_mediums')

    @builtins.property
    def force_alias_creation(self) -> typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.core.IResolvable]]]:
        """``AWS::Cognito::UserPoolUser.ForceAliasCreation``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpooluser.html#cfn-cognito-userpooluser-forcealiascreation
        """
        return self._values.get('force_alias_creation')

    @builtins.property
    def message_action(self) -> typing.Optional[str]:
        """``AWS::Cognito::UserPoolUser.MessageAction``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpooluser.html#cfn-cognito-userpooluser-messageaction
        """
        return self._values.get('message_action')

    @builtins.property
    def user_attributes(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnUserPoolUser.AttributeTypeProperty"]]]]]:
        """``AWS::Cognito::UserPoolUser.UserAttributes``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpooluser.html#cfn-cognito-userpooluser-userattributes
        """
        return self._values.get('user_attributes')

    @builtins.property
    def username(self) -> typing.Optional[str]:
        """``AWS::Cognito::UserPoolUser.Username``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpooluser.html#cfn-cognito-userpooluser-username
        """
        return self._values.get('username')

    @builtins.property
    def validation_data(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnUserPoolUser.AttributeTypeProperty"]]]]]:
        """``AWS::Cognito::UserPoolUser.ValidationData``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpooluser.html#cfn-cognito-userpooluser-validationdata
        """
        return self._values.get('validation_data')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'CfnUserPoolUserProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.implements(aws_cdk.core.IInspectable)
class CfnUserPoolUserToGroupAttachment(aws_cdk.core.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-cognito.CfnUserPoolUserToGroupAttachment"):
    """A CloudFormation ``AWS::Cognito::UserPoolUserToGroupAttachment``.

    see
    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpoolusertogroupattachment.html
    cloudformationResource:
    :cloudformationResource:: AWS::Cognito::UserPoolUserToGroupAttachment
    """
    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, group_name: str, username: str, user_pool_id: str) -> None:
        """Create a new ``AWS::Cognito::UserPoolUserToGroupAttachment``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param group_name: ``AWS::Cognito::UserPoolUserToGroupAttachment.GroupName``.
        :param username: ``AWS::Cognito::UserPoolUserToGroupAttachment.Username``.
        :param user_pool_id: ``AWS::Cognito::UserPoolUserToGroupAttachment.UserPoolId``.
        """
        props = CfnUserPoolUserToGroupAttachmentProps(group_name=group_name, username=username, user_pool_id=user_pool_id)

        jsii.create(CfnUserPoolUserToGroupAttachment, self, [scope, id, props])

    @jsii.member(jsii_name="fromCloudFormation")
    @builtins.classmethod
    def from_cloud_formation(cls, scope: aws_cdk.core.Construct, id: str, resource_attributes: typing.Any, *, finder: aws_cdk.core.ICfnFinder) -> "CfnUserPoolUserToGroupAttachment":
        """A factory method that creates a new instance of this class from an object containing the CloudFormation properties of this resource.

        Used in the @aws-cdk/cloudformation-include module.

        :param scope: -
        :param id: -
        :param resource_attributes: -
        :param finder: The finder interface used to resolve references across the template.

        stability
        :stability: experimental
        """
        options = aws_cdk.core.FromCloudFormationOptions(finder=finder)

        return jsii.sinvoke(cls, "fromCloudFormation", [scope, id, resource_attributes, options])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: aws_cdk.core.TreeInspector) -> None:
        """Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "inspect", [inspector])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, props: typing.Mapping[str, typing.Any]) -> typing.Mapping[str, typing.Any]:
        """
        :param props: -
        """
        return jsii.invoke(self, "renderProperties", [props])

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> str:
        """The CloudFormation resource type name for this resource class."""
        return jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME")

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[str, typing.Any]:
        return jsii.get(self, "cfnProperties")

    @builtins.property
    @jsii.member(jsii_name="groupName")
    def group_name(self) -> str:
        """``AWS::Cognito::UserPoolUserToGroupAttachment.GroupName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpoolusertogroupattachment.html#cfn-cognito-userpoolusertogroupattachment-groupname
        """
        return jsii.get(self, "groupName")

    @group_name.setter
    def group_name(self, value: str):
        jsii.set(self, "groupName", value)

    @builtins.property
    @jsii.member(jsii_name="username")
    def username(self) -> str:
        """``AWS::Cognito::UserPoolUserToGroupAttachment.Username``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpoolusertogroupattachment.html#cfn-cognito-userpoolusertogroupattachment-username
        """
        return jsii.get(self, "username")

    @username.setter
    def username(self, value: str):
        jsii.set(self, "username", value)

    @builtins.property
    @jsii.member(jsii_name="userPoolId")
    def user_pool_id(self) -> str:
        """``AWS::Cognito::UserPoolUserToGroupAttachment.UserPoolId``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpoolusertogroupattachment.html#cfn-cognito-userpoolusertogroupattachment-userpoolid
        """
        return jsii.get(self, "userPoolId")

    @user_pool_id.setter
    def user_pool_id(self, value: str):
        jsii.set(self, "userPoolId", value)


@jsii.data_type(jsii_type="@aws-cdk/aws-cognito.CfnUserPoolUserToGroupAttachmentProps", jsii_struct_bases=[], name_mapping={'group_name': 'groupName', 'username': 'username', 'user_pool_id': 'userPoolId'})
class CfnUserPoolUserToGroupAttachmentProps():
    def __init__(self, *, group_name: str, username: str, user_pool_id: str) -> None:
        """Properties for defining a ``AWS::Cognito::UserPoolUserToGroupAttachment``.

        :param group_name: ``AWS::Cognito::UserPoolUserToGroupAttachment.GroupName``.
        :param username: ``AWS::Cognito::UserPoolUserToGroupAttachment.Username``.
        :param user_pool_id: ``AWS::Cognito::UserPoolUserToGroupAttachment.UserPoolId``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpoolusertogroupattachment.html
        """
        self._values = {
            'group_name': group_name,
            'username': username,
            'user_pool_id': user_pool_id,
        }

    @builtins.property
    def group_name(self) -> str:
        """``AWS::Cognito::UserPoolUserToGroupAttachment.GroupName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpoolusertogroupattachment.html#cfn-cognito-userpoolusertogroupattachment-groupname
        """
        return self._values.get('group_name')

    @builtins.property
    def username(self) -> str:
        """``AWS::Cognito::UserPoolUserToGroupAttachment.Username``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpoolusertogroupattachment.html#cfn-cognito-userpoolusertogroupattachment-username
        """
        return self._values.get('username')

    @builtins.property
    def user_pool_id(self) -> str:
        """``AWS::Cognito::UserPoolUserToGroupAttachment.UserPoolId``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpoolusertogroupattachment.html#cfn-cognito-userpoolusertogroupattachment-userpoolid
        """
        return self._values.get('user_pool_id')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'CfnUserPoolUserToGroupAttachmentProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="@aws-cdk/aws-cognito.CognitoDomainOptions", jsii_struct_bases=[], name_mapping={'domain_prefix': 'domainPrefix'})
class CognitoDomainOptions():
    def __init__(self, *, domain_prefix: str) -> None:
        """Options while specifying a cognito prefix domain.

        :param domain_prefix: The prefix to the Cognito hosted domain name that will be associated with the user pool.

        see
        :see: https://docs.aws.amazon.com/cognito/latest/developerguide/cognito-user-pools-assign-domain-prefix.html
        stability
        :stability: experimental
        """
        self._values = {
            'domain_prefix': domain_prefix,
        }

    @builtins.property
    def domain_prefix(self) -> str:
        """The prefix to the Cognito hosted domain name that will be associated with the user pool.

        stability
        :stability: experimental
        """
        return self._values.get('domain_prefix')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'CognitoDomainOptions(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="@aws-cdk/aws-cognito.CustomAttributeConfig", jsii_struct_bases=[], name_mapping={'data_type': 'dataType', 'mutable': 'mutable', 'number_constraints': 'numberConstraints', 'string_constraints': 'stringConstraints'})
class CustomAttributeConfig():
    def __init__(self, *, data_type: str, mutable: typing.Optional[bool]=None, number_constraints: typing.Optional["NumberAttributeConstraints"]=None, string_constraints: typing.Optional["StringAttributeConstraints"]=None) -> None:
        """Configuration that will be fed into CloudFormation for any custom attribute type.

        :param data_type: The data type of the custom attribute.
        :param mutable: Specifies whether the value of the attribute can be changed. For any user pool attribute that's mapped to an identity provider attribute, you must set this parameter to true. Amazon Cognito updates mapped attributes when users sign in to your application through an identity provider. If an attribute is immutable, Amazon Cognito throws an error when it attempts to update the attribute. Default: false
        :param number_constraints: The constraints for a custom attribute of the 'Number' data type. Default: - None.
        :param string_constraints: The constraints for a custom attribute of 'String' data type. Default: - None.

        stability
        :stability: experimental
        """
        if isinstance(number_constraints, dict): number_constraints = NumberAttributeConstraints(**number_constraints)
        if isinstance(string_constraints, dict): string_constraints = StringAttributeConstraints(**string_constraints)
        self._values = {
            'data_type': data_type,
        }
        if mutable is not None: self._values["mutable"] = mutable
        if number_constraints is not None: self._values["number_constraints"] = number_constraints
        if string_constraints is not None: self._values["string_constraints"] = string_constraints

    @builtins.property
    def data_type(self) -> str:
        """The data type of the custom attribute.

        see
        :see: https://docs.aws.amazon.com/cognito-user-identity-pools/latest/APIReference/API_SchemaAttributeType.html#CognitoUserPools-Type-SchemaAttributeType-AttributeDataType
        stability
        :stability: experimental
        """
        return self._values.get('data_type')

    @builtins.property
    def mutable(self) -> typing.Optional[bool]:
        """Specifies whether the value of the attribute can be changed.

        For any user pool attribute that's mapped to an identity provider attribute, you must set this parameter to true.
        Amazon Cognito updates mapped attributes when users sign in to your application through an identity provider.
        If an attribute is immutable, Amazon Cognito throws an error when it attempts to update the attribute.

        default
        :default: false

        stability
        :stability: experimental
        """
        return self._values.get('mutable')

    @builtins.property
    def number_constraints(self) -> typing.Optional["NumberAttributeConstraints"]:
        """The constraints for a custom attribute of the 'Number' data type.

        default
        :default: - None.

        stability
        :stability: experimental
        """
        return self._values.get('number_constraints')

    @builtins.property
    def string_constraints(self) -> typing.Optional["StringAttributeConstraints"]:
        """The constraints for a custom attribute of 'String' data type.

        default
        :default: - None.

        stability
        :stability: experimental
        """
        return self._values.get('string_constraints')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'CustomAttributeConfig(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="@aws-cdk/aws-cognito.CustomAttributeProps", jsii_struct_bases=[], name_mapping={'mutable': 'mutable'})
class CustomAttributeProps():
    def __init__(self, *, mutable: typing.Optional[bool]=None) -> None:
        """Constraints that can be applied to a custom attribute of any type.

        :param mutable: Specifies whether the value of the attribute can be changed. For any user pool attribute that's mapped to an identity provider attribute, you must set this parameter to true. Amazon Cognito updates mapped attributes when users sign in to your application through an identity provider. If an attribute is immutable, Amazon Cognito throws an error when it attempts to update the attribute. Default: false

        stability
        :stability: experimental
        """
        self._values = {
        }
        if mutable is not None: self._values["mutable"] = mutable

    @builtins.property
    def mutable(self) -> typing.Optional[bool]:
        """Specifies whether the value of the attribute can be changed.

        For any user pool attribute that's mapped to an identity provider attribute, you must set this parameter to true.
        Amazon Cognito updates mapped attributes when users sign in to your application through an identity provider.
        If an attribute is immutable, Amazon Cognito throws an error when it attempts to update the attribute.

        default
        :default: false

        stability
        :stability: experimental
        """
        return self._values.get('mutable')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'CustomAttributeProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="@aws-cdk/aws-cognito.CustomDomainOptions", jsii_struct_bases=[], name_mapping={'certificate': 'certificate', 'domain_name': 'domainName'})
class CustomDomainOptions():
    def __init__(self, *, certificate: aws_cdk.aws_certificatemanager.ICertificate, domain_name: str) -> None:
        """Options while specifying custom domain.

        :param certificate: The certificate to associate with this domain.
        :param domain_name: The custom domain name that you would like to associate with this User Pool.

        see
        :see: https://docs.aws.amazon.com/cognito/latest/developerguide/cognito-user-pools-add-custom-domain.html
        stability
        :stability: experimental
        """
        self._values = {
            'certificate': certificate,
            'domain_name': domain_name,
        }

    @builtins.property
    def certificate(self) -> aws_cdk.aws_certificatemanager.ICertificate:
        """The certificate to associate with this domain.

        stability
        :stability: experimental
        """
        return self._values.get('certificate')

    @builtins.property
    def domain_name(self) -> str:
        """The custom domain name that you would like to associate with this User Pool.

        stability
        :stability: experimental
        """
        return self._values.get('domain_name')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'CustomDomainOptions(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="@aws-cdk/aws-cognito.EmailSettings", jsii_struct_bases=[], name_mapping={'from_': 'from', 'reply_to': 'replyTo'})
class EmailSettings():
    def __init__(self, *, from_: typing.Optional[str]=None, reply_to: typing.Optional[str]=None) -> None:
        """Email settings for the user pool.

        :param from_: The 'from' address on the emails received by the user. Default: noreply
        :param reply_to: The 'replyTo' address on the emails received by the user as defined by IETF RFC-5322. When set, most email clients recognize to change 'to' line to this address when a reply is drafted. Default: - Not set.

        stability
        :stability: experimental
        """
        self._values = {
        }
        if from_ is not None: self._values["from_"] = from_
        if reply_to is not None: self._values["reply_to"] = reply_to

    @builtins.property
    def from_(self) -> typing.Optional[str]:
        """The 'from' address on the emails received by the user.

        default
        :default: noreply

        stability
        :stability: experimental
        verificationemail:
        :verificationemail:: .com
        """
        return self._values.get('from_')

    @builtins.property
    def reply_to(self) -> typing.Optional[str]:
        """The 'replyTo' address on the emails received by the user as defined by IETF RFC-5322.

        When set, most email clients recognize to change 'to' line to this address when a reply is drafted.

        default
        :default: - Not set.

        stability
        :stability: experimental
        """
        return self._values.get('reply_to')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'EmailSettings(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.interface(jsii_type="@aws-cdk/aws-cognito.ICustomAttribute")
class ICustomAttribute(jsii.compat.Protocol):
    """Represents a custom attribute type.

    stability
    :stability: experimental
    """
    @builtins.staticmethod
    def __jsii_proxy_class__():
        return _ICustomAttributeProxy

    @jsii.member(jsii_name="bind")
    def bind(self) -> "CustomAttributeConfig":
        """Bind this custom attribute type to the values as expected by CloudFormation.

        stability
        :stability: experimental
        """
        ...


class _ICustomAttributeProxy():
    """Represents a custom attribute type.

    stability
    :stability: experimental
    """
    __jsii_type__ = "@aws-cdk/aws-cognito.ICustomAttribute"
    @jsii.member(jsii_name="bind")
    def bind(self) -> "CustomAttributeConfig":
        """Bind this custom attribute type to the values as expected by CloudFormation.

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "bind", [])


@jsii.interface(jsii_type="@aws-cdk/aws-cognito.IUserPool")
class IUserPool(aws_cdk.core.IResource, jsii.compat.Protocol):
    """Represents a Cognito UserPool.

    stability
    :stability: experimental
    """
    @builtins.staticmethod
    def __jsii_proxy_class__():
        return _IUserPoolProxy

    @builtins.property
    @jsii.member(jsii_name="userPoolArn")
    def user_pool_arn(self) -> str:
        """The ARN of this user pool resource.

        stability
        :stability: experimental
        attribute:
        :attribute:: true
        """
        ...

    @builtins.property
    @jsii.member(jsii_name="userPoolId")
    def user_pool_id(self) -> str:
        """The physical ID of this user pool resource.

        stability
        :stability: experimental
        attribute:
        :attribute:: true
        """
        ...

    @jsii.member(jsii_name="addClient")
    def add_client(self, id: str, *, auth_flows: typing.Optional["AuthFlow"]=None, generate_secret: typing.Optional[bool]=None, o_auth: typing.Optional["OAuthSettings"]=None, prevent_user_existence_errors: typing.Optional[bool]=None, user_pool_client_name: typing.Optional[str]=None) -> "IUserPoolClient":
        """Create a user pool client.

        :param id: -
        :param auth_flows: The set of OAuth authentication flows to enable on the client. Default: - all auth flows disabled
        :param generate_secret: Whether to generate a client secret. Default: false
        :param o_auth: OAuth settings for this to client to interact with the app. Default: - see defaults in ``OAuthSettings``
        :param prevent_user_existence_errors: Whether Cognito returns a UserNotFoundException exception when the user does not exist in the user pool (false), or whether it returns another type of error that doesn't reveal the user's absence. Default: true for new stacks
        :param user_pool_client_name: Name of the application client. Default: - cloudformation generated name

        stability
        :stability: experimental
        """
        ...


class _IUserPoolProxy(jsii.proxy_for(aws_cdk.core.IResource)):
    """Represents a Cognito UserPool.

    stability
    :stability: experimental
    """
    __jsii_type__ = "@aws-cdk/aws-cognito.IUserPool"
    @builtins.property
    @jsii.member(jsii_name="userPoolArn")
    def user_pool_arn(self) -> str:
        """The ARN of this user pool resource.

        stability
        :stability: experimental
        attribute:
        :attribute:: true
        """
        return jsii.get(self, "userPoolArn")

    @builtins.property
    @jsii.member(jsii_name="userPoolId")
    def user_pool_id(self) -> str:
        """The physical ID of this user pool resource.

        stability
        :stability: experimental
        attribute:
        :attribute:: true
        """
        return jsii.get(self, "userPoolId")

    @jsii.member(jsii_name="addClient")
    def add_client(self, id: str, *, auth_flows: typing.Optional["AuthFlow"]=None, generate_secret: typing.Optional[bool]=None, o_auth: typing.Optional["OAuthSettings"]=None, prevent_user_existence_errors: typing.Optional[bool]=None, user_pool_client_name: typing.Optional[str]=None) -> "IUserPoolClient":
        """Create a user pool client.

        :param id: -
        :param auth_flows: The set of OAuth authentication flows to enable on the client. Default: - all auth flows disabled
        :param generate_secret: Whether to generate a client secret. Default: false
        :param o_auth: OAuth settings for this to client to interact with the app. Default: - see defaults in ``OAuthSettings``
        :param prevent_user_existence_errors: Whether Cognito returns a UserNotFoundException exception when the user does not exist in the user pool (false), or whether it returns another type of error that doesn't reveal the user's absence. Default: true for new stacks
        :param user_pool_client_name: Name of the application client. Default: - cloudformation generated name

        stability
        :stability: experimental
        """
        options = UserPoolClientOptions(auth_flows=auth_flows, generate_secret=generate_secret, o_auth=o_auth, prevent_user_existence_errors=prevent_user_existence_errors, user_pool_client_name=user_pool_client_name)

        return jsii.invoke(self, "addClient", [id, options])


@jsii.interface(jsii_type="@aws-cdk/aws-cognito.IUserPoolClient")
class IUserPoolClient(aws_cdk.core.IResource, jsii.compat.Protocol):
    """Represents a Cognito user pool client.

    stability
    :stability: experimental
    """
    @builtins.staticmethod
    def __jsii_proxy_class__():
        return _IUserPoolClientProxy

    @builtins.property
    @jsii.member(jsii_name="userPoolClientId")
    def user_pool_client_id(self) -> str:
        """Name of the application client.

        stability
        :stability: experimental
        attribute:
        :attribute:: true
        """
        ...


class _IUserPoolClientProxy(jsii.proxy_for(aws_cdk.core.IResource)):
    """Represents a Cognito user pool client.

    stability
    :stability: experimental
    """
    __jsii_type__ = "@aws-cdk/aws-cognito.IUserPoolClient"
    @builtins.property
    @jsii.member(jsii_name="userPoolClientId")
    def user_pool_client_id(self) -> str:
        """Name of the application client.

        stability
        :stability: experimental
        attribute:
        :attribute:: true
        """
        return jsii.get(self, "userPoolClientId")


@jsii.interface(jsii_type="@aws-cdk/aws-cognito.IUserPoolDomain")
class IUserPoolDomain(aws_cdk.core.IResource, jsii.compat.Protocol):
    """Represents a user pool domain.

    stability
    :stability: experimental
    """
    @builtins.staticmethod
    def __jsii_proxy_class__():
        return _IUserPoolDomainProxy

    @builtins.property
    @jsii.member(jsii_name="domainName")
    def domain_name(self) -> str:
        """The domain that was specified to be created.

        If ``customDomain`` was selected, this holds the full domain name that was specified.
        If the ``cognitoDomain`` was used, it contains the prefix to the Cognito hosted domain.

        stability
        :stability: experimental
        attribute:
        :attribute:: true
        """
        ...


class _IUserPoolDomainProxy(jsii.proxy_for(aws_cdk.core.IResource)):
    """Represents a user pool domain.

    stability
    :stability: experimental
    """
    __jsii_type__ = "@aws-cdk/aws-cognito.IUserPoolDomain"
    @builtins.property
    @jsii.member(jsii_name="domainName")
    def domain_name(self) -> str:
        """The domain that was specified to be created.

        If ``customDomain`` was selected, this holds the full domain name that was specified.
        If the ``cognitoDomain`` was used, it contains the prefix to the Cognito hosted domain.

        stability
        :stability: experimental
        attribute:
        :attribute:: true
        """
        return jsii.get(self, "domainName")


@jsii.enum(jsii_type="@aws-cdk/aws-cognito.Mfa")
class Mfa(enum.Enum):
    """The different ways in which a user pool's MFA enforcement can be configured.

    see
    :see: https://docs.aws.amazon.com/cognito/latest/developerguide/user-pool-settings-mfa.html
    stability
    :stability: experimental
    """
    OFF = "OFF"
    """Users are not required to use MFA for sign in, and cannot configure one.

    stability
    :stability: experimental
    """
    OPTIONAL = "OPTIONAL"
    """Users are not required to use MFA for sign in, but can configure one if they so choose to.

    stability
    :stability: experimental
    """
    REQUIRED = "REQUIRED"
    """Users are required to configure an MFA, and have to use it to sign in.

    stability
    :stability: experimental
    """

@jsii.data_type(jsii_type="@aws-cdk/aws-cognito.MfaSecondFactor", jsii_struct_bases=[], name_mapping={'otp': 'otp', 'sms': 'sms'})
class MfaSecondFactor():
    def __init__(self, *, otp: bool, sms: bool) -> None:
        """The different ways in which a user pool can obtain their MFA token for sign in.

        :param otp: The MFA token is a time-based one time password that is generated by a hardware or software token. Default: false
        :param sms: The MFA token is sent to the user via SMS to their verified phone numbers. Default: true

        see
        :see: https://docs.aws.amazon.com/cognito/latest/developerguide/user-pool-settings-mfa.html
        stability
        :stability: experimental
        """
        self._values = {
            'otp': otp,
            'sms': sms,
        }

    @builtins.property
    def otp(self) -> bool:
        """The MFA token is a time-based one time password that is generated by a hardware or software token.

        default
        :default: false

        see
        :see: https://docs.aws.amazon.com/cognito/latest/developerguide/user-pool-settings-mfa-totp.html
        stability
        :stability: experimental
        """
        return self._values.get('otp')

    @builtins.property
    def sms(self) -> bool:
        """The MFA token is sent to the user via SMS to their verified phone numbers.

        default
        :default: true

        see
        :see: https://docs.aws.amazon.com/cognito/latest/developerguide/user-pool-settings-mfa-sms-text-message.html
        stability
        :stability: experimental
        """
        return self._values.get('sms')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'MfaSecondFactor(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.implements(ICustomAttribute)
class NumberAttribute(metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-cognito.NumberAttribute"):
    """The Number custom attribute type.

    stability
    :stability: experimental
    """
    def __init__(self, *, max: typing.Optional[jsii.Number]=None, min: typing.Optional[jsii.Number]=None, mutable: typing.Optional[bool]=None) -> None:
        """
        :param max: Maximum value of this attribute. Default: - no maximum value
        :param min: Minimum value of this attribute. Default: - no minimum value
        :param mutable: Specifies whether the value of the attribute can be changed. For any user pool attribute that's mapped to an identity provider attribute, you must set this parameter to true. Amazon Cognito updates mapped attributes when users sign in to your application through an identity provider. If an attribute is immutable, Amazon Cognito throws an error when it attempts to update the attribute. Default: false

        stability
        :stability: experimental
        """
        props = NumberAttributeProps(max=max, min=min, mutable=mutable)

        jsii.create(NumberAttribute, self, [props])

    @jsii.member(jsii_name="bind")
    def bind(self) -> "CustomAttributeConfig":
        """Bind this custom attribute type to the values as expected by CloudFormation.

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "bind", [])


@jsii.data_type(jsii_type="@aws-cdk/aws-cognito.NumberAttributeConstraints", jsii_struct_bases=[], name_mapping={'max': 'max', 'min': 'min'})
class NumberAttributeConstraints():
    def __init__(self, *, max: typing.Optional[jsii.Number]=None, min: typing.Optional[jsii.Number]=None) -> None:
        """Constraints that can be applied to a custom attribute of number type.

        :param max: Maximum value of this attribute. Default: - no maximum value
        :param min: Minimum value of this attribute. Default: - no minimum value

        stability
        :stability: experimental
        """
        self._values = {
        }
        if max is not None: self._values["max"] = max
        if min is not None: self._values["min"] = min

    @builtins.property
    def max(self) -> typing.Optional[jsii.Number]:
        """Maximum value of this attribute.

        default
        :default: - no maximum value

        stability
        :stability: experimental
        """
        return self._values.get('max')

    @builtins.property
    def min(self) -> typing.Optional[jsii.Number]:
        """Minimum value of this attribute.

        default
        :default: - no minimum value

        stability
        :stability: experimental
        """
        return self._values.get('min')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'NumberAttributeConstraints(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="@aws-cdk/aws-cognito.NumberAttributeProps", jsii_struct_bases=[NumberAttributeConstraints, CustomAttributeProps], name_mapping={'max': 'max', 'min': 'min', 'mutable': 'mutable'})
class NumberAttributeProps(NumberAttributeConstraints, CustomAttributeProps):
    def __init__(self, *, max: typing.Optional[jsii.Number]=None, min: typing.Optional[jsii.Number]=None, mutable: typing.Optional[bool]=None) -> None:
        """Props for NumberAttr.

        :param max: Maximum value of this attribute. Default: - no maximum value
        :param min: Minimum value of this attribute. Default: - no minimum value
        :param mutable: Specifies whether the value of the attribute can be changed. For any user pool attribute that's mapped to an identity provider attribute, you must set this parameter to true. Amazon Cognito updates mapped attributes when users sign in to your application through an identity provider. If an attribute is immutable, Amazon Cognito throws an error when it attempts to update the attribute. Default: false

        stability
        :stability: experimental
        """
        self._values = {
        }
        if max is not None: self._values["max"] = max
        if min is not None: self._values["min"] = min
        if mutable is not None: self._values["mutable"] = mutable

    @builtins.property
    def max(self) -> typing.Optional[jsii.Number]:
        """Maximum value of this attribute.

        default
        :default: - no maximum value

        stability
        :stability: experimental
        """
        return self._values.get('max')

    @builtins.property
    def min(self) -> typing.Optional[jsii.Number]:
        """Minimum value of this attribute.

        default
        :default: - no minimum value

        stability
        :stability: experimental
        """
        return self._values.get('min')

    @builtins.property
    def mutable(self) -> typing.Optional[bool]:
        """Specifies whether the value of the attribute can be changed.

        For any user pool attribute that's mapped to an identity provider attribute, you must set this parameter to true.
        Amazon Cognito updates mapped attributes when users sign in to your application through an identity provider.
        If an attribute is immutable, Amazon Cognito throws an error when it attempts to update the attribute.

        default
        :default: false

        stability
        :stability: experimental
        """
        return self._values.get('mutable')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'NumberAttributeProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="@aws-cdk/aws-cognito.OAuthFlows", jsii_struct_bases=[], name_mapping={'authorization_code_grant': 'authorizationCodeGrant', 'client_credentials': 'clientCredentials', 'implicit_code_grant': 'implicitCodeGrant'})
class OAuthFlows():
    def __init__(self, *, authorization_code_grant: typing.Optional[bool]=None, client_credentials: typing.Optional[bool]=None, implicit_code_grant: typing.Optional[bool]=None) -> None:
        """Types of OAuth grant flows.

        :param authorization_code_grant: Initiate an authorization code grant flow, which provides an authorization code as the response. Default: false
        :param client_credentials: Client should get the access token and ID token from the token endpoint using a combination of client and client_secret. Default: false
        :param implicit_code_grant: The client should get the access token and ID token directly. Default: false

        see
        :see: - the 'Allowed OAuth Flows' section at https://docs.aws.amazon.com/cognito/latest/developerguide/cognito-user-pools-app-idp-settings.html
        stability
        :stability: experimental
        """
        self._values = {
        }
        if authorization_code_grant is not None: self._values["authorization_code_grant"] = authorization_code_grant
        if client_credentials is not None: self._values["client_credentials"] = client_credentials
        if implicit_code_grant is not None: self._values["implicit_code_grant"] = implicit_code_grant

    @builtins.property
    def authorization_code_grant(self) -> typing.Optional[bool]:
        """Initiate an authorization code grant flow, which provides an authorization code as the response.

        default
        :default: false

        stability
        :stability: experimental
        """
        return self._values.get('authorization_code_grant')

    @builtins.property
    def client_credentials(self) -> typing.Optional[bool]:
        """Client should get the access token and ID token from the token endpoint using a combination of client and client_secret.

        default
        :default: false

        stability
        :stability: experimental
        """
        return self._values.get('client_credentials')

    @builtins.property
    def implicit_code_grant(self) -> typing.Optional[bool]:
        """The client should get the access token and ID token directly.

        default
        :default: false

        stability
        :stability: experimental
        """
        return self._values.get('implicit_code_grant')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'OAuthFlows(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


class OAuthScope(metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-cognito.OAuthScope"):
    """OAuth scopes that are allowed with this client.

    see
    :see: https://docs.aws.amazon.com/cognito/latest/developerguide/cognito-user-pools-app-idp-settings.html
    stability
    :stability: experimental
    """
    @jsii.member(jsii_name="custom")
    @builtins.classmethod
    def custom(cls, name: str) -> "OAuthScope":
        """Custom scope is one that you define for your own resource server in the Resource Servers.

        The format is 'resource-server-identifier/scope'.

        :param name: -

        see
        :see: https://docs.aws.amazon.com/cognito/latest/developerguide/cognito-user-pools-define-resource-servers.html
        stability
        :stability: experimental
        """
        return jsii.sinvoke(cls, "custom", [name])

    @jsii.python.classproperty
    @jsii.member(jsii_name="COGNITO_ADMIN")
    def COGNITO_ADMIN(cls) -> "OAuthScope":
        """Grants access to Amazon Cognito User Pool API operations that require access tokens, such as UpdateUserAttributes and VerifyUserAttribute.

        stability
        :stability: experimental
        """
        return jsii.sget(cls, "COGNITO_ADMIN")

    @jsii.python.classproperty
    @jsii.member(jsii_name="EMAIL")
    def EMAIL(cls) -> "OAuthScope":
        """Grants access to the 'email' and 'email_verified' claims.

        Automatically includes access to ``OAuthScope.OPENID``.

        stability
        :stability: experimental
        """
        return jsii.sget(cls, "EMAIL")

    @jsii.python.classproperty
    @jsii.member(jsii_name="OPENID")
    def OPENID(cls) -> "OAuthScope":
        """Returns all user attributes in the ID token that are readable by the client.

        stability
        :stability: experimental
        """
        return jsii.sget(cls, "OPENID")

    @jsii.python.classproperty
    @jsii.member(jsii_name="PHONE")
    def PHONE(cls) -> "OAuthScope":
        """Grants access to the 'phone_number' and 'phone_number_verified' claims.

        Automatically includes access to ``OAuthScope.OPENID``.

        stability
        :stability: experimental
        """
        return jsii.sget(cls, "PHONE")

    @jsii.python.classproperty
    @jsii.member(jsii_name="PROFILE")
    def PROFILE(cls) -> "OAuthScope":
        """Grants access to all user attributes that are readable by the client Automatically includes access to ``OAuthScope.OPENID``.

        stability
        :stability: experimental
        """
        return jsii.sget(cls, "PROFILE")

    @builtins.property
    @jsii.member(jsii_name="scopeName")
    def scope_name(self) -> str:
        """The name of this scope as recognized by CloudFormation.

        see
        :see: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpoolclient.html#cfn-cognito-userpoolclient-allowedoauthscopes
        stability
        :stability: experimental
        """
        return jsii.get(self, "scopeName")


@jsii.data_type(jsii_type="@aws-cdk/aws-cognito.OAuthSettings", jsii_struct_bases=[], name_mapping={'flows': 'flows', 'scopes': 'scopes', 'callback_urls': 'callbackUrls'})
class OAuthSettings():
    def __init__(self, *, flows: "OAuthFlows", scopes: typing.List["OAuthScope"], callback_urls: typing.Optional[typing.List[str]]=None) -> None:
        """OAuth settings to configure the interaction between the app and this client.

        :param flows: OAuth flows that are allowed with this client. Default: - all OAuth flows disabled
        :param scopes: OAuth scopes that are allowed with this client. Default: - no OAuth scopes are configured.
        :param callback_urls: List of allowed redirect URLs for the identity providers. Default: - no callback URLs

        stability
        :stability: experimental
        """
        if isinstance(flows, dict): flows = OAuthFlows(**flows)
        self._values = {
            'flows': flows,
            'scopes': scopes,
        }
        if callback_urls is not None: self._values["callback_urls"] = callback_urls

    @builtins.property
    def flows(self) -> "OAuthFlows":
        """OAuth flows that are allowed with this client.

        default
        :default: - all OAuth flows disabled

        see
        :see: - the 'Allowed OAuth Flows' section at https://docs.aws.amazon.com/cognito/latest/developerguide/cognito-user-pools-app-idp-settings.html
        stability
        :stability: experimental
        """
        return self._values.get('flows')

    @builtins.property
    def scopes(self) -> typing.List["OAuthScope"]:
        """OAuth scopes that are allowed with this client.

        default
        :default: - no OAuth scopes are configured.

        see
        :see: https://docs.aws.amazon.com/cognito/latest/developerguide/cognito-user-pools-app-idp-settings.html
        stability
        :stability: experimental
        """
        return self._values.get('scopes')

    @builtins.property
    def callback_urls(self) -> typing.Optional[typing.List[str]]:
        """List of allowed redirect URLs for the identity providers.

        default
        :default: - no callback URLs

        stability
        :stability: experimental
        """
        return self._values.get('callback_urls')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'OAuthSettings(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="@aws-cdk/aws-cognito.PasswordPolicy", jsii_struct_bases=[], name_mapping={'min_length': 'minLength', 'require_digits': 'requireDigits', 'require_lowercase': 'requireLowercase', 'require_symbols': 'requireSymbols', 'require_uppercase': 'requireUppercase', 'temp_password_validity': 'tempPasswordValidity'})
class PasswordPolicy():
    def __init__(self, *, min_length: typing.Optional[jsii.Number]=None, require_digits: typing.Optional[bool]=None, require_lowercase: typing.Optional[bool]=None, require_symbols: typing.Optional[bool]=None, require_uppercase: typing.Optional[bool]=None, temp_password_validity: typing.Optional[aws_cdk.core.Duration]=None) -> None:
        """Password policy for User Pools.

        :param min_length: Minimum length required for a user's password. Default: 8
        :param require_digits: Whether the user is required to have digits in their password. Default: true
        :param require_lowercase: Whether the user is required to have lowercase characters in their password. Default: true
        :param require_symbols: Whether the user is required to have symbols in their password. Default: true
        :param require_uppercase: Whether the user is required to have uppercase characters in their password. Default: true
        :param temp_password_validity: The length of time the temporary password generated by an admin is valid. This must be provided as whole days, like Duration.days(3) or Duration.hours(48). Fractional days, such as Duration.hours(20), will generate an error. Default: Duration.days(7)

        stability
        :stability: experimental
        """
        self._values = {
        }
        if min_length is not None: self._values["min_length"] = min_length
        if require_digits is not None: self._values["require_digits"] = require_digits
        if require_lowercase is not None: self._values["require_lowercase"] = require_lowercase
        if require_symbols is not None: self._values["require_symbols"] = require_symbols
        if require_uppercase is not None: self._values["require_uppercase"] = require_uppercase
        if temp_password_validity is not None: self._values["temp_password_validity"] = temp_password_validity

    @builtins.property
    def min_length(self) -> typing.Optional[jsii.Number]:
        """Minimum length required for a user's password.

        default
        :default: 8

        stability
        :stability: experimental
        """
        return self._values.get('min_length')

    @builtins.property
    def require_digits(self) -> typing.Optional[bool]:
        """Whether the user is required to have digits in their password.

        default
        :default: true

        stability
        :stability: experimental
        """
        return self._values.get('require_digits')

    @builtins.property
    def require_lowercase(self) -> typing.Optional[bool]:
        """Whether the user is required to have lowercase characters in their password.

        default
        :default: true

        stability
        :stability: experimental
        """
        return self._values.get('require_lowercase')

    @builtins.property
    def require_symbols(self) -> typing.Optional[bool]:
        """Whether the user is required to have symbols in their password.

        default
        :default: true

        stability
        :stability: experimental
        """
        return self._values.get('require_symbols')

    @builtins.property
    def require_uppercase(self) -> typing.Optional[bool]:
        """Whether the user is required to have uppercase characters in their password.

        default
        :default: true

        stability
        :stability: experimental
        """
        return self._values.get('require_uppercase')

    @builtins.property
    def temp_password_validity(self) -> typing.Optional[aws_cdk.core.Duration]:
        """The length of time the temporary password generated by an admin is valid.

        This must be provided as whole days, like Duration.days(3) or Duration.hours(48).
        Fractional days, such as Duration.hours(20), will generate an error.

        default
        :default: Duration.days(7)

        stability
        :stability: experimental
        """
        return self._values.get('temp_password_validity')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'PasswordPolicy(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="@aws-cdk/aws-cognito.RequiredAttributes", jsii_struct_bases=[], name_mapping={'address': 'address', 'birthdate': 'birthdate', 'email': 'email', 'family_name': 'familyName', 'fullname': 'fullname', 'gender': 'gender', 'given_name': 'givenName', 'last_update_time': 'lastUpdateTime', 'locale': 'locale', 'middle_name': 'middleName', 'nickname': 'nickname', 'phone_number': 'phoneNumber', 'preferred_username': 'preferredUsername', 'profile_page': 'profilePage', 'profile_picture': 'profilePicture', 'timezone': 'timezone', 'website': 'website'})
class RequiredAttributes():
    def __init__(self, *, address: typing.Optional[bool]=None, birthdate: typing.Optional[bool]=None, email: typing.Optional[bool]=None, family_name: typing.Optional[bool]=None, fullname: typing.Optional[bool]=None, gender: typing.Optional[bool]=None, given_name: typing.Optional[bool]=None, last_update_time: typing.Optional[bool]=None, locale: typing.Optional[bool]=None, middle_name: typing.Optional[bool]=None, nickname: typing.Optional[bool]=None, phone_number: typing.Optional[bool]=None, preferred_username: typing.Optional[bool]=None, profile_page: typing.Optional[bool]=None, profile_picture: typing.Optional[bool]=None, timezone: typing.Optional[bool]=None, website: typing.Optional[bool]=None) -> None:
        """The set of standard attributes that can be marked as required.

        :param address: Whether the user's postal address is a required attribute. Default: false
        :param birthdate: Whether the user's birthday, represented as an ISO 8601:2004 format, is a required attribute. Default: false
        :param email: Whether the user's e-mail address, represented as an RFC 5322 [RFC5322] addr-spec, is a required attribute. Default: false
        :param family_name: Whether the surname or last name of the user is a required attribute. Default: false
        :param fullname: Whether user's full name in displayable form, including all name parts, titles and suffixes, is a required attibute. Default: false
        :param gender: Whether the user's gender is a required attribute. Default: false
        :param given_name: Whether the user's first name or give name is a required attribute. Default: false
        :param last_update_time: Whether the time, the user's information was last updated, is a required attribute. Default: false
        :param locale: Whether the user's locale, represented as a BCP47 [RFC5646] language tag, is a required attribute. Default: false
        :param middle_name: Whether the user's middle name is a required attribute. Default: false
        :param nickname: Whether the user's nickname or casual name is a required attribute. Default: false
        :param phone_number: Whether the user's telephone number is a required attribute. Default: false
        :param preferred_username: Whether the user's preffered username, different from the immutable user name, is a required attribute. Default: false
        :param profile_page: Whether the URL to the user's profile page is a required attribute. Default: false
        :param profile_picture: Whether the URL to the user's profile picture is a required attribute. Default: false
        :param timezone: Whether the user's time zone is a required attribute. Default: false
        :param website: Whether the URL to the user's web page or blog is a required attribute. Default: false

        see
        :see: https://docs.aws.amazon.com/cognito/latest/developerguide/user-pool-settings-attributes.html#cognito-user-pools-standard-attributes
        stability
        :stability: experimental
        """
        self._values = {
        }
        if address is not None: self._values["address"] = address
        if birthdate is not None: self._values["birthdate"] = birthdate
        if email is not None: self._values["email"] = email
        if family_name is not None: self._values["family_name"] = family_name
        if fullname is not None: self._values["fullname"] = fullname
        if gender is not None: self._values["gender"] = gender
        if given_name is not None: self._values["given_name"] = given_name
        if last_update_time is not None: self._values["last_update_time"] = last_update_time
        if locale is not None: self._values["locale"] = locale
        if middle_name is not None: self._values["middle_name"] = middle_name
        if nickname is not None: self._values["nickname"] = nickname
        if phone_number is not None: self._values["phone_number"] = phone_number
        if preferred_username is not None: self._values["preferred_username"] = preferred_username
        if profile_page is not None: self._values["profile_page"] = profile_page
        if profile_picture is not None: self._values["profile_picture"] = profile_picture
        if timezone is not None: self._values["timezone"] = timezone
        if website is not None: self._values["website"] = website

    @builtins.property
    def address(self) -> typing.Optional[bool]:
        """Whether the user's postal address is a required attribute.

        default
        :default: false

        stability
        :stability: experimental
        """
        return self._values.get('address')

    @builtins.property
    def birthdate(self) -> typing.Optional[bool]:
        """Whether the user's birthday, represented as an ISO 8601:2004 format, is a required attribute.

        default
        :default: false

        stability
        :stability: experimental
        """
        return self._values.get('birthdate')

    @builtins.property
    def email(self) -> typing.Optional[bool]:
        """Whether the user's e-mail address, represented as an RFC 5322 [RFC5322] addr-spec, is a required attribute.

        default
        :default: false

        stability
        :stability: experimental
        """
        return self._values.get('email')

    @builtins.property
    def family_name(self) -> typing.Optional[bool]:
        """Whether the surname or last name of the user is a required attribute.

        default
        :default: false

        stability
        :stability: experimental
        """
        return self._values.get('family_name')

    @builtins.property
    def fullname(self) -> typing.Optional[bool]:
        """Whether user's full name in displayable form, including all name parts, titles and suffixes, is a required attibute.

        default
        :default: false

        stability
        :stability: experimental
        """
        return self._values.get('fullname')

    @builtins.property
    def gender(self) -> typing.Optional[bool]:
        """Whether the user's gender is a required attribute.

        default
        :default: false

        stability
        :stability: experimental
        """
        return self._values.get('gender')

    @builtins.property
    def given_name(self) -> typing.Optional[bool]:
        """Whether the user's first name or give name is a required attribute.

        default
        :default: false

        stability
        :stability: experimental
        """
        return self._values.get('given_name')

    @builtins.property
    def last_update_time(self) -> typing.Optional[bool]:
        """Whether the time, the user's information was last updated, is a required attribute.

        default
        :default: false

        stability
        :stability: experimental
        """
        return self._values.get('last_update_time')

    @builtins.property
    def locale(self) -> typing.Optional[bool]:
        """Whether the user's locale, represented as a BCP47 [RFC5646] language tag, is a required attribute.

        default
        :default: false

        stability
        :stability: experimental
        """
        return self._values.get('locale')

    @builtins.property
    def middle_name(self) -> typing.Optional[bool]:
        """Whether the user's middle name is a required attribute.

        default
        :default: false

        stability
        :stability: experimental
        """
        return self._values.get('middle_name')

    @builtins.property
    def nickname(self) -> typing.Optional[bool]:
        """Whether the user's nickname or casual name is a required attribute.

        default
        :default: false

        stability
        :stability: experimental
        """
        return self._values.get('nickname')

    @builtins.property
    def phone_number(self) -> typing.Optional[bool]:
        """Whether the user's telephone number is a required attribute.

        default
        :default: false

        stability
        :stability: experimental
        """
        return self._values.get('phone_number')

    @builtins.property
    def preferred_username(self) -> typing.Optional[bool]:
        """Whether the user's preffered username, different from the immutable user name, is a required attribute.

        default
        :default: false

        stability
        :stability: experimental
        """
        return self._values.get('preferred_username')

    @builtins.property
    def profile_page(self) -> typing.Optional[bool]:
        """Whether the URL to the user's profile page is a required attribute.

        default
        :default: false

        stability
        :stability: experimental
        """
        return self._values.get('profile_page')

    @builtins.property
    def profile_picture(self) -> typing.Optional[bool]:
        """Whether the URL to the user's profile picture is a required attribute.

        default
        :default: false

        stability
        :stability: experimental
        """
        return self._values.get('profile_picture')

    @builtins.property
    def timezone(self) -> typing.Optional[bool]:
        """Whether the user's time zone is a required attribute.

        default
        :default: false

        stability
        :stability: experimental
        """
        return self._values.get('timezone')

    @builtins.property
    def website(self) -> typing.Optional[bool]:
        """Whether the URL to the user's web page or blog is a required attribute.

        default
        :default: false

        stability
        :stability: experimental
        """
        return self._values.get('website')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'RequiredAttributes(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="@aws-cdk/aws-cognito.SignInAliases", jsii_struct_bases=[], name_mapping={'email': 'email', 'phone': 'phone', 'preferred_username': 'preferredUsername', 'username': 'username'})
class SignInAliases():
    def __init__(self, *, email: typing.Optional[bool]=None, phone: typing.Optional[bool]=None, preferred_username: typing.Optional[bool]=None, username: typing.Optional[bool]=None) -> None:
        """The different ways in which users of this pool can sign up or sign in.

        :param email: Whether a user is allowed to sign up or sign in with an email address. Default: false
        :param phone: Whether a user is allowed to sign up or sign in with a phone number. Default: false
        :param preferred_username: Whether a user is allowed to ign in with a secondary username, that can be set and modified after sign up. Can only be used in conjunction with ``USERNAME``. Default: false
        :param username: Whether user is allowed to sign up or sign in with a username. Default: true

        stability
        :stability: experimental
        """
        self._values = {
        }
        if email is not None: self._values["email"] = email
        if phone is not None: self._values["phone"] = phone
        if preferred_username is not None: self._values["preferred_username"] = preferred_username
        if username is not None: self._values["username"] = username

    @builtins.property
    def email(self) -> typing.Optional[bool]:
        """Whether a user is allowed to sign up or sign in with an email address.

        default
        :default: false

        stability
        :stability: experimental
        """
        return self._values.get('email')

    @builtins.property
    def phone(self) -> typing.Optional[bool]:
        """Whether a user is allowed to sign up or sign in with a phone number.

        default
        :default: false

        stability
        :stability: experimental
        """
        return self._values.get('phone')

    @builtins.property
    def preferred_username(self) -> typing.Optional[bool]:
        """Whether a user is allowed to ign in with a secondary username, that can be set and modified after sign up.

        Can only be used in conjunction with ``USERNAME``.

        default
        :default: false

        stability
        :stability: experimental
        """
        return self._values.get('preferred_username')

    @builtins.property
    def username(self) -> typing.Optional[bool]:
        """Whether user is allowed to sign up or sign in with a username.

        default
        :default: true

        stability
        :stability: experimental
        """
        return self._values.get('username')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'SignInAliases(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.implements(ICustomAttribute)
class StringAttribute(metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-cognito.StringAttribute"):
    """The String custom attribute type.

    stability
    :stability: experimental
    """
    def __init__(self, *, max_len: typing.Optional[jsii.Number]=None, min_len: typing.Optional[jsii.Number]=None, mutable: typing.Optional[bool]=None) -> None:
        """
        :param max_len: Maximum length of this attribute. Default: 2048
        :param min_len: Minimum length of this attribute. Default: 0
        :param mutable: Specifies whether the value of the attribute can be changed. For any user pool attribute that's mapped to an identity provider attribute, you must set this parameter to true. Amazon Cognito updates mapped attributes when users sign in to your application through an identity provider. If an attribute is immutable, Amazon Cognito throws an error when it attempts to update the attribute. Default: false

        stability
        :stability: experimental
        """
        props = StringAttributeProps(max_len=max_len, min_len=min_len, mutable=mutable)

        jsii.create(StringAttribute, self, [props])

    @jsii.member(jsii_name="bind")
    def bind(self) -> "CustomAttributeConfig":
        """Bind this custom attribute type to the values as expected by CloudFormation.

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "bind", [])


@jsii.data_type(jsii_type="@aws-cdk/aws-cognito.StringAttributeConstraints", jsii_struct_bases=[], name_mapping={'max_len': 'maxLen', 'min_len': 'minLen'})
class StringAttributeConstraints():
    def __init__(self, *, max_len: typing.Optional[jsii.Number]=None, min_len: typing.Optional[jsii.Number]=None) -> None:
        """Constraints that can be applied to a custom attribute of string type.

        :param max_len: Maximum length of this attribute. Default: 2048
        :param min_len: Minimum length of this attribute. Default: 0

        stability
        :stability: experimental
        """
        self._values = {
        }
        if max_len is not None: self._values["max_len"] = max_len
        if min_len is not None: self._values["min_len"] = min_len

    @builtins.property
    def max_len(self) -> typing.Optional[jsii.Number]:
        """Maximum length of this attribute.

        default
        :default: 2048

        stability
        :stability: experimental
        """
        return self._values.get('max_len')

    @builtins.property
    def min_len(self) -> typing.Optional[jsii.Number]:
        """Minimum length of this attribute.

        default
        :default: 0

        stability
        :stability: experimental
        """
        return self._values.get('min_len')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'StringAttributeConstraints(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="@aws-cdk/aws-cognito.StringAttributeProps", jsii_struct_bases=[StringAttributeConstraints, CustomAttributeProps], name_mapping={'max_len': 'maxLen', 'min_len': 'minLen', 'mutable': 'mutable'})
class StringAttributeProps(StringAttributeConstraints, CustomAttributeProps):
    def __init__(self, *, max_len: typing.Optional[jsii.Number]=None, min_len: typing.Optional[jsii.Number]=None, mutable: typing.Optional[bool]=None) -> None:
        """Props for constructing a StringAttr.

        :param max_len: Maximum length of this attribute. Default: 2048
        :param min_len: Minimum length of this attribute. Default: 0
        :param mutable: Specifies whether the value of the attribute can be changed. For any user pool attribute that's mapped to an identity provider attribute, you must set this parameter to true. Amazon Cognito updates mapped attributes when users sign in to your application through an identity provider. If an attribute is immutable, Amazon Cognito throws an error when it attempts to update the attribute. Default: false

        stability
        :stability: experimental
        """
        self._values = {
        }
        if max_len is not None: self._values["max_len"] = max_len
        if min_len is not None: self._values["min_len"] = min_len
        if mutable is not None: self._values["mutable"] = mutable

    @builtins.property
    def max_len(self) -> typing.Optional[jsii.Number]:
        """Maximum length of this attribute.

        default
        :default: 2048

        stability
        :stability: experimental
        """
        return self._values.get('max_len')

    @builtins.property
    def min_len(self) -> typing.Optional[jsii.Number]:
        """Minimum length of this attribute.

        default
        :default: 0

        stability
        :stability: experimental
        """
        return self._values.get('min_len')

    @builtins.property
    def mutable(self) -> typing.Optional[bool]:
        """Specifies whether the value of the attribute can be changed.

        For any user pool attribute that's mapped to an identity provider attribute, you must set this parameter to true.
        Amazon Cognito updates mapped attributes when users sign in to your application through an identity provider.
        If an attribute is immutable, Amazon Cognito throws an error when it attempts to update the attribute.

        default
        :default: false

        stability
        :stability: experimental
        """
        return self._values.get('mutable')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'StringAttributeProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="@aws-cdk/aws-cognito.UserInvitationConfig", jsii_struct_bases=[], name_mapping={'email_body': 'emailBody', 'email_subject': 'emailSubject', 'sms_message': 'smsMessage'})
class UserInvitationConfig():
    def __init__(self, *, email_body: typing.Optional[str]=None, email_subject: typing.Optional[str]=None, sms_message: typing.Optional[str]=None) -> None:
        """User pool configuration when administrators sign users up.

        :param email_body: The template to the email body that is sent to the user when an administrator signs them up to the user pool. Default: 'Your username is {username} and temporary password is {####}.'
        :param email_subject: The template to the email subject that is sent to the user when an administrator signs them up to the user pool. Default: 'Your temporary password'
        :param sms_message: The template to the SMS message that is sent to the user when an administrator signs them up to the user pool. Default: 'Your username is {username} and temporary password is {####}'

        stability
        :stability: experimental
        """
        self._values = {
        }
        if email_body is not None: self._values["email_body"] = email_body
        if email_subject is not None: self._values["email_subject"] = email_subject
        if sms_message is not None: self._values["sms_message"] = sms_message

    @builtins.property
    def email_body(self) -> typing.Optional[str]:
        """The template to the email body that is sent to the user when an administrator signs them up to the user pool.

        default
        :default: 'Your username is {username} and temporary password is {####}.'

        stability
        :stability: experimental
        """
        return self._values.get('email_body')

    @builtins.property
    def email_subject(self) -> typing.Optional[str]:
        """The template to the email subject that is sent to the user when an administrator signs them up to the user pool.

        default
        :default: 'Your temporary password'

        stability
        :stability: experimental
        """
        return self._values.get('email_subject')

    @builtins.property
    def sms_message(self) -> typing.Optional[str]:
        """The template to the SMS message that is sent to the user when an administrator signs them up to the user pool.

        default
        :default: 'Your username is {username} and temporary password is {####}'

        stability
        :stability: experimental
        """
        return self._values.get('sms_message')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'UserInvitationConfig(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.implements(IUserPool)
class UserPool(aws_cdk.core.Resource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-cognito.UserPool"):
    """Define a Cognito User Pool.

    stability
    :stability: experimental
    """
    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, auto_verify: typing.Optional["AutoVerifiedAttrs"]=None, custom_attributes: typing.Optional[typing.Mapping[str, "ICustomAttribute"]]=None, email_settings: typing.Optional["EmailSettings"]=None, lambda_triggers: typing.Optional["UserPoolTriggers"]=None, mfa: typing.Optional["Mfa"]=None, mfa_second_factor: typing.Optional["MfaSecondFactor"]=None, password_policy: typing.Optional["PasswordPolicy"]=None, required_attributes: typing.Optional["RequiredAttributes"]=None, self_sign_up_enabled: typing.Optional[bool]=None, sign_in_aliases: typing.Optional["SignInAliases"]=None, sign_in_case_sensitive: typing.Optional[bool]=None, sms_role: typing.Optional[aws_cdk.aws_iam.IRole]=None, sms_role_external_id: typing.Optional[str]=None, user_invitation: typing.Optional["UserInvitationConfig"]=None, user_pool_name: typing.Optional[str]=None, user_verification: typing.Optional["UserVerificationConfig"]=None) -> None:
        """
        :param scope: -
        :param id: -
        :param auto_verify: Attributes which Cognito will look to verify automatically upon user sign up. EMAIL and PHONE are the only available options. Default: - If ``signInAlias`` includes email and/or phone, they will be included in ``autoVerifiedAttributes`` by default. If absent, no attributes will be auto-verified.
        :param custom_attributes: Define a set of custom attributes that can be configured for each user in the user pool. Default: - No custom attributes.
        :param email_settings: Email settings for a user pool. Default: - see defaults on each property of EmailSettings.
        :param lambda_triggers: Lambda functions to use for supported Cognito triggers. Default: - No Lambda triggers.
        :param mfa: Configure whether users of this user pool can or are required use MFA to sign in. Default: Mfa.OFF
        :param mfa_second_factor: Configure the MFA types that users can use in this user pool. Ignored if ``mfa`` is set to ``OFF``. Default: - { sms: true, oneTimePassword: false }, if ``mfa`` is set to ``OPTIONAL`` or ``REQUIRED``. { sms: false, oneTimePassword: false }, otherwise
        :param password_policy: Password policy for this user pool. Default: - see defaults on each property of PasswordPolicy.
        :param required_attributes: The set of attributes that are required for every user in the user pool. Read more on attributes here - https://docs.aws.amazon.com/cognito/latest/developerguide/user-pool-settings-attributes.html Default: - No attributes are required.
        :param self_sign_up_enabled: Whether self sign up should be enabled. This can be further configured via the ``selfSignUp`` property. Default: false
        :param sign_in_aliases: Methods in which a user registers or signs in to a user pool. Allows either username with aliases OR sign in with email, phone, or both. Read the sections on usernames and aliases to learn more - https://docs.aws.amazon.com/cognito/latest/developerguide/user-pool-settings-attributes.html To match with 'Option 1' in the above link, with a verified email, this property should be set to ``{ username: true, email: true }``. To match with 'Option 2' in the above link with both a verified email and phone number, this property should be set to ``{ email: true, phone: true }``. Default: { username: true }
        :param sign_in_case_sensitive: Whether sign-in aliases should be evaluated with case sensitivity. For example, when this option is set to false, users will be able to sign in using either ``MyUsername`` or ``myusername``. Default: true
        :param sms_role: The IAM role that Cognito will assume while sending SMS messages. Default: - a new IAM role is created
        :param sms_role_external_id: The 'ExternalId' that Cognito service must using when assuming the ``smsRole``, if the role is restricted with an 'sts:ExternalId' conditional. Learn more about ExternalId here - https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_create_for-user_externalid.html This property will be ignored if ``smsRole`` is not specified. Default: - No external id will be configured
        :param user_invitation: Configuration around admins signing up users into a user pool. Default: - see defaults in UserInvitationConfig
        :param user_pool_name: Name of the user pool. Default: - automatically generated name by CloudFormation at deploy time
        :param user_verification: Configuration around users signing themselves up to the user pool. Enable or disable self sign-up via the ``selfSignUpEnabled`` property. Default: - see defaults in UserVerificationConfig

        stability
        :stability: experimental
        """
        props = UserPoolProps(auto_verify=auto_verify, custom_attributes=custom_attributes, email_settings=email_settings, lambda_triggers=lambda_triggers, mfa=mfa, mfa_second_factor=mfa_second_factor, password_policy=password_policy, required_attributes=required_attributes, self_sign_up_enabled=self_sign_up_enabled, sign_in_aliases=sign_in_aliases, sign_in_case_sensitive=sign_in_case_sensitive, sms_role=sms_role, sms_role_external_id=sms_role_external_id, user_invitation=user_invitation, user_pool_name=user_pool_name, user_verification=user_verification)

        jsii.create(UserPool, self, [scope, id, props])

    @jsii.member(jsii_name="fromUserPoolArn")
    @builtins.classmethod
    def from_user_pool_arn(cls, scope: aws_cdk.core.Construct, id: str, user_pool_arn: str) -> "IUserPool":
        """Import an existing user pool based on its ARN.

        :param scope: -
        :param id: -
        :param user_pool_arn: -

        stability
        :stability: experimental
        """
        return jsii.sinvoke(cls, "fromUserPoolArn", [scope, id, user_pool_arn])

    @jsii.member(jsii_name="fromUserPoolId")
    @builtins.classmethod
    def from_user_pool_id(cls, scope: aws_cdk.core.Construct, id: str, user_pool_id: str) -> "IUserPool":
        """Import an existing user pool based on its id.

        :param scope: -
        :param id: -
        :param user_pool_id: -

        stability
        :stability: experimental
        """
        return jsii.sinvoke(cls, "fromUserPoolId", [scope, id, user_pool_id])

    @jsii.member(jsii_name="addClient")
    def add_client(self, id: str, *, auth_flows: typing.Optional["AuthFlow"]=None, generate_secret: typing.Optional[bool]=None, o_auth: typing.Optional["OAuthSettings"]=None, prevent_user_existence_errors: typing.Optional[bool]=None, user_pool_client_name: typing.Optional[str]=None) -> "IUserPoolClient":
        """Add a new app client to this user pool.

        :param id: -
        :param auth_flows: The set of OAuth authentication flows to enable on the client. Default: - all auth flows disabled
        :param generate_secret: Whether to generate a client secret. Default: false
        :param o_auth: OAuth settings for this to client to interact with the app. Default: - see defaults in ``OAuthSettings``
        :param prevent_user_existence_errors: Whether Cognito returns a UserNotFoundException exception when the user does not exist in the user pool (false), or whether it returns another type of error that doesn't reveal the user's absence. Default: true for new stacks
        :param user_pool_client_name: Name of the application client. Default: - cloudformation generated name

        see
        :see: https://docs.aws.amazon.com/cognito/latest/developerguide/user-pool-settings-client-apps.html
        stability
        :stability: experimental
        """
        options = UserPoolClientOptions(auth_flows=auth_flows, generate_secret=generate_secret, o_auth=o_auth, prevent_user_existence_errors=prevent_user_existence_errors, user_pool_client_name=user_pool_client_name)

        return jsii.invoke(self, "addClient", [id, options])

    @jsii.member(jsii_name="addDomain")
    def add_domain(self, id: str, *, cognito_domain: typing.Optional["CognitoDomainOptions"]=None, custom_domain: typing.Optional["CustomDomainOptions"]=None) -> "UserPoolDomain":
        """Associate a domain to this user pool.

        :param id: -
        :param cognito_domain: Associate a cognito prefix domain with your user pool Either ``customDomain`` or ``cognitoDomain`` must be specified. Default: - not set if ``customDomain`` is specified, otherwise, throws an error.
        :param custom_domain: Associate a custom domain with your user pool Either ``customDomain`` or ``cognitoDomain`` must be specified. Default: - not set if ``cognitoDomain`` is specified, otherwise, throws an error.

        see
        :see: https://docs.aws.amazon.com/cognito/latest/developerguide/cognito-user-pools-assign-domain.html
        stability
        :stability: experimental
        """
        options = UserPoolDomainOptions(cognito_domain=cognito_domain, custom_domain=custom_domain)

        return jsii.invoke(self, "addDomain", [id, options])

    @jsii.member(jsii_name="addTrigger")
    def add_trigger(self, operation: "UserPoolOperation", fn: aws_cdk.aws_lambda.IFunction) -> None:
        """Add a lambda trigger to a user pool operation.

        :param operation: -
        :param fn: -

        see
        :see: https://docs.aws.amazon.com/cognito/latest/developerguide/cognito-user-identity-pools-working-with-aws-lambda-triggers.html
        stability
        :stability: experimental
        """
        return jsii.invoke(self, "addTrigger", [operation, fn])

    @builtins.property
    @jsii.member(jsii_name="userPoolArn")
    def user_pool_arn(self) -> str:
        """The ARN of the user pool.

        stability
        :stability: experimental
        """
        return jsii.get(self, "userPoolArn")

    @builtins.property
    @jsii.member(jsii_name="userPoolId")
    def user_pool_id(self) -> str:
        """The physical ID of this user pool resource.

        stability
        :stability: experimental
        """
        return jsii.get(self, "userPoolId")

    @builtins.property
    @jsii.member(jsii_name="userPoolProviderName")
    def user_pool_provider_name(self) -> str:
        """User pool provider name.

        stability
        :stability: experimental
        attribute:
        :attribute:: true
        """
        return jsii.get(self, "userPoolProviderName")

    @builtins.property
    @jsii.member(jsii_name="userPoolProviderUrl")
    def user_pool_provider_url(self) -> str:
        """User pool provider URL.

        stability
        :stability: experimental
        attribute:
        :attribute:: true
        """
        return jsii.get(self, "userPoolProviderUrl")


@jsii.implements(IUserPoolClient)
class UserPoolClient(aws_cdk.core.Resource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-cognito.UserPoolClient"):
    """Define a UserPool App Client.

    stability
    :stability: experimental
    """
    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, user_pool: "IUserPool", auth_flows: typing.Optional["AuthFlow"]=None, generate_secret: typing.Optional[bool]=None, o_auth: typing.Optional["OAuthSettings"]=None, prevent_user_existence_errors: typing.Optional[bool]=None, user_pool_client_name: typing.Optional[str]=None) -> None:
        """
        :param scope: -
        :param id: -
        :param user_pool: The UserPool resource this client will have access to.
        :param auth_flows: The set of OAuth authentication flows to enable on the client. Default: - all auth flows disabled
        :param generate_secret: Whether to generate a client secret. Default: false
        :param o_auth: OAuth settings for this to client to interact with the app. Default: - see defaults in ``OAuthSettings``
        :param prevent_user_existence_errors: Whether Cognito returns a UserNotFoundException exception when the user does not exist in the user pool (false), or whether it returns another type of error that doesn't reveal the user's absence. Default: true for new stacks
        :param user_pool_client_name: Name of the application client. Default: - cloudformation generated name

        stability
        :stability: experimental
        """
        props = UserPoolClientProps(user_pool=user_pool, auth_flows=auth_flows, generate_secret=generate_secret, o_auth=o_auth, prevent_user_existence_errors=prevent_user_existence_errors, user_pool_client_name=user_pool_client_name)

        jsii.create(UserPoolClient, self, [scope, id, props])

    @jsii.member(jsii_name="fromUserPoolClientId")
    @builtins.classmethod
    def from_user_pool_client_id(cls, scope: aws_cdk.core.Construct, id: str, user_pool_client_id: str) -> "IUserPoolClient":
        """Import a user pool client given its id.

        :param scope: -
        :param id: -
        :param user_pool_client_id: -

        stability
        :stability: experimental
        """
        return jsii.sinvoke(cls, "fromUserPoolClientId", [scope, id, user_pool_client_id])

    @builtins.property
    @jsii.member(jsii_name="userPoolClientId")
    def user_pool_client_id(self) -> str:
        """Name of the application client.

        stability
        :stability: experimental
        """
        return jsii.get(self, "userPoolClientId")

    @builtins.property
    @jsii.member(jsii_name="userPoolClientName")
    def user_pool_client_name(self) -> str:
        """The client name that was specified via the ``userPoolClientName`` property during initialization, throws an error otherwise.

        stability
        :stability: experimental
        """
        return jsii.get(self, "userPoolClientName")


@jsii.data_type(jsii_type="@aws-cdk/aws-cognito.UserPoolClientOptions", jsii_struct_bases=[], name_mapping={'auth_flows': 'authFlows', 'generate_secret': 'generateSecret', 'o_auth': 'oAuth', 'prevent_user_existence_errors': 'preventUserExistenceErrors', 'user_pool_client_name': 'userPoolClientName'})
class UserPoolClientOptions():
    def __init__(self, *, auth_flows: typing.Optional["AuthFlow"]=None, generate_secret: typing.Optional[bool]=None, o_auth: typing.Optional["OAuthSettings"]=None, prevent_user_existence_errors: typing.Optional[bool]=None, user_pool_client_name: typing.Optional[str]=None) -> None:
        """Options to create a UserPoolClient.

        :param auth_flows: The set of OAuth authentication flows to enable on the client. Default: - all auth flows disabled
        :param generate_secret: Whether to generate a client secret. Default: false
        :param o_auth: OAuth settings for this to client to interact with the app. Default: - see defaults in ``OAuthSettings``
        :param prevent_user_existence_errors: Whether Cognito returns a UserNotFoundException exception when the user does not exist in the user pool (false), or whether it returns another type of error that doesn't reveal the user's absence. Default: true for new stacks
        :param user_pool_client_name: Name of the application client. Default: - cloudformation generated name

        stability
        :stability: experimental
        """
        if isinstance(auth_flows, dict): auth_flows = AuthFlow(**auth_flows)
        if isinstance(o_auth, dict): o_auth = OAuthSettings(**o_auth)
        self._values = {
        }
        if auth_flows is not None: self._values["auth_flows"] = auth_flows
        if generate_secret is not None: self._values["generate_secret"] = generate_secret
        if o_auth is not None: self._values["o_auth"] = o_auth
        if prevent_user_existence_errors is not None: self._values["prevent_user_existence_errors"] = prevent_user_existence_errors
        if user_pool_client_name is not None: self._values["user_pool_client_name"] = user_pool_client_name

    @builtins.property
    def auth_flows(self) -> typing.Optional["AuthFlow"]:
        """The set of OAuth authentication flows to enable on the client.

        default
        :default: - all auth flows disabled

        see
        :see: https://docs.aws.amazon.com/cognito/latest/developerguide/amazon-cognito-user-pools-authentication-flow.html
        stability
        :stability: experimental
        """
        return self._values.get('auth_flows')

    @builtins.property
    def generate_secret(self) -> typing.Optional[bool]:
        """Whether to generate a client secret.

        default
        :default: false

        stability
        :stability: experimental
        """
        return self._values.get('generate_secret')

    @builtins.property
    def o_auth(self) -> typing.Optional["OAuthSettings"]:
        """OAuth settings for this to client to interact with the app.

        default
        :default: - see defaults in ``OAuthSettings``

        stability
        :stability: experimental
        """
        return self._values.get('o_auth')

    @builtins.property
    def prevent_user_existence_errors(self) -> typing.Optional[bool]:
        """Whether Cognito returns a UserNotFoundException exception when the user does not exist in the user pool (false), or whether it returns another type of error that doesn't reveal the user's absence.

        default
        :default: true for new stacks

        see
        :see: https://docs.aws.amazon.com/cognito/latest/developerguide/cognito-user-pool-managing-errors.html
        stability
        :stability: experimental
        """
        return self._values.get('prevent_user_existence_errors')

    @builtins.property
    def user_pool_client_name(self) -> typing.Optional[str]:
        """Name of the application client.

        default
        :default: - cloudformation generated name

        stability
        :stability: experimental
        """
        return self._values.get('user_pool_client_name')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'UserPoolClientOptions(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="@aws-cdk/aws-cognito.UserPoolClientProps", jsii_struct_bases=[UserPoolClientOptions], name_mapping={'auth_flows': 'authFlows', 'generate_secret': 'generateSecret', 'o_auth': 'oAuth', 'prevent_user_existence_errors': 'preventUserExistenceErrors', 'user_pool_client_name': 'userPoolClientName', 'user_pool': 'userPool'})
class UserPoolClientProps(UserPoolClientOptions):
    def __init__(self, *, auth_flows: typing.Optional["AuthFlow"]=None, generate_secret: typing.Optional[bool]=None, o_auth: typing.Optional["OAuthSettings"]=None, prevent_user_existence_errors: typing.Optional[bool]=None, user_pool_client_name: typing.Optional[str]=None, user_pool: "IUserPool") -> None:
        """Properties for the UserPoolClient construct.

        :param auth_flows: The set of OAuth authentication flows to enable on the client. Default: - all auth flows disabled
        :param generate_secret: Whether to generate a client secret. Default: false
        :param o_auth: OAuth settings for this to client to interact with the app. Default: - see defaults in ``OAuthSettings``
        :param prevent_user_existence_errors: Whether Cognito returns a UserNotFoundException exception when the user does not exist in the user pool (false), or whether it returns another type of error that doesn't reveal the user's absence. Default: true for new stacks
        :param user_pool_client_name: Name of the application client. Default: - cloudformation generated name
        :param user_pool: The UserPool resource this client will have access to.

        stability
        :stability: experimental
        """
        if isinstance(auth_flows, dict): auth_flows = AuthFlow(**auth_flows)
        if isinstance(o_auth, dict): o_auth = OAuthSettings(**o_auth)
        self._values = {
            'user_pool': user_pool,
        }
        if auth_flows is not None: self._values["auth_flows"] = auth_flows
        if generate_secret is not None: self._values["generate_secret"] = generate_secret
        if o_auth is not None: self._values["o_auth"] = o_auth
        if prevent_user_existence_errors is not None: self._values["prevent_user_existence_errors"] = prevent_user_existence_errors
        if user_pool_client_name is not None: self._values["user_pool_client_name"] = user_pool_client_name

    @builtins.property
    def auth_flows(self) -> typing.Optional["AuthFlow"]:
        """The set of OAuth authentication flows to enable on the client.

        default
        :default: - all auth flows disabled

        see
        :see: https://docs.aws.amazon.com/cognito/latest/developerguide/amazon-cognito-user-pools-authentication-flow.html
        stability
        :stability: experimental
        """
        return self._values.get('auth_flows')

    @builtins.property
    def generate_secret(self) -> typing.Optional[bool]:
        """Whether to generate a client secret.

        default
        :default: false

        stability
        :stability: experimental
        """
        return self._values.get('generate_secret')

    @builtins.property
    def o_auth(self) -> typing.Optional["OAuthSettings"]:
        """OAuth settings for this to client to interact with the app.

        default
        :default: - see defaults in ``OAuthSettings``

        stability
        :stability: experimental
        """
        return self._values.get('o_auth')

    @builtins.property
    def prevent_user_existence_errors(self) -> typing.Optional[bool]:
        """Whether Cognito returns a UserNotFoundException exception when the user does not exist in the user pool (false), or whether it returns another type of error that doesn't reveal the user's absence.

        default
        :default: true for new stacks

        see
        :see: https://docs.aws.amazon.com/cognito/latest/developerguide/cognito-user-pool-managing-errors.html
        stability
        :stability: experimental
        """
        return self._values.get('prevent_user_existence_errors')

    @builtins.property
    def user_pool_client_name(self) -> typing.Optional[str]:
        """Name of the application client.

        default
        :default: - cloudformation generated name

        stability
        :stability: experimental
        """
        return self._values.get('user_pool_client_name')

    @builtins.property
    def user_pool(self) -> "IUserPool":
        """The UserPool resource this client will have access to.

        stability
        :stability: experimental
        """
        return self._values.get('user_pool')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'UserPoolClientProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.implements(IUserPoolDomain)
class UserPoolDomain(aws_cdk.core.Resource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-cognito.UserPoolDomain"):
    """Define a user pool domain.

    stability
    :stability: experimental
    """
    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, user_pool: "IUserPool", cognito_domain: typing.Optional["CognitoDomainOptions"]=None, custom_domain: typing.Optional["CustomDomainOptions"]=None) -> None:
        """
        :param scope: -
        :param id: -
        :param user_pool: The user pool to which this domain should be associated.
        :param cognito_domain: Associate a cognito prefix domain with your user pool Either ``customDomain`` or ``cognitoDomain`` must be specified. Default: - not set if ``customDomain`` is specified, otherwise, throws an error.
        :param custom_domain: Associate a custom domain with your user pool Either ``customDomain`` or ``cognitoDomain`` must be specified. Default: - not set if ``cognitoDomain`` is specified, otherwise, throws an error.

        stability
        :stability: experimental
        """
        props = UserPoolDomainProps(user_pool=user_pool, cognito_domain=cognito_domain, custom_domain=custom_domain)

        jsii.create(UserPoolDomain, self, [scope, id, props])

    @builtins.property
    @jsii.member(jsii_name="cloudFrontDomainName")
    def cloud_front_domain_name(self) -> str:
        """The domain name of the CloudFront distribution associated with the user pool domain.

        stability
        :stability: experimental
        """
        return jsii.get(self, "cloudFrontDomainName")

    @builtins.property
    @jsii.member(jsii_name="domainName")
    def domain_name(self) -> str:
        """The domain that was specified to be created.

        If ``customDomain`` was selected, this holds the full domain name that was specified.
        If the ``cognitoDomain`` was used, it contains the prefix to the Cognito hosted domain.

        stability
        :stability: experimental
        """
        return jsii.get(self, "domainName")


@jsii.data_type(jsii_type="@aws-cdk/aws-cognito.UserPoolDomainOptions", jsii_struct_bases=[], name_mapping={'cognito_domain': 'cognitoDomain', 'custom_domain': 'customDomain'})
class UserPoolDomainOptions():
    def __init__(self, *, cognito_domain: typing.Optional["CognitoDomainOptions"]=None, custom_domain: typing.Optional["CustomDomainOptions"]=None) -> None:
        """Options to create a UserPoolDomain.

        :param cognito_domain: Associate a cognito prefix domain with your user pool Either ``customDomain`` or ``cognitoDomain`` must be specified. Default: - not set if ``customDomain`` is specified, otherwise, throws an error.
        :param custom_domain: Associate a custom domain with your user pool Either ``customDomain`` or ``cognitoDomain`` must be specified. Default: - not set if ``cognitoDomain`` is specified, otherwise, throws an error.

        stability
        :stability: experimental
        """
        if isinstance(cognito_domain, dict): cognito_domain = CognitoDomainOptions(**cognito_domain)
        if isinstance(custom_domain, dict): custom_domain = CustomDomainOptions(**custom_domain)
        self._values = {
        }
        if cognito_domain is not None: self._values["cognito_domain"] = cognito_domain
        if custom_domain is not None: self._values["custom_domain"] = custom_domain

    @builtins.property
    def cognito_domain(self) -> typing.Optional["CognitoDomainOptions"]:
        """Associate a cognito prefix domain with your user pool Either ``customDomain`` or ``cognitoDomain`` must be specified.

        default
        :default: - not set if ``customDomain`` is specified, otherwise, throws an error.

        see
        :see: https://docs.aws.amazon.com/cognito/latest/developerguide/cognito-user-pools-assign-domain-prefix.html
        stability
        :stability: experimental
        """
        return self._values.get('cognito_domain')

    @builtins.property
    def custom_domain(self) -> typing.Optional["CustomDomainOptions"]:
        """Associate a custom domain with your user pool Either ``customDomain`` or ``cognitoDomain`` must be specified.

        default
        :default: - not set if ``cognitoDomain`` is specified, otherwise, throws an error.

        see
        :see: https://docs.aws.amazon.com/cognito/latest/developerguide/cognito-user-pools-add-custom-domain.html
        stability
        :stability: experimental
        """
        return self._values.get('custom_domain')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'UserPoolDomainOptions(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="@aws-cdk/aws-cognito.UserPoolDomainProps", jsii_struct_bases=[UserPoolDomainOptions], name_mapping={'cognito_domain': 'cognitoDomain', 'custom_domain': 'customDomain', 'user_pool': 'userPool'})
class UserPoolDomainProps(UserPoolDomainOptions):
    def __init__(self, *, cognito_domain: typing.Optional["CognitoDomainOptions"]=None, custom_domain: typing.Optional["CustomDomainOptions"]=None, user_pool: "IUserPool") -> None:
        """Props for UserPoolDomain construct.

        :param cognito_domain: Associate a cognito prefix domain with your user pool Either ``customDomain`` or ``cognitoDomain`` must be specified. Default: - not set if ``customDomain`` is specified, otherwise, throws an error.
        :param custom_domain: Associate a custom domain with your user pool Either ``customDomain`` or ``cognitoDomain`` must be specified. Default: - not set if ``cognitoDomain`` is specified, otherwise, throws an error.
        :param user_pool: The user pool to which this domain should be associated.

        stability
        :stability: experimental
        """
        if isinstance(cognito_domain, dict): cognito_domain = CognitoDomainOptions(**cognito_domain)
        if isinstance(custom_domain, dict): custom_domain = CustomDomainOptions(**custom_domain)
        self._values = {
            'user_pool': user_pool,
        }
        if cognito_domain is not None: self._values["cognito_domain"] = cognito_domain
        if custom_domain is not None: self._values["custom_domain"] = custom_domain

    @builtins.property
    def cognito_domain(self) -> typing.Optional["CognitoDomainOptions"]:
        """Associate a cognito prefix domain with your user pool Either ``customDomain`` or ``cognitoDomain`` must be specified.

        default
        :default: - not set if ``customDomain`` is specified, otherwise, throws an error.

        see
        :see: https://docs.aws.amazon.com/cognito/latest/developerguide/cognito-user-pools-assign-domain-prefix.html
        stability
        :stability: experimental
        """
        return self._values.get('cognito_domain')

    @builtins.property
    def custom_domain(self) -> typing.Optional["CustomDomainOptions"]:
        """Associate a custom domain with your user pool Either ``customDomain`` or ``cognitoDomain`` must be specified.

        default
        :default: - not set if ``cognitoDomain`` is specified, otherwise, throws an error.

        see
        :see: https://docs.aws.amazon.com/cognito/latest/developerguide/cognito-user-pools-add-custom-domain.html
        stability
        :stability: experimental
        """
        return self._values.get('custom_domain')

    @builtins.property
    def user_pool(self) -> "IUserPool":
        """The user pool to which this domain should be associated.

        stability
        :stability: experimental
        """
        return self._values.get('user_pool')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'UserPoolDomainProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


class UserPoolOperation(metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-cognito.UserPoolOperation"):
    """User pool operations to which lambda triggers can be attached.

    stability
    :stability: experimental
    """
    @jsii.member(jsii_name="of")
    @builtins.classmethod
    def of(cls, name: str) -> "UserPoolOperation":
        """A custom user pool operation.

        :param name: -

        stability
        :stability: experimental
        """
        return jsii.sinvoke(cls, "of", [name])

    @jsii.python.classproperty
    @jsii.member(jsii_name="CREATE_AUTH_CHALLENGE")
    def CREATE_AUTH_CHALLENGE(cls) -> "UserPoolOperation":
        """Creates a challenge in a custom auth flow.

        see
        :see: https://docs.aws.amazon.com/cognito/latest/developerguide/user-pool-lambda-create-auth-challenge.html
        stability
        :stability: experimental
        """
        return jsii.sget(cls, "CREATE_AUTH_CHALLENGE")

    @jsii.python.classproperty
    @jsii.member(jsii_name="CUSTOM_MESSAGE")
    def CUSTOM_MESSAGE(cls) -> "UserPoolOperation":
        """Advanced customization and localization of messages.

        see
        :see: https://docs.aws.amazon.com/cognito/latest/developerguide/user-pool-lambda-custom-message.html
        stability
        :stability: experimental
        """
        return jsii.sget(cls, "CUSTOM_MESSAGE")

    @jsii.python.classproperty
    @jsii.member(jsii_name="DEFINE_AUTH_CHALLENGE")
    def DEFINE_AUTH_CHALLENGE(cls) -> "UserPoolOperation":
        """Determines the next challenge in a custom auth flow.

        see
        :see: https://docs.aws.amazon.com/cognito/latest/developerguide/user-pool-lambda-define-auth-challenge.html
        stability
        :stability: experimental
        """
        return jsii.sget(cls, "DEFINE_AUTH_CHALLENGE")

    @jsii.python.classproperty
    @jsii.member(jsii_name="POST_AUTHENTICATION")
    def POST_AUTHENTICATION(cls) -> "UserPoolOperation":
        """Event logging for custom analytics.

        see
        :see: https://docs.aws.amazon.com/cognito/latest/developerguide/user-pool-lambda-post-authentication.html
        stability
        :stability: experimental
        """
        return jsii.sget(cls, "POST_AUTHENTICATION")

    @jsii.python.classproperty
    @jsii.member(jsii_name="POST_CONFIRMATION")
    def POST_CONFIRMATION(cls) -> "UserPoolOperation":
        """Custom welcome messages or event logging for custom analytics.

        see
        :see: https://docs.aws.amazon.com/cognito/latest/developerguide/user-pool-lambda-post-confirmation.html
        stability
        :stability: experimental
        """
        return jsii.sget(cls, "POST_CONFIRMATION")

    @jsii.python.classproperty
    @jsii.member(jsii_name="PRE_AUTHENTICATION")
    def PRE_AUTHENTICATION(cls) -> "UserPoolOperation":
        """Custom validation to accept or deny the sign-in request.

        see
        :see: https://docs.aws.amazon.com/cognito/latest/developerguide/user-pool-lambda-pre-authentication.html
        stability
        :stability: experimental
        """
        return jsii.sget(cls, "PRE_AUTHENTICATION")

    @jsii.python.classproperty
    @jsii.member(jsii_name="PRE_SIGN_UP")
    def PRE_SIGN_UP(cls) -> "UserPoolOperation":
        """Custom validation to accept or deny the sign-up request.

        see
        :see: https://docs.aws.amazon.com/cognito/latest/developerguide/user-pool-lambda-pre-sign-up.html
        stability
        :stability: experimental
        """
        return jsii.sget(cls, "PRE_SIGN_UP")

    @jsii.python.classproperty
    @jsii.member(jsii_name="PRE_TOKEN_GENERATION")
    def PRE_TOKEN_GENERATION(cls) -> "UserPoolOperation":
        """Add or remove attributes in Id tokens.

        see
        :see: https://docs.aws.amazon.com/cognito/latest/developerguide/user-pool-lambda-pre-token-generation.html
        stability
        :stability: experimental
        """
        return jsii.sget(cls, "PRE_TOKEN_GENERATION")

    @jsii.python.classproperty
    @jsii.member(jsii_name="USER_MIGRATION")
    def USER_MIGRATION(cls) -> "UserPoolOperation":
        """Migrate a user from an existing user directory to user pools.

        see
        :see: https://docs.aws.amazon.com/cognito/latest/developerguide/user-pool-lambda-migrate-user.html
        stability
        :stability: experimental
        """
        return jsii.sget(cls, "USER_MIGRATION")

    @jsii.python.classproperty
    @jsii.member(jsii_name="VERIFY_AUTH_CHALLENGE_RESPONSE")
    def VERIFY_AUTH_CHALLENGE_RESPONSE(cls) -> "UserPoolOperation":
        """Determines if a response is correct in a custom auth flow.

        see
        :see: https://docs.aws.amazon.com/cognito/latest/developerguide/user-pool-lambda-verify-auth-challenge-response.html
        stability
        :stability: experimental
        """
        return jsii.sget(cls, "VERIFY_AUTH_CHALLENGE_RESPONSE")

    @builtins.property
    @jsii.member(jsii_name="operationName")
    def operation_name(self) -> str:
        """The key to use in ``CfnUserPool.LambdaConfigProperty``.

        stability
        :stability: experimental
        """
        return jsii.get(self, "operationName")


@jsii.data_type(jsii_type="@aws-cdk/aws-cognito.UserPoolProps", jsii_struct_bases=[], name_mapping={'auto_verify': 'autoVerify', 'custom_attributes': 'customAttributes', 'email_settings': 'emailSettings', 'lambda_triggers': 'lambdaTriggers', 'mfa': 'mfa', 'mfa_second_factor': 'mfaSecondFactor', 'password_policy': 'passwordPolicy', 'required_attributes': 'requiredAttributes', 'self_sign_up_enabled': 'selfSignUpEnabled', 'sign_in_aliases': 'signInAliases', 'sign_in_case_sensitive': 'signInCaseSensitive', 'sms_role': 'smsRole', 'sms_role_external_id': 'smsRoleExternalId', 'user_invitation': 'userInvitation', 'user_pool_name': 'userPoolName', 'user_verification': 'userVerification'})
class UserPoolProps():
    def __init__(self, *, auto_verify: typing.Optional["AutoVerifiedAttrs"]=None, custom_attributes: typing.Optional[typing.Mapping[str, "ICustomAttribute"]]=None, email_settings: typing.Optional["EmailSettings"]=None, lambda_triggers: typing.Optional["UserPoolTriggers"]=None, mfa: typing.Optional["Mfa"]=None, mfa_second_factor: typing.Optional["MfaSecondFactor"]=None, password_policy: typing.Optional["PasswordPolicy"]=None, required_attributes: typing.Optional["RequiredAttributes"]=None, self_sign_up_enabled: typing.Optional[bool]=None, sign_in_aliases: typing.Optional["SignInAliases"]=None, sign_in_case_sensitive: typing.Optional[bool]=None, sms_role: typing.Optional[aws_cdk.aws_iam.IRole]=None, sms_role_external_id: typing.Optional[str]=None, user_invitation: typing.Optional["UserInvitationConfig"]=None, user_pool_name: typing.Optional[str]=None, user_verification: typing.Optional["UserVerificationConfig"]=None) -> None:
        """Props for the UserPool construct.

        :param auto_verify: Attributes which Cognito will look to verify automatically upon user sign up. EMAIL and PHONE are the only available options. Default: - If ``signInAlias`` includes email and/or phone, they will be included in ``autoVerifiedAttributes`` by default. If absent, no attributes will be auto-verified.
        :param custom_attributes: Define a set of custom attributes that can be configured for each user in the user pool. Default: - No custom attributes.
        :param email_settings: Email settings for a user pool. Default: - see defaults on each property of EmailSettings.
        :param lambda_triggers: Lambda functions to use for supported Cognito triggers. Default: - No Lambda triggers.
        :param mfa: Configure whether users of this user pool can or are required use MFA to sign in. Default: Mfa.OFF
        :param mfa_second_factor: Configure the MFA types that users can use in this user pool. Ignored if ``mfa`` is set to ``OFF``. Default: - { sms: true, oneTimePassword: false }, if ``mfa`` is set to ``OPTIONAL`` or ``REQUIRED``. { sms: false, oneTimePassword: false }, otherwise
        :param password_policy: Password policy for this user pool. Default: - see defaults on each property of PasswordPolicy.
        :param required_attributes: The set of attributes that are required for every user in the user pool. Read more on attributes here - https://docs.aws.amazon.com/cognito/latest/developerguide/user-pool-settings-attributes.html Default: - No attributes are required.
        :param self_sign_up_enabled: Whether self sign up should be enabled. This can be further configured via the ``selfSignUp`` property. Default: false
        :param sign_in_aliases: Methods in which a user registers or signs in to a user pool. Allows either username with aliases OR sign in with email, phone, or both. Read the sections on usernames and aliases to learn more - https://docs.aws.amazon.com/cognito/latest/developerguide/user-pool-settings-attributes.html To match with 'Option 1' in the above link, with a verified email, this property should be set to ``{ username: true, email: true }``. To match with 'Option 2' in the above link with both a verified email and phone number, this property should be set to ``{ email: true, phone: true }``. Default: { username: true }
        :param sign_in_case_sensitive: Whether sign-in aliases should be evaluated with case sensitivity. For example, when this option is set to false, users will be able to sign in using either ``MyUsername`` or ``myusername``. Default: true
        :param sms_role: The IAM role that Cognito will assume while sending SMS messages. Default: - a new IAM role is created
        :param sms_role_external_id: The 'ExternalId' that Cognito service must using when assuming the ``smsRole``, if the role is restricted with an 'sts:ExternalId' conditional. Learn more about ExternalId here - https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_create_for-user_externalid.html This property will be ignored if ``smsRole`` is not specified. Default: - No external id will be configured
        :param user_invitation: Configuration around admins signing up users into a user pool. Default: - see defaults in UserInvitationConfig
        :param user_pool_name: Name of the user pool. Default: - automatically generated name by CloudFormation at deploy time
        :param user_verification: Configuration around users signing themselves up to the user pool. Enable or disable self sign-up via the ``selfSignUpEnabled`` property. Default: - see defaults in UserVerificationConfig

        stability
        :stability: experimental
        """
        if isinstance(auto_verify, dict): auto_verify = AutoVerifiedAttrs(**auto_verify)
        if isinstance(email_settings, dict): email_settings = EmailSettings(**email_settings)
        if isinstance(lambda_triggers, dict): lambda_triggers = UserPoolTriggers(**lambda_triggers)
        if isinstance(mfa_second_factor, dict): mfa_second_factor = MfaSecondFactor(**mfa_second_factor)
        if isinstance(password_policy, dict): password_policy = PasswordPolicy(**password_policy)
        if isinstance(required_attributes, dict): required_attributes = RequiredAttributes(**required_attributes)
        if isinstance(sign_in_aliases, dict): sign_in_aliases = SignInAliases(**sign_in_aliases)
        if isinstance(user_invitation, dict): user_invitation = UserInvitationConfig(**user_invitation)
        if isinstance(user_verification, dict): user_verification = UserVerificationConfig(**user_verification)
        self._values = {
        }
        if auto_verify is not None: self._values["auto_verify"] = auto_verify
        if custom_attributes is not None: self._values["custom_attributes"] = custom_attributes
        if email_settings is not None: self._values["email_settings"] = email_settings
        if lambda_triggers is not None: self._values["lambda_triggers"] = lambda_triggers
        if mfa is not None: self._values["mfa"] = mfa
        if mfa_second_factor is not None: self._values["mfa_second_factor"] = mfa_second_factor
        if password_policy is not None: self._values["password_policy"] = password_policy
        if required_attributes is not None: self._values["required_attributes"] = required_attributes
        if self_sign_up_enabled is not None: self._values["self_sign_up_enabled"] = self_sign_up_enabled
        if sign_in_aliases is not None: self._values["sign_in_aliases"] = sign_in_aliases
        if sign_in_case_sensitive is not None: self._values["sign_in_case_sensitive"] = sign_in_case_sensitive
        if sms_role is not None: self._values["sms_role"] = sms_role
        if sms_role_external_id is not None: self._values["sms_role_external_id"] = sms_role_external_id
        if user_invitation is not None: self._values["user_invitation"] = user_invitation
        if user_pool_name is not None: self._values["user_pool_name"] = user_pool_name
        if user_verification is not None: self._values["user_verification"] = user_verification

    @builtins.property
    def auto_verify(self) -> typing.Optional["AutoVerifiedAttrs"]:
        """Attributes which Cognito will look to verify automatically upon user sign up.

        EMAIL and PHONE are the only available options.

        default
        :default:

        - If ``signInAlias`` includes email and/or phone, they will be included in ``autoVerifiedAttributes`` by default.
          If absent, no attributes will be auto-verified.

        stability
        :stability: experimental
        """
        return self._values.get('auto_verify')

    @builtins.property
    def custom_attributes(self) -> typing.Optional[typing.Mapping[str, "ICustomAttribute"]]:
        """Define a set of custom attributes that can be configured for each user in the user pool.

        default
        :default: - No custom attributes.

        stability
        :stability: experimental
        """
        return self._values.get('custom_attributes')

    @builtins.property
    def email_settings(self) -> typing.Optional["EmailSettings"]:
        """Email settings for a user pool.

        default
        :default: - see defaults on each property of EmailSettings.

        stability
        :stability: experimental
        """
        return self._values.get('email_settings')

    @builtins.property
    def lambda_triggers(self) -> typing.Optional["UserPoolTriggers"]:
        """Lambda functions to use for supported Cognito triggers.

        default
        :default: - No Lambda triggers.

        see
        :see: https://docs.aws.amazon.com/cognito/latest/developerguide/cognito-user-identity-pools-working-with-aws-lambda-triggers.html
        stability
        :stability: experimental
        """
        return self._values.get('lambda_triggers')

    @builtins.property
    def mfa(self) -> typing.Optional["Mfa"]:
        """Configure whether users of this user pool can or are required use MFA to sign in.

        default
        :default: Mfa.OFF

        stability
        :stability: experimental
        """
        return self._values.get('mfa')

    @builtins.property
    def mfa_second_factor(self) -> typing.Optional["MfaSecondFactor"]:
        """Configure the MFA types that users can use in this user pool.

        Ignored if ``mfa`` is set to ``OFF``.

        default
        :default:

        - { sms: true, oneTimePassword: false }, if ``mfa`` is set to ``OPTIONAL`` or ``REQUIRED``.
          { sms: false, oneTimePassword: false }, otherwise

        stability
        :stability: experimental
        """
        return self._values.get('mfa_second_factor')

    @builtins.property
    def password_policy(self) -> typing.Optional["PasswordPolicy"]:
        """Password policy for this user pool.

        default
        :default: - see defaults on each property of PasswordPolicy.

        stability
        :stability: experimental
        """
        return self._values.get('password_policy')

    @builtins.property
    def required_attributes(self) -> typing.Optional["RequiredAttributes"]:
        """The set of attributes that are required for every user in the user pool.

        Read more on attributes here - https://docs.aws.amazon.com/cognito/latest/developerguide/user-pool-settings-attributes.html

        default
        :default: - No attributes are required.

        stability
        :stability: experimental
        """
        return self._values.get('required_attributes')

    @builtins.property
    def self_sign_up_enabled(self) -> typing.Optional[bool]:
        """Whether self sign up should be enabled.

        This can be further configured via the ``selfSignUp`` property.

        default
        :default: false

        stability
        :stability: experimental
        """
        return self._values.get('self_sign_up_enabled')

    @builtins.property
    def sign_in_aliases(self) -> typing.Optional["SignInAliases"]:
        """Methods in which a user registers or signs in to a user pool.

        Allows either username with aliases OR sign in with email, phone, or both.

        Read the sections on usernames and aliases to learn more -
        https://docs.aws.amazon.com/cognito/latest/developerguide/user-pool-settings-attributes.html

        To match with 'Option 1' in the above link, with a verified email, this property should be set to
        ``{ username: true, email: true }``. To match with 'Option 2' in the above link with both a verified email and phone
        number, this property should be set to ``{ email: true, phone: true }``.

        default
        :default: { username: true }

        stability
        :stability: experimental
        """
        return self._values.get('sign_in_aliases')

    @builtins.property
    def sign_in_case_sensitive(self) -> typing.Optional[bool]:
        """Whether sign-in aliases should be evaluated with case sensitivity.

        For example, when this option is set to false, users will be able to sign in using either ``MyUsername`` or ``myusername``.

        default
        :default: true

        stability
        :stability: experimental
        """
        return self._values.get('sign_in_case_sensitive')

    @builtins.property
    def sms_role(self) -> typing.Optional[aws_cdk.aws_iam.IRole]:
        """The IAM role that Cognito will assume while sending SMS messages.

        default
        :default: - a new IAM role is created

        stability
        :stability: experimental
        """
        return self._values.get('sms_role')

    @builtins.property
    def sms_role_external_id(self) -> typing.Optional[str]:
        """The 'ExternalId' that Cognito service must using when assuming the ``smsRole``, if the role is restricted with an 'sts:ExternalId' conditional.

        Learn more about ExternalId here - https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_create_for-user_externalid.html

        This property will be ignored if ``smsRole`` is not specified.

        default
        :default: - No external id will be configured

        stability
        :stability: experimental
        """
        return self._values.get('sms_role_external_id')

    @builtins.property
    def user_invitation(self) -> typing.Optional["UserInvitationConfig"]:
        """Configuration around admins signing up users into a user pool.

        default
        :default: - see defaults in UserInvitationConfig

        stability
        :stability: experimental
        """
        return self._values.get('user_invitation')

    @builtins.property
    def user_pool_name(self) -> typing.Optional[str]:
        """Name of the user pool.

        default
        :default: - automatically generated name by CloudFormation at deploy time

        stability
        :stability: experimental
        """
        return self._values.get('user_pool_name')

    @builtins.property
    def user_verification(self) -> typing.Optional["UserVerificationConfig"]:
        """Configuration around users signing themselves up to the user pool.

        Enable or disable self sign-up via the ``selfSignUpEnabled`` property.

        default
        :default: - see defaults in UserVerificationConfig

        stability
        :stability: experimental
        """
        return self._values.get('user_verification')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'UserPoolProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="@aws-cdk/aws-cognito.UserPoolTriggers", jsii_struct_bases=[], name_mapping={'create_auth_challenge': 'createAuthChallenge', 'custom_message': 'customMessage', 'define_auth_challenge': 'defineAuthChallenge', 'post_authentication': 'postAuthentication', 'post_confirmation': 'postConfirmation', 'pre_authentication': 'preAuthentication', 'pre_sign_up': 'preSignUp', 'pre_token_generation': 'preTokenGeneration', 'user_migration': 'userMigration', 'verify_auth_challenge_response': 'verifyAuthChallengeResponse'})
class UserPoolTriggers():
    def __init__(self, *, create_auth_challenge: typing.Optional[aws_cdk.aws_lambda.IFunction]=None, custom_message: typing.Optional[aws_cdk.aws_lambda.IFunction]=None, define_auth_challenge: typing.Optional[aws_cdk.aws_lambda.IFunction]=None, post_authentication: typing.Optional[aws_cdk.aws_lambda.IFunction]=None, post_confirmation: typing.Optional[aws_cdk.aws_lambda.IFunction]=None, pre_authentication: typing.Optional[aws_cdk.aws_lambda.IFunction]=None, pre_sign_up: typing.Optional[aws_cdk.aws_lambda.IFunction]=None, pre_token_generation: typing.Optional[aws_cdk.aws_lambda.IFunction]=None, user_migration: typing.Optional[aws_cdk.aws_lambda.IFunction]=None, verify_auth_challenge_response: typing.Optional[aws_cdk.aws_lambda.IFunction]=None) -> None:
        """Triggers for a user pool.

        :param create_auth_challenge: Creates an authentication challenge. Default: - no trigger configured
        :param custom_message: A custom Message AWS Lambda trigger. Default: - no trigger configured
        :param define_auth_challenge: Defines the authentication challenge. Default: - no trigger configured
        :param post_authentication: A post-authentication AWS Lambda trigger. Default: - no trigger configured
        :param post_confirmation: A post-confirmation AWS Lambda trigger. Default: - no trigger configured
        :param pre_authentication: A pre-authentication AWS Lambda trigger. Default: - no trigger configured
        :param pre_sign_up: A pre-registration AWS Lambda trigger. Default: - no trigger configured
        :param pre_token_generation: A pre-token-generation AWS Lambda trigger. Default: - no trigger configured
        :param user_migration: A user-migration AWS Lambda trigger. Default: - no trigger configured
        :param verify_auth_challenge_response: Verifies the authentication challenge response. Default: - no trigger configured

        see
        :see: https://docs.aws.amazon.com/cognito/latest/developerguide/cognito-user-identity-pools-working-with-aws-lambda-triggers.html
        stability
        :stability: experimental
        """
        self._values = {
        }
        if create_auth_challenge is not None: self._values["create_auth_challenge"] = create_auth_challenge
        if custom_message is not None: self._values["custom_message"] = custom_message
        if define_auth_challenge is not None: self._values["define_auth_challenge"] = define_auth_challenge
        if post_authentication is not None: self._values["post_authentication"] = post_authentication
        if post_confirmation is not None: self._values["post_confirmation"] = post_confirmation
        if pre_authentication is not None: self._values["pre_authentication"] = pre_authentication
        if pre_sign_up is not None: self._values["pre_sign_up"] = pre_sign_up
        if pre_token_generation is not None: self._values["pre_token_generation"] = pre_token_generation
        if user_migration is not None: self._values["user_migration"] = user_migration
        if verify_auth_challenge_response is not None: self._values["verify_auth_challenge_response"] = verify_auth_challenge_response

    @builtins.property
    def create_auth_challenge(self) -> typing.Optional[aws_cdk.aws_lambda.IFunction]:
        """Creates an authentication challenge.

        default
        :default: - no trigger configured

        see
        :see: https://docs.aws.amazon.com/cognito/latest/developerguide/user-pool-lambda-create-auth-challenge.html
        stability
        :stability: experimental
        """
        return self._values.get('create_auth_challenge')

    @builtins.property
    def custom_message(self) -> typing.Optional[aws_cdk.aws_lambda.IFunction]:
        """A custom Message AWS Lambda trigger.

        default
        :default: - no trigger configured

        see
        :see: https://docs.aws.amazon.com/cognito/latest/developerguide/user-pool-lambda-custom-message.html
        stability
        :stability: experimental
        """
        return self._values.get('custom_message')

    @builtins.property
    def define_auth_challenge(self) -> typing.Optional[aws_cdk.aws_lambda.IFunction]:
        """Defines the authentication challenge.

        default
        :default: - no trigger configured

        see
        :see: https://docs.aws.amazon.com/cognito/latest/developerguide/user-pool-lambda-define-auth-challenge.html
        stability
        :stability: experimental
        """
        return self._values.get('define_auth_challenge')

    @builtins.property
    def post_authentication(self) -> typing.Optional[aws_cdk.aws_lambda.IFunction]:
        """A post-authentication AWS Lambda trigger.

        default
        :default: - no trigger configured

        see
        :see: https://docs.aws.amazon.com/cognito/latest/developerguide/user-pool-lambda-post-authentication.html
        stability
        :stability: experimental
        """
        return self._values.get('post_authentication')

    @builtins.property
    def post_confirmation(self) -> typing.Optional[aws_cdk.aws_lambda.IFunction]:
        """A post-confirmation AWS Lambda trigger.

        default
        :default: - no trigger configured

        see
        :see: https://docs.aws.amazon.com/cognito/latest/developerguide/user-pool-lambda-post-confirmation.html
        stability
        :stability: experimental
        """
        return self._values.get('post_confirmation')

    @builtins.property
    def pre_authentication(self) -> typing.Optional[aws_cdk.aws_lambda.IFunction]:
        """A pre-authentication AWS Lambda trigger.

        default
        :default: - no trigger configured

        see
        :see: https://docs.aws.amazon.com/cognito/latest/developerguide/user-pool-lambda-pre-authentication.html
        stability
        :stability: experimental
        """
        return self._values.get('pre_authentication')

    @builtins.property
    def pre_sign_up(self) -> typing.Optional[aws_cdk.aws_lambda.IFunction]:
        """A pre-registration AWS Lambda trigger.

        default
        :default: - no trigger configured

        see
        :see: https://docs.aws.amazon.com/cognito/latest/developerguide/user-pool-lambda-pre-sign-up.html
        stability
        :stability: experimental
        """
        return self._values.get('pre_sign_up')

    @builtins.property
    def pre_token_generation(self) -> typing.Optional[aws_cdk.aws_lambda.IFunction]:
        """A pre-token-generation AWS Lambda trigger.

        default
        :default: - no trigger configured

        see
        :see: https://docs.aws.amazon.com/cognito/latest/developerguide/user-pool-lambda-pre-token-generation.html
        stability
        :stability: experimental
        """
        return self._values.get('pre_token_generation')

    @builtins.property
    def user_migration(self) -> typing.Optional[aws_cdk.aws_lambda.IFunction]:
        """A user-migration AWS Lambda trigger.

        default
        :default: - no trigger configured

        see
        :see: https://docs.aws.amazon.com/cognito/latest/developerguide/user-pool-lambda-migrate-user.html
        stability
        :stability: experimental
        """
        return self._values.get('user_migration')

    @builtins.property
    def verify_auth_challenge_response(self) -> typing.Optional[aws_cdk.aws_lambda.IFunction]:
        """Verifies the authentication challenge response.

        default
        :default: - no trigger configured

        see
        :see: https://docs.aws.amazon.com/cognito/latest/developerguide/user-pool-lambda-verify-auth-challenge-response.html
        stability
        :stability: experimental
        """
        return self._values.get('verify_auth_challenge_response')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'UserPoolTriggers(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="@aws-cdk/aws-cognito.UserVerificationConfig", jsii_struct_bases=[], name_mapping={'email_body': 'emailBody', 'email_style': 'emailStyle', 'email_subject': 'emailSubject', 'sms_message': 'smsMessage'})
class UserVerificationConfig():
    def __init__(self, *, email_body: typing.Optional[str]=None, email_style: typing.Optional["VerificationEmailStyle"]=None, email_subject: typing.Optional[str]=None, sms_message: typing.Optional[str]=None) -> None:
        """User pool configuration for user self sign up.

        :param email_body: The email body template for the verification email sent to the user upon sign up. See https://docs.aws.amazon.com/cognito/latest/developerguide/cognito-user-pool-settings-message-templates.html to learn more about message templates. Default: - 'The verification code to your new account is {####}' if VerificationEmailStyle.CODE is chosen, 'Verify your account by clicking on {##Verify Email##}' if VerificationEmailStyle.LINK is chosen.
        :param email_style: Emails can be verified either using a code or a link. Learn more at https://docs.aws.amazon.com/cognito/latest/developerguide/cognito-user-pool-settings-email-verification-message-customization.html Default: VerificationEmailStyle.CODE
        :param email_subject: The email subject template for the verification email sent to the user upon sign up. See https://docs.aws.amazon.com/cognito/latest/developerguide/cognito-user-pool-settings-message-templates.html to learn more about message templates. Default: 'Verify your new account'
        :param sms_message: The message template for the verification SMS sent to the user upon sign up. See https://docs.aws.amazon.com/cognito/latest/developerguide/cognito-user-pool-settings-message-templates.html to learn more about message templates. Default: - 'The verification code to your new account is {####}' if VerificationEmailStyle.CODE is chosen, not configured if VerificationEmailStyle.LINK is chosen

        stability
        :stability: experimental
        """
        self._values = {
        }
        if email_body is not None: self._values["email_body"] = email_body
        if email_style is not None: self._values["email_style"] = email_style
        if email_subject is not None: self._values["email_subject"] = email_subject
        if sms_message is not None: self._values["sms_message"] = sms_message

    @builtins.property
    def email_body(self) -> typing.Optional[str]:
        """The email body template for the verification email sent to the user upon sign up.

        See https://docs.aws.amazon.com/cognito/latest/developerguide/cognito-user-pool-settings-message-templates.html to
        learn more about message templates.

        default
        :default:

        - 'The verification code to your new account is {####}' if VerificationEmailStyle.CODE is chosen,
          'Verify your account by clicking on {##Verify Email##}' if VerificationEmailStyle.LINK is chosen.

        stability
        :stability: experimental
        """
        return self._values.get('email_body')

    @builtins.property
    def email_style(self) -> typing.Optional["VerificationEmailStyle"]:
        """Emails can be verified either using a code or a link.

        Learn more at https://docs.aws.amazon.com/cognito/latest/developerguide/cognito-user-pool-settings-email-verification-message-customization.html

        default
        :default: VerificationEmailStyle.CODE

        stability
        :stability: experimental
        """
        return self._values.get('email_style')

    @builtins.property
    def email_subject(self) -> typing.Optional[str]:
        """The email subject template for the verification email sent to the user upon sign up.

        See https://docs.aws.amazon.com/cognito/latest/developerguide/cognito-user-pool-settings-message-templates.html to
        learn more about message templates.

        default
        :default: 'Verify your new account'

        stability
        :stability: experimental
        """
        return self._values.get('email_subject')

    @builtins.property
    def sms_message(self) -> typing.Optional[str]:
        """The message template for the verification SMS sent to the user upon sign up.

        See https://docs.aws.amazon.com/cognito/latest/developerguide/cognito-user-pool-settings-message-templates.html to
        learn more about message templates.

        default
        :default:

        - 'The verification code to your new account is {####}' if VerificationEmailStyle.CODE is chosen,
          not configured if VerificationEmailStyle.LINK is chosen

        stability
        :stability: experimental
        """
        return self._values.get('sms_message')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'UserVerificationConfig(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.enum(jsii_type="@aws-cdk/aws-cognito.VerificationEmailStyle")
class VerificationEmailStyle(enum.Enum):
    """The email verification style.

    stability
    :stability: experimental
    """
    CODE = "CODE"
    """Verify email via code.

    stability
    :stability: experimental
    """
    LINK = "LINK"
    """Verify email via link.

    stability
    :stability: experimental
    """

@jsii.implements(ICustomAttribute)
class BooleanAttribute(metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-cognito.BooleanAttribute"):
    """The Boolean custom attribute type.

    stability
    :stability: experimental
    """
    def __init__(self, *, mutable: typing.Optional[bool]=None) -> None:
        """
        :param mutable: Specifies whether the value of the attribute can be changed. For any user pool attribute that's mapped to an identity provider attribute, you must set this parameter to true. Amazon Cognito updates mapped attributes when users sign in to your application through an identity provider. If an attribute is immutable, Amazon Cognito throws an error when it attempts to update the attribute. Default: false

        stability
        :stability: experimental
        """
        props = CustomAttributeProps(mutable=mutable)

        jsii.create(BooleanAttribute, self, [props])

    @jsii.member(jsii_name="bind")
    def bind(self) -> "CustomAttributeConfig":
        """Bind this custom attribute type to the values as expected by CloudFormation.

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "bind", [])


@jsii.implements(ICustomAttribute)
class DateTimeAttribute(metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-cognito.DateTimeAttribute"):
    """The DateTime custom attribute type.

    stability
    :stability: experimental
    """
    def __init__(self, *, mutable: typing.Optional[bool]=None) -> None:
        """
        :param mutable: Specifies whether the value of the attribute can be changed. For any user pool attribute that's mapped to an identity provider attribute, you must set this parameter to true. Amazon Cognito updates mapped attributes when users sign in to your application through an identity provider. If an attribute is immutable, Amazon Cognito throws an error when it attempts to update the attribute. Default: false

        stability
        :stability: experimental
        """
        props = CustomAttributeProps(mutable=mutable)

        jsii.create(DateTimeAttribute, self, [props])

    @jsii.member(jsii_name="bind")
    def bind(self) -> "CustomAttributeConfig":
        """Bind this custom attribute type to the values as expected by CloudFormation.

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "bind", [])


__all__ = [
    "AuthFlow",
    "AutoVerifiedAttrs",
    "BooleanAttribute",
    "CfnIdentityPool",
    "CfnIdentityPoolProps",
    "CfnIdentityPoolRoleAttachment",
    "CfnIdentityPoolRoleAttachmentProps",
    "CfnUserPool",
    "CfnUserPoolClient",
    "CfnUserPoolClientProps",
    "CfnUserPoolDomain",
    "CfnUserPoolDomainProps",
    "CfnUserPoolGroup",
    "CfnUserPoolGroupProps",
    "CfnUserPoolIdentityProvider",
    "CfnUserPoolIdentityProviderProps",
    "CfnUserPoolProps",
    "CfnUserPoolResourceServer",
    "CfnUserPoolResourceServerProps",
    "CfnUserPoolRiskConfigurationAttachment",
    "CfnUserPoolRiskConfigurationAttachmentProps",
    "CfnUserPoolUICustomizationAttachment",
    "CfnUserPoolUICustomizationAttachmentProps",
    "CfnUserPoolUser",
    "CfnUserPoolUserProps",
    "CfnUserPoolUserToGroupAttachment",
    "CfnUserPoolUserToGroupAttachmentProps",
    "CognitoDomainOptions",
    "CustomAttributeConfig",
    "CustomAttributeProps",
    "CustomDomainOptions",
    "DateTimeAttribute",
    "EmailSettings",
    "ICustomAttribute",
    "IUserPool",
    "IUserPoolClient",
    "IUserPoolDomain",
    "Mfa",
    "MfaSecondFactor",
    "NumberAttribute",
    "NumberAttributeConstraints",
    "NumberAttributeProps",
    "OAuthFlows",
    "OAuthScope",
    "OAuthSettings",
    "PasswordPolicy",
    "RequiredAttributes",
    "SignInAliases",
    "StringAttribute",
    "StringAttributeConstraints",
    "StringAttributeProps",
    "UserInvitationConfig",
    "UserPool",
    "UserPoolClient",
    "UserPoolClientOptions",
    "UserPoolClientProps",
    "UserPoolDomain",
    "UserPoolDomainOptions",
    "UserPoolDomainProps",
    "UserPoolOperation",
    "UserPoolProps",
    "UserPoolTriggers",
    "UserVerificationConfig",
    "VerificationEmailStyle",
]

publication.publish()
