import numpy as np
import cv2
import matplotlib.pyplot as plt
import time
from statistics import mode

nrPeople = 40
nrPicturesTrain = 8
resolution = 112 * 92  
image_shape = (112, 92) 
pathDS = r"c:\Users\Rares\Desktop\python labs\ORL"  



def CreateA(pathDS):
    """
    Create a matrix A containing all training images as column vectors.
    Each column corresponds to a vectorized training image.
    """
    A = np.zeros((resolution, nrPeople * nrPicturesTrain))  
    for i in range(1, nrPeople + 1):  
        pathFolder = pathDS + f"/s{i}/"  
        for j in range(1, nrPicturesTrain + 1):  
            pathPhoto = pathFolder + f"{j}.pgm"  
            photo = cv2.imread(pathPhoto, 0)  
            if photo is not None:  
                vectorisedPhoto = photo.reshape(resolution)  
                A[:, (i - 1) * nrPicturesTrain + j - 1] = vectorisedPhoto  
            else:
                print(f"Image {pathPhoto} not found.")  
    print("Dataset shape:", A.shape)  
    return A



def NN(A, testPicture, norm):
    """
    Find the nearest neighbor of the test picture using the specified norm.
    """
    distances = np.zeros(A.shape[1])  
    for i in range(A.shape[1]):  
        
        if norm == 1:
            distances[i] = np.linalg.norm(testPicture - A[:, i], 1)  
        elif norm == 2:
            distances[i] = np.linalg.norm(testPicture - A[:, i], 2)  
        elif norm == 3:
            distances[i] = np.linalg.norm(testPicture - A[:, i], np.inf)  
        elif norm == 4:
            distances[i] = 1 - np.dot(A[:, i], testPicture) / (
                np.linalg.norm(testPicture) * np.linalg.norm(A[:, i])
            )  
    return np.argmin(distances)  


def kNN(A, testPicture, norm, k):
    """
    Find the k nearest neighbors of the test picture and return the most common class.
    """
    testPicture = np.reshape(testPicture, (resolution,)) 
    distances = np.zeros(A.shape[1])  
    if k == 1:  
        return NN(A, testPicture, norm)
    else:
        
        for i in range(len(distances)):
            if norm == 1:
                distances[i] = np.linalg.norm(testPicture - A[:, i], 1)
            elif norm == 2:
                distances[i] = np.linalg.norm(testPicture - A[:, i], 2)
            elif norm == 3:
                distances[i] = np.linalg.norm(testPicture - A[:, i], np.inf)
            elif norm == 4:
                distances[i] = 1 - np.dot(A[:, i], testPicture) / (
                    np.linalg.norm(testPicture) * np.linalg.norm(A[:, i])
                )

        ids = np.argsort(distances)[:k]  
        personId = ids // nrPicturesTrain + 1  
        result = mode(personId)  
    return result

def EF(A, k):                     
    B = A                         
    medie = np.mean(A, axis=1)    
    A = (A.transpose() - medie).transpose()      
    L = np.dot(A.transpose(), A)                
    d, V = np.linalg.eig(L)                     
    idx = np.argsort(d)                         
    idx_k = idx[-1:-k-1:-1]                    
    V = np.dot(A, V)                            
    V = V[:, idx_k]                              
    HQPB = V                                    
    proiectie = np.dot(A.transpose(), V)        
    A = B                                      
    return HQPB, medie, proiectie

def project_test_image(testPicture, medie, HQPB):
    centered_image = testPicture - medie  
    test_projection = np.dot(centered_image, HQPB)  
    return test_projection


def find_closest_image(test_projection, proiectie, nrPicturesTrain):
    distances = np.linalg.norm(proiectie - test_projection, axis=1)  
    closest_index = np.argmin(distances)  
    closest_person = closest_index // nrPicturesTrain + 1  
    closest_image_index = closest_index % nrPicturesTrain + 1 
    return closest_person, closest_image_index, distances[closest_index]



def display(testPicture, A, nn_index, knn_indices, k, image_shape):
    """
    Display the test image, its nearest neighbors, and Eigenfaces visually.
    """
    HQPB, medie, proiectie = EF(A, k)  

    plt.figure(figsize=(12, 4)) 

    # Display test image
    plt.subplot(1, len(knn_indices) + 6, 1)
    plt.imshow(testPicture.reshape(image_shape), cmap="gray")
    plt.title("Test Image")
    plt.axis("off")

    # Display NN match
    plt.subplot(1, len(knn_indices) + 6, 2)
    plt.imshow(A[:, nn_index].reshape(image_shape), cmap="gray")
    plt.title("NN Match")
    plt.axis("off")

    # Display KNN matches
    for i, idx in enumerate(knn_indices):
        plt.subplot(1, len(knn_indices) + 6, i + 3)
        plt.imshow(A[:, idx].reshape(image_shape), cmap="gray")
        plt.title(f"KNN Match {i + 1}")
        plt.axis("off")

    # Display Eigenfaces
    for i in range(k):
        plt.subplot(1, len(knn_indices) + 6, len(knn_indices) + 3 + i)
        plt.imshow(HQPB[:, i].reshape(image_shape), cmap="gray")  
        plt.title(f"Eigenface {i + 1}")
        plt.axis("off")

    plt.show()




def calculateStatistics(A, alg, norm, k=None):
    """
    Calculate recognition rate (RR) and average query time (AQT) for NN or kNN.
    """
    total_time = 0  
    correct_predictions = 0  

    for person_id in range(1, nrPeople + 1):  
        for picture_id in [9, 10]:  
            test_path = f"{pathDS}/s{person_id}/{picture_id}.pgm"  
            test_picture = cv2.imread(test_path, 0)  

            if test_picture is None:  
                print(f"Test image {test_path} not found.")
                continue

            test_picture = test_picture.reshape(resolution)  

            start_time = time.time()  
            if alg == "NN":  
                predicted_index = NN(A, test_picture, norm)
            else:  
                predicted_index = kNN(A, test_picture, norm, k)
            predicted_person = predicted_index // nrPicturesTrain + 1  

            if predicted_person == person_id:  
                correct_predictions += 1

            end_time = time.time()  
            total_time += end_time - start_time  

    RR = correct_predictions / (nrPeople * 2)  
    AQT = total_time / (nrPeople * 2)  
    save_txt(RR, AQT)  
    return RR, AQT



def save_txt(rr, aqt, filename=r"c:\Users\Rares\Desktop\python labs\results.txt"):
    """
    Save the recognition rate (RR) and average query time (AQT) to a text file.
    """
    with open(filename, "a") as file:
        file.write(f"RR: {rr:.4f}, AQT: {aqt:.4f} seconds\n")



A = CreateA(pathDS)


norms = [1, 2, 3, 4]
k = 4


testPerson = int(input("Test person number id: "))
testPicture = int(input("Test picture number: ")) 
testPath = f"{pathDS}/s{testPerson}/{testPicture}.pgm"
testPicture = cv2.imread(testPath, 0)
if testPicture is not None:
    testPicture = np.reshape(testPicture, (resolution,))  
    nn_indices = [NN(A, testPicture, norm) for norm in norms]  
    knn_indices = [
        kNN(A, testPicture, norm, k) if k > 1 else [kNN(A, testPicture, norm, k)]
        for norm in norms
    ]  


    for norm, nn_idx, knn_idx in zip(norms, nn_indices, knn_indices):
        print(f"\nResults for Norm {norm}:")
        print(f"  NN Match Index: {nn_idx}")
        print(f"  kNN Match Indices: {knn_idx}")
        if isinstance(knn_idx, np.int64):  
            knn_idx = [knn_idx]
        display(testPicture, A, nn_idx, knn_idx, k, image_shape)


precision_results = {}
execution_time_results = {}

for norm in norms:
    RR, AQT = calculateStatistics(A, "NN", norm) 
    precision_results[f"NN_norm_{norm}"] = RR
    execution_time_results[f"NN_norm_{norm}"] = AQT
    print(f"NN Norm {norm}: RR = {RR:.4f}, AQT = {AQT:.4f} seconds")

    RR, AQT = calculateStatistics(A, "kNN", norm, k)  
    precision_results[f"kNN_norm_{norm}"] = RR
    execution_time_results[f"kNN_norm_{norm}"] = AQT
    print(f"kNN Norm {norm}: RR = {RR:.4f}, AQT = {AQT:.4f} seconds")


plt.figure(figsize=(10, 5))
plt.plot(norms, [precision_results[f"NN_norm_{norm}"] for norm in norms], label="NN Precision", marker="o")
plt.plot(norms, [precision_results[f"kNN_norm_{norm}"] for norm in norms], label="kNN Precision", marker="o")
plt.xlabel("Norm")
plt.ylabel("Recognition Rate (RR)")
plt.title("Precision Comparison for NN and kNN")
plt.legend()
plt.grid(True)
plt.show()


plt.figure(figsize=(10, 5))
plt.plot(norms, [execution_time_results[f"NN_norm_{norm}"] for norm in norms], label="NN Execution Time", marker="o")
plt.plot(norms, [execution_time_results[f"kNN_norm_{norm}"] for norm in norms], label="kNN Execution Time", marker="o")
plt.xlabel("Norm")
plt.ylabel("Average Query Time (AQT) (seconds)")
plt.title("Execution Time Comparison for NN and kNN")
plt.legend()
plt.grid(True)
plt.show()


