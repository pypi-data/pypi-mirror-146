#include "hcephes.h"

/* Chebyshev coefficients for K0(x) + log(x/2) I0(x)
 * in the interval [0,2].  The odd order coefficients are all
 * zero; only the even order coefficients are listed.
 *
 * lim(x->0){ K0(x) + log(x/2) I0(x) } = -EUL.
 */

static double A[] = {1.37446543561352307156E-16, 4.25981614279661018399E-14,
                     1.03496952576338420167E-11, 1.90451637722020886025E-9,
                     2.53479107902614945675E-7,  2.28621210311945178607E-5,
                     1.26461541144692592338E-3,  3.59799365153615016266E-2,
                     3.44289899924628486886E-1,  -5.35327393233902768720E-1};

/* Chebyshev coefficients for exp(x) sqrt(x) K0(x)
 * in the inverted interval [2,infinity].
 *
 * lim(x->inf){ exp(x) sqrt(x) K0(x) } = sqrt(pi/2).
 */

static double B[] = {5.30043377268626276149E-18, -1.64758043015242134646E-17,
                     5.21039150503902756861E-17, -1.67823109680541210385E-16,
                     5.51205597852431940784E-16, -1.84859337734377901440E-15,
                     6.34007647740507060557E-15, -2.22751332699166985548E-14,
                     8.03289077536357521100E-14, -2.98009692317273043925E-13,
                     1.14034058820847496303E-12, -4.51459788337394416547E-12,
                     1.85594911495471785253E-11, -7.95748924447710747776E-11,
                     3.57739728140030116597E-10, -1.69753450938905987466E-9,
                     8.57403401741422608519E-9,  -4.66048989768794782956E-8,
                     2.76681363944501510342E-7,  -1.83175552271911948767E-6,
                     1.39498137188764993662E-5,  -1.28495495816278026384E-4,
                     1.56988388573005337491E-3,  -3.14481013119645005427E-2,
                     2.44030308206595545468E0};

HCEPHES_API double hcephes_k0(double x) {
    double y, z;

    if (x <= 0.0) {
        hcephes_mtherr("k0", HCEPHES_DOMAIN);
        return (HUGE_VAL);
    }

    if (x <= 2.0) {
        y = x * x - 2.0;
        y = hcephes_chbevl(y, A, 10) - log(0.5 * x) * hcephes_i0(x);
        return (y);
    }
    z = 8.0 / x - 2.0;
    y = exp(-x) * hcephes_chbevl(z, B, 25) / sqrt(x);
    return (y);
}

HCEPHES_API double hcephes_k0e(double x) {
    double y;

    if (x <= 0.0) {
        hcephes_mtherr("k0e", HCEPHES_DOMAIN);
        return (HUGE_VAL);
    }

    if (x <= 2.0) {
        y = x * x - 2.0;
        y = hcephes_chbevl(y, A, 10) - log(0.5 * x) * hcephes_i0(x);
        return (y * exp(x));
    }

    y = hcephes_chbevl(8.0 / x - 2.0, B, 25) / sqrt(x);
    return (y);
}
