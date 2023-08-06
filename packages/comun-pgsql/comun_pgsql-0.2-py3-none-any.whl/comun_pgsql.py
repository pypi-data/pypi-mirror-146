import psycopg as psy


class PgSQL:
    def __init__(self, ip, port, database, user, password):
        self.ip = ip
        self.port = port
        self.database = database
        self.user = user
        self.password = password
        self.connexion = psy.connect(
            host=ip,
            port=port,
            dbname=database,
            user=user,
            password=password
        )
        self.cursor = self.connexion.cursor()

    def __str__(self):
        return f"PostgeSQL connexion data:" \
               f"\n\tIP: {self.ip}" \
               f"\n\tPort: {self.port}" \
               f"\n\tDatabase: {self.database}" \
               f"\n\tUser: {self.user}"

    def close_connexion(self):
        self.connexion.close()

    def insert_or_update_execution(self, query: str):
        self.cursor.execute(query)
        return self.connexion.commit()

    def select_execution(self, query: str):
        self.cursor.execute(query)
        return self.cursor.fetchall()
