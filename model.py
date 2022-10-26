
import cv2
import numpy as np
import box_utils_numpy as box_utils

#Yuz tespiti icin tahmin yapan fonksiyon
def predict(width, height, confidences, boxes, prob_threshold, iou_threshold=0.3, top_k=-1):
    boxes = boxes[0]
    confidences = confidences[0]
    picked_box_probs = []
    picked_labels = []
    for class_index in range(1, confidences.shape[1]):
        probs = confidences[:, class_index]
        mask = probs > prob_threshold
        probs = probs[mask]
        if probs.shape[0] == 0:
            continue
        subset_boxes = boxes[mask, :]
        box_probs = np.concatenate([subset_boxes, probs.reshape(-1, 1)], axis=1)
        box_probs = box_utils.hard_nms(box_probs,
                                       iou_threshold=iou_threshold,
                                       top_k=top_k,
                                       )
        picked_box_probs.append(box_probs)
        picked_labels.extend([class_index] * box_probs.shape[0])
    if not picked_box_probs:
        return np.array([]), np.array([]), np.array([])
    picked_box_probs = np.concatenate(picked_box_probs)
    picked_box_probs[:, 0] *= width
    picked_box_probs[:, 1] *= height
    picked_box_probs[:, 2] *= width
    picked_box_probs[:, 3] *= height
    return picked_box_probs[:, :4].astype(np.int32), np.array(picked_labels), picked_box_probs[:, 4]


#Bu fonksiyon verilen pathdteki resimden yuzu kirpar ve bu yuzleri kaydeder.
def detectAndSaveFace(orig_image_path):
    fileNumber = 0
    threshold = 0.7
    image = cv2.cvtColor(orig_image, cv2.COLOR_BGR2RGB)
    image = cv2.resize(image, (320, 240))
    # image = cv2.resize(image, (640, 480))
    image_mean = np.array([127, 127, 127])
    image = (image - image_mean) / 128
    image = np.transpose(image, [2, 0, 1])
    image = np.expand_dims(image, axis=0)
    image = image.astype(np.float32)
    confidences, boxes = ort_session.run(None, {input_name: image})
    
    boxes, labels, probs = predict(orig_image.shape[1], orig_image.shape[0], confidences, boxes, threshold)
    for i in range(boxes.shape[0]):
        box = boxes[i, :]
        imageName = orig_image_path.split("/")[-1]
        cv2.imwrite(savePath + imageName, orig_image[box[1]: box[3],box[0]: box[2]])
        fileNumber += 1

#Bu fonksiyon verilen pathlerdeki yuzleri birbirleriyle kiyaslar. Benzerlik tespit edilirse tespit edilen resimler bir diziye eklenir ve bu dizi return edilir.
def detectAllFaces(hedef_path, image_path):
    isFounded = False
    print("+")
   
    threshold = 0.7
    compareScore = 0
    gelenResim = cv2.imread(image_path)
    image = cv2.cvtColor(gelenResim, cv2.COLOR_BGR2RGB)
    image = cv2.resize(image, (320, 240))
    
    image_mean = np.array([127, 127, 127])
    image = (image - image_mean) / 128
    image = np.transpose(image, [2, 0, 1])
    image = np.expand_dims(image, axis=0)
    image = image.astype(np.float32)
    confidences, boxes = ort_session.run(None, {input_name: image})
    boxes, labels, probs = predict(gelenResim.shape[1], gelenResim.shape[0], confidences, boxes, threshold)
    image_list = []
    
    for i in range(boxes.shape[0]):
        foundFaceOnImage = False
        box = boxes[i, :]
        last_image = gelenResim[box[1]: box[3], box[0]: box[2]]
        lastImageVector = vector.makeMeVector(last_image, vector.mean)
        isFounded = True
        for i in range(len(hedef_path)):
            hedefVector = vector.makeMeVector(cv2.imread(hedef_path[i]), vector.mean)
            compareScore = vector.compare2Vectors(hedefVector, lastImageVector)
            if compareScore < 0.4:
                if not foundFaceOnImage:
                    cv2.rectangle(gelenResim, (box[0], box[1]), (box[2], box[3]), (0, 255, 0), 4)
                
            else:
                foundFaceOnImage = True
                cv2.rectangle(gelenResim, (box[0], box[1]), (box[2], box[3]), (0, 0, 255), 4)
                cv2.putText(gelenResim, hedef_path[i].split('/')[-1].split('.')[0] + "-" +str(compareScore),
                        (box[0] + 20, box[1] + 40),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        1,  # font scale 
                        (0, 0, 255),
                        2)
                
            image_list.append(gelenResim)
   
    return isFounded, gelenResim

        


            