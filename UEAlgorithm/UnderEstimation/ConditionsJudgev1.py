#!/usr/bin/python  
# -*- coding: utf-8 -*- 
'''
Created on 2014-5-5

@author: qcq
'''
import numpy as np
import math
import random

def ConditionOne(matrix):
    '''
    This function used for compute if the matrix comply to the Condition One
    
    parameters:
        matrix: the input matrix, which should be a squre matrix N * N
        
    return:
        boolean: if matrix comply to Condition One, then return True, otherwise False 
    '''
    #copy the matrix to temporary matrix in order to not change the original matrix
    temporary_matrix = matrix.copy()
    #sort the temporary matrix by column, 
    temporary_matrix.sort(axis = 0)
    #get the diagonal items to form a vector
    diagonal_vector = matrix.diagonal()
    #get the second small items in the temporary matrix to form a vector
    second_small_vector = temporary_matrix[1:2,]
    #judge if the diagonal vector's items less than the second small vector
    #===========================================================================
    #The reason to deal vector like this is because, In every column of matrix 
    #may be have two or more items are smallest items. So, if compare the smallest items formed
    #vector with diagonal items formed vector can occur the problem in which the diagonal
    #items formed vector is not the only smallest items in every column
    #用上述的第二小元素组成的向量参与比较是为了防止在矩阵的每一列之中有两个相同的极小值，从而达不到对角线元素组成的向量之中的元素是
    #矩阵每一列之中唯一的最小值
    #===========================================================================
     
    compare_vector = (diagonal_vector < second_small_vector) 
               
    return compare_vector.all()

def ConditionTwo(matrix, support_vector):
    '''
    This function used for compute if the matrix comply to the Condition Two
    
    parameters:
        matrix: the input matrix, which should be a squre matrix N * N
        support_vector: the computed support vector 1 * N
        
    return:
        boolean: if matrix comply to Condition Two, then return True, otherwise False 
    '''
    #get the diagonal items to form a vector
    diagonal_vector = matrix.diagonal()
    compare_vector = (diagonal_vector >= support_vector)
    
    return compare_vector.all()

def IsRegion(matrix, convertedusr_vector):
    '''
    This function used for judging if the convertedusr_vector within region of the
    matrix
    
    parameters:
        matrix: the input matrix, which should be a squre matrix N * N
        convertedusr_vector: The input usr-convert vector 1 * N
        
    return:
        boolean: if element contains in matrix, then return True, otherwise False 
    '''
    flag = True
    #i is the column of the matrix
    #j is the row of the matrix
    for i in range(matrix.shape[1]):
        for j in range(matrix.shape[0]):
            if i != j:
                xjj = matrix[j, j]
                xi = convertedusr_vector[0, i]
                xj = convertedusr_vector[0, j]
                xji = matrix[j, i]
                if xjj * xi <= xji * xj:
                    flag = False
                    
    return flag

def EstimatedValue(matrix, convertedusr_vector, M):
    '''
    This function used for get the estimated value of the protein
    
    parameters:
        matrix: the input matrix, which should be a squre matrix N * N
        convertedusr_vector: The input usr-convert vector 1 * N
        M: The setted M value, which setted by user
        
    return:
        float: return the estimated value
    '''
    #i is the row of the matrix
    #j is the column of the matrix
    max_temp_vector = []
    for i in range(matrix.shape[0]):
        min_temp_vector = []
        for j in range(matrix.shape[1]):
            min_temp_vector.append(matrix[i, j] * convertedusr_vector[0, i])
        #get the miniature value of the list
        max_temp_vector.append = min(min_temp_vector)
    #get the maximum value of the list
    estimate_value = max(max_temp_vector)
    
    return estimate_value - M

def MatrixReplace(matrix, support_vector):
    '''
    This function used for replace one column of the matrix with the support_vector
    
    parameters:
        matrix: the input matrix, which should be a squre matrix N * N
        support_vector: the computed support vector 1 * N
        
    retrun:
        list: return one list contains matrices which each row replacement by support_vector
                once
    '''
    
    result_matrix = []
    for i in range(matrix.shape[0]):
        #used the copied one, in order to keep the original matrix
        temp_matrix = matrix.copy()
        #let the matrix's i row equals support_vector
        temp_matrix[i,:] = support_vector
        result_matrix.append(temp_matrix)
        
    return result_matrix

def ConvertUsr(usr, usr_bound):
    '''
    This function convert usr list to convertedusr_vector
    
    parameters:
        usr: the input usr, which is a list contains muti-dimensional data of one protein
        usr_bound: this is a list, which items are tuple, in which contains every dimension
                    's lower and upper bound
                    
    return:
        matrix: return a matrix(vector) which is converted usr vector
    '''
    bound_sum = 0.0
    #initial the convertedusr_vector to 1 * (len(usr) + 1)
    convertedusr_vector = np.zeros((1, len(usr) + 1))
    for i in usr_bound:
        bound_sum = bound_sum + (i[1] - i[0])    
    for i, bound in zip(range(len(usr)), usr_bound):
        convertedusr_vector[0, i] = (usr[i] - bound[0]) * 1.0 / bound_sum
    #the last element of convertedusr_vector is the sum of the elements before this element.
    convertedusr_vector[0, len(usr)] = 1 - convertedusr_vector[:,:-1].sum(axis = 1)[0, 0]
    
    return convertedusr_vector
 
def SupportVector(energy, convertedusr_vector, M):
    '''
    This function used for computing the support vector
    
    parameters:
        energy: the protein energy calculated by the score function
        convertedusr_vector: the usr converted vector 1 * N
        M: The setted M value, which setted by user 
        
    return:
        matrix: return support matrix(vector)
    '''
    #initial the support vector
    support_vector = np.zeros((1, max(convertedusr_vector.shape)))
    temp_energy = energy + M
    for i in range(max(convertedusr_vector.shape)):
        support_vector[0, i] = temp_energy * 1.0 / convertedusr_vector[0, i]
    
    return support_vector
        
    
    