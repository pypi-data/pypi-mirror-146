# Authentication
A django user authentication and login application.

### 0.  To install the package, use pip
        
        pip install django-user-login

Instructions

### 1.	Add "authentication" to your INSTALLED_APPS setting like this:

        INSTALLED_APPS = [
            ...
            'authentication',
        ]

### 2.	The App requires [bootstrap@5.3.1](https://getbootstrap.com/docs/5.1/getting-started/introduction/), [bootstrap-icons@1.8.1](https://icons.getbootstrap.com/) and [Django Sessions](https://docs.djangoproject.com/en/4.0/topics/http/sessions/#enabling-sessions)

### 3.	Include the authentication URLconf in your project urls.py like this:

		path('authentication/', include('authentication.urls')),

### 4.	Run `python manage.py migrate` to create the User models (you'll need the Admin app enabled).

### 5.  In your settings.py file include the following:

        SITE_TITLE = 'your site title'
        
        LOGIN_URL = '/authentication/'

        EMAIL_HOST = 'email-host'
        EMAIL_PORT = email-port
        EMAIL_HOST_USER = 'email-address'
        EMAIL_HOST_PASSWORD = 'email-password'
        EMAIL_USE_TLS = True

### 6.  Include these lines within the head tag of your [base template](https://docs.djangoproject.com/en/4.0/ref/templates/language/#template-inheritance-1) (optional)

        <link rel="stylesheet" href="{% static 'authentication/authentication.css' %}">
        <script src="{% static 'authentication/authentication.js' %}"></script>
        <script>
        	var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'))
            var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
                return new bootstrap.Tooltip(tooltipTriggerEl)
            })
        </script>

### 7.  Include this line within the body tag of your [base template](https://docs.djangoproject.com/en/4.0/ref/templates/language/#template-inheritance-1) (optional)
	
    	{% include 'authentication/modals.html' %}

### 8.  For login and logout functionality, use - 
- #### Login
            <a href="{% url 'authentication:login' %}">Login</a> or
		    <a href='/authentication/'>Login</a>
- #### The above functionality will redirect to the "next" parameter in the url after logging the user in.
- #### Logout
            <a href="{% url 'authentication:logout' %}">Logout</a> or
		    <a href="/authentication/logout/">Logout</a>
- #### The above functionality will redirect to the login page after logging the user out.

### 9.  If you have included all the lines mentioned in point 6 and 7, you can also use -
- #### Login via [Bootstrap Modal](https://getbootstrap.com/docs/5.1/components/modal/)
            <button data-bs-toggle="modal" data-bs-target="#loginModal">
                Login
            </button>
- #### The above functionality will display the bootstrap login form Modal and reload the current page after logging the user in.
- #### Logout using JS
            <a href="" onclick="logout(event);">Logout</a>
- #### The above functionality will reload the current page after logging the user out