# SET UP SPARK
import findspark

findspark.init()

from pyspark import SparkContext, SparkConf
from pyspark.sql import SparkSession

config = SparkConf().setMaster("local").setAppName("SparkML_FinalProject")
sc = SparkContext(conf=config)
spark = SparkSession(sc)

# LOAD AND CLEAN DATA SET
import os.path

baseDir = os.path.join('C:/', 'Users', 'llsch', 'Documents', 'Classes', 'ML in Spark')
fileName = 'default of credit card clients1.csv'
filePath = os.path.join(baseDir, fileName)

print("loading data...")
rawRDD = sc.textFile(filePath)
print("parsing data...")
parsedRDD = rawRDD.map(lambda line: line.split(","))
print("removing headers...")
Xheaders = parsedRDD.first()
NoXHeaderRDD = parsedRDD.filter(lambda row: row != Xheaders)
StrHeaders = NoXHeaderRDD.first()
NoHeadersRDD = NoXHeaderRDD.filter(lambda row: row != StrHeaders)

# TRANSFORM INTO LABELED POINTS WITH DENSE VECTOR OF FEATURES
from pyspark.ml.linalg import Vectors

print("transforming data into labels and features...")
TargetRDD = NoHeadersRDD.map(lambda x: (float(x[24]), Vectors.dense(x[0:23])))

# SPLIT DATA INTO TRAINING AND TEST
print("splitting data into training and test sets...")
weights = [.7, .3]
seed = 42
TrainData, TestData = TargetRDD.randomSplit(weights, seed)

nTrain = TrainData.count()
nTest = TestData.count()
print("nTrain", nTrain, "nTest", nTest, "total", nTrain + nTest)
TrainingDF = TrainData.toDF(['label', 'features'])
print("A sample of the training set:")
TrainingDF.show()

# LEARN MODEL
print("learning model...")
from pyspark.ml.classification import LogisticRegression

lr = LogisticRegression(featuresCol='features', labelCol='label', maxIter=50, regParam=0.3, family='binomial')
lrModel = lr.fit(TrainingDF)

print("Coefficients: " + str(lrModel.coefficients))
print("Intercept: " + str(lrModel.intercept))

trainingSummary = lrModel.summary

accuracy = trainingSummary.accuracy
print("The accuracy, the total num correctly classified instances out of total instances, of the model is:", accuracy)
fMeasure = trainingSummary.fMeasureByLabel()
print("The F-Measure for each label in the model is:", fMeasure)
trainingIter = trainingSummary.totalIterations
print("The number of training iterations is:", trainingIter)

# EVALUATE MODEL
print("evaluating the model on test data...")
TestDF = TestData.toDF(['label', 'features'])
predictions = lrModel.transform(TestDF)
print("A sample of the test predictions:")
predictions.show(5)

from pyspark.ml.evaluation import BinaryClassificationEvaluator

evaluator = BinaryClassificationEvaluator(rawPredictionCol="rawPrediction")
print("The area under the ROC curve is:", evaluator.evaluate(predictions))
print("The closer to 1, the better, and the closer to 0, the worse the model performs at accurate classification.")
