**## Authentication**



**`/api/v1/accounts/register/`**

**POST**

Request body

{

&nbsp; "username": "Kwams",

&nbsp; "email": "kwame.nkrumah@ghana.com",

&nbsp; "password": "Blackstar233.",

&nbsp; "password\_confirm": "Blackstar233.",

&nbsp; "first\_name": "Kwame",

&nbsp; "last\_name": "Nkrumah",

&nbsp; "phone\_number": "+2332498051198",

&nbsp; "address\_line\_1": "Black Star Square",

&nbsp; "address\_line\_2": "Opposite Accra Sports Stadium",

&nbsp; "city": "Accra",

&nbsp; "state": "Greater Accra",

&nbsp; "postal\_code": "0233",

&nbsp; "country": "Ghana",

&nbsp; "accept\_terms": true

}



Response body

{

&nbsp; "message": "Account created successfully. Please check your email to verify your account.",

&nbsp; "user": {

&nbsp;   "id": "659e96f9-31c6-4b7a-9db2-73a277a55c6d",

&nbsp;   "username": "kwams",

&nbsp;   "email": "kwame.nkrumah@ghana.com",

&nbsp;   "full\_name": "Kwame Nkrumah"

&nbsp; },

&nbsp; "next\_step": "email\_verification"

}





**`/api/v1/accounts/login/`**

**POST**

Request body

{

&nbsp; "email": "kwame.nkrumah@ghana.com",

&nbsp; "password": "Blackstar233.",

&nbsp; "remember\_me": true

}





Response body

{

&nbsp; "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzU4MTI1NzY2LCJpYXQiOjE3NTgxMTEzNjYsImp0aSI6IjA4YzI5OTUxZmM3ZTRjNmZhODVjYzYxNzhjNzhkNDdjIiwidXNlcl9pZCI6IjY1OWU5NmY5LTMxYzYtNGI3YS05ZGIyLTczYTI3N2E1NWM2ZCJ9.hwjNa3rmQMcaaL3GupYWGnwy1yfD6JQCRAI70lNG2nw",

&nbsp; "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc1ODE5Nzc2NiwiaWF0IjoxNzU4MTExMzY2LCJqdGkiOiJkNGZiYmQwYTIwNDY0Y2I1YWRjYjIyZjBkOWFlNjk2ZCIsInVzZXJfaWQiOiI2NTllOTZmOS0zMWM2LTRiN2EtOWRiMi03M2EyNzdhNTVjNmQifQ.WEcOxbsgTy5h2jKof7TnfSqVJl2sUigXwu4LJDQhOdg",

&nbsp; "user": {

&nbsp;   "id": "659e96f9-31c6-4b7a-9db2-73a277a55c6d",

&nbsp;   "created\_at": "2025-09-17 12:14:02",

&nbsp;   "updated\_at": "2025-09-17 12:14:02",

&nbsp;   "username": "kwams",

&nbsp;   "email": "kwame.nkrumah@ghana.com",

&nbsp;   "first\_name": "Kwame",

&nbsp;   "last\_name": "Nkrumah",

&nbsp;   "phone\_number": "+2332498051198",

&nbsp;   "address\_line\_1": "Black Star Square",

&nbsp;   "address\_line\_2": "Opposite Accra Sports Stadium",

&nbsp;   "city": "Accra",

&nbsp;   "state": "Greater Accra",

&nbsp;   "postal\_code": "0233",

&nbsp;   "country": "Ghana",

&nbsp;   "full\_name": "Kwame Nkrumah",

&nbsp;   "full\_address": "Black Star Square, Opposite Accra Sports Stadium, Accra, Greater Accra, 0233, Ghana",

&nbsp;   "is\_email\_verified": false,

&nbsp;   "bio": "",

&nbsp;   "date\_of\_birth": null,

&nbsp;   "newsletter\_subscription": false

&nbsp; }

}



**/api/v1/accounts/logout/**

**POST**







**/api/v1/accounts/token/refresh/**

**POST**

Request body

{

&nbsp; "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc1ODE5Nzc2NiwiaWF0IjoxNzU4MTExMzY2LCJqdGkiOiJkNGZiYmQwYTIwNDY0Y2I1YWRjYjIyZjBkOWFlNjk2ZCIsInVzZXJfaWQiOiI2NTllOTZmOS0zMWM2LTRiN2EtOWRiMi03M2EyNzdhNTVjNmQifQ.WEcOxbsgTy5h2jKof7TnfSqVJl2sUigXwu4LJDQhOdg"

}



Response body

200

{

&nbsp; "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzU4MTI4Njc1LCJpYXQiOjE3NTgxMTQyNzUsImp0aSI6IjQxNzNhZmI0NTkwYTQ1NTM4NDQwMDQwOGRhZjliOGJlIiwidXNlcl9pZCI6IjY1OWU5NmY5LTMxYzYtNGI3YS05ZGIyLTczYTI3N2E1NWM2ZCJ9.vPStol\_KTa7m6uvuKvAEHSQpO6zI8vVCmtXAY7551Xs",

&nbsp; "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc1ODIwMDY3NSwiaWF0IjoxNzU4MTE0Mjc1LCJqdGkiOiI0ZTQ5OGRlMjVjMzQ0MWYxODAxMTIwZjZjMDAxNzFmNCIsInVzZXJfaWQiOiI2NTllOTZmOS0zMWM2LTRiN2EtOWRiMi03M2EyNzdhNTVjNmQifQ.eBFba3UPwjwPVS2n6is4crLPXaz02Jn\_HYb7Vc9SEeQ"

}





Response body

401: Error: Unauthorized

{

&nbsp; "detail": "Token is blacklisted",

&nbsp; "code": "token\_not\_valid"

}





**## User Profile**

**`/api/v1/accounts/profiles/`**

**GET**

Response body

{

&nbsp; "count": 1,

&nbsp; "total\_pages": 1,

&nbsp; "current\_page": 1,

&nbsp; "page\_size": 20,

&nbsp; "next": null,

&nbsp; "previous": null,

&nbsp; "results": \[

&nbsp;   {

&nbsp;     "id": "659e96f9-31c6-4b7a-9db2-73a277a55c6d",

&nbsp;     "created\_at": "2025-09-17 12:14:02",

&nbsp;     "updated\_at": "2025-09-17 12:28:41",

&nbsp;     "is\_active": true,

&nbsp;     "username": "kwams",

&nbsp;     "email": "kwame.nkrumah@ghana.com",

&nbsp;     "first\_name": "Kwame",

&nbsp;     "last\_name": "Nkrumah",

&nbsp;     "phone\_number": "+2332498051198",

&nbsp;     "address\_line\_1": "Black Star Square",

&nbsp;     "address\_line\_2": "Opposite Accra Sports Stadium",

&nbsp;     "city": "Accra",

&nbsp;     "state": "Greater Accra",

&nbsp;     "postal\_code": "GA233",

&nbsp;     "country": "Ghana",

&nbsp;     "full\_name": "Kwame Nkrumah",

&nbsp;     "full\_address": "Black Star Square, Opposite Accra Sports Stadium, Accra, Greater Accra, GA233, Ghana",

&nbsp;     "is\_email\_verified": false,

&nbsp;     "bio": "Coming soon",

&nbsp;     "date\_of\_birth": "1957-03-06",

&nbsp;     "newsletter\_subscription": true,

&nbsp;     "account\_status": "PENDING",

&nbsp;     "user\_type": "CUSTOMER",

&nbsp;     "date\_joined": "2025-09-17 12:14:00",

&nbsp;     "last\_login": "2025-09-17 12:16:06"

&nbsp;   }

&nbsp; ],

&nbsp; "\_meta": {

&nbsp;   "has\_next": false,

&nbsp;   "has\_previous": false,

&nbsp;   "start\_index": 1,

&nbsp;   "end\_index": 1

&nbsp; }

}





**`/api/v1/accounts/profiles/`**

**POST**

Request body

{

&nbsp; "is\_active": true,

&nbsp; "email": "user@example.com",

&nbsp; "first\_name": "Jerry",

&nbsp; "last\_name": "Rawlings",

&nbsp; "newsletter\_subscription": false

}

Response body

{

&nbsp; "message": "Profile creation is not allowed through this endpoint. Please use the registration endpoint at /api/v1/accounts/register/"

}





**`/api/v1/accounts/profiles/{id}/`**

**GET**

id\* required: 659e96f9-31c6-4b7a-9db2-73a277a55c6d



Response body

{

&nbsp; "id": "659e96f9-31c6-4b7a-9db2-73a277a55c6d",

&nbsp; "created\_at": "2025-09-17 12:14:02",

&nbsp; "updated\_at": "2025-09-17 12:28:41",

&nbsp; "is\_active": true,

&nbsp; "username": "kwams",

&nbsp; "email": "kwame.nkrumah@ghana.com",

&nbsp; "first\_name": "Kwame",

&nbsp; "last\_name": "Nkrumah",

&nbsp; "phone\_number": "+2332498051198",

&nbsp; "address\_line\_1": "Black Star Square",

&nbsp; "address\_line\_2": "Opposite Accra Sports Stadium",

&nbsp; "city": "Accra",

&nbsp; "state": "Greater Accra",

&nbsp; "postal\_code": "GA233",

&nbsp; "country": "Ghana",

&nbsp; "full\_name": "Kwame Nkrumah",

&nbsp; "full\_address": "Black Star Square, Opposite Accra Sports Stadium, Accra, Greater Accra, GA233, Ghana",

&nbsp; "is\_email\_verified": false,

&nbsp; "bio": "Coming soon",

&nbsp; "date\_of\_birth": "1957-03-06",

&nbsp; "newsletter\_subscription": true,

&nbsp; "account\_status": "PENDING",

&nbsp; "user\_type": "CUSTOMER",

&nbsp; "date\_joined": "2025-09-17 12:14:00",

&nbsp; "last\_login": "2025-09-17 12:16:06"

}





**/api/v1/accounts/profiles/{id}/**

**PUT | PATCH**

id\* required: 659e96f9-31c6-4b7a-9db2-73a277a55c6d

Resquest body

{

&nbsp; "created\_by": "3fa85f64-5717-4562-b3fc-2c963f66afa6",

&nbsp; "updated\_by": "3fa85f64-5717-4562-b3fc-2c963f66afa6",

&nbsp; "is\_active": true,

&nbsp; "email": "user@example.com",

&nbsp; "first\_name": "string",

&nbsp; "last\_name": "string",

&nbsp; "phone\_number": "string",

&nbsp; "address\_line\_1": "string",

&nbsp; "address\_line\_2": "string",

&nbsp; "city": "string",

&nbsp; "state": "string",

&nbsp; "postal\_code": "string",

&nbsp; "country": "string",

&nbsp; "bio": "string",

&nbsp; "date\_of\_birth": "2025-09-17",

&nbsp; "newsletter\_subscription": true

}



Response body

{

&nbsp; "id": "659e96f9-31c6-4b7a-9db2-73a277a55c6d",

&nbsp; "created\_at": "2025-09-17 12:14:02",

&nbsp; "updated\_at": "2025-09-17 12:46:50",

&nbsp; "is\_active": true,

&nbsp; "username": "kwams",

&nbsp; "email": "user@example.com",

&nbsp; "first\_name": "string",

&nbsp; "last\_name": "string",

&nbsp; "phone\_number": "string",

&nbsp; "address\_line\_1": "string",

&nbsp; "address\_line\_2": "string",

&nbsp; "city": "string",

&nbsp; "state": "string",

&nbsp; "postal\_code": "string",

&nbsp; "country": "string",

&nbsp; "full\_name": "string string",

&nbsp; "full\_address": "string, string, string, string, string, string",

&nbsp; "is\_email\_verified": false,

&nbsp; "bio": "string",

&nbsp; "date\_of\_birth": "2025-09-17",

&nbsp; "newsletter\_subscription": true,

&nbsp; "account\_status": "PENDING",

&nbsp; "user\_type": "CUSTOMER",

&nbsp; "date\_joined": "2025-09-17 12:14:00",

&nbsp; "last\_login": "2025-09-17 12:16:06"

}





**`/api/v1/accounts/users/{id}/`**

**DEL**

id\* required: 659e96f9-31c6-4b7a-9db2-73a277a55c6d



Response

* 204	Profile deleted successfully
* 401	Authentication credentials were not provided
* 403	You do not have permission to delete this profile
* 404	Profile not found







**`/api/v1/accounts/profiles/{id}/activate-user/`**

**POST**

id\* required: 659e96f9-31c6-4b7a-9db2-73a277a55c6d

Request body

{

&nbsp; "is\_active": true,

&nbsp; "email": "kwame.nkrumah@ghana.com",

&nbsp; "first\_name": "Kwame",

&nbsp; "last\_name": "Nkrumah",

&nbsp; "phone\_number": "+2332498051198",

&nbsp; "address\_line\_1": "Black Star Square",

&nbsp; "address\_line\_2": "Opposite Accra Sports Stadium",

&nbsp; "city": "Accra",

&nbsp; "state": "Greater Accra",

&nbsp; "postal\_code": "GA233",

&nbsp; "country": "Ghana",

&nbsp; "bio": "Coming soon",

&nbsp; "date\_of\_birth": "1957-03-06",

&nbsp; "newsletter\_subscription": true

}



Response body





403: Error: Forbidden

{

&nbsp; "detail": "You do not have permission to perform this action."

}





**`/api/v1/accounts/profiles/{id}/restore/`**

**POST**

id\* required: 659e96f9-31c6-4b7a-9db2-73a277a55c6d

Request body

{

&nbsp; "email": "kwame.nkrumah@ghana.com",

&nbsp; "first\_name": "Kwame",

&nbsp; "last\_name": "Nkrumah",

&nbsp; "phone\_number": "+2332498051198",

&nbsp; "address\_line\_1": "Black Star Square",

&nbsp; "address\_line\_2": "Opposite Accra Sports Stadium",

&nbsp; "city": "Accra",

&nbsp; "state": "Greater Accra",

&nbsp; "postal\_code": "GA233",

&nbsp; "country": "Ghana",

&nbsp; "bio": "Coming soon",

&nbsp; "date\_of\_birth": "1957-03-06",

&nbsp; "newsletter\_subscription": true

}



Response body

400: Error: Bad Request

{

&nbsp; "error": "Restore operation not supported"

}





**/api/v1/accounts/profiles/{id}/suspend-user/**

**POST**

Request body



Response body

403: Error: Forbidden

Request response

{

&nbsp; "detail": "You do not have permission to perform this action."

}





`/api/v1/accounts/password/change/`

POST

Request body

{

&nbsp; "old\_password": "Independence57.",

&nbsp; "new\_password": "Blackstar233.",

&nbsp; "new\_password\_confirm": "Blackstar233."

}



Response body

200

{

&nbsp; "message": "Password changed successfully.",

&nbsp; "next\_steps": \[

&nbsp;   "You have been logged out of all other devices.",

&nbsp;   "Please log in again with your new password."

&nbsp; ]

}



400: Error: Bad request

{

&nbsp; "message": "Password change failed. Please check the errors below.",

&nbsp; "errors": {

&nbsp;   "old\_password": \[

&nbsp;     "Current password is incorrect."

&nbsp;   ]

&nbsp; }

}





**/api/v1/accounts/profiles/me/**

**GET**

Response body

{

&nbsp; "id": "659e96f9-31c6-4b7a-9db2-73a277a55c6d",

&nbsp; "created\_at": "2025-09-17 12:14:02",

&nbsp; "updated\_at": "2025-09-17 12:14:02",

&nbsp; "is\_active": true,

&nbsp; "username": "kwams",

&nbsp; "email": "kwame.nkrumah@ghana.com",

&nbsp; "first\_name": "Kwame",

&nbsp; "last\_name": "Nkrumah",

&nbsp; "phone\_number": "+2332498051198",

&nbsp; "address\_line\_1": "Black Star Square",

&nbsp; "address\_line\_2": "Opposite Accra Sports Stadium",

&nbsp; "city": "Accra",

&nbsp; "state": "Greater Accra",

&nbsp; "postal\_code": "0233",

&nbsp; "country": "Ghana",

&nbsp; "full\_name": "Kwame Nkrumah",

&nbsp; "full\_address": "Black Star Square, Opposite Accra Sports Stadium, Accra, Greater Accra, 0233, Ghana",

&nbsp; "is\_email\_verified": false,

&nbsp; "bio": "",

&nbsp; "date\_of\_birth": null,

&nbsp; "newsletter\_subscription": false,

&nbsp; "account\_status": "PENDING",

&nbsp; "user\_type": "CUSTOMER",

&nbsp; "date\_joined": "2025-09-17 12:14:00",

&nbsp; "last\_login": "2025-09-17 12:16:06"

}





**`/api/v1/accounts/profiles/me/`**

**PUT | PATCH**

Request body

{

&nbsp; "is\_active": true,

&nbsp; "email": "kwame.nkrumah@ghana.com",

&nbsp; "first\_name": "Kwame",

&nbsp; "last\_name": "Nkrumah",

&nbsp; "phone\_number": "+2332498051198",

&nbsp; "address\_line\_1": "Black Star Square",

&nbsp; "address\_line\_2": "Opposite Accra Sports Stadium",

&nbsp; "city": "Accra",

&nbsp; "state": "Greater Accra",

&nbsp; "postal\_code": "GA233",

&nbsp; "country": "Ghana",

&nbsp; "bio": "Coming soon",

&nbsp; "date\_of\_birth": "1957-03-06",

&nbsp; "newsletter\_subscription": true

}



Response body

{

&nbsp; "message": "Profile updated successfully",

&nbsp; "user": {

&nbsp;   "id": "659e96f9-31c6-4b7a-9db2-73a277a55c6d",

&nbsp;   "created\_at": "2025-09-17 12:14:02",

&nbsp;   "updated\_at": "2025-09-17 12:22:27",

&nbsp;   "is\_active": true,

&nbsp;   "username": "kwams",

&nbsp;   "email": "kwame.nkrumah@ghana.com",

&nbsp;   "first\_name": "Kwame",

&nbsp;   "last\_name": "Nkrumah",

&nbsp;   "phone\_number": "+2332498051198",

&nbsp;   "address\_line\_1": "Black Star Square",

&nbsp;   "address\_line\_2": "Opposite Accra Sports Stadium",

&nbsp;   "city": "Accra",

&nbsp;   "state": "Greater Accra",

&nbsp;   "postal\_code": "GA233",

&nbsp;   "country": "Ghana",

&nbsp;   "full\_name": "Kwame Nkrumah",

&nbsp;   "full\_address": "Black Star Square, Opposite Accra Sports Stadium, Accra, Greater Accra, GA233, Ghana",

&nbsp;   "is\_email\_verified": false,

&nbsp;   "bio": "Coming soon",

&nbsp;   "date\_of\_birth": "1957-03-06",

&nbsp;   "newsletter\_subscription": true,

&nbsp;   "account\_status": "PENDING",

&nbsp;   "user\_type": "CUSTOMER",

&nbsp;   "date\_joined": "2025-09-17 12:14:00",

&nbsp;   "last\_login": "2025-09-17 12:16:06"

&nbsp; }

}







**`/api/v1/accounts/profiles/request-password-reset/`**

**POST**

Request body

{

&nbsp; "email": "kwame.nkrumah@ghana.com"

}



Response body

{

&nbsp; "message": "If the email exists in our system, you will receive password reset instructions."

}



Email Message Sample

Content-Type: multipart/alternative;

&nbsp;boundary="===============4718208076344061899=="

MIME-Version: 1.0

Subject: Password Reset Request

From: festus233@gmail.com

To: kwame.nkrumah@ghana.com

Date: Wed, 17 Sep 2025 14:15:14 -0000

Message-ID: <175811851441.82612.6901922752009398036@MSI>



--===============4718208076344061899==

Content-Type: text/plain; charset="utf-8"

MIME-Version: 1.0

Content-Transfer-Encoding: 7bit





<!DOCTYPE html>

<html>



<head>

&nbsp;   <meta http-equiv="Content-Type" content="text/html; charset=utf-8">

&nbsp;   <meta name="viewport" content="width=device-width, initial-scale=1.0">

&nbsp;   <title>Password Reset - ALX E-Commerce</title>

&nbsp;   <style>

&nbsp;       body {

&nbsp;           font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;

&nbsp;           line-height: 1.6;

&nbsp;           color: #333;

&nbsp;           margin: 0;

&nbsp;           padding: 0;

&nbsp;           background-color: #f5f5f5;

&nbsp;       }



&nbsp;       .container {

&nbsp;           max-width: 600px;

&nbsp;           margin: 0 auto;

&nbsp;           padding: 20px;

&nbsp;       }



&nbsp;       .header {

&nbsp;           background-color: #4a6fa5;

&nbsp;           color: white;

&nbsp;           padding: 20px 0;

&nbsp;           text-align: center;

&nbsp;           border-radius: 5px 5px 0 0;

&nbsp;       }



&nbsp;       .content {

&nbsp;           background-color: #ffffff;

&nbsp;           padding: 30px;

&nbsp;           border-radius: 0 0 5px 5px;

&nbsp;           box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);

&nbsp;       }



&nbsp;       .button {

&nbsp;           display: inline-block;

&nbsp;           padding: 12px 24px;

&nbsp;           margin: 20px 0;

&nbsp;           background-color: #4a6fa5;

&nbsp;           color: white !important;

&nbsp;           text-decoration: none;

&nbsp;           border-radius: 4px;

&nbsp;           font-weight: bold;

&nbsp;       }



&nbsp;       .footer {

&nbsp;           margin-top: 30px;

&nbsp;           font-size: 12px;

&nbsp;           color: #777;

&nbsp;           text-align: center;

&nbsp;       }



&nbsp;       .reset-link {

&nbsp;           word-break: break-all;

&nbsp;           color: #4a6fa5;

&nbsp;           text-decoration: none;

&nbsp;       }

&nbsp;   </style>

</head>



<body>

&nbsp;   <div class="container">

&nbsp;       <div class="header">

&nbsp;           <h1>Password Reset Request</h1>

&nbsp;       </div>

&nbsp;       <div class="content">

&nbsp;           <p>Hello Kwame Nkrumah,</p>



&nbsp;           <p>You're receiving this email because you requested a password reset for your ALX E-Commerce account.</p>        



&nbsp;           <p>Please click the button below to reset your password:</p>



&nbsp;           <p style="text-align: center;">

&nbsp;               <a href="http://localhost:3000  # Your frontend URL/reset-password/NjU5ZTk2ZjktMzFjNi00YjdhLTlkYjItNzNhMjc3YTU1YzZk/cwa29e-e0c47bf982c9d82c303c357e80d95dcb/" class="button">Reset Password</a>

&nbsp;           </p>



&nbsp;           <p>Or copy and paste this link into your browser:</p>

&nbsp;           <p><a href="http://localhost:3000  # Your frontend URL/reset-password/NjU5ZTk2ZjktMzFjNi00YjdhLTlkYjItNzNhMjc3YTU1YzZk/cwa29e-e0c47bf982c9d82c303c357e80d95dcb/" class="reset-link">http://localhost:3000  # Your frontend URL/reset-password/NjU5ZTk2ZjktMzFjNi00YjdhLTlkYjItNzNhMjc3YTU1YzZk/cwa29e-e0c47bf982c9d82c303c357e80d95dcb/</a></p>



&nbsp;           <p>This link will expire in 24 hours for security reasons.</p>



&nbsp;           <p>If you didn't request this password reset, please ignore this email. Your password will remain unchanged.      

&nbsp;           </p>



&nbsp;           <p>Thanks,<br>The ALX E-Commerce Team</p>



&nbsp;           <div class="footer">

&nbsp;               <p>This is an automated message, please do not reply to this email.</p>

&nbsp;               <p>\&copy; 2025 ALX E-Commerce. All rights reserved.</p>

&nbsp;           </div>

&nbsp;       </div>

&nbsp;   </div>

</body>



</html>



--===============4718208076344061899==





**`/api/v1/accounts/profiles/request-verification-email/`**

**POST**

Request body

{

&nbsp; "email": "kwame.nkrumah@ghana.com"

}



Response body

200

{

&nbsp; "message": "Verification email sent successfully"

}



400: Error: Bad Request

{

&nbsp; "message": "Email is already verified."

}





**`/api/v1/accounts/profiles/update-profile/`**

**PUT | PATCH**

Request body

{

&nbsp; "is\_active": true,

&nbsp; "email": "kwame.nkrumah@ghana.com",

&nbsp; "first\_name": "Kwame",

&nbsp; "last\_name": "Nkrumah",

&nbsp; "phone\_number": "+2332498051198",

&nbsp; "address\_line\_1": "Black Star Square",

&nbsp; "address\_line\_2": "Opposite Accra Sports Stadium",

&nbsp; "city": "Osu",

&nbsp; "state": "Greater Accra",

&nbsp; "postal\_code": "GA233",

&nbsp; "country": "Ghana",

&nbsp; "bio": "Coming soon",

&nbsp; "date\_of\_birth": "1957-03-06",

&nbsp; "newsletter\_subscription": false

}





Response body

{

&nbsp; "message": "Profile updated successfully",

&nbsp; "user": {

&nbsp;   "id": "659e96f9-31c6-4b7a-9db2-73a277a55c6d",

&nbsp;   "created\_at": "2025-09-17 12:14:02",

&nbsp;   "updated\_at": "2025-09-17 13:45:07",

&nbsp;   "is\_active": true,

&nbsp;   "username": "kwams",

&nbsp;   "email": "kwame.nkrumah@ghana.com",

&nbsp;   "first\_name": "Kwame",

&nbsp;   "last\_name": "Nkrumah",

&nbsp;   "phone\_number": "+2332498051198",

&nbsp;   "address\_line\_1": "Black Star Square",

&nbsp;   "address\_line\_2": "Opposite Accra Sports Stadium",

&nbsp;   "city": "Osu",

&nbsp;   "state": "Greater Accra",

&nbsp;   "postal\_code": "GA233",

&nbsp;   "country": "Ghana",

&nbsp;   "full\_name": "Kwame Nkrumah",

&nbsp;   "full\_address": "Black Star Square, Opposite Accra Sports Stadium, Osu, Greater Accra, GA233, Ghana",

&nbsp;   "is\_email\_verified": true,

&nbsp;   "bio": "Coming soon",

&nbsp;   "date\_of\_birth": "1957-03-06",

&nbsp;   "newsletter\_subscription": false,

&nbsp;   "account\_status": "PENDING",

&nbsp;   "user\_type": "CUSTOMER",

&nbsp;   "date\_joined": "2025-09-17 12:14:00",

&nbsp;   "last\_login": "2025-09-17 13:02:16"

&nbsp; }

}



**`/api/v1/accounts/profiles/verify-email/`**

**POST**

Request body

{

&nbsp; "token": "iNKR2qKEdVdWS5852xYXuDxUGuFz37qyNVSBCc2g0MnljsaP4MdDCpViNKr4CEjh",

&nbsp; "email": "kwame.nkrumah@ghana.com"

}



Response body

{

&nbsp; "message": "Email verified successfully. Your account is now active."

}







**ADMIN**

**{**

  **"access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzU4MTQ2NDYxLCJpYXQiOjE3NTgxMzIwNjEsImp0aSI6IjgwZGM1NjU4YTU5NjRmNTY5YzU2ZDk0Yzg3MWFlZWI0IiwidXNlcl9pZCI6IjI1ZmUwMmMzLWEzY2UtNGMzNi1iNWMzLTMxNTZlZDkwNzg1OCJ9.C9IE0ToYbz1u2WrMHpc6RQVhIsrChbS\_MXfrHoSpotw",**

  **"refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc1ODIxODQ2MSwiaWF0IjoxNzU4MTMyMDYxLCJqdGkiOiI2ZGYyZDZiYzZkNWY0ZTZkYWM2NDJlZGU4ZWE5MTA0NSIsInVzZXJfaWQiOiIyNWZlMDJjMy1hM2NlLTRjMzYtYjVjMy0zMTU2ZWQ5MDc4NTgifQ.W96cvY07v1RZzxdmV68vMTrxGk\_t2f6y9GFYvWZKPy8**

