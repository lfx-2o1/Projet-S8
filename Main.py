import numpy as np
import matplotlib.pyplot as plt
from sklearn import metrics
from Image_reading import read_image
from Color_descriptors import *
from Shape_descriptors import fft_shape
from Texture_descriptors import lbp

from Clustering import clustering_kmeans


if __name__ == '__main__':
    n1=300
    n2=340
    n_clusters_=n2-n1
    color_space='hsv'
    bins=[4,4,4]
    n_colors=8
    distances=[1,4,9]
    n_fft=64
    hist_size_lbp=100
    
    classes_true=[]
    for i in range(0,n2-n1):
        classes_true=classes_true+[i]*3
    classes_true=np.array(classes_true)
    
    X_all=[]
    for i in range(3*(n2-n1)):
        X_all.append([])
    
    for i in range(n2-n1):
        for j in range(3):
            X=read_image(i+n1,j)
            # ********************Color_features***********************
            moments_ftr=moments_calcul(X,color_space)
            X_all[3*i+j]=X_all[3*i+j]+[moments_ftr]
            
            hist= color_histogram(X,color_space,bins)
            # hist=histogram_filter(hist)
            # hist=histogram_normalization(hist)
            X_all[3*i+j]=X_all[3*i+j]+[hist]
            
            """
            # ********************Shape_features***********************
            shape_fft=fft_shape(X,n_fft)
            X_all[3*i+j]=X_all[3*i+j]+[shape_fft]
            
            """
            # ********************Texture_features***********************
            lbp_feature=lbp(X,hist_size_lbp)
            X_all[3*i+j]=X_all[3*i+j]+[lbp_feature]
            
            
            
            X_all[3*i+j]=np.concatenate(X_all[3*i+j])
    
    X_all=np.array(X_all).astype(float)
    print("Number of images= "+ str(X_all.shape[0]))
    print("Number of features= "+ str(X_all.shape[1]))
    
    # ********************Clustering************************
    classes=clustering_kmeans(X_all,n_clusters_)
    
    
    print("**************Clustering_results*********************")
    print('adjusted_rand_score=%0.2f' % metrics.adjusted_rand_score(classes_true,classes))
    # print('normalized_mutual_info_score=%0.2f' % metrics.normalized_mutual_info_score(classes_true,classes))
    print('homogeneity_score=%0.2f' % metrics.homogeneity_score(classes_true,classes))
    print('completeness_score=%0.2f' % metrics.completeness_score(classes_true,classes))
    print('v_measure_score=%0.2f' % metrics.v_measure_score(classes_true,classes))
    print('fowlkes_mallows_score=%0.2f' % metrics.fowlkes_mallows_score(classes_true,classes))
    print("\n")
