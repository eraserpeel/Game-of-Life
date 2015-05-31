from game_of_life import GameOfLife as GameOflife
import random as rnd
import numpy
from hashlib import sha1
import threading

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float, Boolean
from sqlalchemy.orm import scoped_session, sessionmaker

Base = declarative_base()
class Dataset(Base):
    __tablename__ = 'dataset'
    id = Column(Integer, primary_key=True)
    percent_fill = Column(Float)
    intial_fill = Column(Float)
    final_fill = Column(Float)
    is_empty = Column(Boolean)
    generations = Column(Integer)
    generation_loop = Column(Integer)
    loop_length = Column(Integer)
    initial_generation = Column(String(10000))
    

class DataThread(threading.Thread): 

    def __init__(self, thread_name, iters, db_session):
        super(DataThread, self).__init__()
        self.db_session = db_session
        self.thread_name = thread_name
        self.iters = iters
        self.MAX_CYCLES = 50000

    def run(self):
        for i in range(0, self.iters):
            coverage = rnd.random()
            gol = GameOflife(50, 50, coverage)
            cycle_detected_flag = False
            grids_saved = {} 
            iterations = 0
            initial_grid_state = str(gol.get_as_tuple())
            living_cells_count = gol.get_living_count()
            all_dead = False
            
            while not cycle_detected_flag and iterations < self.MAX_CYCLES:
                current_grid_state = hash(gol.get_as_tuple())
                if current_grid_state not in grids_saved:
                    grids_saved[current_grid_state] = iterations
                    iterations += 1
                else:
                    cycle_detected_flag = True
                    final_living_cells_count = gol.get_living_count()
                    if final_living_cells_count == 0:
                        all_dead = True
                    entry = Dataset(percent_fill = coverage,
                                    intial_fill = living_cells_count, 
                                    final_fill = final_living_cells_count,
                                    is_empty = all_dead,
                                    generations = iterations,
                                    generation_loop = grids_saved[current_grid_state],
                                    loop_length = iterations - grids_saved[current_grid_state],
                                    initial_generation = initial_grid_state)
                    self.db_session.add(entry)
                    self.db_session.commit()
                gol.run_rules()
            print(self.thread_name, i)
        

if __name__ == "__main__":
    DB_URI = "mysql+mysqlconnector://{user}:{password}@{host}:{port}/{db}"
 
    engine = create_engine(DB_URI.format(
      user ='root',
      password = '',
      host = '127.0.0.1',
      port = '3306',
      db = 'ca'))
    Base.metadata.create_all(engine)
    Base.metadata.bind = engine
    session_factory = sessionmaker(bind=engine, autoflush=True)
    db_session = scoped_session(session_factory)
    
    for i in range(0, 100):
        t = DataThread(str(i), 100, db_session)
        t.start()
    

