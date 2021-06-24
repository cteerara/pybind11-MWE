#include <pybind11/pybind11.h>
#include <iostream>

namespace py = pybind11;
using namespace std;


class Pet {

  public:
    string name;
    int age;
    Pet(string name_, int age_){
      name = name_;
      age = age_;
    }

    string getName(){
      return name; 
    }

};


int main(){
  Pet p("Browney", 15);
  printf("Pet name %s age %d years old\n", p.name.c_str(), p.age);
  return 0;
}




PYBIND11_MODULE(example_03, m) {

  py::class_<Pet>(m, "Pet", py::dynamic_attr()) // dynamic_attr is use to dynamically set attributes in python

    // -- Create constructor
    .def(py::init<const std::string &, const int &>())

    // -- read/write member variable. in python: Pet.name
    .def_readwrite("name", &Pet::name)

    // -- read only member variable. in python: Pet.age
    .def_readonly("age", &Pet::age)

    // -- Call function
    .def("getName", &Pet::getName)

;}




