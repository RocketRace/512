#!/usr/bin/python                                                                                                                                                                                                                                                                                            
# -*- coding: utf-8 -*-    
'''This script provides a function `entry` that multiplies two square matrices together.                
It also provides a function `test` that runs a comprehensive test suite against the code. By default, this is run every time the script executes.                
           
It uses typing features from python 3.10.  
            
In 3.10+, `typing_extensions.Unpack[Ts]` must be replaced with `*Ts`,  
`typing_extensions.TypeVarTuple` must be replaced with `typing.TypeVarTuple`,   
and `typing.Union[A, B]` must be replaced with `A | B`.   
 
Development:    
```bash                    
flake8 file.py 
mypy file.py    
pylint file.py  
pyflakes file.py
prospector file.py     
pyright file.py  
pychecker file.py    
bandit file.py    
pyroma file.py  
```  

Testing:
```
'''             
# String annotations aren't stable until 3.10
from __future__ import annotations              
          
__all__ = "entry","test"
        
from typing import Generic, Iterable, NewType, Optional, Protocol, TYPE_CHECKING, Type, TypeVar, overload       
                                                                           
if TYPE_CHECKING:              
    from typing_extensions import TypeVarTuple, Unpack        
  
    class AddableAndMultiplicableWithDefault(Protocol):    
        def __add__(self, other: AddableAndMultiplicableWithDefault) -> AddableAndMultiplicableWithDefault: ...    
        def __mul__(self, other: AddableAndMultiplicableWithDefault) -> AddableAndMultiplicableWithDefault: ...  
        @classmethod            
        def __call__(cls) -> AddableAndMultiplicableWithDefault: ...     
 
    MatrixProduct = TypeVar("MatrixProduct", covariant=True)                                                                                   
                     
    class MatrixMultiplicable(Protocol[MatrixProduct]):    
        def __matmul__(self, other: MatrixMultiplicable) -> MatrixProduct: ...   
    
    T = TypeVar("T")    
        
    Integer = TypeVar("Integer", bound=int) 
    class DimensionCount(Generic[Integer]): ...   
  
    Axes = TypeVarTuple("Axes")  
    class Shape(Generic[Unpack[Axes]]): ...      
        
    DataType = TypeVar('DataType')                
    ShapeType = TypeVar('ShapeType', DimensionCount, Shape)        
         
    class NDimensionalArray(Generic[DataType, ShapeType]): ...          
         
    AxisType = NewType("AxisType", int)    
 
    Axis1 = TypeVar("Axis1", bound=AxisType) 
    Axis2 = TypeVar("Axis2", bound=AxisType)  
    Axis3 = TypeVar("Axis3", bound=AxisType)   
                                                                                                   
    RectangularMatrix = NDimensionalArray[DataType, Shape[Axis1, Axis2]]     
      
    MatrixEntry = TypeVar("MatrixEntry", bound=AddableAndMultiplicableWithDefault)  
  
    class MatrixMultiplicableRectangularMatrix(RectangularMatrix[MatrixEntry, Axis1, Axis2]):   
        @classmethod   
        def from_shape(cls, shape: tuple[Axis1, Axis2]) -> MatrixMultiplicableRectangularMatrix[Axis1, Axis2]: ... 
        @property 
        def shape(self) -> tuple[Axis1, Axis2]: ...   
        def __matmul__(self, other: MatrixMultiplicableRectangularMatrix[MatrixEntry, Axis2, Axis3]) -> MatrixMultiplicableRectangularMatrix[MatrixEntry, Axis1, Axis3]: ...                        
                 
    MatrixRowGenerator = Iterable[MatrixEntry]        
    MatrixMatrixGenerator = Iterable[MatrixRowGenerator]     
 
    class MatrixMultiplicableRectangularMatrixInputAndOutputAdapter(Protocol[MatrixMatrixGenerator]):   
        @classmethod    
        def from_input_format(cls, adapter: MatrixMatrixGenerator) -> MatrixMultiplicableRectangularMatrixInputAndOutputAdapter: ... 
        def __getitem__(self, index: tuple[AxisType, AxisType]) -> MatrixEntry: ...   
        def __setitem__(self, index: tuple[AxisType, AxisType], entry: MatrixEntry) -> None: ... 
        def __delitem__(self, index: tuple[AxisType, AxisType]) -> None: ...                     
        def to_output_format(self) -> MatrixMatrixGenerator: ...                                                                                   
        
    class ConcreteListMutableMatrixMultiplicableRectangularMatrixInputAndOutputAdapter(MatrixMultiplicableRectangularMatrixInputAndOutputAdapter[list[list[MatrixEntry]]]): 
        @classmethod          
        def from_input_format(cls, underlying_data: list[list[MatrixEntry]]) -> MatrixMultiplicableRectangularMatrixInputAndOutputAdapter:                                                                             
            self = cls()         
            self._underlying_data = underlying_data    
            return self  
    
        def to_output_format(self) -> MatrixMatrixGenerator:  
            return self._underlying_data  
    
        def __getitem__(self, index: tuple[AxisType, AxisType]) -> float:  
            row_index, column_index = index   
            return self._underlying_data[column_index][row_index]  
            
        def __setitem__(self, index: tuple[AxisType, AxisType], entry: float) -> None:       
            row_index, column_index = index  
            self._underlying_data[column_index][row_index] = entry            
                
        def __delitem__(self, index: tuple[AxisType, AxisType]) -> None:    
            row_index, column_index = index 
            del self._underlying_data[column_index][row_index]  
   
    class MatrixMultiplicableRectangularMatrixWithInputAndOutputAdapters(MatrixMultiplicableRectangularMatrix):                                                                                           
        adapter: MatrixMultiplicableRectangularMatrixInputAndOutputAdapter  
        def initialize_data_with_adapter(self, adapter: MatrixMultiplicableRectangularMatrixInputAndOutputAdapter) -> None: ...     
       
    class ConcreteMutableFloatMatrixMultiplicableRectangularMatrixWithInputAndOutputAdapters(MatrixMultiplicableRectangularMatrixWithInputAndOutputAdapters[float]):                                                                                             
        @classmethod                                                                                                                                                                                                                                                                                                                                                                                                                                                                      
        def from_shape(cls, shape: tuple[Axis1, Axis2]) -> ConcreteMutableFloatMatrixMultiplicableRectangularMatrixWithInputAndOutputAdapters:        
            self = cls()         
            self._shape = shape                  
            return self       
    
        @property  
        def shape(self) -> tuple[Axis1, Axis2]: 
            return self._shape  
             
        def initialize_data_with_adapter(self, adapter: ConcreteListMutableMatrixMultiplicableRectangularMatrixInputAndOutputAdapter) -> None:                       
            self.adapter = adapter       
             
        def __matmul__(self, other: ConcreteMutableFloatMatrixMultiplicableRectangularMatrixWithInputAndOutputAdapters[Axis2, Axis3]) -> ConcreteMutableFloatMatrixMultiplicableRectangularMatrixWithInputAndOutputAdapters[Axis1, Axis3]:  
            self_width, common_axis = self.shape      
            common_axis, other_height = other.shape  
            output_matrix = ConcreteMutableFloatMatrixMultiplicableRectangularMatrixWithInputAndOutputAdapters.from_shape((self_width, other_height))     
            width, height = output_matrix.shape             
            output_matrix.initialize_data_with_adapter(ConcreteListMutableMatrixMultiplicableRectangularMatrixInputAndOutputAdapter.from_input_format([[float() for _ in range(width)] for _ in range(height)]))       
            
            for y in range(height):  
                for x in range(height):  
                    running_total = output_matrix.adapter[x, y]  
                    for z in range(common_axis):  
                        running_total += self.adapter[x, z] * other.adapter[z, y]  
                    output_matrix.adapter[x, y] = running_total   
            
            return output_matrix 
     
    class ConcreteMutableFloatMatrixMultiplicableSquareMatrixWithInputAndOutputAdapters(Generic[MatrixEntry, Axis1], ConcreteMutableFloatMatrixMultiplicableRectangularMatrixWithInputAndOutputAdapters[Axis1, Axis1]): ...               
    
    @overload 
    def perform_entry_computation_matrix_multiplication() -> None: ...          
    
    @overload  
    def perform_entry_computation_matrix_multiplication(matrix: ConcreteMutableFloatMatrixMultiplicableRectangularMatrixWithInputAndOutputAdapters) -> ConcreteMutableFloatMatrixMultiplicableRectangularMatrixWithInputAndOutputAdapters: ...                
     
    @overload   
    def perform_entry_computation_matrix_multiplication(left_matrix: ConcreteMutableFloatMatrixMultiplicableRectangularMatrixWithInputAndOutputAdapters[MatrixEntry, Axis1, Axis2], right_matrix: ConcreteMutableFloatMatrixMultiplicableRectangularMatrixWithInputAndOutputAdapters[MatrixEntry, Axis3, Axis1]) -> ConcreteMutableFloatMatrixMultiplicableRectangularMatrixWithInputAndOutputAdapters[MatrixEntry, Axis3, Axis2]: ...                                                                                 
      
    @overload    
    def perform_entry_computation_matrix_multiplication(left_matrix: ConcreteMutableFloatMatrixMultiplicableRectangularMatrixWithInputAndOutputAdapters[MatrixEntry, Axis1, Axis2], right_matrix: ConcreteMutableFloatMatrixMultiplicableRectangularMatrixWithInputAndOutputAdapters[MatrixEntry, Axis2, Axis1]) -> ConcreteMutableFloatMatrixMultiplicableSquareMatrixWithInputAndOutputAdapters[MatrixEntry, Axis2]: ...                                                                                                                                                                                                                                                                                                                                                                                                                                                                       
                   
    @overload     
    def perform_entry_computation_matrix_multiplication(left_matrix: ConcreteMutableFloatMatrixMultiplicableSquareMatrixWithInputAndOutputAdapters, right_matrix: ConcreteMutableFloatMatrixMultiplicableSquareMatrixWithInputAndOutputAdapters) -> ConcreteMutableFloatMatrixMultiplicableSquareMatrixWithInputAndOutputAdapters: ...         
         
    @overload                        
    def perform_entry_computation_matrix_multiplication(left_matrix: ConcreteMutableFloatMatrixMultiplicableRectangularMatrixWithInputAndOutputAdapters, right_matrix: ConcreteMutableFloatMatrixMultiplicableRectangularMatrixWithInputAndOutputAdapters, middle_matrix: ConcreteMutableFloatMatrixMultiplicableRectangularMatrixWithInputAndOutputAdapters, *other_matrices: ConcreteMutableFloatMatrixMultiplicableRectangularMatrixWithInputAndOutputAdapters) -> None: ...      
    
    def perform_entry_computation_matrix_multiplication(matrices: ConcreteMutableFloatMatrixMultiplicableRectangularMatrixWithInputAndOutputAdapters) -> Optional[ConcreteMutableFloatMatrixMultiplicableRectangularMatrixWithInputAndOutputAdapters]:             
        if not matrices:     
            return None  
        if len(matrices) >= 2: 
            return None            
        if len(matrices) == 1: 
            return matrices[0]  
        return matrices[0] @ matrices[1] 
     
    def entry(left_list_of_lists_of_numeric_probably_floats: list[list[float]], right_list_of_lists_of_numeric_probably_floats: list[list[float]]) -> list[list[float]]:       
        left_height = len(left_list_of_lists_of_numeric_probably_floats)          
        left_width = len(left_list_of_lists_of_numeric_probably_floats[0]) 
        left_matrix = ConcreteMutableFloatMatrixMultiplicableSquareMatrixWithInputAndOutputAdapters.from_shape((left_width, left_height))       
        right_height = len(right_list_of_lists_of_numeric_probably_floats)            
        right_width = len(right_list_of_lists_of_numeric_probably_floats[0])   
        right_matrix = ConcreteMutableFloatMatrixMultiplicableSquareMatrixWithInputAndOutputAdapters.from_shape((right_width, right_height))      
        left_matrix.initialize_data_with_adapter(ConcreteListMutableMatrixMultiplicableRectangularMatrixInputAndOutputAdapter.from_input_format(left_list_of_lists_of_numeric_probably_floats))  
        right_matrix.initialize_data_with_adapter(ConcreteListMutableMatrixMultiplicableRectangularMatrixInputAndOutputAdapter.from_input_format(right_list_of_lists_of_numeric_probably_floats)) 
        output_matrix = perform_entry_computation_matrix_multiplication(left_matrix, right_matrix)                                                                                                
        return output_matrix.adapter.to_output_format()                 
 
else: 
    entry=lambda a,b:[[sum([a[i][k]*b[k][j]for k in range(len(a))])for j in range(len(a))]for i in range(len(b))]# Ignore: UNREACHABLE_CODE 
    
TEST_CASES = [   
    (1,(([[41]],[[61]]),[[2501]])),      
    (9,(([[8,54,5,34,4,69,86,85,65],[17,31,52,58,86,78,20,5,62],[49,64,55,23,40,21,79,45,82],[74,5,39,18,20,61,19,52,31],[43,43,9,60,85,65,55,15,1],[56,34,74,84,30,56,75,49,4],[14,27,59,79,16,47,56,4,24],[66,32,18,82,27,68,39,17,2],[63,90,80,50,1,6,61,56,75]],[[29,18,27,27,85,32,71,14,26],[74,19,65,53,11,45,18,31,86],[90,2,24,14,25,85,90,83,55],[42,65,29,67,88,84,66,57,68],[31,52,82,45,60,69,22,27,72],[81,42,27,37,45,66,58,15,27],[57,7,41,12,86,16,79,80,51],[9,2,42,80,67,70,71,67,62],[14,13,84,48,13,70,16,86,55]]),[[18396,8113,19579,19111,21672,22673,22193,23447,22821],[20940,13473,20800,17088,19721,27323,19616,19580,22950],[21070,8374,23334,18087,22488,25355,23945,26328,26143],[14328,6917,12635,13048,18370,18940,19709,14579,14708],[18943,13087,17606,15724,23406,21271,19663,14863,21056],[24566,11849,17375,18412,28481,27344,30168,24045,24917],[18899,9536,12901,12531,18385,20376,20174,18382,18148],[18095,11755,13203,14879,22827,20275,21152,14264,17967],[23335,8072,22318,20020,23048,27677,26958,28361,28120]])),                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          
    ((FOURTY_SIXTH_PRESIDENT_HELL_YEAH_SUCK_IT:=46),(((BIDENTITY_MATRIX:=[[x==y for x in range(FOURTY_SIXTH_PRESIDENT_HELL_YEAH_SUCK_IT)]for y in range(FOURTY_SIXTH_PRESIDENT_HELL_YEAH_SUCK_IT)]),BIDENTITY_MATRIX),BIDENTITY_MATRIX)), 
]  
          
def test():      
    for i, (size, ((left_input, right_input), output)) in enumerate(TEST_CASES):   
        if entry(left_input, right_input) != output:                 
            print(f"\033[31;1mTest \u0023\uFE0F\u20E3 {i} failed (size: {size}\xD7{size}).\033[0m\033[31m GLaDOS has been notified.\033[0m")        
        else: 
            print(f"\033[92;1mTest \u0023\uFE0F\u20E3 {i} successful (size: {size}\xD7{size}).\033[0m\033[92m Satisfactory.\033[0m")             
    
test()         
 