import numpy as np

def compute_gradient_matrix(X, y, w, b): 
    """
    Computes the gradient for linear regression 
 
    Args:
      X : (array_like Shape (m,n)) variable such as house size 
      y : (array_like Shape (m,1)) actual value 
      w : (array_like Shape (n,1)) Values of parameters of the model      
      b : (scalar )                Values of parameter of the model      
    Returns
      dj_dw: (array_like Shape (n,1)) The gradient of the cost w.r.t. the parameters w. 
      dj_db: (scalar)                The gradient of the cost w.r.t. the parameter b. 
                                  
    """
    m,n = X.shape
    f_wb = X @ w + b              
    e   = f_wb - y                
    dj_dw  = (1/m) * (X.T @ e)    
    dj_db  = (1/m) * np.sum(e)    
        
    return dj_db,dj_dw


if __name__ == '__main__':
    arr_1 = np.array([1,2,3])
    X =  np.array([arr_1, arr_1*2,arr_1*3])
    y =  np.array([1,2,3])
    w = np.array([4,5,6])
    b = 2 

    ret = compute_gradient_matrix(X, y, w, b)
    print(f"ret == {ret}")