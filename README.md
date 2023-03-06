# Project 2: Cellular Throughput Prediction

## UPDATE: added new operators and traces
New operator: `Divide` and `LatestEventToState` (see the updated documentation for details)

New traces: can be found in the trace folder

## 1. Your Task

<img width="420" alt="image" src="https://user-images.githubusercontent.com/25103655/219903829-cdb5560f-5182-47a8-8bbb-84963c471b57.png">
In this project, you need to develop a predictor for cellular network throughput.

The input data can be found in `training_data/` folder. 
Each trace is a json file consists with hundreds of records with the following fields
![image](https://user-images.githubusercontent.com/25103655/219903744-12f03991-1bee-4052-ac1e-5d5b3fcc3681.png)

During the testing, you will see all the fields **EXCEPT** the ground truth throughput. You need to generate your own prediction.



## 2. Installation and dependencies
<img width="843" alt="image" src="https://user-images.githubusercontent.com/25103655/219903870-0816e80c-c351-4b8a-8ea4-260b8cb17504.png">

## 3. Running the prototype

<img width="835" alt="image" src="https://user-images.githubusercontent.com/25103655/219903886-8ff23d82-04e7-48ec-889c-f261e43218fc.png">


## 4. Overview of the tool
<img width="915" alt="image" src="https://user-images.githubusercontent.com/25103655/219904008-6039dbfd-c087-4e47-b3dc-3a0e48467c67.png">

## 5. Detailed doumentation
For the detailed documentation, please refer to [documentation.pdf](../master/doc/documentation.pdf) or [documentation.pptx](../master/doc/documentation.pptx)

## 5. Notes

- The testing traces will be available in a few days
- If you have any questions or want to extend the operator list, please contact Yihua Cheng (yihua98@uchicago.edu)
