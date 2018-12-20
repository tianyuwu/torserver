#!/usr/bin/env python
# encoding: utf-8
from app.model import BaseModel


class UsersModel(BaseModel):

    async def list_all(self):
        """query data by self.db"""
        return None