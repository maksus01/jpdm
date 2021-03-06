#!/usr/bin/python

import sys
import random
import itertools
import datetime
sys.path.insert(0, '../util')
import cluster
import read
import dataset
import normalize
import distance
import regression
import util

##############################################################
# Experiment Template
##############################################################

# ------------------------------------------------------------
# RUN EXPERIMENT FOR EVERY POSSIBLE N
# ------------------------------------------------------------

# def experiment1(datasets):

# ------------------------------------------------------------
# PART 1: ECTOR CONFIGURATION (CHOOSING COLUMNS) 
# ------------------------------------------------------------
	# "Manually" configure, or configure with regression:
	# < Put work here -- if desired, use regression to reduce 
	# dimensionality/columns to uniform k>

# ------------------------------------------------------------
# PART 2: CHOOSE NORMALIZATION AND DISTANCE FUNCTIONS
# ------------------------------------------------------------
	# < Put work here >

# ------------------------------------------------------------
# PART 3: RUN -- CHOOSE CLUSTERING ALGORITHM
# ------------------------------------------------------------
	# < Put work here >

# ------------------------------------------------------------
# PART 4: WRITE RESULTS 
# ------------------------------------------------------------
	# Use WriteFile function--- BE THOROUGH FOR GOODNESS SAKE!

##############################################################
##############################################################

# Automatically generates results for every N
# datasets: Sets to be clustered 
# dimensionality: If >0, then set to this value, if <=0 set to maximum valid dimensionality for  this data.
def experiment3(datasets, dimensionality):

	expIndex = "Christopher"

	clusterFileNames=[]
	centerCosts = []
	meanCosts = []

	# First, find the number of examples between all datasets. 
	# This is the maximum number of clusters that can be made.
	maxClusters = 0
	for d in datasets:
		maxClusters+=d.getNumPoints()

	if(dimensionality<1):
		dimensionality = util.getMinDimensionalityAcrossDatasets(datasets)


	# --------------------------------------------------------------------------------------
	# --------------------------------------------------------------------------------------


	# Now, run experiment for every possible number of clusters
	for numClusters in range(1, maxClusters+1):

		# ------------------------------------------------------------
		# PART 1: CHOOSING DATA (columns)
		# ------------------------------------------------------------
		for d in datasets:
			reducedDictionary = regression.getLowerSpace(d.getVectors(), dimensionality)
			d.setReducedDictionary(reducedDictionary, dimensionality)
		
		# ------------------------------------------------------------
		# PART 2: NORMALIZATION AND CHOOSING DISTANCE MEASURE 
		# ------------------------------------------------------------

		###############---VECTOR NORMALIZATION---################

		# At this point, have list of dictionaries of uniform dimensionality. 
		# Each dictionary contains labels mapping to vectors.
		normalizedDictionaries = []
		for d in datasets:
			# print d, "\n"
			# print d
			normalizedDictionaries.append(normalize.normalizeStandardize(d.getReducedVectors())) # THERE ARE ALSO OTHER WAYS TO NORMALIZE

		# ------------------------------------------------------------
		# PART 3: RUN
		# ------------------------------------------------------------
		###################---CLUSTERING---#####################

		# clusterList = [cluster.gonzalez,cluster.lloyds]

		# distanceList = [distance.euclidean,distance.manhattan,distance.infNorm,distance.jaccard,distance.cosine]

		crunchedData = util.crunchDictionaryList(normalizedDictionaries)
		clusterResults  = cluster.lloyds(crunchedData, numClusters, distance.euclidean);

		# ------------------------------------------------------------
		# PART 4: Get costs (if gonzalez or lloyds)
		# ------------------------------------------------------------
		centerCosts.append(cluster.centerCost(crunchedData, clusterResults[0], clusterResults[1], distance.euclidean))
		meanCosts.append(cluster.meanCost(crunchedData, clusterResults[0], clusterResults[1], distance.euclidean))
		
		# ------------------------------------------------------------
		# PART 5: WRITE RESULTS 
		# ------------------------------------------------------------
		##################---STORE RESULTS---####################
		# def writeFile(expIndex, numClusters, clusteringAlgorithmInfo, distanceMeasurementInfo, vectorConfigurationInfo, clusters):
		# Prepare to write experiment file -- fill in the below values for this experiment.

		clusteringAlgorithmInfo = "lloyds"
		distanceMeasurementInfo = "euclidean"
		vectorConfigurationInfo = "{}, {}".format("configured using regression, reduced to dimensionality:", dimensionality)
		clusterFileNames.append(util.writeFile(expIndex, numClusters, clusteringAlgorithmInfo, distanceMeasurementInfo,vectorConfigurationInfo, 
			"Using All columns, using euclidean distatnce for the center costs and mean costs, regression being used is SVD",clusterResults[1]))

	# --------------------------------------------------------------------------------------
	# --------------------------------------------------------------------------------------
	# WRITE COST INFO TO FILE
	util.writeCostFile(expIndex, maxClusters, centerCosts, meanCosts, clusterFileNames)

if __name__ == "__main__":

	#-----------------------------------
	# Read ALL data files.
	reader = read.Read(False) # READS EVERYTHING, and makes dataset objects from each T#.txt file
	# Get data as list of dataset objects.
	datasets = reader.getDataSets() # EVERY DATASET IS NOW AT YOUR DISPOSAL, and indices match dataset titles.
	#-----------------------------------

	copy2 = list(datasets)
	experiment3([copy2[20]],-1)