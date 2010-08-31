You should execute tz-restore.sh to recreate the tangaza db and bootstrap it with the needed data.

Techinical requirements:
***********************
1. MySQL 5.0 or higher

TODO:
****
1. Create a database (the setup script assumes the database is called 'tangaza'.)
1. Edit tz-restore.sh and insert appropriate values for user, password and host.
Change the DB values if your database in 1. above is not called 'tangaza'.
tz-restore.sh will create the required tables. Some django* tables are also
created. These can be deleted in case you want to create your own tables or you
are not using django.