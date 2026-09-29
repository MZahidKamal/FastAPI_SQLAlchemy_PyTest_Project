# External imports -----------------------------------------------------------------------------------------------------
from sqlalchemy import create_engine
from sqlalchemy import text
from sqlalchemy.orm import sessionmaker
# Internal imports -----------------------------------------------------------------------------------------------------
from src.core.config import env_settings





# Necessary classes, objects and functions -----------------------------------------------------------------------------

db_engine = create_engine(env_settings.sb_connection_string)

DB_SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=db_engine)

def get_db():
    db = DB_SessionLocal()
    try:
        yield db
    finally:
        db.close()





# Checking database cloud accessibility (Option 01) --------------------------------------------------------------------

# If we keep this code snippet active, and run 'python -m src.db.session' in the terminal, then only this session.py file
# will run, then database connection object will print as a simple string. The database connection and accessibility will
# be confirmed.

# if __name__ == "__main__":
#     with db_engine.connect() as connection:
#         print("Connection successful:", connection)





# Checking database cloud accessibility (Option 02) --------------------------------------------------------------------

# If we keep this code snippet active, and run 'python -m src.db.session' in the terminal, then only this session.py file
# will run, then database connection object with some useful information will print as a organized string. The database
# connection and accessibility will be confirmed.

# if __name__ == "__main__":
#     try:
#         with db_engine.connect() as connection:
#             result = connection.execute(text("SELECT version();"))
#             db_version = result.scalar()
#             print("✅ Database connection established successfully.")
#             print(f"✅ Connected to: {db_engine.url.database} @ {db_engine.url.host}")
#             print(f"✅ PostgreSQL version: {db_version}")
#     except Exception as error:
#         print("❌ Failed to connect to the database.")
#         print(f"   Reason: {error}")





# Checking database cloud accessibility (Option 03) --------------------------------------------------------------------

# If we keep this code snippet active, then every time we will run this project, the database connection object with some
# useful information will print as a organized string. The database connection and accessibility will be confirmed.

def check_db_connection():
    try:
        with db_engine.connect() as connection:
            result = connection.execute(text("SELECT version();"))
            db_version = result.scalar()
            print("\nChecking if database connection is established correctly...")
            print("    ✅ Database connection established successfully.")
            print(f"    ✅ Connected to: {db_engine.url.database} @ {db_engine.url.host}")
            print(f"    ✅ PostgreSQL version: {db_version}")
    except Exception as error:
        print("❌ Failed to connect to the database.")
        print(f"   Reason: {error}")


if __name__ == "__main__":
    check_db_connection()




