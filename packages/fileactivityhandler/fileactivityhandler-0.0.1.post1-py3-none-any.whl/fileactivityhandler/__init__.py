def checkPathExistorNot(pathName = ""):

  '''
  
  Function    : checkPathExistorNot
  Parameter   : 1 argument is mandatory to pass
  Description : To check source path exist or not 
  
  '''

  try:
    
    import os

    try:
      
      if pathName is None or pathName == 'None' :
        raise TypeError("You cannot pass 'None' as an Argument")
      
      if pathName == "" or pathName =='' or pathName.strip() == '':
        raise TypeError("No argument passed ...Fucntion expect one parameter")
      
      try:
        
        if os.path.isdir(pathName):
          
          return True 
          
        else:

          raise Exception("The following mentioned source path does not exist : ",pathName)
      
      except Exception as err:
        
        print('Error : ',repr(err))

    except Exception as err:
      print('Error : ',repr(err))

  except Exception as err:
    print('Error : ',repr(err))

  return   








def checkFileExistorNot(fileName = ""):

  '''
  
  Function    : checkPathExistorNot
  Parameter   : 1 argument is mandatory to pass
  Description : To check file exist or not 
  
  '''

  try:
    
    import os

    try:
      
      if fileName is None or fileName == 'None' :
        raise TypeError("You cannot pass 'None' as an Argument")
      
      if fileName == "" or fileName =='' or fileName.strip() == '':
        raise TypeError("No argument passed ...Fucntion expect one parameter")
      
      try:
        
        if os.path.isfile(fileName):
          
          return True 
          
        else:

          raise Exception("The following mentioned source file does not exist : ",fileName)
      
      except Exception as err:
        
        print('Error : ',repr(err))

    except Exception as err:
      print('Error : ',repr(err))

  except Exception as err:
    print('Error : ',repr(err))

  return   









def checkFileExtensionExistorNot(fileName = ""):

  '''
  
  Function    : checkFileExtensionExistorNot
  Parameter   : 1 argument is mandatory to pass
  Description : To check file extension exist or not 
  
  '''

  try:
    
    import os

    try:
      
      if fileName is None or fileName == 'None' :
        raise TypeError("You cannot pass 'None' as an Argument")
      
      if fileName == "" or fileName =='' or fileName.strip() == '':
        raise TypeError("No argument passed ...Fucntion expect one parameter")
      
      try:
        
        if os.path.isfile(fileName):

          try:

            import ntpath

            filename = ntpath.basename(fileName)
            
            if filename:
              if os.path.splitext(filename)[-1]:
                return True
              else:
                return 
            else:
              return 

          except Exception as err:
            print('Error : ',repr(err))
   
        else:

          raise Exception("The following mentioned source file does not exist : ",fileName)
      
      except Exception as err:
        
        print('Error : ',repr(err))

    except Exception as err:
      print('Error : ',repr(err))

  except Exception as err:
    print('Error : ',repr(err))

  return   








def checkFileSize(fileName = ""):

  '''

  Function    : checkFileSize
  Parameter   : 1 argument is mandatory to pass
  Description : To check file size 
  
  '''

  try:
    
    import os

    try:
      
      if fileName is None or fileName == 'None' :
        raise TypeError("You cannot pass 'None' as an Argument")
      
      if fileName == "" or fileName =='' or fileName.strip() == '':
        raise TypeError("No argument passed ...Fucntion expect one parameter")
      
      try:
        
        if os.path.isfile(fileName):

          if os.path.getsize(fileName) !=0:
            
            return True 

          else:

            return  

        else:

          raise Exception("The following mentioned source file does not exist : ",fileName)
      
      except Exception as err:
        
        print('Error : ',repr(err))

    except Exception as err:
      print('Error : ',repr(err))

  except Exception as err:
    print('Error : ',repr(err))

  return   









def monitorFilearrival(fileName = ""):

  '''

  Function    : checkFileExistatServer
  Parameter   : 1 argument is mandatory to pass
  Description : To check file exist or not at server 
  
  '''

  try:
    
    import os

    try:
      
      if fileName is None or fileName == 'None' :
        raise TypeError("You cannot pass 'None' as an Argument")
      
      if fileName == "" or fileName =='' or fileName.strip() == '':
        raise TypeError("No argument passed ...Fucntion expect one parameter")
      
      try:
        
        while True:
          
          if os.path.isfile(fileName):
            return True 

      except Exception as err:
        
        print('Error : ',repr(err))

    except Exception as err:
      print('Error : ',repr(err))

  except Exception as err:
    print('Error : ',repr(err))

  return   







def getFileExtension(fileName = ""):

  '''

  Function    : getFileExtension
  Parameter   : 1 argument is mandatory to pass
  Description : To get file extension 
  
  '''

  try:
    
    import os

    try:
      
      if fileName is None or fileName == 'None' :
        raise TypeError("You cannot pass 'None' as an Argument")
      
      if fileName == "" or fileName =='' or fileName.strip() == '':
        raise TypeError("No argument passed ...Fucntion expect one parameter")
      
      try:
        
        if os.path.isfile(fileName):
          
          filename, ext = os.path.splitext(fileName)
          if ext != '':
            return ext
          else:
            return    
        else:

          raise Exception("The following mentioned source file does not exist : ",fileName)
      
      except Exception as err:
        
        print('Error : ',repr(err))

    except Exception as err:
      print('Error : ',repr(err))

  except Exception as err:
    print('Error : ',repr(err))

  return  








def getFileName(fileName = ""):

  '''

  Function    : getFileName
  Parameter   : 1 argument is mandatory to pass
  Description : To get file name 
  
  '''

  try:
    
    import os

    try:
      
      if fileName is None or fileName == 'None' :
        raise TypeError("You cannot pass 'None' as an Argument")
      
      if fileName == "" or fileName =='' or fileName.strip() == '':
        raise TypeError("No argument passed ...Fucntion expect one parameter")
      
      try:
        
        if os.path.isfile(fileName):

          try:
            import ntpath

            filename = ntpath.basename(fileName)
            return filename

          except Exception as err:
            
            print('Error : ',repr(err))
          
        else:

          raise Exception("The following mentioned source file does not exist : ",fileName)
      
      except Exception as err:
        
        print('Error : ',repr(err))

    except Exception as err:
      print('Error : ',repr(err))

  except Exception as err:
    print('Error : ',repr(err))

  return 







def copyFileA2BPath(SourcePath="",DestinationPath="",fileName=""):

  '''

  Function    : copyFileA2BPath
  Parameter   : 3 argument are required
  Description : TO copy file from path A to path B 
  
  '''

  try:
    
    import os
    import shutil

    try:
      

      if SourcePath is None or SourcePath == 'None' :
        raise TypeError("You cannot pass Source path as an Argument : 'None' ")
       
      if SourcePath == "" or SourcePath =='' or SourcePath.strip() == '':
        raise TypeError("Source path is not passed to function")

      if DestinationPath is None or DestinationPath == 'None' :
        raise TypeError("You cannot pass Destination path as an Argument : 'None'")
       
      if DestinationPath == "" or DestinationPath =='' or DestinationPath.strip() == '':
        raise TypeError("Destination path is not passed to function")

      if fileName is None or fileName == 'None' :
        raise TypeError("You cannot pass 'None' as an Argument")
      
      if fileName == "" or fileName =='' or fileName.strip() == '':
        raise TypeError("FileName is not passed to the fucntion")
      
      try:

        srcFilename  = os.path.join(SourcePath, fileName)
        destFilename = os.path.join(DestinationPath, fileName)

        if os.path.isfile(srcFilename):

          if os.path.isdir(DestinationPath):

            shutil.copyfile(srcFilename,destFilename)
            return True

          else:

            raise Exception("The following mentioned Destination path does not exist : ",DestinationPath)
        
        else:

          raise Exception("The following mentioned source file does not exist : ",fileName)

      except Exception as err:
        
        print('Error : ',repr(err))

    except Exception as err:
      print('Error : ',repr(err))

  except Exception as err:
    print('Error : ',repr(err))

  return




