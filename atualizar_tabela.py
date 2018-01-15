from tabledef import *        
        
# create tables
Base.metadata.drop_all(engine)
#utiliza os dados de tabledef
Base.metadata.create_all(engine)
