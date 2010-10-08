
from kokki import *

env.include_recipe("apache2")

Package("nagios3")

File("/etc/apache2/conf.d/nagios3.conf",
    action = "delete",
    notifies = [("restart", env.resources["Service"]["apache2"])])

File("/etc/apache2/sites-available/nagios3",
    owner = "www-data",
    group = "www-data",
    mode = 0644,
    content = Template("nagios3/apache2-site.j2"),
    notifies = [("restart", env.resources["Service"]["apache2"])])

env.cookbooks.apache2.site("nagios3")