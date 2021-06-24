#include <pybind11/pybind11.h>

namespace py = pybind11;


int add(int i, int j){
  return i+j;
}


// -- Pybind line. The first argument must be the file name
PYBIND11_MODULE(example_01, m){

  m.doc() = "pybind11 example plugin";

  // -- Basic add function
  m.def("add", &add, "A function which adds two numbers");

  // -- Function with keyword arguments. This defines an alternative way to call the 'add' function
  m.def("add", &add, "Add with keyword arguments", py::arg("i"), py::arg("j"));  

  // -- Function with keyword arguments
  m.def("add", &add, "Add with default arguments" , py::arg("i")=1, py::arg("j")=4); 
  
  // -- Export values using attr 
  m.attr("the_answer") = 42;
  py::object world = py::cast("World"); // convert objects
  m.attr("what") = world;


}



