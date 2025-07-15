import psycopg2
from faker import Faker
import random

DB_CONFIG = dict(
    host="localhost",
    port=5432,
    user="crmuser",
    password="crmsecret",
    dbname="crm"
)

NUM_ACCOUNTS = 10
NUM_CONTACTS = 30
NUM_EMAILS = 60

fake = Faker()

conn = psycopg2.connect(**DB_CONFIG)
cur = conn.cursor()

# Insert accounts
def seed_accounts():
    account_ids = []
    for _ in range(NUM_ACCOUNTS):
        name = fake.company()
        industry = fake.job()
        cur.execute(
            "INSERT INTO accounts (name, industry) VALUES (%s, %s) RETURNING id;",
            (name, industry)
        )
        account_ids.append(cur.fetchone()[0])
    return account_ids

# Insert contacts
def seed_contacts(account_ids):
    contact_ids = []
    for _ in range(NUM_CONTACTS):
        account_id = random.choice(account_ids)
        first = fake.first_name()
        last = fake.last_name()
        email = fake.unique.email()
        phone = fake.phone_number()
        cur.execute(
            "INSERT INTO contacts (account_id, first_name, last_name, email, phone) VALUES (%s, %s, %s, %s, %s) RETURNING id;",
            (account_id, first, last, email, phone)
        )
        contact_ids.append(cur.fetchone()[0])
    return contact_ids

# Insert emails
def seed_emails(contact_ids):
    for _ in range(NUM_EMAILS):
        contact_id = random.choice(contact_ids)
        subject = fake.sentence(nb_words=6)
        body = fake.paragraph(nb_sentences=3)
        cur.execute(
            "INSERT INTO emails (contact_id, subject, body) VALUES (%s, %s, %s);",
            (contact_id, subject, body)
        )

if __name__ == "__main__":
    print("Seeding accounts...")
    account_ids = seed_accounts()
    print("Seeding contacts...")
    contact_ids = seed_contacts(account_ids)
    print("Seeding emails...")
    seed_emails(contact_ids)
    conn.commit()
    cur.close()
    conn.close()
    print("Done!")
