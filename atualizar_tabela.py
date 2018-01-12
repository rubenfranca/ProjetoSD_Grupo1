from tabledef import *        
        
# create tables
Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)