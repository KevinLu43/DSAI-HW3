# DSAI-HW3

### Model Construction
In order to dicide what action should be take, we built the prediction model of consumption and generation.
We combined all the training data into one dataset then divide the data into training set and testing set by following 80/20 rule.
The Gradient Boosting Machine (GBM) was used to constuct the predictive model. 
The results of training and testing were shown below:

|   Training(10-CV)   |   MSE(std.)    |
|---------------------|:-------------  |
|     Consumption     |  0.051(0.02)   |
|     Generation      |  0.023(0.003)  |


---
    
|    Testing   |   MSE(std.)  |   
|--------------|:-------------|
|  Consumption |  0.35(0.05)  |
|  Generation  |  0.13(0.03)  |
  
### Strategy
The comparison showed that the performance of model is acceptable. Therefore the difference between consumption and generation was used to help what action to be taken.
Although the performance of predictive model is quite good, there are still bias between the forecast and the actual value.
The conservative strategy was taken in the agent.

When consumption was more than generation, the strategy is **Buy**, however, we only buy part of the difference. When consumption is less than generation, we only **Sell** part of the difference.
The ratio between different strategy is not the same. 
