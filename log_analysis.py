import psycopg2
from time import strftime


def connect(db_name):
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=%s" % db_name)


def request_db(db_name, fetch, *args):
    result = []
    conn = connect(db_name)
    cur = conn.cursor()
    for command in args:
        cur.execute(command)
        if fetch:
            result.append(cur.fetchall())
    conn.commit()
    conn.close()
    return result


def test_log_analysis():
    log = LogsAnalysis()
    log.top_3_articles()
    log.top_3_authors()
    log.p1_errs()


class LogsAnalysis(object):

    db = 'news'
    table_log_stats = 'log_stats'

    def top_3_articles(self):
        self._top_n(3, 'article', 'views')

    def top_3_authors(self):
        self._top_n(3, 'author', 'views')

    def p1_errs(self):
        self._errs(0.1)

    def _top_n(self, num, key, unit):
        valid_key = ['article', 'author']
        if key not in valid_key:
            return
        top_n = request_db(self.db, True,
                           'select %s, count(*) from \
                             (select \
                              articles.title as article, \
                              authors.name as author \
                              from log left join articles \
                              on log.path like \'%%\' || articles.slug \
                              left join authors \
                              on articles.author=authors.id \
                              where log.path!=\'/\') n1 \
                            group by %s \
                            order by count(*) desc \
                            limit %s' % (key, key, num))
        self._print_result(unit, top_n[0])

    def _print_result(self, unit, data):
        for d in data:
            # print 'data', d
            print '%s -- %s %s' % (d[0], d[1], unit)
        print '\n'

    def _errs(self, ratio):
        key = '404 NOT FOUND'
        command = 'select * from \
                 (select n1.date, 1.0*n2.num/n1.num as ratio from \
                   (select count(*) as num, log.time::date as date \
                    from log group by log.time::date) n1 \
                   right join \
                   (select count(*) as num, log.time::date as date \
                    from log where log.status=\'%s\' \
                    group by log.time::date) n2 \
                  on n1.date=n2.date) n3 \
               where n3.ratio>0.01;' % key
        err = request_db(self.db, True, command)[0]
        err_stats = [(e[0].strftime('%B %d, %Y'),
                      '{0:.2%}'.format(e[1])) for e in err]
        self._print_result('percent', err_stats)


if __name__ == '__main__':
    test_log_analysis()
