# get_confusion_matrix
Give two python lists containing labels as inputs and find the most likely confusion matrix for them.

Often, it so happens that we have results from 2 clustering algorithms on the same data, but with different labels. 
We want to calculate the confusion matrix (and indices like accuracy, specificity, sensitivity, et cetera) for these, but we do not know the correspondence between the labels.

This repo will contain functions which will calculate those indices for you. You MUST have scikit and numpy installed for this to work.

Thanks!
