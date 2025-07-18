import sqlite3
from sqlite3 import Error

def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)
    return conn

def create_panic(conn, panic):
    sql = '''insert into panics(name, panic_string, description, comment)
            values(?, ?, ?, ?)'''
    cur = conn.cursor()
    cur.execute(sql, panic)
    conn.commit()
    return cur.lastrowid

def update_panic(conn, panic):
    sql = '''update panics
            set name = ? ,
                panic_string = ?,
                description = ?,
                comment = ?
            where id = ?'''
    cur = conn.cursor()
    cur.execute(sql, panic)
    conn.commit()

# def main():
#     database = r"data_base/pythonsqlite.db"
#     conn = create_connection(database)
#     with conn:
#         panic = ("panic #1", "panic(cpu 4 caller 0xfffffff0148c0c90)", "Этот паник означает, что ядро процессора номер 4 вышло из строя", "Надо подумать как написать по-другому")
#         panic_id = create_panic(conn, panic)

# if __name__ == '__main__':
#     main()

