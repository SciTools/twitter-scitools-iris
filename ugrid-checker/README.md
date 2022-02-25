I originally ran ugrid-checker `v0.1.1` on [data_C4_warn_error.nc](data_C4_warn_error.nc).

Unfortunately `v0.1.1` includes a mistake ([pp-mo/ugrid-checks#34](https://github.com/pp-mo/ugrid-checks/issues/34)), so I manually edited the output text to make the `A304` warning into an appropriate `A303` warning instead:

```
  ... WARN A303 : Mesh connectivity variable "face_nodes" of mesh "topology" has a 'start_index' of type "float32", which is different from the variable type, "int64".
```
