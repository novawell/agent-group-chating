import sys

def config_chroma_for_streamlit_deploy():
    __import__('pysqlite3')
    sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')