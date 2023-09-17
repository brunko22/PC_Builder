import Builds
import ConnectionDB
import User
from psycopg2.extras import RealDictCursor


class operation:

    def ricerca(utilizzo, tipo_ram, fascia):
        conn = ConnectionDB.Connection().conn()
        cur = conn.cursor(cursor_factory=RealDictCursor)
        query = "Select * from builds"
        val=None
        if utilizzo is not None and utilizzo or tipo_ram is not None and tipo_ram:
            query = query + " where"
        if utilizzo is not None and utilizzo:
            query = query + " utilizzo ilike %s"
            val=(utilizzo,)
            if tipo_ram is not None and tipo_ram:
                 query = query + " and tipo_ram ilike %s"
                 val = val + (tipo_ram,)
        elif tipo_ram is not None and tipo_ram:
            query = query + " tipo_ram ilike %s"
            val=(tipo_ram,)
        if fascia is not None and fascia:
            query = query + " ORDER BY ABS(fascia - %s) LIMIT 1"
            if val is not None:
                val = val + (fascia,)
            else:
                val=(fascia,)
        cur.execute(query,val)
        rows = cur.fetchall()
        builds = []
        for row in rows:
            build = Builds.Build()
            build.set_prezzo(row['prezzo'])
            build.set_tipo_ram(row['tipo_ram'])
            build.set_fascia(row['fascia'])
            build.set_utilizzo(row['utilizzo'])
            build.set_uid(row['uid'])
            build.set_componenti(row['componenti'])
            builds.append(build)
        ConnectionDB.Connection.close(conn)
        return builds


    def ricercaAll():
        conn = ConnectionDB.Connection().conn()
        cur = conn.cursor(cursor_factory=RealDictCursor)
        query = "Select * from builds"
        cur.execute(query)
        rows = cur.fetchall()
        builds = []
        for row in rows:
            build = Builds.Build()
            build.set_prezzo(row['prezzo'])
            build.set_tipo_ram(row['tipo_ram'])
            build.set_fascia(row['fascia'])
            build.set_utilizzo(row['utilizzo'])
            build.set_uid(row['uid'])
            build.set_componenti(row['componenti'])
            builds.append(build)
        ConnectionDB.Connection.close(conn)
        return builds


    def ricercaUid(uid):
        conn = ConnectionDB.Connection().conn()
        cur = conn.cursor(cursor_factory=RealDictCursor)
        query = "Select * from builds where uid=%s"
        val=(uid,)
        cur.execute(query,val)
        rows = cur.fetchall()
        builds = []
        for row in rows:
            build = Builds.Build()
            build.set_prezzo(row['prezzo'])
            build.set_tipo_ram(row['tipo_ram'])
            build.set_fascia(row['fascia'])
            build.set_utilizzo(row['utilizzo'])
            build.set_uid(row['uid'])
            build.set_componenti(row['componenti'])
            builds.append(build)
        ConnectionDB.Connection.close(conn)
        return builds

    def ricerca_user(email):
        conn = ConnectionDB.Connection().conn()
        cur = conn.cursor(cursor_factory=RealDictCursor)
        query="Select * From utenti where email ilike %s"
        val=(email,)
        cur.execute(query,val)
        rows = cur.fetchall()
        user = None
        for row in rows:
            user = User.User()
            user.set_email(row['email'])
            user.set_admin(row['admin'])
            ConnectionDB.Connection.close(conn)
        return user

    def insert_build(prezzo, tipo_ram, fascia, utilizzo, componenti):
        conn = ConnectionDB.Connection().conn()
        cur = conn.cursor()
        sql="Insert into builds (prezzo,tipo_ram,fascia,utilizzo,componenti)  values (%s,%s,%s,%s,%s)"
        val = (prezzo,tipo_ram,fascia,utilizzo,componenti)
        cur.execute(sql,val)
        conn.commit();
        ConnectionDB.Connection.close(conn)


    def update(uid, prezzo, fascia, componenti, utilizzo, tipo_ram):
        conn = ConnectionDB.Connection().conn()
        cur = conn.cursor()
        sql=("Update builds"
             " set  prezzo=%s, fascia=%s, componenti=%s, utilizzo=%s,tipo_ram=%s"
             " where uid=%s")
        val=(prezzo,fascia,componenti,utilizzo,tipo_ram,uid)
        cur.execute(sql,val)
        conn.commit()
        ConnectionDB.Connection.close(conn)

    def delete(uid):
        conn = ConnectionDB.Connection().conn()
        cur = conn.cursor()
        sql = "Delete from builds where uid=%s"
        val = (uid,)
        cur.execute(sql, val)
        conn.commit()
        ConnectionDB.Connection.close(conn)







