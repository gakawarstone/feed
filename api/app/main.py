from manage import get_app


if __name__ == '__main__':
    import uvicorn
    uvicorn.run(get_app())
