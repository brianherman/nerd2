
class SQLiteDB:
    def setup(self, fname):
        self.conn = 




class ModreqDB(SQLiteDB):
    def __init__(self, server_name):
        self.setup(config.MODREQ_DB % server_name)
    def getRequests(self, **params):
        defaults = {
            'status': 'all',
            'limit': 100,
            'sort': 'desc',
        }
        
        final = dict(defaults)
        final.update(params)
        
        q = 'SELECT * from modreq_requests'
        
        if final['status'] != 'all':
            q += 'WHERE status = "%s"' % final['status']
        
        q += 'ORDER BY ID %s' % final['sort']
        q += 'LIMIT %d' % final['limit']
        
        return query_db(q, self.conn)
        
