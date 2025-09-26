python3.10 -m venv mysite/env
source mysite/env/bin/activate

cd mysite
python manage.py runserver

http://127.0.0.1:8000 

deactivate

# Different APIs for Blog
http://127.0.0.1:8000/api/v2/pages/?type=blog.BlogPage
http://127.0.0.1:8000/api/v2/pages/?type=blog.BlogPage&fields=date_display,intro,body,authors
http://localhost:8000/api/v2/pages/?type=blog.BlogPage&fields=*&limit=1
http://127.0.0.1:8000/api/v2/pages/?type=blog.BlogPage&search=basil

# Different APIs for Teams
http://127.0.0.1:8000/api/team/members/
http://127.0.0.1:8000/api/team/members/?format=json
http://localhost:8000/api/team/members/?search=python
http://127.0.0.1:8000/api/team/departments/
http://127.0.0.1:8000/api/team/stats/
http://127.0.0.1:8000/api/team/members/4/