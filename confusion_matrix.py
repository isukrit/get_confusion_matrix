def get_confusion_matrix(true_labels, pred_labels):
	#print (true_labels, pred_labels)
	print ('true_labels', true_labels, 'pred_labels', pred_labels)
	new_labels_true, true_labels, pred_labels =  np.array(true_labels[:]), np.array(true_labels), np.array(pred_labels) 
	num_labels_true = int(np.max(true_labels) - np.min(true_labels) + 1)
	num_labels_pred = int(np.max(pred_labels) - np.min(pred_labels) + 1)
	num_samples = true_labels.size
	
	all_matches = np.zeros((num_labels_pred, num_labels_true))

	labels_taken = np.zeros(num_labels_pred) #set to 1 if a pred label is already used
	for label_true in range(num_labels_true):
		best_match = 0
		print (num_labels_pred, num_labels_true)
		for label_pred in range(num_labels_pred):
			match = calculate_matches(true_labels, label_true, pred_labels, label_pred)
			all_matches[label_pred][label_true] = match

	label_mapping, max_matches = find_best_match(all_matches)

	label_positions_in_pred = np.zeros((num_labels_true, num_samples))

	for label, new_label in enumerate(label_mapping): #cannot change labels at once since the label names may clash
		labels = np.where(true_labels == label)[0]
		label_positions_in_pred[label][labels] = 1

	for label, new_label in enumerate(label_mapping): #cannot change labels at once since the label names may clash
		labels = np.where(label_positions_in_pred[label] == 1)[0]
		new_labels_true[labels] = new_label

	confusion_matrix = metrics.confusion_matrix(new_labels_true, pred_labels, labels= range(num_labels_true))
	print ('Confusion Matrix:',  confusion_matrix.shape, confusion_matrix)
	return confusion_matrix
  
def calculate_matches(true_labels, label_true, pred_labels, label_pred):
	module_labels_true, module_labels_pred = true_labels[:], pred_labels[:]
	
	pred_match_labels = np.where(module_labels_pred == label_pred)[0]
	true_match_labels = np.where(module_labels_true == label_true)[0]


	matches = np.intersect1d(pred_match_labels, true_match_labels).size
	#print (matches)
	return matches

def find_best_match(all_matches):
	num_labels_pred, num_labels_true = all_matches.shape[0], all_matches.shape[1]
	labels_to_assign = range(num_labels_true)
	max_matches = np.zeros(num_labels_true)
	label_mapping = np.zeros(num_labels_true) #index is the label_true and value is the correspoding label from pred_labels with highest matches

	while len(labels_to_assign) > 0:
		for l_true in labels_to_assign:
			max_in_l_true = np.max(all_matches[:, l_true])
			label_max_in_l_true = np.where(all_matches[:, l_true] == max_in_l_true)[0][0]
			
			max_in_l_pred = np.max(all_matches[label_max_in_l_true, :])
			label_max_in_l_pred = np.where(all_matches[label_max_in_l_true, :] == max_in_l_pred)[0][0]

			print ('all_matches', all_matches, all_matches.shape, 'l_true', l_true, 'max_in_l_true', max_in_l_true, 'max_in_l_pred', max_in_l_pred,  'label_max_in_l_true', label_max_in_l_true)

			if max_in_l_pred == max_in_l_true:
				
				label_mapping[l_true] = label_max_in_l_true
				max_matches [l_true] = max_in_l_true
				all_matches[label_max_in_l_true, :] = 0
				all_matches[:, l_true] = 0
				labels_to_assign = np.setdiff1d(labels_to_assign, np.array(l_true))
				#print ('***************************** l_true ***************************************', l_true, 'label_mapping', label_mapping, 'max_matches', max_matches )
				break

	
	print ('label_mapping', label_mapping, 'max_matches', max_matches)
	
	return label_mapping, max_matches


