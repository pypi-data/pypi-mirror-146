#include "hcephes.h"

static double PP[7] = {
    7.96936729297347051624E-4, 8.28352392107440799803E-2, 1.23953371646414299388E0,
    5.44725003058768775090E0,  8.74716500199817011941E0,  5.30324038235394892183E0,
    9.99999999999999997821E-1,
};
static double PQ[7] = {
    9.24408810558863637013E-4, 8.56288474354474431428E-2, 1.25352743901058953537E0,
    5.47097740330417105182E0,  8.76190883237069594232E0,  5.30605288235394617618E0,
    1.00000000000000000218E0,
};

static double QP[8] = {
    -1.13663838898469149931E-2, -1.28252718670509318512E0, -1.95539544257735972385E1,
    -9.32060152123768231369E1,  -1.77681167980488050595E2, -1.47077505154951170175E2,
    -5.14105326766599330220E1,  -6.05014350600728481186E0,
};
static double QQ[7] = {
    /*  1.00000000000000000000E0,*/
    6.43178256118178023184E1, 8.56430025976980587198E2, 3.88240183605401609683E3,
    7.24046774195652478189E3, 5.93072701187316984827E3, 2.06209331660327847417E3,
    2.42005740240291393179E2,
};

static double YP[8] = {
    1.55924367855235737965E4,   -1.46639295903971606143E7,  5.43526477051876500413E9,
    -9.82136065717911466409E11, 8.75906394395366999549E13,  -3.46628303384729719441E15,
    4.42733268572569800351E16,  -1.84950800436986690637E16,
};
static double YQ[7] = {
    /* 1.00000000000000000000E0,*/
    1.04128353664259848412E3,  6.26107330137134956842E5,  2.68919633393814121987E8,
    8.64002487103935000337E10, 2.02979612750105546709E13, 3.17157752842975028269E15,
    2.50596256172653059228E17,
};

/*  5.783185962946784521175995758455807035071 */
static double DR1 = 5.78318596294678452118E0;
/* 30.47126234366208639907816317502275584842 */
static double DR2 = 3.04712623436620863991E1;

static double RP[4] = {
    -4.79443220978201773821E9,
    1.95617491946556577543E12,
    -2.49248344360967716204E14,
    9.70862251047306323952E15,
};
static double RQ[8] = {
    /* 1.00000000000000000000E0,*/
    4.99563147152651017219E2,  1.73785401676374683123E5,  4.84409658339962045305E7,
    1.11855537045356834862E10, 2.11277520115489217587E12, 3.10518229857422583814E14,
    3.18121955943204943306E16, 1.71086294081043136091E18,
};

HCEPHES_API double hcephes_j0(double x) {
    double w, z, p, q, xn;

    if (x < 0)
        x = -x;

    if (x <= 5.0) {
        z = x * x;
        if (x < 1.0e-5)
            return (1.0 - z / 4.0);

        p = (z - DR1) * (z - DR2);
        p = p * hcephes_polevl(z, RP, 3) / hcephes_p1evl(z, RQ, 8);
        return (p);
    }

    w = 5.0 / x;
    q = 25.0 / (x * x);
    p = hcephes_polevl(q, PP, 6) / hcephes_polevl(q, PQ, 6);
    q = hcephes_polevl(q, QP, 7) / hcephes_p1evl(q, QQ, 7);
    xn = x - HCEPHES_PIO4;
    p = p * cos(xn) - w * q * sin(xn);
    return (p * HCEPHES_SQ2OPI / sqrt(x));
}

/*							y0() 2	*/
/* Bessel function of second kind, order zero	*/

/* Rational approximation coefficients YP[], YQ[] are used here.
 * The function computed is  y0(x)  -  2 * log(x) * j0(x) / PI,
 * whose value at x = 0 is  2 * ( log(0.5) + EUL ) / PI
 * = 0.073804295108687225.
 */

HCEPHES_API double hcephes_y0(double x) {
    double w, z, p, q, xn;

    if (x <= 5.0) {
        if (x <= 0.0) {
            hcephes_mtherr("y0", HCEPHES_DOMAIN);
            return (-HUGE_VAL);
        }
        z = x * x;
        w = hcephes_polevl(z, YP, 7) / hcephes_p1evl(z, YQ, 7);
        w += HCEPHES_TWOOPI * log(x) * j0(x);
        return (w);
    }

    w = 5.0 / x;
    z = 25.0 / (x * x);
    p = hcephes_polevl(z, PP, 6) / hcephes_polevl(z, PQ, 6);
    q = hcephes_polevl(z, QP, 7) / hcephes_p1evl(z, QQ, 7);
    xn = x - HCEPHES_PIO4;
    p = p * sin(xn) + w * q * cos(xn);
    return (p * HCEPHES_SQ2OPI / sqrt(x));
}
