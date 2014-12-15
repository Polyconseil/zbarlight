#include <Python.h>
#include <stdlib.h>
#include <zbar.h>

/* Extract QR code from raw image (using zbar) */
char* zbar_qr_code_scanner(const void *raw_image_data,
                           unsigned long raw_image_data_length,
                           unsigned width,
                           unsigned height) {
    int decoded;
    int format = *(int *) "Y800";
    char *data = NULL;

    zbar_image_scanner_t *scanner = zbar_image_scanner_create();
    zbar_image_scanner_parse_config(scanner, "qr.enable");

    zbar_image_t *image = zbar_image_create();
    zbar_image_set_format(image, format);
    zbar_image_set_size(image, width, height);
    zbar_image_set_data(image, raw_image_data, raw_image_data_length, NULL);

    decoded = zbar_scan_image(scanner, image);
    if (decoded == 1) {
        const zbar_symbol_t *symbol = zbar_image_first_symbol(image);
        unsigned int data_length = zbar_symbol_get_data_length(symbol);
        data = malloc(data_length + 1);
        strncpy(data, zbar_symbol_get_data(symbol), data_length);
        data[data_length] = '\0';
    }

    zbar_image_destroy(image);
    zbar_image_scanner_destroy(scanner);
    return data;
}

/* Python wrapper for zbar_qr_code_scanner() */
PyObject* qr_code_scanner(PyObject *self, PyObject *args) {
    PyObject *python_image;
    char *raw_image_data;
    Py_ssize_t raw_image_data_length;
    unsigned int width;
    unsigned int height;
    char *result;
    PyObject *data;

    if (!PyArg_ParseTuple(args, "SII", &python_image, &width, &height)) {
        return NULL;
    }
    PyBytes_AsStringAndSize(python_image, &raw_image_data, &raw_image_data_length);

    result = zbar_qr_code_scanner(raw_image_data, raw_image_data_length, width, height);
    if (result == NULL) {
        Py_RETURN_NONE;
    }

#if PY_MAJOR_VERSION >= 3
    data = PyBytes_FromString(result);
#else
    data = PyString_FromString(result);
#endif
    free(result);

    return data;
}

/* Get zbar version */
static PyObject* version(PyObject *self, PyObject *args) {
    unsigned int major, minor;

    if (!PyArg_ParseTuple(args, "")) {
        return NULL;
    }

    zbar_version(&major, &minor);
    return Py_BuildValue("II", major, minor);
}

/* Module initialization */
static PyMethodDef zbarlight_functions[] = {
    { "version", version, METH_VARARGS, NULL},
    { "qr_code_scanner", qr_code_scanner, METH_VARARGS, NULL},
    { NULL }
};

#if PY_MAJOR_VERSION >= 3
static struct PyModuleDef zbarlight_moduledef = {
    PyModuleDef_HEAD_INIT,
    "zbarlight",
    NULL,
    -1,
    zbarlight_functions,
};
#define PY_INIT_FCT() PyModule_Create(&zbarlight_moduledef)
#else
#define PY_INIT_FCT() Py_InitModule("zbarlight", zbarlight_functions)
#endif

PyObject* PyInit_zbarlight(void) { /* Python 3 way */
    return PY_INIT_FCT();
}

void initzbarlight(void) { /* Python 2 way */
    PyInit_zbarlight();
}
