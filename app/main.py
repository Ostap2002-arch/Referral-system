import sys
from os.path import dirname, abspath

from fastapi import FastAPI

sys.path.insert(0, dirname(dirname(abspath(__file__))))

from app.users.router import router as user_router
from app.referral_system.router import router as router_referral_system

app = FastAPI()

app.include_router(user_router)
app.include_router(router_referral_system)

