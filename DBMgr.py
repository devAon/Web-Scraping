import pymysql as my

class DBHelper:
    def __init__(self):
        self.db_init()
    
    def db_init(self):
        self.conn = my.connect(
                        host='localhost',
                        user='root',
                        password='thfxkfbb46',
                        db='pythonDB',
                        charset='utf8',
                        cursorclass=my.cursors.DictCursor )
    
    def db_free(self):
        if self.conn:
            self.conn.close()

    def db_selectKeyword(self):
        rows = None
        with self.conn.cursor() as cursor:
            sql  = "select * from tbl_keyword;"
            cursor.execute(sql)
            rows = cursor.fetchall()
            print(rows)
        return rows
        
    def db_insertCrawlingData(self, title, price, area, contents, keyword ):
        with self.conn.cursor() as cursor:
            sql = '''
            insert into `tbl_crawlingdata` 
            (title, price, area, contents, keyword) 
            values( %s,%s,%s,%s,%s )
            '''
            cursor.execute(sql, (title, price, area, contents, keyword) )
        self.conn.commit()
        

if __name__=='__main__':
    db = DBHelper()
    print( db.db_selectKeyword() )
    print( db.db_insertCrawlingData('1','2','3','4','5') )
    db.db_free()