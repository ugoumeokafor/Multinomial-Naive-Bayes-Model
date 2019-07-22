# Multinomial-Naive-Bayes-Model
The training dataset contains 80% records randomly selected from the dataset while remaining 20% were used for testing. The training dataset contains attributes like usernames, date and time, longitude, and latitude and country codes of countries where the photos were uploaded. For example, if we want to train the classifier for users who uploaded photos in the United Kingdom (country code 206), we count all the users who have feature 206 in their trajectory and mark them as “visited_206”, we use the features before 206 as the training features. In the same way, all the users who have no feature 206 will be marked as “no visit to_206” and all the features in their trajectory used as training features for not visiting 206. The trained model produced prior probabilities and likelihood probabilities of visiting and not visiting 206 respectively. The two probabilities will be used to calculate the posterior probability in the test dataset. An example is shown below.
To compute prior probabilities for a feature belonging to class A, we use Equation 3,

P(A) =  (∑ V)/U
			
P(A) is the prior probability of features belonging to class A. ∑V is the sum of the count of features that belong to class A. U is the size of the document.
We also calculated the prior probabilities for a feature not belonging to class A using Equation 4,
P(notA) =  (∑ V)/U
P(notA) is the prior probability of a feature not belonging to class A. ∑V is the sum of the count of features not belonging to a class. U is the size of the document. 
To compute the likelihood probabilities of features (in this case B) belonging to a class A and likelihood probabilities of features not belonging to class A, we use Equations 5 and 6 below.
P(B/A) =  (∑ C)/(∑ D +∑ E)
Equation 5 is used to calculate the likelihood probability of feature B in class A, i.e., P(B/A). ∑C  is the sum of the count of occurrence of feature B in class A. Then ∑D is the sum of count of features B before feature A while  ∑E is the sum of number of unique features in the dataset.

P〖(B/no〗_A) =  (∑  C_notA)/(∑ D_notA  +∑E)

Equation 6 is used to calculate the likelihood of feature B not belonging to class A, i.e., P(B/notA). ∑ C_notA  is the count of occurrence where features B does not belong to class A, ∑ D_notA is the count of occurrence where feature A is not in the trajectory while  ∑E is the sum of number of unique features in the dataset. 
We demonstrate a simple worked example from Table 2, using country code 206 as an example.
Table 2. Sample training data
User_id	Countries visited
10006374@N03	{119,23}
10014738@N05	{238,85,206}
10016029@N04	{81,206}
10017016@N03	{64,85}
10017201@N02	{85,23}
10017367@N03	{50,206,71,85}
100460312@N04	{71,206}
10019779@N00	{82,185,187}

Prior probabilities of features belonging to class 206 and not belonging to class 206, using Equation 3, 
P(206) = 4/8 = 0.5 ≈ 50%. 
For the probability of not belonging to 206, using Equation 4, 
P(N206) = 4/8  = 0.5 ≈ 50%. 
For all the features in the training dataset, to calculate the likelihood probabilities of features belonging to class 206, using Equation 5, 
P(119|206)=(0+1)/(5+12) = 1/17 , P(23|206) = (0+1)/(5+12) = 1/17 etc., when a particular feature does not appear in a document, its conditional probability is equal to 0, to avoid this problem, we use add-one or Laplace smoothing by adding 1. 
To calculate the likelihood probabilities of features not belonging to class 206, using Equation 6, 
P(119|N206) = (1+1)/(9+12) = 2/21, P(23|N206) = (2+1)/(9+12) = 3/21 etc, again we added Laplace smoothing by adding 1.
As shown, the trained model produced four probabilities, two prior probabilities and two likelihood probabilities for user 1 with two features (119 & 23).

3.2.2 Testing 
We used the remaining 20% of our dataset as test data. We used the results from the training set to calculate the posterior probability and then used the selected posterior probability to test the accuracy of the model. We did this using Equations 7, 8, 9 and 10.
P(A/B) ∝ P(A) x P(B/A) 
P(Anot/B) ∝ P(Anot) x P(B/Anot) 
      Equations 6 and 7 are varying the proportionality over A for a given B.
                 (9)
           (10)
Using Equations 9 and 10, for each user in the test dataset, we calculated the posterior probabilities of belonging to class 206 and posterior probability of not belonging to class 206 respectively and compare it to the actual travel history of each user to check the accuracy of our model.  Equations 9 and 10 is a combination of priors and likelihood probabilities from Equations 7 and 8 respectively. 
For our prediction, we compare the two posterior probabilities; the highest probability is used to classify a user to either belonging to class 206 or not belonging to class 206. The same steps will be repeated for all the classes and users in the dataset.
Again, we demonstrate a simple worked example from Table 3, using country code 206 as an example.
Table 3 Sample testing data
User_id	Countries visited
10020416@N06	{153,23,206}
100212960@N05	{82,185,50}
10021381@N05	{50,153,206}
10022497@N03	{81,71,85}

For user 1 in the test dataset, the posterior probabilities of belonging and not belonging to class 206 is given as; 
P(206|test) α  4/8 * 1/17 = 4/136
P(N206|test)  α  4/8 * 3/21 = 12/168
P(206|test) =  ( 4/136  )/((4/136  + 12/168) )=0.292 ≈ 29%
P(N206|test) = (12/168  )/((12/168  + 4/136) )=0.71 ≈ 71%
From the example above, given the trajectory of user1, it shows that the user belongs to class 206 which is the truth, but our model predicts that there is only a 29% probability of the user being classified to class 206 and there is a 71% probability of the user not being classified to class 206. The poor accuracy of the prediction is because we trained the model on only two features. We are only using this example as an illustration of how the Multinomial Naïve Bayes classifier works in document classification. 

