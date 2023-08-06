select dbdata.id as id, dbdata.code as code, 
dbdata.path as path, dbdata.host as host, dbdata.port as port, 
dbdata.user as user, dbdata.passw as passw, dbdata.dbname as dbname,
dbdata.info as info, dbtype.id as type_id, dbtype.name as type_name, 
dbtype.typedb as type_db, dbtype.url as url, dbtype.data_list as data_list
from dbdata inner join dbtype on dbtype_id=dbtype.id
