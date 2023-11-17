#pip install PyQt5==5.14.2

import cv2
import sys, os
import networkx as nx
import pickle 



def simpleFrame(video_file, frame_number, savepath):    
  # 비디오 캡처 객체 생성
  cap = cv2.VideoCapture(video_file)

  # 특정 프레임 번호

  # 프레임 번호로 이동
  cap.set(cv2.CAP_PROP_POS_FRAMES, frame_number)

  # 비디오 프레임 읽기
  ret, frame = cap.read()

  if ret:
      # 이미지를 화면에 표시
      # cv2.imshow('Frame', frame)
      cv2.imwrite(savepath, frame)
      cv2.waitKey(0)

  # 화면 종료
  cv2.destroyAllWindows()

  # 캡처 객체 해제
  cap.release()





def showNodeBox(video_file, frame_number, savepath, bbox_dict):
  # 비디오 캡처 객체 생성
  cap = cv2.VideoCapture(video_file)
  # 프레임 번호로 이동
  cap.set(cv2.CAP_PROP_POS_FRAMES, frame_number)

  # 비디오 프레임 읽기
  ret, frame = cap.read()

  if ret:
    for fId, bbox_info in bbox_dict.items():
          bbox = bbox_info['bbox']
          name = bbox_info['name']
          xmin, ymin, xmax, ymax = bbox['xmin'], bbox['ymin'], bbox['xmax'], bbox['ymax']
          
          # 박스 그리기
          cv2.rectangle(frame, (xmin, ymin), (xmax, ymax), (0, 255, 0), 2)
          
          # 레이블 추가
          label_text = f"{name} (fId: {fId})"
          label_size, _ = cv2.getTextSize(label_text, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 2)
          cv2.rectangle(frame, (xmin, ymin - label_size[1]), (xmin + label_size[0], ymin), (0, 255, 0), cv2.FILLED)
          cv2.putText(frame, label_text, (xmin, ymin - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2)
    
    # 이미지를 화면에 표시
    cv2.imwrite(savepath, frame)
    cv2.waitKey(0)

    # 화면 종료
    cv2.destroyAllWindows()

  # 캡처 객체 해제
  cap.release()



def main():
  # 비디오 파일 경로
  with open('data/scenegraph/6673828083.json.pkl', 'rb') as f:
      scenegraphs = pickle.load(f)
  frame_number = scenegraphs[2][532]

  video_file = 'data/video/6673828083.mp4'
  # frame_number = 203  # 원하는 프레임 번호로 변경
  queryId = 10

  savepath = 'data/img/query/qId_'+str(queryId)+'_fn'+str(frame_number)+'_originGraph.png'
  filenames = ["query_graph.pkl"]
  
  # key_value_dict = {}
  # for filename in filenames:
  #     with open("data/scenegraph/"+ filename, "rb") as fr:
  #         tmp = pickle.load(fr)
  #         frameIds = tmp[2][0]
  #         for idx, fId in enumerate(frameIds):
  #            key_value_dict[fId] = dict(tmp[0][0][idx].nodes(data=True))

  # showNodeBox(video_file, frame_number, savepath, key_value_dict[frame_number]) # 이미지 내 모든 노드


  with open("data/query_graphs.pkl", "rb") as fr:
      tmp = pickle.load(fr)
      queryG = tmp[queryId]
      qnodeDict = dict(queryG.nodes(data=True))
  
  showNodeBox(video_file, frame_number, savepath, qnodeDict) # 이미지 내 쿼리 그래프 여부



if __name__ == "__main__":
    main()

