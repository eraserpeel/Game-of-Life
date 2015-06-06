from neural_network import BackPropogationNetwork
import numpy as np

import random as rnd
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float, Boolean
from sqlalchemy.orm import scoped_session, sessionmaker
import ast
import pickle
from pybrain.structure import FeedForwardNetwork
from pybrain.structure import LinearLayer, SigmoidLayer
from pybrain.structure import FullConnection
from pybrain.datasets            import SupervisedDataSet
from pybrain.utilities           import percentError
from pybrain.tools.shortcuts     import buildNetwork
from pybrain.supervised.trainers import BackpropTrainer
from pybrain.structure.modules   import SoftmaxLayer
from scipy import diag, arange, meshgrid, where
from numpy.random import multivariate_normal


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

    
if __name__ == "__main__":
    nn = BackPropogationNetwork((2500, 1500, 40))

    DB_URI = "mysql+mysqlconnector://{user}:{password}@{host}:{port}/{db}"
 
    engine = create_engine(DB_URI.format(
      user ='root',
      password = '',
      host = '127.0.0.1',
      port = '3306',
      db = 'ca'))
    Base.metadata.create_all(engine)
    Base.metadata.bind = engine
    Session = sessionmaker(bind=engine, autoflush=True)
    db_session = Session()

    row_count = db_session.query(Dataset).count()
    

    SET_MAX = 10000

    shuffled_ids = list(range(row_count))
            
    rnd.shuffle(shuffled_ids)    
    list_of_ids = shuffled_ids[:SET_MAX]
    input_data = []
    target_data = []
    CLASSIFICATIONS = 80

    
    count = 0
    rows = db_session.query(Dataset).filter(Dataset.id.in_(list_of_ids)).all()
    print("Loading " + str(len(rows)) + " data points.")
    count = 0
    train_data = SupervisedDataSet(2500,  CLASSIFICATIONS)
    test_data = SupervisedDataSet(2500, CLASSIFICATIONS)
    for row in rows:
        generation = list(sum(ast.literal_eval(row.initial_generation), ()))
        target = [0] * CLASSIFICATIONS
        target[int(row.generations/50)] = 1
        
        if count < SET_MAX * 0.75:
            train_data.addSample(tuple(generation), int(row.generations/50))
        else: 
            test_data.addSample(tuple(generation), int(row.generations/50))
        count += 1 
    

    fnn = buildNetwork( train_data.indim, 1500, train_data.outdim, bias=True, hiddenclass=SigmoidLayer, outclass=SigmoidLayer)
    fnn.randomize()
    trainer = BackpropTrainer(fnn, dataset = train_data, momentum=0.2, verbose=True, learningrate = 0.001, weightdecay=0.01)
    print("Training network...")
    print("Number of training patterns: ", len(train_data))
    print("Number of training patterns: ", len(test_data))
    print("Input and output dimensions: ", train_data.indim, train_data.outdim)
    

    trueTrain = train_data['target'].argmax(axis=1)  
    trueTest = test_data['target'].argmax(axis=1)

    EPOCHS = 20
    for i in range(EPOCHS):
        trainer.trainEpochs(1)
        outTrain = fnn.activateOnDataset(train_data)
        outTrain = outTrain.argmax(axis=1)
        resTrain = 100 - percentError(outTrain, trueTrain)

        outTest = fnn.activateOnDataset(test_data)
        outTest = outTest.argmax(axis=1)
        resTest = 100 - percentError(outTest, trueTest)

        print("epoch: %4d " % trainer.totalepochs,"\ttrain acc: %5.2f%% " % resTrain, "\ttest acc: %5.2f%%" % resTest)

    with open('nn.pkl', 'wb') as output:
        pickle.dump(fnn, output, pickle.HIGHEST_PROTOCOL)
        pickle.dump(trainer, output, pickle.HIGHEST_PROTOCOL)
