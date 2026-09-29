# External imports -----------------------------------------------------------------------------------------------------
from fastapi import FastAPI
from contextlib import asynccontextmanager
# Internal imports -----------------------------------------------------------------------------------------------------
from src.core.config import check_env_settings
from src.core.security import check_jwt_settings
from src.db.session import check_db_connection
from src.features.users.router import router as users_router
from src.features.users import models  # noqa: F401





# Decorator ------------------------------------------------------------------------------------------------------------

# Option 01: If we keep this code snippet active, and run the project, then lifespan function will check the .env
# accessibility and database connection before running the project.

# @asynccontextmanager
# async def lifespan(app: FastAPI):
#     check_env_settings()
#     check_db_connection()
#     yield





# Option 02: If we keep this code snippet active, and run the project, then lifespan function will check the .env
# accessibility and database connection before running the project and will give us confirmation if the project runs
# properly. It will show error if there is any. And it will give us shutdown confirmation if it needs to shut down.

@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        check_env_settings()
        check_db_connection()
        check_jwt_settings()
        print("\nApplication startup checks completed successfully.")
        yield
    except Exception as error:
        print(f"Startup failed due to: {error}")
        raise error
    finally:
        # এখানে সার্ভার শাটডাউন হওয়ার সময় কোনো রিসোর্স ক্লিনআপ করার থাকলে তা করতে পারেন
        print("Application shutting down...")





# FastAPI main App -----------------------------------------------------------------------------------------------------
app = FastAPI(title="FastAPI_SQLAlchemy_PyTest_Project App", lifespan=lifespan)





# Root API Routers -----------------------------------------------------------------------------------------------------
@app.get("/", tags=["root api"])
async def root():
    return {"message": "Hello World"}





# Imported API Routers -----------------------------------------------------------------------------------------------------
app.include_router(users_router)




