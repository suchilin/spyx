from flask_seeder import Seeder, Faker, generator
from app.auth.models import User

class DemoSeeder(Seeder):

  def run(self):
    giusepi=User(email="giusepi@spyx.com", name="Giusepi", description="The superboss")
    giusepi.set_password("")
    self.db.session.add(giusepi)

    manager1=User(email="manager1@spyx.com", name="Manager One", description="The first manager")
    manager1.set_password("Manager1_2021")
    self.db.session.add(manager1)

    manager2=User(email="manager2@spyx.com", name="Manager Two", description="The first manager")
    manager2.set_password("Manager2_2021")
    self.db.session.add(manager2)

    manager3=User(email="manager3@spyx.com", name="Manager Three", description="The first manager")
    manager3.set_password("Manager3_2021")
    self.db.session.add(manager3)

    for i in range(1,10):
        name="user%s" % i
        email="user%s@spyx.com" % i
        description = "The user # %s" %i
        password = "User%s_2021" %i
        user=User(name=name, email=email, description=description)
        user.set_password(password)
        if i<=3:
            user.manager=manager1
        elif i<=6:
            user.manager=manager2
        else:
            user.manager=manager3
        self.db.session.add(user)

