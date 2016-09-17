#### AffineTransformOp.py 
#### Defines a class for performing an affine transformation on 2x2 points 
#### Author: Maxie D. Schmidt
#### Created: 2016.02.19 

from sage.all import vector, matrix

## 
 # AffineTransformOp
 # Defines a 2x2 affine transformation on points in R^2
##
class AffineTransformOp(object): 
     
     ## __init__
      # Initialization function for the AffineTransformOp class
      # @param mOp   The transformation matrix
      # @param tOp   The translation term in the transformation
      # @param sfunc An optional simplify function to post-process 
      #              symbolic matrices
     ##
     def __init__(self, mOp, tOp, sfunc = None): 
          self.matrix_M = mOp; 
          self.matrix_T = tOp; 
          self.simp_func = sfunc; 

     ## apply
      # Applies another affine transformation to the local transformation 
      # @param apply_op The affine transformation object we are applying
      # @return         A new affine transformation object representing the 
      #                 result
     ##
     def apply(self, apply_op): 
          matrix_M = apply_op.matrix_M * self.matrix_M; 
          matrix_T = apply_op.matrix_M * self.matrix_T + apply_op.matrix_T; 
          matrix_M = copy(matrix_M); 
          matrix_T = copy(matrix_T); 
          if self.simp_func != None:  
               matrix_M = self.simp_func(matrix_M); 
               matrix_T = self.simp_func(matrix_T); 
          ## if 
          return AffineTransformOp(matrix_M, matrix_T, self.simp_func); 

     ## apply_to_point
      # Applies this affine transformation to a point
      # @param point The point to be transformed
      # @return      The transformed point
     ##
     def apply_to_point(self, point): 
          tpoint = self.matrix_M * point + self.matrix_T; 
          if self.simp_func != None: 
               tpoint = self.simp_func(tpoint);
          return tpoint; 

     ## M
      # Access to the matrix term in the transformation
     ##
     @property
     def M(self): 
          return copy(self.matrix_M); 

     ## T
      # Access to the translation term in the transformation
     ##     
     @property
     def T(self): 
          return copy(self.matrix_T); 

## class 
