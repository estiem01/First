import sqlite3
from dataclasses import dataclass
from tabulate import tabulate

class DB:
    con = sqlite3.connect("LC_db.sqlite")
    cur = con.cursor()

@dataclass
class Users(DB):
    id: int = None
    name: str = None

    def select(self):
        if not self.id:
            query = """select * from users"""
        else:
            query = f"""select * from users where id = {self.id}"""
        self.cur.execute(query)
        users = self.cur
        return users

@dataclass()
class Category(DB):
    id: int = None
    name: str = None

    def select(self):
        if not self.id:
            query = """select * from categories"""
        else:
            query = f"""select * from categories where id = {self.id}"""
        self.cur.execute(query)
        categories = self.cur
        return categories

@dataclass()
class Solution(DB):
    id: int = None
    issue_num: int = None
    user_id: int = None
    category_id: int = None

    def check(self):
        query = f"""select * from solutions where issue_num = {self.issue_num}
        and category_id = {self.category_id} and user_id = {self.user_id}"""
        self.cur.execute(query)
        if bool(self.cur.fetchone()):
            raise Exception("Bunday misol oldin ishlangan !")

    def add(self):
        self.check()
        query = """
            insert into solutions(issue_num, user_id, category_id) values (?, ?, ?)
        """
        params = (self.issue_num, self.user_id, self.category_id)
        self.cur.execute(query, params)
        self.con.commit()
        print(f"Successfully added {self.issue_num} !")

class Project:
    def run(self):
        try:
            users: list[tuple[int, str]] = Users().select().fetchall()
            print(tabulate(users, headers=("id", "name"), tablefmt='simple_grid'))
            self.user_id: int = int(input(">>> "))
            if not self.user_id in dict(users).keys():
                raise ValueError("Invalid user id !")
            self.categories_menu()
        except Exception as e:
            print(e)
            self.run()

    def categories_menu(self):
        try:
            categories: list[tuple[int, str]] = Category().select().fetchall()
            print(tabulate(categories, headers=("id", "name"), tablefmt='simple_grid'))
            self.category_id: int = int(input(">>> "))
            if not self.category_id in dict(categories).keys():
                raise ValueError("Invalid user id !")
            self.solution_menu()

        except Exception as e:
            print(e)
            self.categories_menu()

    def show(self):
        pass

    def count(self):
        pass

    def solution_menu(self):
        try:
            menu = """
            1) add
            2) back
            3) main_menu
                >>> """
            key: int = int(input(menu))
            if key not in (1, 2, 3):
                raise ValueError("Invalid key !")

            match key:
                case 1:
                    issue_num = input("issue number: ")
                    if not issue_num.isdigit():
                        raise ValueError("Invalid issue number !")
                    issue_num = int(issue_num)
                    Solution(issue_num=issue_num, user_id=self.user_id, category_id=self.category_id).add()
                    self.solution_menu()
                case 2:
                    self.categories_menu()
                case 3:
                    self.run()
        except Exception as e:
            print(e)
            self.solution_menu()

Project().run()