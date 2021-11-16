from fastapi import Request


def db(request: Request):
    return request.state.db
