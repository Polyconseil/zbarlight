#include <Python.h>
#include <stdlib.h>
#include <zbar.h>

/* Python 2 and Python 3 Compatibility */
#if PY_MAJOR_VERSION >= 3
#define PY_BYTES_FROM_STRING(result) PyBytes_FromString(result)
#define PY_INIT_FCT() PyModule_Create(&zbarlight_moduledef)
#else
#define PY_BYTES_FROM_STRING(result) PyString_FromString(result)
#define PY_INIT_FCT() Py_InitModule("_zbarlight", zbarlight_functions)
#endif

/* Extract QR code from raw image (using zbar) */
static char** _zbar_code_scanner(
    const int symbologie,
    const void *raw_image_data,
    unsigned long raw_image_data_length,
    unsigned int width,
    unsigned int height
) {
    int decoded = -2;
    int format = *(int *) "Y800";
    char **data = NULL;

    zbar_image_scanner_t *scanner = zbar_image_scanner_create();
    zbar_image_scanner_set_config(scanner, 0, ZBAR_CFG_ENABLE, 0); /* disable all symbologies */
    zbar_image_scanner_set_config(scanner, symbologie, ZBAR_CFG_ENABLE, 1);

    zbar_image_t *image = zbar_image_create();
    zbar_image_set_format(image, format);
    zbar_image_set_size(image, width, height);
    zbar_image_set_data(image, raw_image_data, raw_image_data_length, NULL);

    decoded = zbar_scan_image(scanner, image);
    if (decoded > 0) {
        const zbar_symbol_t *symbol = zbar_image_first_symbol(image);
        data = calloc(decoded + 1, sizeof(char*));

        for(int i=0; i < decoded; i++) {
            unsigned int item_length = zbar_symbol_get_data_length(symbol);
            data[i] = calloc(item_length + 1, sizeof(char));
            if (data[i]) {
                strncpy(data[i], zbar_symbol_get_data(symbol), item_length);
                data[i][item_length] = '\0';
            }
            symbol = zbar_symbol_next(symbol);
        } while(symbol != NULL);
    }

    zbar_image_destroy(image);
    zbar_image_scanner_destroy(scanner);
    return data;
}

/* Python wrapper for _zbar_code_scanner() */
static PyObject* zbar_code_scanner(PyObject *self, PyObject *args) {
    PyObject *python_image = NULL;
    int symbologie = 0;
    char *raw_image_data = NULL;
    Py_ssize_t raw_image_data_length = 0;
    unsigned int width = 0;
    unsigned int height = 0;
    char **result = NULL;
    PyObject *data = NULL;

    if (!PyArg_ParseTuple(args, "ISII", &symbologie, &python_image, &width, &height)) {
        return NULL;
    }
    PyBytes_AsStringAndSize(python_image, &raw_image_data, &raw_image_data_length);

    result = _zbar_code_scanner(symbologie, raw_image_data, raw_image_data_length, width, height);
    if (result == NULL) {
        Py_RETURN_NONE;
    }

    data = PyList_New(0);
    for(int i=0; result[i] != NULL; i++) {
        PyObject *item = PY_BYTES_FROM_STRING(result[i]);
        PyList_Append(data, item);
        free(result[i]);
    }
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
    { "zbar_code_scanner", zbar_code_scanner, METH_VARARGS, NULL},
    { NULL }
};

#if PY_MAJOR_VERSION >= 3
static struct PyModuleDef zbarlight_moduledef = {
    PyModuleDef_HEAD_INIT,
    "_zbarlight",
    NULL,
    -1,
    zbarlight_functions,
};
#endif

PyObject* PyInit__zbarlight(void) { /* Python 3 way */
    PyObject* module = PY_INIT_FCT();
    PyObject * symbologies = Py_BuildValue(
        #if ZBAR_VERSION_MAJOR == 0 && ZBAR_VERSION_MINOR < 11
        "{s:i,s:i,s:i,s:i,s:i,s:i,s:i,s:i,s:i,s:i,s:i}",
        #else
        "{s:i,s:i,s:i,s:i,s:i,s:i,s:i,s:i,s:i,s:i,s:i,s:i,s:i,s:i,s:i}",
        "DATABAR", ZBAR_DATABAR,
        "DATABAR_EXP", ZBAR_DATABAR_EXP,
        "CODABAR", ZBAR_CODABAR,
        "CODE93", ZBAR_CODE93,
        #endif
        "EAN8", ZBAR_EAN8,
        "UPCE", ZBAR_UPCE,
        "ISBN10", ZBAR_ISBN10,
        "UPCA", ZBAR_UPCA,
        "EAN13", ZBAR_EAN13,
        "ISBN13", ZBAR_ISBN13,
        "I25", ZBAR_I25,
        "CODE39", ZBAR_CODE39,
        "PDF417", ZBAR_PDF417,
        "QRCODE", ZBAR_QRCODE,
        "CODE128", ZBAR_CODE128
    );
    PyModule_AddObject(module, "Symbologies", symbologies);
    return module;
}

void init_zbarlight(void) { /* Python 2 way */
    PyInit__zbarlight();
}
