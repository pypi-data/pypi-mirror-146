#define PY_SSIZE_T_CLEAN
#define NPY_NO_DEPRECATED_API NPY_1_7_API_VERSION
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <Python.h>
#include "numpy/ndarraytypes.h"
#include "numpy/ufuncobject.h"
#include "numpy/npy_3kcompat.h"
#include <math.h>


static PyMethodDef CompetitionRankingMethods[] = {
        {NULL, NULL, 0, NULL}
};

/* Competition ranking in C */
typedef struct {
    int key;
    int value;
} item;

item* get_item(item* items, int size, const int64_t key) {
    for (int i=0; i<size; i++) {
        if (items[i].key == key) {
            return &items[i];
        }
    }
    return NULL;
}

npy_intp elem_in_arr_with_val(char *vec, npy_intp step, npy_intp n, int val){
    npy_intp res = 0;
    for (npy_intp i=0; i<n; i++){
        if (*(int *)vec == val | -*(int *)vec == val){
            res++;
        }
        vec += step;
    }
    return res;
}

npy_intp inner(int prio, char *vec, npy_intp step, npy_intp n, item d[], int *dn){
    int sign = prio < 0 ? -1 : 1;
    prio = sign * prio;
    npy_intp p, res;
    item* _item = get_item(d, *dn, prio);
    if (_item != NULL)
    {
        return sign * _item->value;
    }
    if (prio == 0){
        res = 0;
    }
    else if (prio == 1)
    {
        res = 1;
    }
    else
    {
        p = inner(prio-1, vec, step, n, d, dn);
        p = p < 0 ? -p: p;
        res = p * elem_in_arr_with_val(vec, step, n, prio-1) + p;
    }
    item item_res = {prio, res};
    d[prio] = item_res;
    (*dn)++;
    return sign * res;
}

int max(char *vec, npy_intp step, npy_intp n)
{
    int res = -1;
    for (int i=0; i<n; i++){
        int sign =  *(int *)vec < 0 ? -1: 1;
        res = (sign * (*(int *)vec)) > res ? (sign * (*(int *)vec)): res;
        vec += step;
    }
    return res;
}

/* End competition ranking in C */

static void competition_ranking_64(char **args, npy_intp *dimensions,
                            npy_intp* steps, void* data)
{
    npy_intp i;
    npy_intp n = dimensions[0];
    char *in = args[0], *out = args[1];
    char *vec = in;
    npy_intp in_step = steps[0], out_step = steps[1];
    int _max = max(vec, in_step, n);
    item d[_max];
    int dn=0;

    int64_t tmp;
    for (i = 0; i < n; i++) {
        /*BEGIN main ufunc computation*/
        tmp = *(int64_t *)in;
        tmp = inner(tmp, vec, in_step, n, d, &dn);
        *((int64_t *)out) = tmp;
        /*END main ufunc computation*/

        in += in_step;
        out += out_step;
    }
}

/*This a pointer to the above function*/
PyUFuncGenericFunction funcs[1] = {&competition_ranking_64};

/* These are the input and return dtypes of prio2weight.*/
static char types[2] = {NPY_INT64, NPY_INT64};

static void *data[1] = {NULL};

static struct PyModuleDef moduledef = {
    PyModuleDef_HEAD_INIT,
    "npufunc",
    NULL,
    -1,
    CompetitionRankingMethods,
    NULL,
    NULL,
    NULL,
    NULL
};

PyMODINIT_FUNC PyInit_npufunc(void)
{
    PyObject *m, *competition_ranking_64, *d;
    m = PyModule_Create(&moduledef);
    if (!m) {
        return NULL;
    }

    import_array();
    import_umath();

    competition_ranking_64 = PyUFunc_FromFuncAndData(funcs, data, types, 1, 1, 1,
                                        PyUFunc_None, "competition_ranking_64",
                                        "competition_ranking_docstring", 0);

    d = PyModule_GetDict(m);

    PyDict_SetItemString(d, "competition_ranking_64", competition_ranking_64);
    Py_DECREF(competition_ranking_64);

    return m;
}