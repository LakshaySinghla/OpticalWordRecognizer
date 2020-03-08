#returns the equivalent letter output from neural network output node number
classes = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z',
          'a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z',
          'zero','one','two','three','four','five','six','seven','eight','nine',
          'equal','times','slash','ampersand','minus','plus','backslash',
          'BigLeftPar','LeftPar','MiddleLeftPar','RightPar','BigRightPar','MiddleRightPar',
          'semicolon','cdot','comma','period']

mapping={i:v for i,v in enumerate(classes)}
inv_mapping = {v:k for k,v in mapping.items()}
