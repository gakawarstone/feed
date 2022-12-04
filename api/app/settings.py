import tomllib

SOURCES_LIST = [s.strip() for s in open('sources')]

with open('sources.toml') as f:
    content = f.read()
    SOURCES_DATA = tomllib.loads(content)
