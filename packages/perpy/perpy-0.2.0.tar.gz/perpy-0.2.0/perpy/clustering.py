import perpy as py
import copy
import numpy as np
from sklearn import metrics as mt
from munkres import Munkres,print_matrix


def mini_map(labels_true, labels_pred):
    '''
    Example:
        a = [0,1,2], b = [1,2,3]
        a,b = mini_map(a,b)
        a = [0,1,2], b = [0,1,2]

    :param labels_true:
    :param labels_pred:
    :return:
    '''
    labels_true = np.array(labels_true)
    labels_pred = np.array(labels_pred)
    bias1 = min(labels_true)
    labels_true -= bias1
    bias2 = min(labels_pred)
    labels_pred -= bias2

    return labels_true, labels_pred

def best_map(L1,L2):
    L1 = np.array(L1)
    L2 = np.array(L2)
    #L1 should be the labels and L2 should be the clustering number we got
    Label1 = np.unique(L1)       # 去除重复的元素，由小大大排列
    nClass1 = len(Label1)        # 标签的大小
    Label2 = np.unique(L2)
    nClass2 = len(Label2)
    nClass = np.maximum(nClass1,nClass2)
    G = np.zeros((nClass,nClass))
    for i in range(nClass1):
        ind_cla1 = L1 == Label1[i]
        ind_cla1 = ind_cla1.astype(float)
        for j in range(nClass2):
            ind_cla2 = L2 == Label2[j]
            ind_cla2 = ind_cla2.astype(float)
            G[i,j] = np.sum(ind_cla2 * ind_cla1)
    m = Munkres()
    index = m.compute(-G.T)
    index = np.array(index)
    c = index[:,1]
    newL2 = np.zeros(L2.shape)
    for i in range(nClass2):
        newL2[L2 == Label2[i]] = Label1[c[i]]
    return newL2

def NMI(labels_true, labels_pred):
    labels_true, labels_pred = mini_map(labels_true, labels_pred)
    labels_pred = best_map(labels_true, labels_pred)

    return mt.normalized_mutual_info_score(labels_true, labels_pred)

def ARI(labels_true, labels_pred):
    labels_true, labels_pred = mini_map(labels_true, labels_pred)
    labels_pred = best_map(labels_true, labels_pred)

    return mt.adjusted_rand_score(labels_true, labels_pred)

def ACC(labels_true, labels_pred):
    labels_true, labels_pred = mini_map(labels_true, labels_pred)
    labels_pred = best_map(labels_true, labels_pred)

    return mt.accuracy_score(labels_true, labels_pred)

def AMI(labels_true, labels_pred):
    labels_true, labels_pred = mini_map(labels_true, labels_pred)
    labels_pred = best_map(labels_true, labels_pred)

    return mt.adjusted_mutual_info_score(labels_true, labels_pred)

def Completeness(labels_true, labels_pred):
    labels_true, labels_pred = mini_map(labels_true, labels_pred)
    labels_pred = best_map(labels_true, labels_pred)

    return mt.completeness_score(labels_true, labels_pred)

def Homogeneity(labels_true, labels_pred):
    labels_true, labels_pred = mini_map(labels_true, labels_pred)
    labels_pred = best_map(labels_true, labels_pred)

    return mt.homogeneity_score(labels_true, labels_pred)

def k_means(x, k, max_iterations=None):
    num_x = x.shape[0]
    num_feature = x.shape[1]
    index = np.random.choice(np.arange(num_x), size=k, replace=False)
    centers = x[index]
    labels = np.zeros(num_x)

    if max_iterations is None:
        while True:
            centers_old = copy.deepcopy(centers)

            for i in range(num_x):
                min_value = 999
                for j in range(k):
                    if py.dist(x[i], centers[j]) < min_value:
                        min_value = py.dist(x[i], centers[j])
                        labels[i] = j

            for i in range(k):
                for d in range(num_feature):
                    sum_value = 0.0
                    count = 0
                    for j in range(num_x):
                        if labels[j] == i:
                            sum_value += x[j, d]
                            count += 1
                    mean = sum_value / count
                    centers[i, d] = mean
            if centers.all() == centers_old.all():
                break

    else:
        for i in range(max_iterations):
            centers_old = copy.deepcopy(centers)

            for i in range(num_x):
                min_value = 999
                for j in range(k):
                    if py.dist(x[i], centers[j]) < min_value:
                        min_value = py.dist(x[i], centers[j])
                        labels[i] = j

            for i in range(k):
                for d in range(num_feature):
                    sum_value = 0.0
                    count = 0
                    for j in range(num_x):
                        if labels[j] == i:
                            sum_value += x[j, d]
                            count += 1
                    mean = sum_value / count
                    centers[i, d] = mean
            if centers.all() == centers_old.all():
                break

    return labels, centers