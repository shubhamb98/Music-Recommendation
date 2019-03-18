from pyspark.ml.recommendation import ALS
from pyspark.ml.evaluation import RegressionEvaluator

# Let's initialize our ALS learner
als = ALS()

# Now set the parameters for the method
als.setMaxIter(5)\
   .setSeed(seed)\
   .setItemCol("new_songId")\
   .setRatingCol("Plays")\
   .setUserCol("new_userId")

# Now let's compute an evaluation metric for our test dataset
# We Create an RMSE evaluator using the label and predicted columns
reg_eval = RegressionEvaluator(predictionCol="prediction", labelCol="Plays", metricName="rmse")

tolerance = 0.03
ranks = [4, 8, 12, 16]
regParams = [0.15, 0.2, 0.25]
errors = [[0]*len(ranks)]*len(regParams)
models = [[0]*len(ranks)]*len(regParams)
err = 0
min_error = float('inf')
best_rank = -1
i = 0
for regParam in regParams:
  j = 0
  for rank in ranks:
    # Set the rank here:
    als.setParams(rank = rank, regParam = regParam)
    # Create the model with these parameters.
    model = als.fit(training_df)
    # Run the model to create a prediction. Predict against the validation_df.
    predict_df = model.transform(validation_df)

    # Remove NaN values from prediction (due to SPARK-14489)
    predicted_plays_df = predict_df.filter(predict_df.prediction != float('nan'))
    predicted_plays_df = predicted_plays_df.withColumn("prediction", F.abs(F.round(predicted_plays_df["prediction"],0)))
    # Run the previously created RMSE evaluator, reg_eval, on the predicted_ratings_df DataFrame
    error = reg_eval.evaluate(predicted_plays_df)
    errors[i][j] = error
    models[i][j] = model
    print ('For rank %s, regularization parameter %s the RMSE is %s' % (rank, regParam, error))
    if error < min_error:
      min_error = error
      best_params = [i,j]
    j += 1
  i += 1

als.setRegParam(regParams[best_params[0]])
als.setRank(ranks[best_params[1]])
print ('The best model was trained with regularization parameter %s' % regParams[best_params[0]])
print ('The best model was trained with rank %s' % ranks[best_params[1]])
my_model = models[best_params[0]][best_params[1]]