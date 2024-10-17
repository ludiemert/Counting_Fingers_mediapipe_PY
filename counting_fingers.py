
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'  # Suprimir avisos do TensorFlow Lite
os.environ["PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION"] = "python"  # Suprimir aviso do protobuf

import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'  # Suprimir todos os avisos do TensorFlow (INFO e WARNING)

import warnings
warnings.filterwarnings("ignore", category=UserWarning, module='google.protobuf')  # Suprimir avisos de UserWarning relacionados ao protobuf


import cv2
import mediapipe as mp

video = cv2.VideoCapture(0)

#variaveis
hand = mp.solutions.hands #mapeamento das maos, variavel
Hand = hand.Hands(max_num_hands=1) #vamos usar 1 mao para o proj, variavel resp p fazer a detec dentro do video
mpDraw = mp.solutions.drawing_utils  #variavel resp por fazer as ligacoes dos dedos na mao (draw)

#usar a webcan mao esquerda
while True:
    check,img = video.read()
    imgRGB = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)  #converter a img da camera para usar a mediappe
    results = Hand.process(imgRGB)  #processar a img com o mediapipe
    handsPoints = results.multi_hand_landmarks  #extrair resultados, os pontos das maoes
    h,w,_ = img.shape   #converter os valores p pixels, extraindo as dimensoes da img
    pontos = []  #array dos pontos

    # retornar as coordenadas para cada ponto
    if handsPoints:
        for points in handsPoints:
            #print(points)
            mpDraw.draw_landmarks(img,points,hand.HAND_CONNECTIONS) #desenhar os pontos dentro da img
            for id,cord in enumerate(points.landmark):    #logica que vai enumerar os pontos da mao
                cx, cy = int(cord.x*w), int(cord.y*h)
                #cv2.putText(img,str(id),(cx,cy+10),cv2.FONT_HERSHEY_SIMPLEX,0.5,(255,0,0),2)   #ver funcionar
                pontos.append((cx,cy))   #incrementar valor a cada frame, cx e cy as coordenadas
                #print(pontos)#retorna o array todos os frames dos pontos da mao

    fingers = [8,12,16,20]     #array => upper fingers - dedos superiores, menos o dedao logica diferente
    contador = 0 #inicia contador com valor 0
    if pontos:  #so vai executar se a variavel nao estiver vazia
        if pontos[4][0] < pontos[2][0]:    #logica para o dedao - thumb posicao 4, pega eixo x 0 (que vai dar essa informacao)  e nao y, [2]2 pontos abaixo do ponto 4 para x 0
            contador +=1  #se for verdadeira +1num
        for x in fingers: #loop percorre todos os pontos
            if pontos[x][1] < pontos[x - 2][1]: #x-2 esta 2 pontos abaixo do 8, [1] valor 1 eh o eixo y
                contador +=1

    #print(contador)#print contador fora do loop

    #inserir a inf dentro da img
    cv2.rectangle(img,(80,10),(200,100),(255,0,0),-1)
    cv2.putText(img,str(contador),(100,100),cv2.FONT_HERSHEY_SIMPLEX,4,(255,255,0),5)



    #web
    cv2.imshow("Imagem", img)
    cv2.waitKey(1)