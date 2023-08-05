#include "hcephes.h"

#define EUL 0.57721566490153286060
#define BIG 1.44115188075855872E+17

HCEPHES_API double hcephes_expn(int n, double x) {
    double ans, r, t, yk, xk;
    double pk, pkm1, pkm2, qk, qkm1, qkm2;
    double psi, z;
    int i, k;
    static double big = BIG;

    if (n < 0)
        goto domerr;

    if (x < 0) {
    domerr:
        hcephes_mtherr("expn", HCEPHES_DOMAIN);
        return (HUGE_VAL);
    }

    if (x > HCEPHES_MAXLOG)
        return (0.0);

    if (x == 0.0) {
        if (n < 2) {
            hcephes_mtherr("expn", HCEPHES_SING);
            return (HUGE_VAL);
        } else
            return (1.0 / (n - 1.0));
    }

    if (n == 0)
        return (exp(-x) / x);

    /*							expn.c	*/
    /*		Expansion for large n		*/

    if (n > 5000) {
        xk = x + n;
        yk = 1.0 / (xk * xk);
        t = n;
        ans = yk * t * (6.0 * x * x - 8.0 * t * x + t * t);
        ans = yk * (ans + t * (t - 2.0 * x));
        ans = yk * (ans + t);
        ans = (ans + 1.0) * exp(-x) / xk;
        goto done;
    }

    if (x > 1.0)
        goto cfrac;

    /*							expn.c	*/

    /*		Power series expansion		*/

    psi = -EUL - log(x);
    for (i = 1; i < n; i++)
        psi = psi + 1.0 / i;

    z = -x;
    xk = 0.0;
    yk = 1.0;
    pk = 1.0 - n;
    if (n == 1)
        ans = 0.0;
    else
        ans = 1.0 / pk;
    do {
        xk += 1.0;
        yk *= z / xk;
        pk += 1.0;
        if (pk != 0.0) {
            ans += yk / pk;
        }
        if (ans != 0.0)
            t = fabs(yk / ans);
        else
            t = 1.0;
    } while (t > HCEPHES_MACHEP);
    k = (int)xk;
    t = n;
    r = n - 1;
    ans = (pow(z, r) * psi / hcephes_gamma(t)) - ans;
    goto done;

/*							expn.c	*/
/*		continued fraction		*/
cfrac:
    k = 1;
    pkm2 = 1.0;
    qkm2 = x;
    pkm1 = 1.0;
    qkm1 = x + n;
    ans = pkm1 / qkm1;

    do {
        k += 1;
        if (k & 1) {
            yk = 1.0;
            xk = n + (k - 1) / 2;
        } else {
            yk = x;
            xk = k / 2;
        }
        pk = pkm1 * yk + pkm2 * xk;
        qk = qkm1 * yk + qkm2 * xk;
        if (qk != 0) {
            r = pk / qk;
            t = fabs((ans - r) / r);
            ans = r;
        } else
            t = 1.0;
        pkm2 = pkm1;
        pkm1 = pk;
        qkm2 = qkm1;
        qkm1 = qk;
        if (fabs(pk) > big) {
            pkm2 /= big;
            pkm1 /= big;
            qkm2 /= big;
            qkm1 /= big;
        }
    } while (t > HCEPHES_MACHEP);

    ans *= exp(-x);

done:
    return (ans);
}
