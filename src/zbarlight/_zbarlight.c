#include <Python.h>
#include <stdlib.h>
#include <zbar.h>

#define KNOWN_SYMNOLOGIES 15

struct Symbologies {
    int number;
    int symbologie[KNOWN_SYMNOLOGIES];  /* Do not use malloc, allocate space for all known symbologies */
};

/* Extract QR code from raw image (using zbar) */
static char** _zbar_code_scanner(
    const struct Symbologies *symbologies,
    const void *raw_image_data,
    unsigned long raw_image_data_length,
    unsigned int width,
    unsigned int height,
    unsigned int is_binary
) {
    int decoded = -2;
    int format = *(int *) "Y800";
    char **data = NULL;

    zbar_image_scanner_t *scanner = zbar_image_scanner_create();
    zbar_image_scanner_set_config(scanner, 0, ZBAR_CFG_ENABLE, 0); /* disable all symbologies */
    if (is_binary){
        zbar_image_scanner_set_config(scanner, 0, ZBAR_CFG_BINARY, 1);
    }
    for (int i=0; i < symbologies->number; i++) {
        zbar_image_scanner_set_config(scanner, symbologies->symbologie[i], ZBAR_CFG_ENABLE, 1);
    }

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
    PyObject * python_symbologies = NULL;
    char *raw_image_data = NULL;
    Py_ssize_t raw_image_data_length = 0;
    unsigned int width = 0;
    unsigned int height = 0;
    unsigned int is_binary = 0;
    struct Symbologies symbologies;
    char **result = NULL;
    PyObject *data = NULL;

    if (!PyArg_ParseTuple(args, "O!SIII", &PyList_Type, &python_symbologies, &python_image, &width, &height, &is_binary)) {
        return NULL;
    }
    PyBytes_AsStringAndSize(python_image, &raw_image_data, &raw_image_data_length);

    symbologies.number = PyList_Size(python_symbologies);
    for (int i=0; i < symbologies.number && i < KNOWN_SYMNOLOGIES; i++) {
        PyObject * obj = PyList_GetItem(python_symbologies, i);
        symbologies.symbologie[i] = PyLong_AsLong(obj);
    }

    result = _zbar_code_scanner(&symbologies, raw_image_data, raw_image_data_length, width, height, is_binary);
    if (result == NULL) {
        Py_RETURN_NONE;
    }

    data = PyList_New(0);
    for(int i=0; result[i] != NULL; i++) {
        PyObject *item = PyBytes_FromString(result[i]);
        PyList_Append(data, item);
        free(result[i]);
    }
    free(result);
    return data;
}

/* Module initialization */
static PyMethodDef zbarlight_functions[] = {
    { "zbar_code_scanner", zbar_code_scanner, METH_VARARGS, NULL },
    { NULL }
};

static struct PyModuleDef zbarlight_moduledef = {
    PyModuleDef_HEAD_INIT,
    "_zbarlight",
    NULL,
    -1,
    zbarlight_functions,
};

PyObject* PyInit__zbarlight(void) {
    PyObject* module = PyModule_Create(&zbarlight_moduledef);
    PyObject * symbologies = Py_BuildValue(
        /* XXX: Do not forget to update KNOWN_SYMNOLOGIES when updating this */
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
