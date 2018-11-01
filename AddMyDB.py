# -*- coding: utf-8 -*-
"""
Created on Sun Aug 26 14:54:23 2018

@author: user
"""

import boto3
import time
import mysql.connector


if __name__ == "__main__":
    
    maxResults=2
    tokens=True
    
    start = time.time()

    # Connect MySQL database
    cnx = mysql.connector.connect(host='localhost', 
                              port='3306', 
                              user='user', 
                              password='pass', 
                              database='test',
                              charset='utf8')
    if cnx.is_connected():
        print('Connected to MySQL database')
    else:
        print('Cannot connect to MySQL database') 
    
    cur = cnx.cursor(buffered=True, dictionary=True)
    #cur.execute('show slave status')
    cur.execute("select * from smart119;")

    # Connect S3 
    region="us-east-2"
    
    client=boto3.client('rekognition', region)
    collectionId='smart119-test'
        
    response=client.list_faces(CollectionId=collectionId,
                               MaxResults=maxResults)
    
    # Search all faceID in the collection
    print('Faces in collection ' + collectionId)       

    while tokens:

        faces=response['Faces']
        
        for face in faces:
            print (face['FaceId'])
            try:
                cur.execute("insert into smart119 values(%s, %s)", ["hoge", face['FaceId']]) # 名前はあとで手動入力できるようにする
                cnx.commit()
            except:
                cnx.rollback()
                raise

        if 'NextToken' in response:
            nextToken=response['NextToken']
            response=client.list_faces(CollectionId=collectionId, NextToken=nextToken,MaxResults=maxResults)
        else:
            tokens=False    
    
    cur.close
    cnx.close  
    
    elapsed_time = time.time() - start
    print ("{0}".format(elapsed_time) + "[sec]")
